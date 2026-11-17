# Prompt design

Every prompt is assembled from the same blocks: the student's choices fill the blanks, and the learning, content and safety rules never change. The sketch below shows the shape; the final wording is written and tested in phase 1.

## Prompt skeleton

```text
ROLE: You are an expert educational game developer and teacher.
LEARNER: {study level}, studying "{topic}". Language of the game: {language}.
GAME: {game type}, {levels} levels, {items} items per level, difficulty {difficulty}.
PROGRESS: {save on this device: yes or no}. SCOREBOARD: {top ten on this device: yes or no}.
LEARNING RULES:
- The student answers before the answer is shown.
- Missed items come back later in the same game.
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
- Keyboard and touch play, readable contrast, no sound.
OUTPUT: One code block with the whole file, then three short lines: how to open it
and which answers to double-check.
SOURCE: {student's pasted notes, optional}
```

## Design choices

- **Questions in a readable data block.** A student who does not program can still read and correct a wrong question without touching the game code.
- **Games compute, not guess.** In maths and similar games the prompt requires the code to calculate correct answers, so a typing slip in the data cannot create a wrong key.
- **A built-in second step.** After the game works, a "fact-check" prompt asks the AI to act as a sceptical teacher and list every item it is not sure about.
- **Prompt language follows the page language.** The Estonian page produces an Estonian prompt; the language of the game is chosen separately. Trials run in both languages, and if one performs clearly worse, the project owner is told before building further.

## Follow-up prompts

Offered after the first result: repair ("it does not work", with a place to paste the error), make it harder or easier, add more items, fact-check, translate the game, and explain my mistakes (F9).

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
