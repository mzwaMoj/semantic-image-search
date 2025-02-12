import os
import random
import shutil

random.seed(42)
# Define source and target directories
source_dir = "./dataset/sample_data/test_data_v2"
target_dir = "./sample_images"

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# List all image files in the source directory
image_files = [f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

# Check if there are at least 500 images
if len(image_files) < 500:
    raise ValueError("The source directory does not contain 500 images.")

# Randomly select 500 images
selected_images = random.sample(image_files, 500)

# Copy selected images to the target directory
for image in selected_images:
    src_path = os.path.join(source_dir, image)
    dst_path = os.path.join(target_dir, image)
    shutil.copy(src_path, dst_path)

print(f"Successfully copied {len(selected_images)} images to {target_dir}.")
