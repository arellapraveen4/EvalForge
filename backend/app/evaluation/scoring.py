def calculate_weighted_score(scores, rubric):
    total = 0.0
    total_weight = 0.0
    for dimension, config in rubric.items():
        if dimension not in scores:
            continue
        score = scores[dimension].get("score") if isinstance(scores[dimension], dict) else scores[dimension]
        if isinstance(score, (int, float)):
            total += float(score) * float(config["weight"])
            total_weight += float(config["weight"])
    if total_weight == 0:
        return None
    return round(total / total_weight, 2)
