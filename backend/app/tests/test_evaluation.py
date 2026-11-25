from app.evaluation.deterministic import exact_match, word_overlap
from app.evaluation.pairwise import compare_responses
from app.evaluation.scoring import calculate_weighted_score
from app.evaluation.rubrics import RUBRICS


def test_exact_match_normalizes_text():
    assert exact_match("Paris!", " paris ") == 1


def test_word_overlap():
    assert word_overlap("the capital is paris", "Paris") == 1.0


def test_weighted_score():
    scores = {"correctness": 5, "instruction_following": 3, "relevance": 4, "completeness": 3, "clarity": 4}
    assert calculate_weighted_score(scores, RUBRICS["general"]) == 3.95


def test_pairwise_comparison():
    assert compare_responses(4.0, 3.0) == "A"
    assert compare_responses(3.0, 4.0) == "B"
