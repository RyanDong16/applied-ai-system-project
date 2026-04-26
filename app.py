import random
from pathlib import Path

import streamlit as st

from logic_utils import (
    GAME_STATUS_LOST,
    GAME_STATUS_PLAYING,
    GAME_STATUS_WON,
    DEFAULT_DIFFICULTY,
    DEFAULT_SCORE,
    check_guess,
    configure_logging,
    get_attempt_limit,
    get_range_for_difficulty,
    log_game_event,
    parse_guess,
    sanitize_history,
    update_score,
    validate_game_state,
)

# Ensure log directory exists and logging is configured once.
Path("logs").mkdir(exist_ok=True)
logger = configure_logging("logs/game.log")

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game with reliability guardrails built in.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

VALID_STATUSES = {GAME_STATUS_PLAYING, GAME_STATUS_WON, GAME_STATUS_LOST}


def initialize_game_state(selected_difficulty: str) -> None:
    """
    Initialize missing session state keys safely.
    """
    range_low, range_high = get_range_for_difficulty(selected_difficulty)

    if "difficulty" not in st.session_state:
        st.session_state.difficulty = selected_difficulty

    if "secret" not in st.session_state:
        st.session_state.secret = random.randint(range_low, range_high)

    if "attempts" not in st.session_state:
        st.session_state.attempts = 0

    if "score" not in st.session_state:
        st.session_state.score = DEFAULT_SCORE

    if "status" not in st.session_state:
        st.session_state.status = GAME_STATUS_PLAYING

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history = sanitize_history(st.session_state.history)


def reset_game(selected_difficulty: str, preserve_score: bool = False) -> None:
    """
    Reset the game safely for the selected difficulty.
    """
    range_low, range_high = get_range_for_difficulty(selected_difficulty)
    st.session_state.difficulty = selected_difficulty
    st.session_state.secret = random.randint(range_low, range_high)
    st.session_state.attempts = 0
    st.session_state.status = GAME_STATUS_PLAYING
    st.session_state.history = []
    if not preserve_score:
        st.session_state.score = DEFAULT_SCORE

    log_game_event(
        logger,
        "new_game",
        difficulty=selected_difficulty,
        low=range_low,
        high=range_high,
        preserve_score=preserve_score,
    )


def recover_invalid_state(selected_difficulty: str, reasons: list[str]) -> None:
    """
    Recover from invalid or corrupted game state.
    """
    old_score = st.session_state.get("score", DEFAULT_SCORE)

    reset_game(selected_difficulty, preserve_score=False)
    st.session_state.score = old_score if isinstance(old_score, int) else DEFAULT_SCORE

    log_game_event(
        logger,
        "state_recovered",
        difficulty=selected_difficulty,
        reasons=" | ".join(reasons),
        restored_score=st.session_state.score,
    )


initialize_game_state(difficulty)

# Handle difficulty change as a meaningful state transition.
if st.session_state.get("difficulty") != difficulty:
    log_game_event(
        logger,
        "difficulty_changed",
        old_difficulty=st.session_state.get("difficulty"),
        new_difficulty=difficulty,
    )
    reset_game(difficulty, preserve_score=False)
    st.success(f"Difficulty changed to {difficulty}. A new game has started.")
    st.rerun()

# Validate state before rendering major interactions.
is_valid, validation_errors = validate_game_state(
    secret=st.session_state.secret,
    attempts=st.session_state.attempts,
    attempt_limit=attempt_limit,
    score=st.session_state.score,
    status=st.session_state.status,
    low=low,
    high=high,
)

if not is_valid:
    recover_invalid_state(difficulty, validation_errors)
    st.warning(
        "A game-state issue was detected and automatically repaired. "
        "A fresh round has been started safely."
    )
    st.rerun()

st.subheader("Make a guess")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Status:", st.session_state.status)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(difficulty, preserve_score=False)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != GAME_STATUS_PLAYING:
    if st.session_state.status == GAME_STATUS_WON:
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    try:
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            log_game_event(
                logger,
                "invalid_guess",
                raw_guess=raw_guess,
                error=err,
                attempts=st.session_state.attempts,
                score=st.session_state.score,
            )
            st.error(err)
        else:
            next_attempt_number = st.session_state.attempts + 1

            # Pre-check before mutating critical state.
            if next_attempt_number > attempt_limit:
                log_game_event(
                    logger,
                    "submit_blocked",
                    reason="attempt_limit_would_be_exceeded",
                    attempts=st.session_state.attempts,
                    attempt_limit=attempt_limit,
                )
                st.session_state.status = GAME_STATUS_LOST
                st.error(
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                st.rerun()

            st.session_state.attempts = next_attempt_number
            st.session_state.history.append(guess_int)

            outcome, message = check_guess(guess_int, st.session_state.secret)

            if show_hint:
                st.warning(message)

            old_score = st.session_state.score
            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            log_game_event(
                logger,
                "guess_submitted",
                guess=guess_int,
                outcome=outcome,
                attempts=st.session_state.attempts,
                score_before=old_score,
                score_after=st.session_state.score,
                show_hint=show_hint,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = GAME_STATUS_WON
                log_game_event(
                    logger,
                    "game_won",
                    secret=st.session_state.secret,
                    attempts=st.session_state.attempts,
                    final_score=st.session_state.score,
                )
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = GAME_STATUS_LOST
                    log_game_event(
                        logger,
                        "game_lost",
                        secret=st.session_state.secret,
                        attempts=st.session_state.attempts,
                        final_score=st.session_state.score,
                    )
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )

            # Post-check after updates.
            is_valid_after, validation_errors_after = validate_game_state(
                secret=st.session_state.secret,
                attempts=st.session_state.attempts,
                attempt_limit=attempt_limit,
                score=st.session_state.score,
                status=st.session_state.status,
                low=low,
                high=high,
            )

            if not is_valid_after:
                log_game_event(
                    logger,
                    "post_submit_validation_failed",
                    reasons=" | ".join(validation_errors_after),
                )
                recover_invalid_state(difficulty, validation_errors_after)
                st.error(
                    "A consistency issue was detected after processing your guess. "
                    "The round was safely reset."
                )
                st.rerun()

    except Exception as exc:
        log_game_event(
            logger,
            "unexpected_error",
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        st.error(
            "An unexpected error occurred while processing your guess. "
            "The issue was logged safely."
        )

attempts_left = max(0, attempt_limit - st.session_state.attempts)

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

st.divider()
st.caption("Built by an AI that now logs its behavior and validates game state.")