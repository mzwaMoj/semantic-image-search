# config.py
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')
    DEFAULT_NUM_RESULTS: int = 9
    MAX_NUM_RESULTS: int = 30
    MODEL_NAME: str = 'clip-ViT-B-32' # model to use
    DEVICE: str = 'cpu'  # Change to 'cuda' if using GPU

    # Set base directory explicitly
    BASE_DIR: Path = Path("../..") # Parent directory
    DATA_DIR: Path = BASE_DIR / "dataset/embeddings"  # where to save index and embeddings

    # Files for FAISS index and embeddings
    INDEX_PATH: Path = DATA_DIR / "image_index.faiss"
    EMBEDDINGS_PATH: Path = DATA_DIR / "image_embeddings.npy"
    PATHS_FILE: Path = DATA_DIR / "image_paths.npy"
