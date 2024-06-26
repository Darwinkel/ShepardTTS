"""Gradio web interface for ShepardTTS."""

import time
from pathlib import Path

import gradio as gr
import numpy as np
import torch
from torchaudio.io import CodecConfig, StreamWriter

from . import settings
from .app_helpers import description, examples, links
from .utils import language2id, load_checkpoint, normalize_line

MODEL = None if settings.DUMMY else load_checkpoint()

QUARTER_SECOND_PAUSE = torch.tensor(np.zeros(24000 // 4), dtype=torch.float32)
MIN_PROMPT_LENGTH = 2
MAX_PROMPT_LENGTH = 2500
MIN_AMOUNT_OF_SAMPLES = 3


def get_available_speaker_embeddings() -> list[str]:
    """Return a list of all available pre-generated speaker embeddings."""
    available_speaker_embeddings = []
    for file in Path(settings.MEAN_CHARACTER_EMBEDDINGS_PATH).glob("*_speaker_embedding.pt"):
        character = file.stem[:-18]
        no_samples = int(character.split("_")[0])

        # Only keep embeddings which have 3 or more samples
        if no_samples >= MIN_AMOUNT_OF_SAMPLES:
            available_speaker_embeddings.append(character)

    # Sort descending by amount of samples it is based on
    available_speaker_embeddings.sort(key=lambda x: int(x.split("_")[0]), reverse=True)

    return available_speaker_embeddings


def get_speaker_embeddings() -> tuple[dict[str, torch.Tensor], dict[str, torch.Tensor]]:
    """Load pre-generated speaker embeddings from disk into memory. Currently unused."""
    character_speaker_embeddings = {}
    character_gpt_cond_latents = {}

    for character in get_available_speaker_embeddings():
        character_speaker_embeddings[character] = torch.load(
            f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_speaker_embedding.pt",
            map_location=torch.device(settings.DEVICE),
        )
        character_gpt_cond_latents[character] = torch.load(
            f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_gpt_cond_latent.pt",
            map_location=torch.device(settings.DEVICE),
        )
        print(character)

    return character_speaker_embeddings, character_gpt_cond_latents


def predict(
    prompt: str,
    character: str,
    language: str = "English",
    codec_format: str = "ogg",
    top_k: float = 30.0,
    top_p: float = 0.5,
    temperature: float = 0.6,
    speed: float = 1.0,
    repetition_penalty: float = 10.0,
    length_penalty: float = 1.0,
) -> tuple[str | None, str | None]:
    """Predicts and outputs a compressed waveform for a given prompt and configuration."""
    if len(prompt) < MIN_PROMPT_LENGTH:
        gr.Warning("Please give a longer prompt text")
        return (
            None,
            None,
        )
    if len(prompt) > MAX_PROMPT_LENGTH:
        gr.Warning("Text length limited to 2500 characters for this demo, please try a shorter text.")
        return (
            None,
            None,
        )

    total_time = time.time()

    if MODEL:
        character_gpt_cond_latent = torch.load(
            f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_gpt_cond_latent.pt",
            map_location=torch.device(settings.DEVICE),
        )

        character_speaker_embedding = torch.load(
            f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_speaker_embedding.pt",
            map_location=torch.device(settings.DEVICE),
        )

        out = MODEL.inference(
            text=normalize_line(prompt),
            language=language2id()[language],
            gpt_cond_latent=character_gpt_cond_latent,
            speaker_embedding=character_speaker_embedding,
            top_k=int(top_k),
            top_p=float(top_p),
            temperature=float(temperature),
            speed=float(speed),
            repetition_penalty=float(repetition_penalty),
            length_penalty=float(length_penalty),
            enable_text_splitting=True,
        )
    else:
        out = {"wav": [torch.tensor([])]}

    inference_time = time.time() - total_time
    postprocessing_time = time.time()

    waveform = torch.tensor([])

    for sentence in out["wav"]:
        waveform = torch.cat((waveform, QUARTER_SECOND_PAUSE, sentence, QUARTER_SECOND_PAUSE))

    base_filename = f"{settings.GRADIO_EXAMPLES_CACHE}/{int(time.time())}_{character}"

    if codec_format == "mp3":
        # Write compressed mp3
        filename = f"{base_filename}.mp3"
        s = StreamWriter(dst=filename)
        s.add_audio_stream(
            sample_rate=24000,
            num_channels=1,
            encoder="libmp3lame",
            codec_config=CodecConfig(compression_level=0, qscale=0),
        )

    else:
        # Write compressed opus ogg
        filename = f"{base_filename}.ogg"
        s = StreamWriter(dst=filename)
        s.add_audio_stream(
            sample_rate=24000, num_channels=1, encoder="libopus", codec_config=CodecConfig(compression_level=10)
        )

    with s.open():
        s.write_audio_chunk(0, waveform.unsqueeze(1))

    postprocessing_time = time.time() - postprocessing_time

    return (
        filename,
        f"Inference time: {inference_time:.4f}s. Postprocessing time: {postprocessing_time:.4f}s.",
    )


def main() -> None:
    """Launch the Gradio app."""
    with gr.Blocks(analytics_enabled=False) as demo:
        with gr.Row():
            with gr.Column():
                gr.Markdown(description)
            with gr.Column():
                gr.Markdown(links)

        with gr.Row():
            with gr.Column():
                input_text_gr = gr.TextArea(
                    label="Text Prompt",
                    info="Make sure you use proper punctuation.",
                    value="Hi there, I'm a voice from Mass Effect. "
                    "I can talk as much as you want, "
                    "provided the input text is split in small to medium length sentences.",
                )

                char_gr = gr.Dropdown(
                    label="Character",
                    info="Select a reference voice for the synthesised speech.",
                    choices=get_available_speaker_embeddings(),
                    multiselect=False,
                    value="73_ME2-f_player_f_Shepard-nor_yeoman_d_dlg",
                )

                language_gr = gr.Dropdown(
                    label="Language",
                    info="Select the language to be used by the model. "
                    "The prompt should be written in the language selected here.",
                    choices=language2id().keys(),
                    multiselect=False,
                    value="English",
                )

                format_gr = gr.Radio(
                    label="Format",
                    info="Encode and compress waveform as opus/ogg or mp3?",
                    choices=["ogg", "mp3"],
                    value="ogg",
                )

                top_k_gr = gr.Slider(
                    label="Top K",
                    minimum=1.0,
                    maximum=100.0,
                    value=30.0,
                    step=1.0,
                    info="K value used in top-k sampling. [0,inf]. "
                    "Lower values mean the decoder produces more 'likely' (aka boring) outputs. "
                    "Defaults to 50.",
                )

                top_p_gr = gr.Slider(
                    label="Top P",
                    minimum=0.01,
                    maximum=0.99,
                    value=0.50,
                    step=0.01,
                    info="P value used in nucleus sampling. (0,1). "
                    "Lower values mean the decoder produces more 'likely' (aka boring) outputs. "
                    "Defaults to 0.8.",
                )
                temperature_gr = gr.Slider(
                    label="Temperature",
                    minimum=0.01,
                    maximum=0.99,
                    value=0.6,
                    step=0.01,
                    info="The softmax temperature of the autoregressive model. Defaults to 0.65.",
                )

                speed_gr = gr.Slider(
                    label="Speed",
                    minimum=0.1,
                    maximum=2.0,
                    value=1.0,
                    step=0.1,
                    info="Speed modifier for the voice. Defaults to 1.0.",
                )

                repetition_penalty_gr = gr.Slider(
                    label="Repetition penalty",
                    minimum=0.1,
                    maximum=20.0,
                    value=10.0,
                    step=0.1,
                    info="A penalty that prevents the autoregressive decoder from repeating itself during decoding. "
                    "Can be used to reduce the incidence of long silences or 'uhhhhhhs', etc. "
                    "Defaults to 10.0.",
                )

                length_penalty_gr = gr.Slider(
                    label="Length penalty",
                    minimum=0.1,
                    maximum=2.0,
                    value=1.0,
                    step=0.1,
                    info="A length penalty applied to the autoregressive decoder. "
                    "Higher settings causes the model to produce more terse outputs. "
                    "Defaults to 1.0.",
                )

                tts_button = gr.Button("Synthesise", elem_id="send-btn", visible=True)

            with gr.Column():
                audio_gr = gr.Audio(label="Synthesised Audio", autoplay=True)
                out_text_gr = gr.Text(label="Metrics")

        with gr.Row():
            gr.Examples(
                examples,
                label="Examples",
                inputs=[input_text_gr, char_gr],
                outputs=[audio_gr, out_text_gr],
                fn=predict,
                cache_examples=True,
                examples_per_page=30,
            )

        tts_button.click(
            predict,
            [
                input_text_gr,
                char_gr,
                language_gr,
                format_gr,
                top_k_gr,
                top_p_gr,
                temperature_gr,
                speed_gr,
                repetition_penalty_gr,
                length_penalty_gr,
            ],
            outputs=[audio_gr, out_text_gr],
        )

    demo.queue(max_size=10)
    demo.launch(debug=False, show_api=True, share=False, auth=("shepard", settings.SECRET_KEY))


if __name__ == "__main__":
    main()
