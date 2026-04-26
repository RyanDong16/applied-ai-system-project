from logic_utils import (
    GAME_STATUS_LOST,
    GAME_STATUS_PLAYING,
    GAME_STATUS_WON,
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    sanitize_history,
    update_score,
    validate_game_state,
)


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_string_secret_comparison_bug():
    outcome, _ = check_guess(3, "20")
    assert outcome == "Too Low"


def test_string_secret_too_high():
    outcome, message = check_guess(30, "20")
    assert outcome == "Too High"
    assert "LOWER" in message


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    assert get_range_for_difficulty("something") == (1, 100)


def test_get_attempt_limit():
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5
    assert get_attempt_limit("something") == 8


def test_update_score_win_and_hints():
    new = update_score(0, "Win", 1)
    assert new > 0
    assert update_score(10, "Too High", 2) in (5, 15)
    assert update_score(10, "Too Low", 3) == 5


def test_parse_guess():
    ok, val, err = parse_guess(None)
    assert not ok and err

    ok, val, err = parse_guess("")
    assert not ok and err

    ok, val, err = parse_guess("42.0")
    assert ok and val == 42

    ok, val, err = parse_guess("abc")
    assert not ok and "number" in err


def test_sanitize_history_returns_same_list():
    history = [1, 2, "3"]
    assert sanitize_history(history) == history


def test_sanitize_history_replaces_invalid_value():
    assert sanitize_history(None) == []
    assert sanitize_history("not-a-list") == []


def test_validate_game_state_success():
    valid, errors = validate_game_state(
        secret=50,
        attempts=2,
        attempt_limit=8,
        score=10,
        status=GAME_STATUS_PLAYING,
        low=1,
        high=100,
    )
    assert valid is True
    assert errors == []


def test_validate_game_state_rejects_secret_out_of_range():
    valid, errors = validate_game_state(
        secret=500,
        attempts=2,
        attempt_limit=8,
        score=10,
        status=GAME_STATUS_PLAYING,
        low=1,
        high=100,
    )
    assert valid is False
    assert "secret is outside the allowed range" in errors


def test_validate_game_state_rejects_negative_attempts():
    valid, errors = validate_game_state(
        secret=50,
        attempts=-1,
        attempt_limit=8,
        score=10,
        status=GAME_STATUS_PLAYING,
        low=1,
        high=100,
    )
    assert valid is False
    assert "attempts cannot be negative" in errors


def test_validate_game_state_rejects_attempt_overflow():
    valid, errors = validate_game_state(
        secret=50,
        attempts=9,
        attempt_limit=8,
        score=10,
        status=GAME_STATUS_PLAYING,
        low=1,
        high=100,
    )
    assert valid is False
    assert "attempts exceeded attempt limit" in errors


def test_validate_game_state_rejects_invalid_status():
    valid, errors = validate_game_state(
        secret=50,
        attempts=1,
        attempt_limit=8,
        score=10,
        status="broken",
        low=1,
        high=100,
    )
    assert valid is False
    assert "status is invalid" in errors


def test_validate_game_state_allows_win_and_loss_statuses():
    valid_won, errors_won = validate_game_state(
        secret=10,
        attempts=1,
        attempt_limit=6,
        score=50,
        status=GAME_STATUS_WON,
        low=1,
        high=20,
    )
    valid_lost, errors_lost = validate_game_state(
        secret=10,
        attempts=6,
        attempt_limit=6,
        score=0,
        status=GAME_STATUS_LOST,
        low=1,
        high=20,
    )

    assert valid_won is True
    assert errors_won == []
    assert valid_lost is True
    assert errors_lost == []