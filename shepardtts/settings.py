"""Contains some universal settings."""

import os

import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CHECKPOINT_DIR = "/xtts_model"
CHECKPOINTS_CONFIG_JSON = "/xtts_model/config.json"
CHECKPOINT_VOCAB_JSON = "/xtts_model/vocab.json"
MEAN_CHARACTER_EMBEDDINGS_PATH = "/mean_character_embeddings"

GRADIO_EXAMPLES_CACHE = os.environ["GRADIO_EXAMPLES_CACHE"]
SECRET_KEY = os.environ["SECRET_KEY"]
