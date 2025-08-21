import os
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# ---- Config ----
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTS = {".mp3", ".wav"}  # keep it simple per requirements
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# Choose a default transcription model.
# You can switch to "gpt-4o-transcribe" if you want the larger model.
DEFAULT_TRANSCRIBE_MODEL = os.getenv("TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Initialize OpenAI client (expects OPENAI_API_KEY in env)
client = OpenAI()

def allowed_file(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Max 50MB."}), 413

@app.post("/transcribe")
def transcribe():
    """
    Accepts multipart/form-data with:
    - file: audio file (.mp3/.wav)
    - language: optional BCP-47 or ISO code (e.g., 'en', 'hr', 'es')
    - model: optional override (e.g., gpt-4o-transcribe)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(f.filename):
        return jsonify({"error": "Unsupported file type. Use .mp3 or .wav."}), 400

    language = request.form.get("language", "").strip() or None
    model = request.form.get("model", "").strip() or DEFAULT_TRANSCRIBE_MODEL

    # Persist the upload to disk (optional but useful for debugging)
    filename = secure_filename(f.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    saved_path = UPLOAD_DIR / f"{timestamp}-{filename}"
    f.save(saved_path)

    try:
        # Send to OpenAI Transcriptions
        with open(saved_path, "rb") as audio_file:
            # The Python SDK returns an object with a `.text` field for transcriptions
            result = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language=language  # let OpenAI auto-detect if None
                # You can also set: response_format="text"  # returns raw text
            )
        text = getattr(result, "text", None)
        if not text:
            # Fallback: some SDK versions put text under result["text"]
            try:
                text = result["text"]
            except Exception:
                text = ""

        return jsonify({
            "ok": True,
            "text": text,
            "model": model,
            "language": language
        })
    except Exception as e:
    # Don't leak internals in production; log instead.
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500


if __name__ == "__main__":
    # Debug=True auto-reloads on changes; remove in production
    app.run(host="127.0.0.1", port=5000, debug=True)


