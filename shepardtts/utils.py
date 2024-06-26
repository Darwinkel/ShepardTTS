"""Contains some helper functionality."""

import re

import torch
from cleantext import clean
from num2words import num2words
from TTS.tts.configs.xtts_config import XttsConfig

from . import settings
from .overrides import ShepardXtts  # type: ignore[attr-defined]


def load_checkpoint() -> ShepardXtts:
    """Load a model checkpoint from settings module."""
    use_deepspeed = False
    if settings.DEVICE == "cuda":
        use_deepspeed = True

    print(f"Loading model on {settings.DEVICE}. DeepSpeed is {use_deepspeed}.")
    config = XttsConfig()
    config.load_json(settings.CHECKPOINTS_CONFIG_JSON)
    model = ShepardXtts.init_from_config(config)
    model.load_checkpoint(
        config,
        checkpoint_dir=settings.CHECKPOINT_DIR,
        vocab_path=settings.CHECKPOINT_VOCAB_JSON,
        use_deepspeed=use_deepspeed,
    )
    model.to(settings.DEVICE)
    model.eval()

    if settings.DEVICE == "cpu":
        import intel_extension_for_pytorch as ipex

        model = ipex.optimize(model, weights_prepack=False)
        model = torch.compile(model, backend="ipex")

    return model


NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"  # noqa: E501 RUF001
)


def normalize_line(line: str) -> str:
    """Normalize a line of text."""
    cleaned = clean(
        text=line,
        fix_unicode=True,  # fix various unicode errors
        to_ascii=True,  # transliterate to closest ASCII representation
        lower=False,  # lowercase text
        no_line_breaks=True,  # fully strip line breaks as opposed to only normalizing them
        no_urls=False,  # replace all URLs with a special token
        no_emails=False,  # replace all email addresses with a special token
        no_phone_numbers=False,  # replace all phone numbers with a special token
        no_numbers=False,  # replace all numbers with a special token
        no_digits=False,  # replace all digits with a special token
        no_currency_symbols=False,  # replace all currency symbols with a special token
        no_punct=False,  # remove punctuations
        lang="en",  # set to 'de' for German special handling
    )

    return NUMBERS_REGEX.sub(lambda m: normalize_numbers(m.group()), cleaned)


def normalize_numbers(string: str) -> str:
    """Normalize numbers in a string."""
    # Required for when a comma is used inside a digit (one occurence in dataset)
    return str(num2words(string.replace(",", "")))


def language2id() -> dict[str, str]:
    """Convert language choice to its Xttsv2 code."""
    return {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portugese": "pt",
        "Polish": "pl",
        "Turkish": "tr",
        "Russian": "ru",
        "Dutch": "nl",
        "Czech": "cs",
        "Arabic": "ar",
        "Chinese": "zh-cn",
        "Japanese": "ja",
        "Korean": "ko",
        "Hungarian": "hu",
        "Hindi": "hi",
    }
