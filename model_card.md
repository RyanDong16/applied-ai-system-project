# Model Card: Glitchy Guesser AI Hint System

## Model Overview

**Model Name:** Glitchy Guesser AI Hint System  
**Type:** Rule-based / deterministic AI (non-ML)  
**Version:** 1.0  
**Developed By:** [Your Name]  
**Date:** 2026  

This model generates hints for a number guessing game. It analyzes the user's guess relative to a hidden number and provides directional feedback (higher, lower, or correct) while enforcing safety constraints.

---

## Intended Use

### Primary Use
- Provide safe and consistent hints in a number guessing game
- Demonstrate reliability and testing practices in AI systems
- Serve as a teaching example for AI system design and evaluation

### Users
- Students learning AI system design
- Developers interested in reliability-focused AI applications
- Instructors evaluating applied AI projects

### Out of Scope
- General-purpose natural language generation
- Real-world decision-making systems
- High-stakes applications (medical, legal, financial)

---

## Model Details

### Input
- `secret` (int): The hidden target number
- `guess` (int): User’s current guess
- `history` (list[int]): Previous guesses
- `low`, `high` (int): Valid range
- `attempts`, `attempt_limit` (int): Game state

### Output
- A text hint indicating:
  - "higher"
  - "lower"
  - "correct"

### Behavior
- Deterministic: same input → same output
- Guardrailed: never reveals the secret number
- Consistent: produces stable outputs across repeated runs

---

## How It Works

The system:
1. Compares the guess to the secret number
2. Determines direction (higher, lower, correct)
3. Generates a structured hint message
4. Applies guardrails to prevent unsafe output
5. Returns a consistent, validated response

---

## Evaluation & Reliability

### Testing Methods
- **Unit Tests (pytest)**:
  - Validate guess logic
  - Validate score updates
  - Validate input parsing
- **AI Consistency Evaluation**:
  - Repeats identical inputs multiple times
  - Measures output stability
- **Guardrail Checks**:
  - Ensures secret number is never exposed
  - Prevents contradictory hints

### Metrics
- Consistency Rate: **1.00 (100%)**
- Guardrail Violations: **0**
- Test Pass Rate: **100%**

### Example Result
```
Average consistency: 1.00
Total guardrail violations: 0
Overall status: PASS
```

---

## Limitations

- Not a true machine learning model
- Cannot adapt or learn from new data
- Limited to simple numerical reasoning
- Produces predictable (non-creative) outputs
- Not suitable for complex or real-world AI tasks

---

## Ethical Considerations

### Risks
- Overestimating AI capability due to consistent behavior
- Misinterpreting deterministic logic as “intelligence”

### Mitigations
- Transparent design (rule-based, not black-box)
- Logging and validation for traceability
- Guardrails to prevent unsafe outputs

---

## Safety Features

- Secret number is never revealed
- Contradictory hints are blocked
- Invalid inputs are handled safely
- Game state is validated before and after each action
- All major actions are logged

---

## Human-AI Interaction

- Humans interact through the Streamlit UI
- Developers review logs and test outputs
- Reliability is verified through automated testing and manual inspection

---

## Future Improvements

- Integrate a real LLM for more dynamic hints
- Add confidence scoring to outputs
- Track user behavior for adaptive difficulty
- Expand evaluation metrics beyond consistency

---

## Dependencies

- Python 3.x
- Streamlit
- Pytest

---

## Summary

This model demonstrates that **reliability, consistency, and safety are core components of AI systems**. While simple, it highlights best practices in validation, testing, and responsible AI design.