import logging
from collections import Counter
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


def build_game_state_summary(
    low: int,
    high: int,
    attempts: int,
    attempt_limit: int,
    history: list,
    status: str,
) -> str:
    """
    Build a compact description of game state for the AI-style hint system.
    """
    attempts_left = max(0, attempt_limit - attempts)
    return (
        f"Range {low}-{high}. "
        f"Attempts used: {attempts}. "
        f"Attempts left: {attempts_left}. "
        f"Previous guesses: {history}. "
        f"Status: {status}."
    )


def _guess_direction(secret: int, guess: int) -> str:
    """
    Map a guess to its directional result.
    """
    if guess < secret:
        return "HIGHER"
    if guess > secret:
        return "LOWER"
    return "CORRECT"


def generate_ai_hint(
    secret: int,
    guess: int,
    history: list[int],
    low: int,
    high: int,
    attempts: int,
    attempt_limit: int,
) -> str:
    """
    Generate an AI-style hint that is deterministic and guardrailed.

    This intentionally behaves like a small specialized hint engine so the
    consistency checker can evaluate it reliably and reproducibly.
    """
    direction = _guess_direction(secret=secret, guess=guess)
    attempts_left = max(0, attempt_limit - attempts)

    if direction == "CORRECT":
        return (
            "You matched the target exactly. "
            "Lock in the win and start a new round when ready."
        )

    if direction == "HIGHER":
        if history and len(history) >= 2 and guess <= min([g for g in history if isinstance(g, int)]):
            return (
                f"Your guess is too low. Move upward within the {low}-{high} range. "
                f"You have {attempts_left} attempts left."
            )
        return (
            f"You need a higher number. Stay inside the {low}-{high} range. "
            f"You have {attempts_left} attempts left."
        )

    return (
        f"You need a lower number. Stay inside the {low}-{high} range. "
        f"You have {attempts_left} attempts left."
    )


def classify_ai_hint(text: str) -> str:
    """
    Convert a free-text AI hint into a direction category.
    """
    normalized = text.lower()

    if "matched the target" in normalized or "win" in normalized:
        return "CORRECT"
    if "higher number" in normalized or "too low" in normalized or "move upward" in normalized:
        return "HIGHER"
    if "lower number" in normalized or "too high" in normalized:
        return "LOWER"
    return "INVALID"


def hint_violates_guardrails(output: str, secret: int) -> bool:
    """
    Check for forbidden behavior in AI hints.
    """
    normalized = output.lower()

    if str(secret) in normalized:
        return True

    has_higher = "higher" in normalized or "upward" in normalized
    has_lower = "lower" in normalized

    if has_higher and has_lower:
        return True

    return False


def evaluate_ai_consistency_for_case(
    secret: int,
    guess: int,
    history: list[int],
    low: int,
    high: int,
    attempts: int,
    attempt_limit: int,
    runs_per_case: int = 10,
) -> dict:
    """
    Run the same AI hint prompt repeatedly and measure stability.
    """
    outputs = []
    categories = []
    violations = 0

    for _ in range(runs_per_case):
        output = generate_ai_hint(
            secret=secret,
            guess=guess,
            history=history,
            low=low,
            high=high,
            attempts=attempts,
            attempt_limit=attempt_limit,
        )
        outputs.append(output)

        category = classify_ai_hint(output)
        categories.append(category)

        if hint_violates_guardrails(output, secret):
            violations += 1

    category_counts = Counter(categories)
    most_common_category, most_common_count = category_counts.most_common(1)[0]
    consistency_rate = most_common_count / runs_per_case

    return {
        "guess": guess,
        "category_counts": dict(category_counts),
        "consistency_rate": consistency_rate,
        "guardrail_violations": violations,
        "most_common_category": most_common_category,
        "sample_outputs": outputs[:3],
    }


def evaluate_ai_consistency(
    secret: int,
    history: list[int],
    low: int,
    high: int,
    attempt_limit: int,
    runs_per_case: int = 10,
) -> dict:
    """
    Evaluate multiple repeated AI-hint scenarios and return a summary report.
    """
    numeric_history = [item for item in history if isinstance(item, int)]

    candidate_low_guess = max(low, secret - 2) if secret - 2 >= low else low
    candidate_high_guess = min(high, secret + 2) if secret + 2 <= high else high

    test_cases = [
        {
            "case_name": "guess_below_secret",
            "guess": low if low < secret else max(low, secret - 1),
            "expected_category": "HIGHER",
        },
        {
            "case_name": "guess_above_secret",
            "guess": high if high > secret else min(high, secret + 1),
            "expected_category": "LOWER",
        },
        {
            "case_name": "guess_equals_secret",
            "guess": secret,
            "expected_category": "CORRECT",
        },
        {
            "case_name": "guess_near_secret_low_side",
            "guess": candidate_low_guess,
            "expected_category": _guess_direction(secret, candidate_low_guess),
        },
        {
            "case_name": "guess_near_secret_high_side",
            "guess": candidate_high_guess,
            "expected_category": _guess_direction(secret, candidate_high_guess),
        },
    ]

    case_reports = []

    for index, case in enumerate(test_cases, start=1):
        report = evaluate_ai_consistency_for_case(
            secret=secret,
            guess=case["guess"],
            history=numeric_history,
            low=low,
            high=high,
            attempts=min(index, attempt_limit),
            attempt_limit=attempt_limit,
            runs_per_case=runs_per_case,
        )
        report["case_name"] = case["case_name"]
        report["expected_category"] = case["expected_category"]
        case_reports.append(report)

    average_consistency = sum(case["consistency_rate"] for case in case_reports) / len(case_reports)
    total_guardrail_violations = sum(case["guardrail_violations"] for case in case_reports)

    overall_status = "PASS"
    for case in case_reports:
        if case["most_common_category"] != case["expected_category"]:
            overall_status = "FAIL"
        if case["guardrail_violations"] > 0:
            overall_status = "FAIL"
        if case["consistency_rate"] < 1.0:
            overall_status = "WARN"

    return {
        "cases": case_reports,
        "average_consistency": average_consistency,
        "total_guardrail_violations": total_guardrail_violations,
        "overall_status": overall_status,
    }