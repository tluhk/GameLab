# Game catalogue and options

Each game has its own prompt module that is written and tested in advance, so students cannot pick an untested combination. The catalogue is a proposal; version 1 is the six games marked 1.

## Game catalogue

| Game | What the student does | Learning purpose | Bloom level | Version |
| --- | --- | --- | --- | --- |
| Quiz Quest | Picks the right answer; each level is harder | Recognising facts and concepts | Remember, understand | 1 |
| Flashcards | Flips a card, then rates how well they knew it; weak cards return sooner | Spaced recall of terms and definitions | Remember | 1 |
| Memory Match | Flips cards to find pairs, such as a term and its meaning | Linking terms to meanings | Remember | 1 |
| Type the Answer | Types the answer instead of choosing it | Producing the answer from memory | Remember, apply | 1 |
| Sort and Classify | Drags or taps items into categories | Telling categories apart | Understand, analyse | 1 |
| Sequence Builder | Puts steps or events in the right order | Processes and chronology | Understand | 1 |
| Scenario Adventure | Makes choices in a short story that need the topic knowledge | Applying knowledge in a situation | Apply, analyse | 2 |
| Boss Review | Answers mixed questions from all earlier levels with few mistakes allowed | Mixed review | Remember to analyse | 2 |
| Math Practice | Solves generated problems with step hints; the game's code computes the correct answers | Procedural skill | Apply | 2 |
| Word Guess | Guesses a hidden term from clues | Vocabulary and spelling | Remember | 2 |
| Escape Puzzle | Solves a chain of questions to unlock the next room | Applying across topics | Apply, analyse | 3 |
| Concept Map | Connects concept cards with labelled links | Seeing relations between ideas | Analyse | 3 |
| Platformer Quiz | Runs and jumps through a level; correct answers open the gates | Recall under light action; must be tested against the cognitive-load rule | Remember, apply | 3 |

More advanced types such as platformers are wanted later (decision 3 in [decisions.md](decisions.md)).

## Options the student can choose

The main screen asks for five things; everything else sits under "More options" with defaults, so a first-time user never faces a long form.

| Option | Choices | Default | Screen |
| --- | --- | --- | --- |
| Topic | Free text, for example "photosynthesis" | Required | Main |
| Study level | Introductory, intermediate or advanced course; professional or continuing training | Must choose | Main |
| Game type | One of the catalogue | Must choose | Main |
| Difficulty | Easy, medium, hard, adaptive (the game adjusts to the player) | Medium | Main |
| Number of levels | 1 to 5; each level moves up the Bloom ladder | 3 | Main |
| Subject area | Languages, maths, natural sciences, humanities, other; used to suggest fitting games | Suggests only | More |
| Items per level | 5, 8, 10, 15 | 8 | More |
| Source material | The AI's own knowledge, or the student's notes pasted as plain text, or a file attached in the AI chat, with a copyright notice and steps for attaching | AI's own knowledge, with a hint that notes give more accurate questions | More |
| Language of the game | Estonian, English, other | Same as the page language | More |
| Mastery rule | Off, or answer correctly twice before an item is done | On | More |
| Replay missed items | On, off | On | More |
| Feedback | Right or wrong only; short explanation | Short explanation | More |
| Hints | None; one hint per question | None | More |
| Time pressure | Off, relaxed, tight | Off | More |
| Lives | Off, three lives | Off | More |
| Look | Calm light, dark, high contrast, plus a cosmetic theme in a few words | Calm light | More |
| Result summary | A short text the student can copy at the end | On | More |
| Save progress | Off, or on this device: the game remembers which items are mastered, with a reset button | On | More |
| Scoreboard | Off, or a top-ten list kept on this device, with an optional nickname | Off | More |

Some rules are never options and are written into every prompt: play by keyboard and touch, readable contrast, no sound, no outside resources, and no requests for real names, contact details or passwords.

## Source mode

- The student can paste notes as plain text; the prompt then restricts questions to that text (F25).
- For longer material, the page shows steps for attaching a file in the AI chat, and the prompt refers to the attached file (F26).
- Whenever source mode is used, a copyright and privacy notice appears (F27): use only material you own, may share with AI tools, or that is openly licensed; no confidential material or personal data; follow your institution's rules. This is general guidance, not legal advice; the college or the project owner should check its wording.

## Study levels

Study levels are course levels for university students (introductory, intermediate, advanced; professional or continuing training), worded in plain language in both languages. The student's age or school stage is not asked.
