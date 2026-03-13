#FIX: Refactored logic into logic_utils.py using Copilot Agent mode).

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # same logic as the original app but pulled into a reusable helper
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    # default fallback
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # normalize types so we can compare numerically even if the secret
    # is stored as a string (bug we encountered earlier).  If both
    # values are convertible to int, compare as ints; otherwise fall back
    # to the original semantics.
    try:
        # try casting both to int for a fair numeric comparison
        if isinstance(secret, str):
            secret_val = int(secret)
        else:
            secret_val = secret
    except Exception:
        # if conversion fails just keep original secret
        secret_val = secret

    # same for guess just in case
    try:
        if isinstance(guess, str):
            guess_val = int(guess)
        else:
            guess_val = guess
    except Exception:
        guess_val = guess

    if guess_val == secret_val:
        return "Win", "🎉 Correct!"

    try:
        if guess_val > secret_val:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # fallback to string comparison logic from original app
        g = str(guess_val)
        s = str(secret_val)
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
