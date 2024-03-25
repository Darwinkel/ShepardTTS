"""Contains some universal settings."""

import os

import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CHECKPOINT_DIR = os.environ.get("CHECKPOINT_DIR", "/xtts_model")
CHECKPOINTS_CONFIG_JSON = os.environ.get("CHECKPOINTS_CONFIG_JSON", "/xtts_model/config.json")
CHECKPOINT_VOCAB_JSON = os.environ.get("CHECKPOINT_VOCAB_JSON", "/xtts_model/vocab.json")
MEAN_CHARACTER_EMBEDDINGS_PATH = os.environ.get("MEAN_CHARACTER_EMBEDDINGS_PATH", "/mean_character_embeddings")

GRADIO_EXAMPLES_CACHE = os.environ.get("GRADIO_EXAMPLES_CACHE", "/tmp/")  # noqa: S108
SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")

DUMMY = os.environ.get("DUMMY", False)  # If set, do not load the model
