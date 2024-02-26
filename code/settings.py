"""Contains some universal settings."""

import torch

CHECKPOINTS_CONFIG_JSON = "./current_model/config.json"
CHECKPOINT_DIR = "./current_model"
CHECKPOINT_VOCAB = "./current_model/vocab.json"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
