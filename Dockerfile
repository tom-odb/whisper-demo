# Use the official slim Python image (updated to Python 3.11)
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and to flush output immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set an environment variable for the model directory
ENV MODEL_DIR=/models/whisper

# Install system dependencies (ffmpeg is required by Whisper to process audio)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the model directory (this directory will be mounted as a volume)
RUN mkdir -p /models/whisper

# Declare the /models directory as a mount point (persistent volume)
VOLUME ["/models"]

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app into the container.
COPY app.py .

# Expose port 80 (or adjust as needed)
EXPOSE 80

# Define the default command to run the app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
