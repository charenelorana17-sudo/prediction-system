from app import calculate_accuracy_score


def test_accuracy_score_matches_expected_percentage_style_metric():
    actual = [100, 100, 100]
    predicted = [84, 84, 84]

    assert calculate_accuracy_score(actual, predicted) == 84


def test_accuracy_score_is_robust_to_outlier_predictions():
    actual = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    predicted = [84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 100000]

    assert calculate_accuracy_score(actual, predicted) == 84
