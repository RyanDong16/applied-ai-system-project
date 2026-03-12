# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
+ Upon running the game for the first time on Normal difficulty, I see that on the main screen with the 'Attempts left' counter, it doesn't decrease by one after submitting a guess into the textbox, at least not for the first guess. After submitting a guess number, a hint textbox pops up saying to 'Go LOWER!'. There a dropdown menu called 'Developer Debug Info' that shows the 'secret' number, number of 'attempts', a 'score' counter, the 'difficulty' setting, and the 'history' of your guesses. There are three buttons: 'Submit Guess', 'New Game', and a checkoff option on whether you want to 'Show hint' after you submit a guess.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

+ 1. I guessed a random number (40) and the hint message says to 'Go LOWER!'. The second guess was (30), and the hint message says to 'Go LOWER!'. I guessed (20), (10), (1), and (0) and the hint message still says 'Go LOWER!'.  This is a bug because when guessing (0) and (1), the hint message falsely reports that the I need to guess a lower number. The correct result of guessing (0) is a hint message popping up and saying something like "out of range" NOT to guess a lower number. The bug is that the secret number is not in the proper range depending on the difficulty setting.
+ 2. When the setting difficulty is set to Normal, the highlighted message indictor on the game screen says 'Guess a number between 1 and 100. Attempts left: 7'. However, on the Settings sidebar, the normal difficulty says 'Range: 1 to 100' and says 'Attempts allowed: 8'. The bug is that there is a mismatch on the number of attempts allowed between the Settings sidebar and the game screen indictor. If setting sidebar level has 8 attempts allowed, the main screen attempts left should also have 8 attempts left. 
+ 3. After the game is over, whether win or lose on guessing the secret number, clicking on the 'New Game' button does not reset the game. The old guessed number should be clear out and the attempts left counter should be resetted to the full allowed amount depending on the difficulty level. 

 not cleared out to indict that a new game is ready to start.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
+ GitHub Copilot

- Give one example of the AI suggestion that was correct (including what the AI suggested and how you verified the result).
+ One example of an AI suggestion being correct was with the check_guess function. The AI suggested that when the guess is too high, the message should says "Go LOWER". When the guess is too low, the message should says "Go HIGHER". The AI Agent refactor my code to work correctly because through verification, whenever I guessed a high number to the secret number, the hint message returns to tell me to go lower with my guess. The same thing occurs when I guessed a low number to the secret number, the hint message returns to tell me to go higher with my guess.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
+ 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
+ I determined if it was an error by reviewing what the AI Agent said and testing the game to see if the error appeared. The AI Agent said that there is a mismatch on the attempts allowed between the sidebar setting display and the main screen banner display. The AI shows me that I needed to set the banner 'attempts' counter to 0, not the default, 1. After refactoring the code, the banner 'attempts' counted properly and the bug was fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
+

- Did AI help you design or understand any tests? How?
+ 


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
