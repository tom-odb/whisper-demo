import os
import tempfile
import whisper
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI(
    title="Whisper Transcription API",
    description="Upload an MP3 file to be transcribed using the Whisper API.",
    version="1.0.0"
)

# Get the model directory from the environment (default to /models/whisper)
MODEL_DIR = os.environ.get("MODEL_DIR", "/models/whisper")

# Load the Whisper model once at startup using a persistent download root.
try:
    model = whisper.load_model("turbo", download_root=MODEL_DIR)
except Exception as e:
    raise RuntimeError(f"Failed to load Whisper model: {e}")

@app.post("/transcribe", summary="Transcribe an audio file", response_description="The transcription result")
async def transcribe(file: UploadFile = File(...)):
    # Validate that the uploaded file is an MP3
    if not file.filename.lower().endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an mp3 file.")

    # Save the uploaded file to a temporary file
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.") from e

    # Transcribe the audio file using Whisper
    try:
        result = model.transcribe(temp_path)
        transcription = result.get("text", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Transcription failed.") from e
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {"transcription": transcription}
