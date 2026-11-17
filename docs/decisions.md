# Decisions

All ten planning questions are settled for version 1.

| # | Topic | Decision | Effect on the plan |
| --- | --- | --- | --- |
| 1 | Audience | University students, mostly adults, no programming background | Study levels become course levels; plain adult wording; no school-stage choices |
| 2 | Who uses it | Students first; teacher links later | Teacher links stay in version 2 (F13) |
| 3 | Version 1 games | The six listed; more advanced types such as platformers later | Platformers and similar go to version 3 with their own tests |
| 4 | Prompt language | Follows the page language | The Estonian page produces an Estonian prompt; both languages are tested |
| 5 | Safe Player and storage | Safe Player in version 1 for first testing; progress and scores use local storage; the scoreboard is a builder option | Requirements F21 to F23; storage bridge in the player |
| 6 | Source mode | In version 1: notes pasted as plain text, steps for attaching files in the AI chat, and a copyright notice | Requirements F25 to F27 |
| 7 | Public code | Public code is fine; an open licence and a Haapsalu College credit are wanted but left out of the first version | Credit and licence file move to F24, added later. Until then normal copyright applies, so others may view the code but not reuse it. Proposal: MIT for code and CC BY 4.0 for texts |
| 8 | Reviewer | The project owner reviews the Estonian text and runs the trials in other AIs | Phases 1 and 4 depend on their time |
| 9 | Name | Mängulabor (English: Game Lab) | Used on the page and in the README |
| 10 | Other languages | Maybe later | Not in version 1 (F18) |

## Input from the owner's students

Before this project, the owner's students tried making study games with AI. They reported two main problems: poor contrast on some elements, and answer options not shuffled (for example, correct answers often first). These became fixed prompt rules and automatic quality-gate checks (requirements F28 and F29; see [prompt-design.md](prompt-design.md)). More feedback from the students should be gathered before and during the phase 4 pilot.

## Repository

The project lives in the `tluhk/GameLab` GitHub repository (created by the project owner). GitHub Pages is planned for hosting; free Pages normally needs a public repository, and GitHub's current rules are to be confirmed before publishing.

## Assumptions to check

- The copyright notice is general guidance and not legal advice; the owner or the college should check its wording.
- Nothing is assumed about which AI tools university students have; the tool works with any chat AI.
- The pass mark of 9 of 10 trial runs is a proposal, to be agreed before phase 1.
- The Estonian words for "prompt" and the app need agreeing, and all Estonian text needs native review.
- The search for existing tools was mainly in English; an Estonian tool may exist that was missed.

## Next step

Phase 1, the prompt lab (see [plan-and-requirements.md](plan-and-requirements.md)).
