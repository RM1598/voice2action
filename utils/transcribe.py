import tempfile
import whisper

# Load the Whisper model once when the file is imported
# "base" is a good balance between quality and speed for a student project
model = whisper.load_model("base")


def transcribe_audio(uploaded_file):
    """
    Save uploaded audio temporarily and return the transcribed text.
    """
    suffix = ".wav"
    original_name = getattr(uploaded_file, "name", "")

    if "." in original_name:
        suffix = "." + original_name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    result = model.transcribe(temp_path)
    text = result.get("text", "").strip()
    return text