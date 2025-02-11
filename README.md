# Semantic Image Search Project

This project provides a semantic image search application that allows users to search for images using natural language descriptions. The application leverages the **CLIP (Contrastive Language–Image Pretraining)** model to generate embeddings for both text and images, and uses **FAISS (Facebook AI Similarity Search)** for efficient similarity search.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Creating Embeddings and Index](#creating-embeddings-and-index)
   - [Running the Application](#running-the-application)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Dependencies](#dependencies)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## Project Overview

The project consists of the following components:
- **Embedding Generation**: Uses the CLIP model to generate embeddings for images and text.
- **Indexing**: Creates a FAISS index for efficient similarity search.
- **Search Interface**: A Gradio-based web interface for searching images using text queries.

The workflow is as follows:
1. Generate embeddings for all images in a directory.
2. Create a FAISS index using the embeddings.
3. Use the index to search for images based on text queries.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/semantic-image-search.git
   cd semantic-image-search
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Creating Embeddings and Index
Before running the application, you need to generate embeddings and create a FAISS index for your images.

1. Place your images in a directory (e.g., `dataset/images`).
2. Run the `create_embeddings.py` script:
   ```bash
   python create_embeddings.py --image_dir /path/to/your/image/directory
   ```
   Replace `/path/to/your/image/directory` with the path to your image directory.

   This script will:
   - Generate embeddings for all images in the directory.
   - Create a FAISS index and save it to the `dataset/embeddings` directory (as specified in `config.py`).

   **Note**: Ensure the `dataset/embeddings` directory exists or update the `Config.DATA_DIR` path in `config.py`.

### 2. Running the Application
Once the embeddings and index are created, you can start the application.

1. Run the `app.py` script:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to the URL provided in the terminal (usually `http://127.0.0.1:7860`).

3. Use the interface to:
   - Enter a text query (e.g., "a sunny beach scene").
   - Adjust the number of results using the slider.
   - Click the "Search" button to view the results.

---

## Configuration
The project's configuration is managed in the `config.py` file. Key settings include:

- **`IMAGE_EXTENSIONS`**: Supported image file extensions.
- **`MODEL_NAME`**: The CLIP model to use (default: `clip-ViT-B-32`).
- **`DEVICE`**: The device to use for inference (`cpu` or `cuda`).
- **`DATA_DIR`**: Directory to save embeddings and index files.
- **`INDEX_PATH`**, **`EMBEDDINGS_PATH`**, **`PATHS_FILE`**: Paths to the FAISS index, embeddings, and image paths files.

Update these settings as needed.

---

## Project Structure
```
semantic-image-search/
├── create_embeddings.py       # Script to generate embeddings and create FAISS index
├── app.py                     # Main application file (Gradio interface)
├── config.py                  # Configuration settings
├── utils/
│   ├── embeddings.py          # Embedding generation using CLIP
│   └── indexer.py             # FAISS index creation and search
├── dataset/                   # Directory for images and embeddings
│   ├── images/                # Place your images here
│   └── embeddings/            # Embeddings and index files are saved here
├── requirements.txt           # List of dependencies
└── README.md                  # This file
```

---

## Dependencies
The project relies on the following Python libraries:
- `torch` (PyTorch)
- `sentence-transformers` (for CLIP model)
- `faiss-cpu` or `faiss-gpu` (for similarity search)
- `gradio` (for the web interface)
- `Pillow` (for image processing)
- `numpy` (for numerical operations)

Install them using:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting
1. **CUDA/GPU Issues**:
   - If you encounter CUDA-related errors, ensure you have the correct version of PyTorch installed for your GPU.
   - Alternatively, set `DEVICE = "cpu"` in `config.py`.

2. **File Not Found Errors**:
   - Ensure the `dataset/embeddings` directory exists or update `Config.DATA_DIR` in `config.py`.

3. **Gradio Interface Not Loading**:
   - Ensure the application is running and accessible at `http://127.0.0.1:7860`.
   - Check for port conflicts or firewall settings.

4. **No Results Found**:
   - Ensure the image directory contains valid images with supported extensions (`.png`, `.jpg`, `.jpeg`, `.webp`).

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy building and using your semantic image search application! 🚀
