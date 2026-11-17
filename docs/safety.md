# Safety: running AI-generated games in the browser

Safety rests on three layers because no single one is reliable alone.

| Layer | What it does | Limit |
| --- | --- | --- |
| Prompt rules | Ask for one self-contained file with no outside links, no network calls, no pop-ups, no downloads, no requests for personal data | The AI can still ignore a rule |
| Safe Player | Runs the pasted game in a locked frame and warns about risky code first | Cannot stop an endless loop from freezing the tab; the warnings are a rough check, not proof |
| Student guidance | A short checklist before opening any game, and advice on what never to paste into a prompt | Relies on students reading it |

## How the Safe Player works

The student pastes the AI's reply. The player removes the markdown fences and scans for outside addresses and risky calls (network requests such as `fetch`, `XMLHttpRequest` and `WebSocket`, `eval`, cookies, `window.open`) and shows warnings. The game then runs inside an iframe, loaded through `srcdoc`, with these settings:

- **Sandbox with scripts only.** `allow-scripts` is the only permission: no forms, pop-ups, downloads or navigation of our page. `allow-same-origin` is never added, because together with scripts it lets the game remove its own sandbox (source: agentpatterns.ai, see [sources.md](sources.md)).
- **A content policy added to the game.** A meta tag allows inline scripts and styles and `data:` and `blob:` images only, for example `default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:`, which blocks network requests. The same source reports the frame cannot remove such a policy.
- **Side effect: storage is blocked inside the sandbox,** so a game would lose its progress and scores. To keep them, the player adds a small storage bridge (F23): the game asks the player page to save or load a small piece of data, and the player keeps it in this browser under a name tied to that game and refuses anything large or unexpected. The game still cannot reach the network or other storage.
- Games saved as `.html` files and opened directly can use browser storage themselves; every game therefore uses one small save/load helper with try/catch and a memory fallback.

## Scoreboard and privacy

- The scoreboard is device-only: a top-ten list in this browser with an optional nickname, never a real name. For sharing, the page offers a "copy my result" text.
- Mängulabor's own page sets no cookies, runs no analytics and loads nothing from other sites, so it sends no student data anywhere. What it keeps, such as the language choice and game progress, stays in the student's own browser. This also makes it simpler for a school to approve.

## Known limits

- The cited source does not cover endless loops or other heavy computing, so a faulty game can freeze its own tab; closing the tab fixes it.
- A policy set in a page tag cannot carry every protection a server header can. This is acceptable because the site holds no logins or secrets.
- The pre-run scan is heuristic.
- The Safe Player has not been tested across browsers yet; that happens in phase 4 (see [plan-and-requirements.md](plan-and-requirements.md)). Planned tests feed it deliberately bad pages (network request, pop-up, cookie access, redirect) to confirm each is blocked.

## Student guidance

- Run a game only after the checklist; open games from an AI chat in the Safe Player.
- Never put names, contacts or other personal data into the topic or notes, and use a nickname, not your real name, on a scoreboard.
- Paste only notes you may share, and follow your institution's AI rules.
- Check at least three answers against a textbook; AI-written questions can be wrong (see [learning-science.md](learning-science.md)).
