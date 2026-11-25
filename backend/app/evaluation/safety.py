UNSAFE_PATTERNS = ("bomb", "weapon", "poison", "self-harm", "suicide", "kill")


def assess_safety(text: str) -> dict:
    normalized = (text or "").lower()
    matches = [pattern for pattern in UNSAFE_PATTERNS if pattern in normalized]
    return {"score": 1 if matches else 5, "flags": matches, "warning": bool(matches)}
