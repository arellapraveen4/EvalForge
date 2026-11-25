def compare_responses(score_a, score_b):
    if score_a is None or score_b is None:
        return "Tie"
    if score_a > score_b:
        return "A"
    if score_b > score_a:
        return "B"
    return "Tie"


def compare_dimensions(scores_a, scores_b):
    results = {}
    for dimension, a in scores_a.items():
        b = scores_b.get(dimension)
        if b is None:
            continue
        if isinstance(a, dict):
            a = a["score"]
        if isinstance(b, dict):
            b = b["score"]
        results[dimension] = "A" if a > b else "B" if b > a else "Tie"
    return results
