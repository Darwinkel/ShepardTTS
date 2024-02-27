"""Gradio web interface for ShepardTTS."""

import time
from pathlib import Path

import gradio as gr
import numpy as np
import settings
import torch
from app_helpers import description, examples, links
from torchaudio.io import CodecConfig, StreamWriter
from utils import load_checkpoint, normalize_line

model = load_checkpoint()

QUARTER_SECOND_PAUSE = torch.tensor(np.zeros(24000 // 4), dtype=torch.float32)
MIN_PROMPT_LENGTH = 2
MAX_PROMPT_LENGTH = 2500

# Load speaker embeddings and gpt cond latents into memory for performance (~100mb)
CHARACTER_SPEAKER_EMBEDDINGS = {}
CHARACTER_GPT_COND_LATENTS = {}
for file in Path(settings.MEAN_CHARACTER_EMBEDDINGS_PATH).glob("*_speaker_embedding.pt"):
    character = file.stem[:-18]

    CHARACTER_SPEAKER_EMBEDDINGS[character] = torch.load(
        f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_speaker_embedding.pt",
        map_location=torch.device(settings.DEVICE),
    )
    CHARACTER_GPT_COND_LATENTS[character] = torch.load(
        f"{settings.MEAN_CHARACTER_EMBEDDINGS_PATH}/{character}_gpt_cond_latent.pt",
        map_location=torch.device(settings.DEVICE),
    )
    print(file)
    print(character)


def predict(
    prompt: str,
    character: str,
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

    out = model.inference(
        normalize_line(prompt),
        "en",
        CHARACTER_GPT_COND_LATENTS[character],
        CHARACTER_SPEAKER_EMBEDDINGS[character],
        top_k=int(top_k),
        top_p=float(top_p),
        temperature=float(temperature),
        speed=float(speed),
        repetition_penalty=float(repetition_penalty),
        length_penalty=float(length_penalty),
        enable_text_splitting=True,
    )

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
                choices=list(CHARACTER_SPEAKER_EMBEDDINGS.keys()),
                multiselect=False,
                value="ME2_f-player_f-Shepard",
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
        )

    tts_button.click(
        predict,
        [
            input_text_gr,
            char_gr,
            format_gr,
            top_p_gr,
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
