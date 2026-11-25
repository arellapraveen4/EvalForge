def split_claims(text: str) -> list[str]:
    if not text:
        return []
    import re
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text.strip()) if sentence.strip()]
