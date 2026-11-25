from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix


def evaluate_judge(human_labels, ai_labels):
    labels = ["A", "B", "Tie", "BothPoor"]
    return {
        "accuracy": accuracy_score(human_labels, ai_labels),
        "kappa": cohen_kappa_score(human_labels, ai_labels),
        "confusion_matrix": confusion_matrix(human_labels, ai_labels, labels=labels).tolist(),
    }
