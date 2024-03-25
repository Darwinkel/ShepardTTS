"""Create speaker embeddings and conditioning latents for all wav files of a character."""

from pathlib import Path

import torch

from .utils import load_checkpoint


def main() -> None:
    """Run main function."""
    mapped_unique_characters: dict[str, list[Path]] = {}

    for file in Path("ljspeech/wavs").glob("*.wav"):
        character_metadata = file.stem.split("-")

        game = character_metadata[0]
        character = character_metadata[1]
        conversation = character_metadata[2]
        string_id = character_metadata[3]

        print(file)
        print(game, character, conversation, string_id)

        character_conversation = f"{game}-{character}-{conversation}"

        if character_conversation not in mapped_unique_characters:
            mapped_unique_characters[character_conversation] = []

        mapped_unique_characters[character_conversation].append(file)

    model = load_checkpoint()

    for key, value in mapped_unique_characters.items():
        print(f"Computing speaker latents for {key} ({len(value)} samples)")
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(
            audio_path=value, max_ref_length=30, gpt_cond_len=6, gpt_cond_chunk_len=3
        )
        torch.save(gpt_cond_latent, f"mean_character_embeddings/{len(value)}_{key}_gpt_cond_latent.pt")
        torch.save(speaker_embedding, f"mean_character_embeddings/{len(value)}_{key}_speaker_embedding.pt")


if __name__ == "__main__":
    main()
