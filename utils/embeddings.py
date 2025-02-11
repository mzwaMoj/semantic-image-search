# utils/embeddings.py
import torch
import numpy as np
from typing import Optional
from sentence_transformers import SentenceTransformer
from PIL import Image
from config import Config
import torch.nn.functional as F

class EmbeddingGenerator:
    def __init__(self, model_name: str = Config.MODEL_NAME):
        """Initialize the embedding generator with error handling."""
        try:
            self.device = torch.device(Config.DEVICE)
            self.model = SentenceTransformer(model_name)
            # SentenceTransformer manages device placement internally,
            # but we explicitly move it for consistency.
            self.model.to(self.device)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize embedding generator: {e}")

    def get_text_embedding(self, text: str) -> np.ndarray:
        """Generate normalized embedding for text query."""
        try:
            # Generate embedding as a torch tensor
            embedding = self.model.encode(text, convert_to_tensor=True)
            # Normalize using L2 norm (beneficial for cosine similarity)
            embedding = F.normalize(embedding, p=2, dim=-1)
            return embedding.cpu().numpy().astype('float32')
        except Exception as e:
            raise RuntimeError(f"Failed to generate text embedding: {e}")

    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """Generate normalized embedding for an image."""
        try:
            # Ensure image is in RGB format
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Process the image as a single-item batch and generate embedding
            embedding = self.model.encode([image], convert_to_tensor=True)
            # Normalize the embedding vector
            embedding = F.normalize(embedding[0], p=2, dim=-1)
            return embedding.cpu().numpy().astype('float32')
        except Exception as e:
            raise RuntimeError(f"Failed to generate image embedding: {e}")