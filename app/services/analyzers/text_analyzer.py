RISK_KEYWORDS = {
    "hate_speech": ["hate", "racist", "slur", "kill them"],
    "violence": ["kill", "attack", "shoot", "weapon", "blood"],
    "sexual": ["explicit", "nude", "sex"],
    "drug_related": ["cocaine", "heroin", "meth", "drug"],
    "self_harm": ["suicide", "self harm", "cut myself"],
}


def analyze_transcript_segments(segments):
    findings = []

    for segment in segments:
        text = segment.get("text", "").lower()
        start_time = float(segment.get("start_time", 0))
        end_time = float(segment.get("end_time", start_time + 5))

        for category, keywords in RISK_KEYWORDS.items():
            matched = [kw for kw in keywords if kw in text]

            if matched:
                findings.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "category": category,
                    "severity": "high" if category in ["violence", "self_harm"] else "medium",
                    "confidence": 0.75,
                    "evidence": f"Transcript contains risk terms: {', '.join(matched)}",
                    "source": "transcript_analysis"
                })

    return findings