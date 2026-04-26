# Glitchy Guesser: Reliable AI Game System

## Original Project (Modules 1–3)
This project started as a simple Streamlit-based number guessing game built in earlier modules. The original goal was to allow a user to guess a randomly generated number with different difficulty levels, while tracking attempts and score. Core capabilities included input parsing, guess checking, and score updates using helper functions.

---

## Title & Summary
**Glitchy Guesser**  
A Reliable AI-Assisted Guessing Game

This project is an interactive number guessing game enhanced with an AI-style hint system and a built-in reliability/testing framework. Beyond basic gameplay, the system actively validates its own state, logs behavior, and evaluates whether its AI hints are consistent and safe. This matters because modern AI systems must not only work—but also be **trustworthy, testable, and reproducible**.

---

## Architecture Overview
The system is composed of four main components:

- **Streamlit App (`app.py`)**: Handles user interaction, UI, and game flow  
- **Core Logic (`logic_utils.py`)**: Implements game rules like parsing guesses, checking results, and updating score  
- **AI + Reliability Layer**: Generates hints, validates system state, enforces guardrails, and logs events  
- **Testing & Evaluation Layer**: Uses pytest and a custom consistency script to verify correctness and stability  

**Data Flow:**  
User Input → Streamlit App → Core Logic → AI Hint + Validation → Output to User  

Testing tools independently evaluate the AI by repeatedly running the same inputs and checking for consistent outputs.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd applied-ai-system-project
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate environment

**Mac/Linux:**
```bash
source .venv/bin/activate
```

**Windows (Git Bash / PowerShell):**
```bash
source .venv/Scripts/activate
```

### 4. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Run the app
```bash
python -m streamlit run app.py
```

### 6. Run tests
```bash
python -m pytest
```

### 7. Run AI consistency evaluation
```bash
python eval_ai_consistency.py
```

---

## Sample Interactions

### Example 1
**Input:** Guess = 30, Secret = 50  
**AI Output:**  
"You need a higher number. Stay inside the 1-100 range."

### Example 2
**Input:** Guess = 70, Secret = 50  
**AI Output:**  
"You need a lower number. Stay inside the 1-100 range."

### Example 3
**Input:** Guess = 50, Secret = 50  
**AI Output:**  
"You matched the target exactly. Lock in the win."

### Consistency Check Output
```text
Average consistency: 1.00
Total guardrail violations: 0
Overall status: PASS
```

---

## Design Decisions

- **Separation of concerns**: UI and logic are split (`app.py` vs `logic_utils.py`) for easier testing  
- **Deterministic AI hints**: Instead of a real LLM, a controlled hint generator ensures reproducibility and testability  
- **Guardrails**: Prevent revealing the secret or giving contradictory hints  
- **Logging system**: Tracks all events for debugging and transparency  

### Trade-offs
- Did not use a real LLM to keep behavior deterministic and testable  
- Simpler AI logic means less “creative” responses but higher reliability  

---

## Testing Summary

### What worked
- All core game logic passed pytest tests  
- AI hints were 100% consistent across repeated runs  
- Guardrails successfully prevented secret leakage  

### What didn’t
- Initial environment setup issues (missing dependencies)  
- Needed to use `python -m` commands for reliability on Windows  

### What I learned
Testing AI behavior requires more than unit tests—it requires **repeated evaluation and consistency measurement**.

---

## Reflection

This project taught me that building AI systems is not just about generating outputs—it’s about ensuring those outputs are reliable, safe, and consistent. I learned how to design systems that validate themselves, log behavior for debugging, and test AI-like components rigorously. The biggest takeaway is that **trust in AI comes from strong engineering practices, not just model capability**.

---

## Project Structure

```text
applied-ai-system-project/
├── app.py
├── logic_utils.py
├── eval_ai_consistency.py
├── requirements.txt
├── tests/
│   ├── test_game_logic.py
│   └── test_ai_consistency.py
└── logs/
```

---

## Why This Project Matters

This project demonstrates:
- End-to-end system design  
- Integration of AI-like components  
- Reliability and testing practices  
- Real-world software engineering discipline  

It shows not just that I can build an application—but that I can build one that is **robust, testable, and trustworthy**.


--- 

## Reliability and Evauluation

This project is designed to **prove that the AI works, not just appear to work**. Multiple reliability mechanisms are built into the system:

- **Automated tests**: Pytest is used to verify core game logic and AI hint behavior (`test_game_logic.py`, `test_ai_consistency.py`)
- **Consistency evaluation**: The AI hint system is tested by running the same input multiple times and measuring output stability
- **Logging and error handling**: The application logs all key events, errors, and state transitions to help diagnose issues
- **Guardrails**: The AI is prevented from revealing the secret number or producing contradictory hints
- **Human evaluation**: The developer can review logs, debug output, and consistency reports to verify correctness

### Testing Results

- All core game logic tests passed successfully  
- AI hint consistency achieved **100% stability across repeated runs**  
- **0 guardrail violations** detected (no secret leakage or contradictions)  
- System successfully recovered from invalid states during runtime validation  

### Summarize your testing in a few lines

> All tests passed; the AI maintained consistent outputs across repeated evaluations.  
> Guardrails prevented unsafe behavior, and reliability improved through validation and structured logging.


---

## Reflection & Ethics

AI isn't just about what works — it's about what is **responsible, reliable, and safe**.

### What are the limitations or biases in your system?

- The AI hint system is **rule-based and deterministic**, which means it lacks creativity and cannot adapt to complex player behavior.
- It assumes all users follow normal gameplay patterns and may not handle adversarial or unexpected inputs beyond defined guardrails.
- Because it is not trained on real-world data, it avoids bias from datasets—but is limited in flexibility and nuance.

### Could your AI be misused, and how would you prevent that?

- The system could be misused by attempting to reverse-engineer the secret number through repeated interactions.
- To prevent this:
  - Guardrails ensure the AI never reveals the secret directly
  - Consistency checks prevent contradictory hints
  - Logging allows developers to monitor suspicious patterns or abnormal usage

### What surprised you while testing your AI's reliability?

- One surprising result was how easy it is for an AI system to appear correct while still being unreliable.
- Repeated testing showed that **consistency and guardrails are just as important as correctness**.
- Building the consistency checker highlighted that even small logic changes can introduce subtle reliability issues.

### describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.

Throughout this project, AI was used as a development assistant to help design, debug, and improve the system.

- AI was helpful when it suggested separating the game logic into `logic_utils.py`, which made the code easier to test, maintain, and extend.

- One time the AI was flawed was when the AI-generated logic introduced inconsistent behavior by mixing string and integer comparisons. This caused incorrect results and required debugging and validation tests to fix.