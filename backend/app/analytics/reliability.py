import random


def bootstrap_metric(values, metric_fn, iterations=1000, confidence=0.95):
    if not values:
        return {"estimate": None, "lower": None, "upper": None}
    estimates = []
    rng = random.Random(42)
    for _ in range(iterations):
        sample = [rng.choice(values) for _ in values]
        estimate = metric_fn(sample)
        if estimate is not None:
            estimates.append(estimate)
    if not estimates:
        return {"estimate": None, "lower": None, "upper": None}
    estimates.sort()
    tail = (1 - confidence) / 2
    return {
        "estimate": round(metric_fn(values), 4),
        "lower": round(estimates[int(tail * len(estimates))], 4),
        "upper": round(estimates[int((1 - tail) * len(estimates)) - 1], 4),
    }
