"""Contains some helper functionality."""

import re

import settings
from cleantext import clean
from num2words import num2words
from overrides import ShepardXtts
from TTS.tts.configs.xtts_config import XttsConfig


def load_checkpoint():
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
        vocab_path=settings.CHECKPOINT_VOCAB,
        use_deepspeed=use_deepspeed,
    )
    model.to(settings.DEVICE)
    return model


NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"
)


def normalize_line(line: str):
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


def normalize_numbers(string):
    # Required for when a comma is used inside a digit (one occurence in dataset)
    return num2words(string.replace(",", ""))
