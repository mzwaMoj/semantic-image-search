# utils/indexer.py
import os
from pathlib import Path
import numpy as np
import faiss
from PIL import Image
from typing import Tuple, List, Optional
from .embeddings import EmbeddingGenerator
from config import Config

class ImageIndexer:
    def __init__(self, embedding_generator: EmbeddingGenerator):
        """Initialize the indexer with the embedding generator."""
        self.embedding_generator = embedding_generator
        self.index: Optional[faiss.Index] = None
        self.image_paths: Optional[np.ndarray] = None

    def create_index(self, image_dir: str) -> None:
        """Process images from directory, create FAISS index and save files."""
        try:
            image_paths, embeddings = self._process_images(image_dir)

            if len(embeddings) == 0:
                raise ValueError("No valid images found to process.")

            # Convert list to NumPy arrays
            embeddings_array = np.array(embeddings).astype('float32')
            paths_array = np.array(image_paths)

            dim = embeddings_array.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings_array)

            # Ensure the data directory exists before saving
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            faiss.write_index(index, str(Config.INDEX_PATH))
            np.save(str(Config.EMBEDDINGS_PATH), embeddings_array)
            np.save(str(Config.PATHS_FILE), paths_array)
            print("Index and embeddings successfully created.")
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {e}")

    def _process_images(self, image_dir: str) -> Tuple[List[str], List[np.ndarray]]:
        """Process all images inside the provided directory and generate embeddings."""
        image_paths: List[str] = []
        embeddings: List[np.ndarray] = []

        for filename in os.listdir(image_dir):
            if filename.lower().endswith(Config.IMAGE_EXTENSIONS):
                try:
                    image_path = os.path.join(image_dir, filename)
                    with Image.open(image_path) as img:
                        embedding = self.embedding_generator.get_image_embedding(img)
                    image_paths.append(image_path)
                    embeddings.append(embedding)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        return image_paths, embeddings

    def load_index(self) -> Tuple[faiss.Index, np.ndarray]:
        """Load FAISS index and image paths from disk."""
        try:
            if not Path(Config.INDEX_PATH).exists():
                raise FileNotFoundError("Index file not found. Please run create_embeddings.py first.")

            self.index = faiss.read_index(str(Config.INDEX_PATH))
            self.image_paths = np.load(str(Config.PATHS_FILE))
            return self.index, self.image_paths
        except Exception as e:
            raise RuntimeError(f"Failed to load index: {e}")

    def search(self, query_embedding: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """Search the FAISS index for similar image embeddings."""
        if self.index is None:
            raise RuntimeError("Index not loaded. Call load_index() first.")
        return self.index.search(query_embedding.reshape(1, -1), k)