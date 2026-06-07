import os


def analyze_sampled_frames(frame_paths):
    findings = []

    for frame_path in frame_paths:
        filename = os.path.basename(frame_path)

        try:
            timestamp = float(filename.replace("frame_", "").replace(".jpg", ""))
        except ValueError:
            timestamp = 0.0

        # Lightweight prototype heuristic.
        # Production path: replace with CLIP / NSFW detector / violence detector.
        if "unsafe" in filename.lower():
            findings.append({
                "start_time": timestamp,
                "end_time": timestamp + 5,
                "category": "visual_risk",
                "severity": "medium",
                "confidence": 0.60,
                "evidence": "Frame marked as visually risky by prototype visual analyzer.",
                "source": "visual_analysis"
            })

    return findings