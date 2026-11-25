from scipy.stats import spearmanr


def calculate_correlation(values_a, values_b):
    if len(values_a) != len(values_b) or len(values_a) < 2:
        return None
    result = spearmanr(values_a, values_b)
    return round(float(result.statistic), 4)
