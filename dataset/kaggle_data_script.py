#!/usr/bin/env python3
import os
import subprocess
import zipfile
import random
import shutil

# Set parameters
dataset_id = "alessandrasala79/ai-vs-human-generated-dataset"
zip_filename = "ai_vs_human_generated.zip"
extract_folder = "kaggle_dataset"
source_subfolder = "test_data_v2"  # Name of the folder containing images in the dataset
target_folder = "sample_images"
num_images = 500

def download_dataset():
    # Download the dataset using Kaggle API if the zip does not exist.
    if not os.path.exists(zip_filename):
        print("Downloading dataset from Kaggle...")
        cmd = [
            "kaggle", "datasets", "download",
            "-d", dataset_id,
            "-p", "."
        ]
        subprocess.run(cmd, check=True)
    else:
        print("Dataset zip already exists.")

def extract_dataset():
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder, exist_ok=True)
    print("Extracting dataset...")
    with zipfile.ZipFile(zip_filename, "r") as z:
        z.extractall(path=extract_folder)
    # Determine the location of test_data_v2 folder
    # This assumes that the zip file contains a folder named 'test_data_v2' (or similar)
    # Adjust accordingly if the folder structure differs.
    dataset_folder = os.path.join(extract_folder, source_subfolder)
    if not os.path.exists(dataset_folder):
        raise FileNotFoundError(f"Folder '{source_subfolder}' not found in the extracted dataset.")
    return dataset_folder

def select_random_images(source_dir):
    print("Selecting random images...")
    # List image files with common extensions
    supported_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(supported_exts)]
    
    if len(image_files) < num_images:
        raise ValueError(f"Source folder {source_dir} only has {len(image_files)} images; at least {num_images} required.")
    
    selected_files = random.sample(image_files, num_images)
    return selected_files

def copy_images(source_dir, images):
    os.makedirs(target_folder, exist_ok=True)
    print("Copying images...")
    for img in images:
        src_path = os.path.join(source_dir, img)
        dst_path = os.path.join(target_folder, img)
        shutil.copy(src_path, dst_path)
    print(f"Successfully copied {len(images)} images to {target_folder}.")

if __name__ == "__main__":
    # Set a fixed seed for reproducibility
    random.seed(42)
    
    # Step 1: Download the dataset using Kaggle API
    download_dataset()
    
    # Step 2: Extract the downloaded dataset
    dataset_path = extract_dataset()
    
    # Step 3: Randomly select images and copy them
    selected = select_random_images(dataset_path)
    copy_images(dataset_path, selected)