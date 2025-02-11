# app.py: Main application file for the Semantic Image Search application.
import gradio as gr
import os
from PIL import Image
from typing import List
import sys
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from utils.embeddings import EmbeddingGenerator
from utils.indexer import ImageIndexer
from config import Config

class ImageSearchApp:
    def __init__(self):
        """Initialize the image search application."""
        try:
            self.embedding_generator = EmbeddingGenerator()
            self.indexer = ImageIndexer(self.embedding_generator)
            self.index, self.image_paths = self.indexer.load_index()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize application: {e}")

    def search_images(self, query: str, num_results: int) -> List[str]:
        """Search for images based on text query."""
        try:
            query_embedding = self.embedding_generator.get_text_embedding(query)
            distances, indices = self.indexer.search(query_embedding, num_results)
            # Return image paths corresponding to the indices
            return [self.image_paths[i] for i in indices[0]]
        except Exception as e:
            raise RuntimeError(f"Search failed: {e}")

    def load_images(self, image_paths: List[str]) -> List[Image.Image]:
        """Load images from disk given a list of paths."""
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                print(f"Error loading {path}: {e}")
        return images

def search_interface(query: str, num_results: int):
    if not query or query.strip() == "":
        return "No query provided. Please type your query.", [], None

    try:
        app_instance = ImageSearchApp()
    except Exception as init_err:
        return f"Failed to initialize application: {init_err}", [], None

    try:
        results = app_instance.search_images(query, num_results)
        images = app_instance.load_images(results)
        status = f"Found {len(images)} results for query: '{query}'"
        return status, images, query
    except Exception as search_err:
        return f"Search failed: {search_err}", [], None

# Updated custom CSS for a larger, more spacious UI look.
custom_css = """
/* Increase container width and add padding for larger UI */
.gradio-container {
    max-width: 1400px;
    margin: auto;
    padding: 20px;
}

/* Increase header font size and add margin */
.gradio-header {
    text-align: center;
    margin-bottom: 30px;
    font-size: 2rem;
}

/* Style search button with a bigger font */
.gradio-button {
    background-color: #4CAF50 !important;
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 5px !important;
    font-size: 18px !important;
}

.gradio-button:hover {
    background-color: #45a049 !important;
}

/* Increase spacing above the gallery */
.gradio-gallery {
    margin-top: 30px;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🔍 Semantic Image Search", elem_classes=["gradio-header"])
    gr.Markdown("Search for images using natural language descriptions. Please type your query below.")

    with gr.Row():
        query_input = gr.Textbox(
            label="Enter your search query:",
            placeholder="e.g., 'a sunny beach scene'",
            interactive=True
        )
        num_results_input = gr.Slider(
            label="Number of results",
            minimum=1,
            maximum=Config.MAX_NUM_RESULTS,
            value=Config.DEFAULT_NUM_RESULTS,
            step=1,
            interactive=True
        )
    
    search_button = gr.Button("🔍 Search", elem_classes=["gradio-button"])
    
    output_status = gr.Textbox(label="Status", interactive=False)
    gallery = gr.Gallery(label="Search Results", show_label=True, columns=3, elem_classes=["gradio-gallery"])
    transcribed_query = gr.Textbox(label="Query", visible=False)

    search_button.click(
        fn=search_interface,
        inputs=[query_input, num_results_input],
        outputs=[output_status, gallery, transcribed_query]
    )

if __name__ == "__main__":
    demo.launch()