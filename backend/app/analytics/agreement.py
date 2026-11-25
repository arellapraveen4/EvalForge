from collections import Counter


def percentage_agreement(labels):
    if not labels:
        return None
    counts = Counter(labels)
    return round(max(counts.values()) / len(labels), 4)


def group_agreement(rows: list[list[str]]) -> dict:
    per_task = [percentage_agreement(row) for row in rows]
    return {
        "mean_agreement": round(sum(v for v in per_task if v is not None) / len(per_task), 4) if per_task else None,
        "per_task": per_task,
    }
