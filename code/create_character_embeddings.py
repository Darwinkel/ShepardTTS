"""Create speaker embeddings and conditioning latents for all wav files of a character."""

from pathlib import Path

import torch

from utils import load_checkpoint


def main():
    mapped_unique_characters = {}

    for file in Path("ljspeech/wavs").glob("*.wav"):
        # character = get_character(file.stem[:-7]) # NOTE: Let's not unify things for now. More options for users.
        character = file.stem[:-7]
        print(file)
        print(character)
        if character not in mapped_unique_characters:
            mapped_unique_characters[character] = []

        mapped_unique_characters[character].append(file)

    model = load_checkpoint()

    for key, value in mapped_unique_characters.items():
        print(f"Computing speaker latents for {key} ({len(value)} samples)")
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(
            audio_path=value, max_ref_length=30, gpt_cond_len=6, gpt_cond_chunk_len=3
        )
        torch.save(gpt_cond_latent, f"mean_character_embeddings/{key}_gpt_cond_latent.pt")
        torch.save(speaker_embedding, f"mean_character_embeddings/{key}_speaker_embedding.pt")


if __name__ == "__main__":
    main()
