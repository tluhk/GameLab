# Learning science: theories and design rules

The central finding behind the design is that spreading out practice and recalling answers beat re-reading. Every game must therefore make the student retrieve an answer before it is shown.

This page lists six findings, what the research says, and the rule each one gives the app. These are general findings. No study tests Mängulabor's specific games, so the pilot in phase 4 (see [plan-and-requirements.md](plan-and-requirements.md)) is the real test. Sources are marked in [sources.md](sources.md) by whether the full page was read.

## Summary table

| Finding | What the research says | Design rule in the app |
| --- | --- | --- |
| Retrieval practice and spacing | A 2021 meta-analysis of ten learning techniques found distributed practice and practice testing the most effective; re-reading and highlighting did worse long-term | The student answers before seeing the answer. Missed items return later in the same game. The app suggests replaying over several days. |
| Successive relearning | Practising an item until it is correct, then again in later sessions, is reported to be potent | A "mastery rule" option: an item counts as learned only after it is answered correctly more than once (default on). |
| Cognitive load | In one serious-game study the game gave less short-term learning than a slideshow with the same content, and higher load went with lower gains | A plain screen during questions: no decorative animation, no sound, no timer by default. Feedback appears next to the question. Themes are cosmetic only. |
| Gamification | Meta-analyses report positive effects (g = 0.46 and g = 0.82 in two of them), with very high variation between studies and earlier mixed results | Use game elements that serve learning: levels, progress, instant feedback. Lives, timers and competition are optional and off by default. No effect size is promised. |
| Bloom's levels | The revised taxonomy runs from remembering to creating. AI questions matched lower-order levels well, while raters spotted human-written questions more easily at higher levels | The "levels" option follows the ladder remember, understand, apply, analyse. The prompt defines each level with an example. Higher-level items are marked for a human check. |
| Accuracy of AI questions | LLM-written answer keys had fewer hallucinations than human-written ones, but their wrong options had more | Use only supplied source text when given. Every item gets a one-line explanation. All questions sit in one readable block at the top of the file. A "fact-check" follow-up prompt and a student checklist are included. |

## Retrieval practice and spacing

Hattie and Donoghue (2021) meta-analysed ten learning techniques across 242 studies. They report that distributed practice and practice testing are the most effective techniques; re-reading and highlighting did worse long-term. The figures here come from a secondary summary page (evidencebased.education), not from the original paper.

**Rules for the app:** every game asks before it tells; a missed item comes back later in the same game; the post-game screen suggests replaying over several days (requirement F14); progress saving (F21) lets practice span days.

## Successive relearning

A 2022 review reports that successive relearning, practising an item until it is correct and then again in later sessions, is potent. Only the abstract was seen in search results.

**Rule for the app:** the mastery option (default on) requires more than one correct answer before an item is done, and saved progress carries mastery between sessions.

## Cognitive load and game-based learning

A Utrecht University study of a serious game found that the game gave less short-term learning than a slideshow with the same content, and that higher cognitive load went with lower learning gains. The full page was read.

This is one study of one game, so it is a caution, not a law. It still shapes the defaults: a plain screen during questions, feedback beside the question, no sound, no timer unless chosen, and cosmetic-only themes. Action-heavy games such as platformers (F17) must be tested against this rule before release.

## Gamification

Gamification meta-analyses report positive effects with wide variation:

- Li, Ma and Shi (2023): Hedges' g = 0.82. Heterogeneity between studies is very high (I² about 94%), and the overall effect is larger than the 0.40 to 0.60 range reported in earlier reviews, so it should be read with caution. The full page was read.
- Huang and colleagues (2020): g = 0.46. Seen only as an abstract in search results.

**Rules for the app:** game elements must serve learning (levels, progress, instant feedback). Lives, timers and competition are off by default and optional. Because effects vary so widely, the project makes no claim about effect size.

## Bloom's revised taxonomy

The revised taxonomy has six levels, from remembering to creating. The app maps its "number of levels" option onto the lower four: remember, understand, apply, analyse. A 2025 study found that AI-written questions matched lower-order levels well, while raters spotted human-written questions more easily at higher-order levels. Only the abstract was seen; the full page would not open.

**Rules for the app:** the prompt defines each level with a short example, and items at higher levels are marked for a human check. The game catalogue records the Bloom range of each game ([game-catalogue-and-options.md](game-catalogue-and-options.md)).

## Accuracy of AI-written questions

A 2026 conference paper found that LLM-written answer keys had fewer hallucinations than human-written ones, while the wrong options (distractors) had more. A separate paper names four error types in multiple-choice generation: reasoning, unsolvable questions, facts and maths. Both were seen only as search summaries.

**Rules for the app:**

- With source mode, the prompt restricts questions to the supplied text (requirement F25).
- Every item carries a one-line explanation, which makes errors easier to spot.
- All questions sit in one readable block at the top of the file, so a student who does not program can correct a wrong item.
- In maths-like games the code computes correct answers instead of storing them.
- A "fact-check" follow-up prompt asks the AI to act as a sceptical teacher and list every item it is unsure about.
- The student checklist asks the student to verify three answers against a textbook.

## Answer order and retrieval

Students' earlier AI-made games often left the answer options in a fixed order, with the right answer frequently first (reported by the project owner; not a published study). This works against retrieval practice: if the position gives the answer away, the student recognises a pattern instead of recalling the content. The rule is that options are shuffled in code every time (requirement F28, see [prompt-design.md](prompt-design.md)). Shuffling, together with readable contrast (F29), is also a basic requirement of low cognitive load: nothing on screen should make the task harder or easier than the content does.

## What this page does not claim

- No study here tests Mängulabor itself.
- Effect sizes are quoted to show direction and uncertainty, not to promise results.
- Findings from school-age and clinical samples may not transfer fully to adult university students; the pilot should include the real target group.
