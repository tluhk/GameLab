# Trial results

Games the AI chats produced are saved in `runs/`. "Automatic checks" means `tools/check_game.py` (outside links, runtime requests, script errors, contrast, shuffling).

| Game | Language | AI chat | Date | Opens | Plays without edits | Automatic checks | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sequence Builder, topic "JavaScript basics", 3 levels, 8 items | Estonian | not stated | 2026-11-17 | Yes | Yes (Claude solved three tasks in a headless browser; the owner reviewed it) | Pass | Works and is correct to look at, but the look is plain, like a first prototype (owner). The AI also left the file work to the student instead of creating the file (owner). Both led to prompt changes: see "Trial run 1" in `docs/decisions.md`. File: `runs/et-sequence-javascript-run1.html` |

| Sequence Builder, topic "JavaScript basics", 3 levels, 8 items | Estonian | not stated | 2026-11-17 | Yes | Yes (Claude solved four tasks and tried "give up" in a headless browser, desktop and phone width; no script errors) | Pass | Run 2, with the new wording (modern look, AI creates the file). Owner: "now it looks like this". Start screen, header band, centred card, progress bar, task chips, rounded buttons; readable on phone. File: `runs/et-sequence-javascript-run2.html` |

Run 1 does not count toward the pass mark for the new prompt text; it was made with the earlier wording. Run 2 is the first run with the new wording (1 of 1 passed so far, nowhere near the 9 of 10 needed).
