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

## Feedback through GitHub issues (F30)

Question from the owner: can users submit feature requests or feedback as GitHub issues? Yes, in one way that fits the plan, with a limit.

- **Chosen approach.** A link on the page opens GitHub's "new issue" form in the repository, with the title, label and a few fields prefilled. The student reviews and submits on GitHub. The page itself makes no request and holds no token, so Q1 still holds. The repository carries three bilingual issue forms (feedback, feature request, something is wrong) in `.github/ISSUE_TEMPLATE/`.
- **Limit: a GitHub account is needed.** Students without one cannot submit this way. Public issues also show the writer's GitHub name.
- **Public by default.** Every issue is visible to everyone, so the forms and the page warn against real names, contact details and confidential material.
- **Not chosen: submitting from the page without an account.** This would need a server or serverless function holding a GitHub token, which breaks the no-backend rule (Q1), adds running costs and moderation work, and invites spam. It can be revisited later.
- **Decided: GitHub issues only for now.** Other routes can be added later if needed, for example GitHub Discussions (still needs an account) or an external form such as a Google or Microsoft form, which would mean linking to another site.
- **Prefilled link detail.** The prefilled text must never include what the student typed in the builder (topic or pasted notes), because it would become public.

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
