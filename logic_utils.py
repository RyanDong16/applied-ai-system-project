import logging
from pathlib import Path
from typing import Any

GAME_STATUS_PLAYING = "playing"
GAME_STATUS_WON = "won"
GAME_STATUS_LOST = "lost"

DEFAULT_DIFFICULTY = "Normal"
DEFAULT_SCORE = 0

ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def configure_logging(log_path: str = "logs/game.log") -> logging.Logger:
    """
    Configure and return a shared application logger.

    Safe to call multiple times; handlers are only added once.
    """
    logger = logging.getLogger("glitchy_guesser")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def log_game_event(logger: logging.Logger, event_name: str, **details: Any) -> None:
    """
    Log a structured event for debugging and auditing.
    """
    ordered_items = sorted(details.items(), key=lambda item: item[0])
    detail_text = ", ".join(f"{key}={value!r}" for key, value in ordered_items)
    logger.info("event=%s%s", event_name, f" | {detail_text}" if detail_text else "")


def get_range_for_difficulty(difficulty: str):
    """
    Return (low, high) inclusive range for a given difficulty.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    """
    Return allowed attempts for a difficulty, with a safe fallback.
    """
    return ATTEMPT_LIMIT_MAP.get(difficulty, ATTEMPT_LIMIT_MAP[DEFAULT_DIFFICULTY])


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
    try:
        secret_val = int(secret) if isinstance(secret, str) else secret
    except Exception:
        secret_val = secret

    try:
        guess_val = int(guess) if isinstance(guess, str) else guess
    except Exception:
        guess_val = guess

    if guess_val == secret_val:
        return "Win", "🎉 Correct!"

    try:
        if guess_val > secret_val:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess_val)
        s = str(secret_val)
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.
    """
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


def sanitize_history(history: Any) -> list:
    """
    Ensure history is always a safe list.
    """
    if isinstance(history, list):
        return history
    return []


def validate_game_state(
    secret: Any,
    attempts: Any,
    attempt_limit: Any,
    score: Any,
    status: Any,
    low: Any,
    high: Any,
):
    """
    Validate session state used by the game.

    Returns:
        (is_valid: bool, errors: list[str])
    """
    errors = []

    if not isinstance(low, int) or not isinstance(high, int):
        errors.append("range bounds must be integers")
    elif low >= high:
        errors.append("range bounds are invalid")

    if not isinstance(secret, int):
        errors.append("secret must be an integer")
    elif isinstance(low, int) and isinstance(high, int):
        if not (low <= secret <= high):
            errors.append("secret is outside the allowed range")

    if not isinstance(attempt_limit, int) or attempt_limit <= 0:
        errors.append("attempt_limit must be a positive integer")

    if not isinstance(attempts, int):
        errors.append("attempts must be an integer")
    elif attempts < 0:
        errors.append("attempts cannot be negative")
    elif isinstance(attempt_limit, int) and attempt_limit > 0 and attempts > attempt_limit:
        errors.append("attempts exceeded attempt limit")

    if not isinstance(score, int):
        errors.append("score must be an integer")

    if status not in {GAME_STATUS_PLAYING, GAME_STATUS_WON, GAME_STATUS_LOST}:
        errors.append("status is invalid")

    return len(errors) == 0, errors