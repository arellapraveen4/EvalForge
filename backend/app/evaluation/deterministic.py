import re


def normalize(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[^\w\s]", "", text)


def exact_match(prediction, reference):
    if prediction is None or reference is None:
        return None
    return int(normalize(prediction) == normalize(reference))


def word_overlap(prediction, reference):
    if not prediction or not reference:
        return 0.0
    prediction_words = set(normalize(prediction).split())
    reference_words = set(normalize(reference).split())
    if not reference_words:
        return 0.0
    return len(prediction_words & reference_words) / len(reference_words)
