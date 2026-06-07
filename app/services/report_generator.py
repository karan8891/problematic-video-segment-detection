def calculate_overall_risk(findings):
    if not findings:
        return "low"

    severities = [f.get("severity") for f in findings]

    if "high" in severities:
        return "high"

    if "medium" in severities:
        return "medium"

    return "low"