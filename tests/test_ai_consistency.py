from logic_utils import (
    classify_ai_hint,
    evaluate_ai_consistency,
    evaluate_ai_consistency_for_case,
    generate_ai_hint,
    hint_violates_guardrails,
)


def test_generate_ai_hint_points_higher_when_guess_is_low():
    output = generate_ai_hint(
        secret=50,
        guess=30,
        history=[10, 20, 30],
        low=1,
        high=100,
        attempts=3,
        attempt_limit=8,
    )
    assert classify_ai_hint(output) == "HIGHER"


def test_generate_ai_hint_points_lower_when_guess_is_high():
    output = generate_ai_hint(
        secret=50,
        guess=70,
        history=[80, 75, 70],
        low=1,
        high=100,
        attempts=3,
        attempt_limit=8,
    )
    assert classify_ai_hint(output) == "LOWER"


def test_generate_ai_hint_points_correct_when_guess_matches_secret():
    output = generate_ai_hint(
        secret=50,
        guess=50,
        history=[40, 45, 50],
        low=1,
        high=100,
        attempts=3,
        attempt_limit=8,
    )
    assert classify_ai_hint(output) == "CORRECT"


def test_ai_hint_does_not_reveal_secret():
    secret = 42
    output = generate_ai_hint(
        secret=secret,
        guess=20,
        history=[10, 15, 20],
        low=1,
        high=100,
        attempts=3,
        attempt_limit=8,
    )
    assert hint_violates_guardrails(output, secret) is False
    assert str(secret) not in output


def test_evaluate_ai_consistency_for_case_is_fully_consistent():
    report = evaluate_ai_consistency_for_case(
        secret=50,
        guess=30,
        history=[10, 20, 30],
        low=1,
        high=100,
        attempts=3,
        attempt_limit=8,
        runs_per_case=10,
    )
    assert report["consistency_rate"] == 1.0
    assert report["guardrail_violations"] == 0
    assert report["most_common_category"] == "HIGHER"


def test_evaluate_ai_consistency_summary_passes():
    report = evaluate_ai_consistency(
        secret=50,
        history=[10, 20, 30],
        low=1,
        high=100,
        attempt_limit=8,
        runs_per_case=10,
    )
    assert report["average_consistency"] == 1.0
    assert report["total_guardrail_violations"] == 0
    assert report["overall_status"] == "PASS"


def test_classify_ai_hint_invalid_when_unrecognized():
    assert classify_ai_hint("This sentence has no directional hint.") == "INVALID"