def analyze_metadata(metadata):
    findings = []

    duration = metadata.get("duration_seconds")

    if duration and duration > 1800:
        findings.append({
            "start_time": 0.0,
            "end_time": min(float(duration), 30.0),
            "category": "metadata_review",
            "severity": "low",
            "confidence": 0.50,
            "evidence": "Long video duration may require additional reviewer sampling.",
            "source": "metadata_analysis"
        })

    return findings