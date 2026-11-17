# Prompt design

The working prompt texts are in [`prompts/`](../prompts/README.md); the sketch here is a simplified view. Every prompt is assembled from the same blocks: the student's choices fill the blanks, and the learning, content and safety rules never change. The sketch below shows the shape; the final wording is written and tested in phase 1.

## Prompt skeleton

```text
ROLE: You are an expert educational game developer and teacher.
LEARNER: {study level}, studying "{topic}". Language of the game: {language}.
GAME: {game type}, {levels} levels, {items} items per level, difficulty {difficulty}.
PROGRESS: {save on this device: yes or no}. SCOREBOARD: {top ten on this device: yes or no}.
LEARNING RULES:
- The student answers before the answer is shown.
- Missed items come back later in the same game.
- Whenever answer options are shown, shuffle them in code every time the question appears, using a Fisher-Yates shuffle. The correct answer must not sit in a fixed position, and the data block must not rely on option order.
- An item is done only after {N} correct answers.
- Level 1 = remember, level 2 = understand, and so on (with a short example each).
- After every answer, show a one-line explanation.
CONTENT RULES:
- Use only the SOURCE below. If it does not cover something, leave it out.
- Put all questions in one labelled data block at the top of the file.
TECHNICAL AND SAFETY RULES:
- One self-contained HTML file: no links, libraries, fonts or images from outside.
- No network calls, no eval, no pop-ups, no downloads, no forms that submit.
- Never ask for a real name, email or password; an optional nickname for the scoreboard stays on this device.
- Save and load progress and scores only through one small helper that uses try/catch and falls back to memory if browser storage is blocked.
- Keyboard and touch play, no sound.
- Contrast: set text colour and background colour explicitly on every element. Normal text at least 4.5:1 against its background, buttons and borders at least 3:1, no light-grey text, and never show right or wrong by colour alone (add a symbol and a word).
OUTPUT: One code block with the whole file, then three short lines: how to open it
and which answers to double-check.
SOURCE: {student's pasted notes, optional}
```

## Design choices

- **Questions in a readable data block.** A student who does not program can still read and correct a wrong question without touching the game code.
- **Games compute, not guess.** In maths and similar games the prompt requires the code to calculate correct answers, so a typing slip in the data cannot create a wrong key.
- **A built-in second step.** After the game works, a "fact-check" prompt asks the AI to act as a sceptical teacher and list every item it is not sure about.
- **Prompt language follows the page language.** The Estonian page produces an Estonian prompt; the language of the game is chosen separately. Trials run in both languages, and if one performs clearly worse, the project owner is told before building further.

## Problems seen in students' earlier games

The project owner's students tried making games with AI before this project. Two problems came up most:

1. **Answer order not randomised.** When a game offered answers to choose from, the order was not shuffled, so for example the right answer was often the first one. Students could then win by pattern instead of knowing the material, which defeats retrieval practice (see [learning-science.md](learning-science.md)). A likely cause is that the AI lists the correct answer first in the question data and the game shows the list as it is.
2. **Bad contrast.** Some elements, sometimes, were hard to read.

How the project answers them:

- Both are written into every prompt as fixed rules (shown in the skeleton above), not as options. The prompt asks for a Fisher-Yates shuffle, because AI-written games often use a biased shortcut such as sorting with a random comparison.
- Order-based games (Sequence Builder) must shuffle the starting order and check that it differs from the correct order. Sort and Classify and Memory Match shuffle item and card positions.
- The quality gate below tests both automatically, so they do not depend on the AI obeying the prompt (see "Automatic checks").
- The student checklist in the Safe Player guidance includes "does the right answer stay in the same place?" and "can I read everything?".
- A follow-up prompt, "fix answer order and contrast", is added to the follow-up list.

## Follow-up prompts

Offered after the first result: repair ("it does not work", with a place to paste the error), make it harder or easier, add more items, fact-check, translate the game, explain my mistakes, and fix answer order and contrast (F9, F28, F29).

## "Why does the prompt say this?"

Each block has a short explanation in plain language (F11). This turns the tool into a lesson on writing prompts and on how to study, which fits the AI Leap aim of using AI to deepen learning, not bypass it.

## Estonian and English

- **Page language.** Default follows the browser (Estonian if the browser is set to Estonian, otherwise English). A switch is always visible, and the choice is remembered in the browser; only the language code is stored.
- **One text file per language.** Every sentence on the page lives in a language file (`i18n/et.js`, `i18n/en.js`) with one entry per text, so wording can be fixed without touching code, and a third language later means one new file.
- **Game language.** Estonian, English or "other", where the student types the language name. The prompt tells the AI to write all questions and feedback in it.
- **Estonian quality risk.** Estonian has about one million native speakers and is a low-resource language for AI models; research reports uneven performance for smaller languages. The prompt therefore asks for standard Estonian with correct case endings, the trials include Estonian output, and the page warns that AI-written Estonian can contain errors.
- **Review.** A native speaker must review every Estonian text on the page. The Estonian word for "prompt" and for the app itself still need to be agreed.

## Quality gate

No game module ships until it has run in a set of trial runs (each game, in both languages, in several chat AIs) and the result opened, played and contained no outside links. The proposed pass mark is at least 9 of 10 runs that open, play without edits and contain no outside links; the pass mark is agreed before phase 1 starts. Claude can run trials with Claude; trials in other chat AIs need a person with access to them (decision 8 in [decisions.md](decisions.md)).

### Automatic checks

For each trial result, a script opens the game in a headless browser and:

- **Answer order.** Starts the same question set many times and records where the correct answer appears. The gate fails if one position is clearly favoured. The exact count and threshold are set in phase 1.
- **Contrast.** Measures the contrast ratio of every visible text element against its background and fails the game below 4.5:1 for normal text, or 3:1 for large text and controls.
- **Outside links.** Looks for outside addresses and network calls.

These checks cannot judge whether a question is correct; that still needs a human (see [learning-science.md](learning-science.md)).
