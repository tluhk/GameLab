# Prompt lab (phase 1)

The prompt texts of Mängulabor live here as data, one file per page language:

- `en.json`: English prompt text (shared rule blocks and the six game modules)
- `et.json`: Estonian prompt text (a draft written by Claude; needs review by a native speaker)
- `examples/`: ready-made prompts with default options, topic "Photosynthesis" / "Fotosüntees", 3 levels, 8 items per level. Paste one into an AI chat to try it.

`tools/build_prompt.py` assembles a prompt from these files. The web page will do the same in JavaScript in phase 2. Example:

```text
python3 tools/build_prompt.py --lang en --game quiz --topic "Photosynthesis" --levels 3 --items 8 > prompt.txt
python3 tools/build_prompt.py --lang et --game sort --topic "Fotosüntees" --scoreboard --look dark
python3 tools/build_prompt.py --lang en --game quiz,memory --topic "Photosynthesis" --mix-style turns   # a mix of up to three games
```

Run `python3 tools/build_prompt.py --help` for all options (they match the options in `docs/game-catalogue-and-options.md`).

## Shared rules that never change

Learning rules (answer before it is shown, missed items return, mastery rule, levels up a ladder of thinking skills, explanation after each answer), content rules (one readable data block, unique ids, no invented facts, source restriction), look rules (fixed colour palettes with checked contrast, symbol plus word for right and wrong), and technical and safety rules (one file, no outside resources, no network, one save/load helper, exact shuffle function, keyboard and touch, no sound).

## Checking a generated game

`tools/check_game.py` opens a generated `.html` file in a headless Chrome and checks: outside links and risky calls (static and at runtime), script errors, text contrast against 4.5:1 (3:1 for large text), whether the first screen varies between reloads (shuffling), and for quiz games the position of the correct answer.

```text
pip install playwright
python3 tools/check_game.py game.html --game quiz
```

Needs Chrome (set the `CHROME` environment variable if it is not at `/usr/bin/google-chrome`). The files in `tools/testdata/` are a known-good quiz and three known-bad ones (not shuffled, low contrast, network call) used to confirm the checker catches what it should.

What the checker cannot do: judge whether questions are factually right, whether a game is pleasant, or detect every risky pattern. Those need a person.

## Status

The prompts and the checker are written and the checker is tested on known-good and known-bad games. Trial runs with real AI chats, which decide the quality gate, are still to do; results go in `trials/`.

## Mixed games

`--game` accepts up to three games separated by commas. The prompt gets a MIXED GAME section and one RULES FOR GAME TYPE section per game; `--mix-style all` (default) puts a round of every game in each level, `--mix-style turns` gives each level one game in turn. `examples/` has two mixes per language.

## The web page (test version)

`index.html` is a test version of the prompt builder. Open it in a browser (double-click the file, or use GitHub Pages) and choose a topic, level, game and options; the prompt appears below and can be copied. It uses `js/prompt.js` (the same assembly as `tools/build_prompt.py`), `data/prompts.js` (generated from the JSON files; run `python3 tools/build_data.py` after editing them), and the texts in `i18n/`.

Tests (need Python with Playwright and Chrome):

```text
python3 tools/test_parity.py     # the page and the Python script give identical prompts
python3 tools/test_ui.py         # flow, both languages, copy, source mode, contrast, no outside requests
```
