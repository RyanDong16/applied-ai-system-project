from logic_utils import (
    # FIX: I implemented the missing game logic in logic_utils.py (matching the original app.py code and correcting the string‑comparison bug) and then added a focused regression test in test_game_logic.py
    check_guess,
    get_range_for_difficulty,
    update_score,
    parse_guess,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_string_secret_comparison_bug():
    # Verify numeric comparison still works when secret is a string
    outcome, _ = check_guess(3, "20")
    assert outcome == "Too Low"


def test_string_secret_too_high():
    # regression test for the bug where string comparison would treat
    # "30" as less than "4" lexicographically.  Guess 30 vs secret "20"
    # should correctly return "Too High".
    outcome, message = check_guess(30, "20")
    assert outcome == "Too High"
    assert "LOWER" in message

# FIX: I implemented the missing game logic in logic_utils.py (matching the original app.py code and correcting the string‑comparison bug) and then added a focused regression test in test_game_logic.py
def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    assert get_range_for_difficulty("something") == (1, 100)


def test_update_score_win_and_hints():
    # starting score 0, first win should give positive points
    new = update_score(0, "Win", 1)
    assert new > 0
    # outcomes other than Win affect score appropriately
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
