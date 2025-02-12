FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port Gradio uses (default 7860)
EXPOSE 7860

# Launch the application
CMD ["python", "app.py"]
