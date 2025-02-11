# create_embeddings.py
import argparse
import sys
from utils.embeddings import EmbeddingGenerator
from utils.indexer import ImageIndexer
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Create image embeddings and FAISS index')
    parser.add_argument('--image_dir', type=str, required=True, help='Directory containing images')
    args = parser.parse_args()

    try:
        print("Initializing embedding generator...")
        embedding_generator = EmbeddingGenerator(model_name="clip-ViT-B-32")
        print("Creating image index...")
        indexer = ImageIndexer(embedding_generator)
        indexer.create_index(args.image_dir)
        print("✅ Embeddings and index created successfully!")
        print(f"Files saved in: {Config.DATA_DIR}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()