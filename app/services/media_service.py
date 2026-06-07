import os
import subprocess
import requests


def download_video(video_url: str, video_id: str) -> str:
    video_dir = os.path.join("data", "videos", video_id)
    os.makedirs(video_dir, exist_ok=True)

    output_path = os.path.join(video_dir, "input.mp4")

    response = requests.get(video_url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    return output_path


def extract_frames(video_path: str, video_id: str, every_seconds: int = 5):
    artifact_dir = os.path.join("data", "artifacts", video_id)
    frames_dir = os.path.join(artifact_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    output_pattern = os.path.join(frames_dir, "frame_%04d.jpg")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{every_seconds}",
        "-q:v", "2",
        output_pattern,
        "-y"
    ]

    subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    frame_paths = [
        os.path.join(frames_dir, file)
        for file in sorted(os.listdir(frames_dir))
        if file.endswith(".jpg")
    ]

    return frame_paths


def get_video_duration(video_path: str) -> float:
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    return float(result.stdout.strip())