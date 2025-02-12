import os
import numpy as np
from config import Config

def main():
    # Convert Path objects to strings
    embeddings_path = str(Config.EMBEDDINGS_PATH)
    paths_file = str(Config.PATHS_FILE)
    images_dir = str(Config.BASE_DIR.parent / "dataset/sample_images") 

    # Load embeddings and image paths arrays
    embeddings = np.load(embeddings_path)
    image_paths = np.load(paths_file)

    # Find unique embeddings by comparing full rows (duplicate if every value is the same)
    unique_embeddings, unique_indices = np.unique(embeddings, axis=0, return_index=True)
    unique_image_paths = image_paths[unique_indices]

    num_duplicates = len(embeddings) - len(unique_embeddings)
    print(f"Found {num_duplicates} duplicates.")

    # Save the pruned arrays back to disk
    np.save(embeddings_path, unique_embeddings)
    np.save(paths_file, unique_image_paths)
    print("Updated embeddings and image paths saved.")

    # Remove duplicate image files
    # Build a set of unique (absolute) file paths for quick membership testing.
    unique_set = set(unique_image_paths.tolist())
    removed_count = 0
    for path in image_paths:
        if path not in unique_set:
            if os.path.exists(path):
                os.remove(path)
                removed_count += 1
                print(f"Removed duplicate image: {path}")

    print(f"Removed {removed_count} duplicate image files from disk.")

if __name__ == "__main__":
    main()
