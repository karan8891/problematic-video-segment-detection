import os
import subprocess
from functools import lru_cache


def extract_audio(video_path: str, video_id: str) -> str:
    artifact_dir = os.path.join("data", "artifacts", video_id)
    audio_dir = os.path.join(artifact_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    audio_path = os.path.join(audio_dir, "audio.wav")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
        "-y"
    ]

    subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    return audio_path


@lru_cache(maxsize=1)
def load_whisper_model():
    import whisper
    return whisper.load_model("tiny")


def transcribe_audio(audio_path: str):
    model = load_whisper_model()

    result = model.transcribe(
        audio_path,
        fp16=False
    )

    segments = []

    for segment in result.get("segments", []):
        segments.append({
            "start_time": float(segment.get("start", 0.0)),
            "end_time": float(segment.get("end", 0.0)),
            "text": segment.get("text", "")
        })

    return segments