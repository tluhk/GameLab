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
| 7 | Public code and licence | First: public code with an open licence (MIT and CC BY 4.0 were proposed) and a Haapsalu College credit. **Changed on 17 November 2026:** the owner asked for a licence with a fee to use the application and its source code | A paid licence replaces the open-licence proposal (see "Paid licence" below). The code stays public, so others can view it. The Haapsalu College credit stays as F24 |
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

## Mixing game types and the "More options" button

On 17 November 2026 the owner asked for two changes: students should be able to mix game types (for example flashcards and memory match), and the "More options" control was hard to find.

- **Mixing (F31).** Up to three of the six version 1 games can be combined, in two ways (every level has all, or one game per level in turns). Action games cannot be mixed. See [game-catalogue-and-options.md](game-catalogue-and-options.md).
- **More options (F32).** The control is now a large labelled button that says what is inside. Moving the "source material" choice (own notes or file) out of "More options" onto the main screen is still possible if students miss that too.

## Paid licence

On 17 November 2026 the owner asked for a licence that requires a fee to use the application and its source code. A first draft is in the `LICENSE` file at the root of the repository.

What the draft says:
- Anyone may view the code and run the application for evaluation for a limited time, and may view and fork the repository within GitHub as GitHub's terms allow.
- Any other use, such as hosting it, offering it to students, copying, modifying or redistributing it, needs a written licence and payment. The fee and scope are not in the file; they are agreed in the written licence.
- Topics, notes and games that students create are theirs. Prompts the application generates, and games made from them, can be used and shared by a licensee without a further fee. This is an assumption by Claude and can be changed.
- Contributions sent to the licensor can be used and licensed by it, including under paid licences.

What it cannot do, and what needs a decision:
- **The licensor is not named.** The file has placeholders for the licensor's name, contact address, evaluation period, country and court. Whose copyright this is (the owner, the college or a university) is not known to Claude. If the work is done as part of a job, the employer may hold the rights.
- **A licence is a legal agreement, not a lock.** A public repository can be read and forked by anyone, and a public GitHub Pages site can be used by anyone who finds it. The fee can only be enforced through the agreement. If the fee must be enforced technically, the application would need to be private or behind sign-in, which needs a different setup: free GitHub Pages needs a public repository, and the plan has no accounts or server (Q1).
- **Free use by the college's own students.** The draft does not say who pays. If the college's students or teachers are to use it free of charge, or an institution pays on behalf of its students, this has to be written into the licence agreement.
- **Fee, term and legal review.** The fee level, billing, taxes, public-procurement and consumer rules, and the exact legal wording need a lawyer. The draft is not legal advice, and an Estonian version may be needed.
- **No third-party code.** The page uses no libraries or fonts from elsewhere, so no other licence conflicts with this one. Development tools (Playwright, Chrome) are used for testing only and are not part of the files.

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
