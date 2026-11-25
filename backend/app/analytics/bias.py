def position_bias(original, reversed):
    if len(original) != len(reversed) or not original:
        return {"sample_size": 0, "sensitive_preference_rate": 0.0}
    changed = sum(a != b for a, b in zip(original, reversed))
    return {"sample_size": len(original), "sensitive_preference_rate": round(changed / len(original), 4)}
