"""Create a clean, normalized, unified dataset from game dumps and export it into the ljspeech format."""

from collections.abc import Iterator
from pathlib import Path

import pandas as pd
import soundfile
from datasets import Audio, Dataset, concatenate_datasets

from .utils import normalize_line


def dataset_from_iterator(path_to_dialogue_dump: str, path_to_audio: str, game: str) -> Iterator[dict[str, str]]:
    """Yield examples by cross referencing dialogues and audio files."""
    dialogue_dump_df = pd.read_excel(path_to_dialogue_dump)

    audio_files_found = 0
    dialogue_strings_found = len(dialogue_dump_df)
    audio_dialogues_found = 0
    audio_dialogue_matches_cross_referenced = 0

    for file in Path(path_to_audio).rglob("*.ogg"):
        audio_files_found += 1

        # Get string ID, if any
        string_id = file.stem[-8:-2]
        if string_id.isnumeric():
            audio_dialogues_found += 1

            row = dialogue_dump_df.loc[dialogue_dump_df["TLK StringRef"] == int(string_id)]
            if len(row) > 0:
                audio_dialogue_matches_cross_referenced += 1

                # Get gender of speaker
                gender = file.stem[-1]

                # Take character from dialogue dump
                character_from_dialogue = row["Speaker"].values[0]  # noqa: PD011

                # Prefix character with gender
                probable_character = f"{gender}-"

                # Strip quotes and normalize sentence
                line = normalize_line(row["Line"].values[0][1:-1])  # noqa: PD011

                if game == "ME2":
                    # Replace folder name (minus `s_int`) with empty string,
                    # Remove `en_us_` and `_00xxxxxx_x` from whatever remains
                    character_from_filename = file.stem.replace(file.parts[-2][:-5], "")[6:-11]

                    if character_from_dialogue in (character_from_filename, "Owner"):
                        probable_character += character_from_filename
                    else:
                        probable_character += f"{character_from_filename}-{character_from_dialogue}"

                elif game == "ME3":
                    # Take character from dialogue dump
                    probable_character += character_from_dialogue

                print(game, string_id, probable_character, line, file)
                yield {
                    "game": game,
                    "string_id": string_id,
                    "character": probable_character,
                    "line": line,
                    "audio": str(file),
                }

    print(f"Dialogue strings found: {dialogue_strings_found}")
    print(f"Audio files found: {audio_files_found}")
    print(f"Audio dialogues found: {audio_dialogues_found}")
    print(
        f"Audio dialogues and strings cross-referenced: {audio_dialogue_matches_cross_referenced} "
        f"(may be high due to multiple speakers per string)"
    )


def is_valid_sample(example: dict[str, Dataset]) -> bool:  # noqa: PLR0911
    """Check if a sample is likely to be valid."""
    min_line_length = 4
    min_audio_length = 2

    line = example["line"]
    audio_array = example["audio"]["array"]

    # Filter empty strings
    if line in ("", ".", " ", "!", "?", "Aaah!"):
        print("Invalid line")
        print(example)
        return False

    # Decoding errors
    if "x0000" in line:
        print("Decoding error")
        print(example)
        return False

    # Filter too short lines (but allow Yes.)
    if len(line) < min_line_length:
        print("Line too short")
        print(example)
        return False

    # {Chuckles}, {{Falling- short distance 5}} used in ME3
    if line.startswith("{") and line.endswith("}"):
        print("Sound effect line")
        print(example)
        return False

    # Audio array is all zeroes
    if not audio_array.any():
        print("Zeroed audio array")
        print(example)
        return False

    # Audio array is waaaay to short
    if len(audio_array) < min_audio_length:
        print("Too short audio array")
        print(example)
        return False

    return True


def main() -> None:
    """Run main function."""
    me2_dataset = Dataset.from_generator(
        dataset_from_iterator,
        gen_kwargs={
            "path_to_dialogue_dump": "datasets/localization/ME2DialogueDump.xlsx",
            "path_to_audio": "datasets/audio/ME2Dump",
            "game": "ME2",
        },
    )
    me3_dataset = Dataset.from_generator(
        dataset_from_iterator,
        gen_kwargs={
            "path_to_dialogue_dump": "datasets/localization/ME3DialogueDump.xlsx",
            "path_to_audio": "datasets/audio/ME3Dump",
            "game": "ME3",
        },
    )

    # Sort by line to get a good view of multiple speakers for the same line
    complete_dataset = concatenate_datasets([me2_dataset, me3_dataset]).sort(["line", "character"])

    # Original sampling rate: 24000
    # SpeechT5 requires 16000, xttsv2 requires 22050, and cast to mono just to be safe
    complete_dataset_with_audio = complete_dataset.cast_column("audio", Audio(mono=True, sampling_rate=22050))

    # Remove invalid and broken audio and lines
    complete_dataset_with_valid_audio = complete_dataset_with_audio.filter(is_valid_sample, num_proc=11)

    # Write to ljspeech format
    with open("ljspeech/metadata.csv", "w") as file:  # noqa: PTH123
        for sample in complete_dataset_with_valid_audio:
            filename_without_extension = f"{sample['game']}_{sample['character']}_{sample['string_id']}"
            normalized_text = sample["line"]
            soundfile.write(
                f"ljspeech/wavs/{filename_without_extension}.wav",
                sample["audio"]["array"],
                samplerate=sample["audio"]["sampling_rate"],
            )
            file.write(f"{filename_without_extension}|{normalized_text}|{normalized_text}\n")


if __name__ == "__main__":
    main()
