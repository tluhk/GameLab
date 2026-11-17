#!/usr/bin/env python3
"""Assemble a Mängulabor prompt from prompts/<lang>.json.

Phase 1 prototype: the web page will later do the same in JavaScript.
Usage example:
  python3 tools/build_prompt.py --lang en --game quiz --topic "Photosynthesis" > prompt.txt
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GAMES = ["quiz", "flashcards", "memory", "typeanswer", "sort", "sequence"]


def load(lang):
    with open(os.path.join(ROOT, "prompts", lang + ".json"), encoding="utf-8") as f:
        return json.load(f)


NAMES = {"en": {"et": "Estonian", "en": "English"}, "et": {"et": "eesti keel", "en": "inglise keel"}}


def lang_name(a):
    g = a.game_language or a.lang
    return NAMES[a.lang][g] if g in ("et", "en") else g


def is_estonian(a):
    g = a.game_language or a.lang
    return g == "et" or g.strip().lower() in ("estonian", "eesti keel", "eesti")


def build(a):
    t = load(a.lang)
    g = t["games"][a.game]
    levels = max(1, min(5, a.levels))
    steps = "; ".join("%d = %s" % (i + 1, t["ladder"][i]) for i in range(levels))
    game_language = lang_name(a)
    note = t["standard_lang_note"].get("et", "") if is_estonian(a) else ""

    out = []

    def block(key, lines):
        out.append(t["headings"][key] + ":")
        out.extend(lines)
        out.append("")

    block("role", [t["role"]])
    block("learner", [t["learner"].replace("{level_text}", t["levels_text"][a.level])
                       .replace("{topic}", a.topic).replace("{game_language}", game_language)
                       .replace("{standard_lang_note}", note)])
    block("game", [t["game_line"].replace("{game_name}", g["name"]).replace("{levels}", str(levels))
                    .replace("{items}", str(a.items)).replace("{difficulty_text}", t["difficulty_text"][a.difficulty])])
    block("progress", [t["progress_on" if a.progress else "progress_off"],
                       t["scoreboard_on" if a.scoreboard else "scoreboard_off"]])

    if g.get("level_rule"):
        level_rule = g["level_rule"].replace("{items}", str(a.items))
    else:
        level_rule = t["level_rule_default"].replace("{ladder_steps}", steps)
    rules = []
    for r in t["learning"]:
        r = (r.replace("{replay_rule}", t["replay_on" if a.replay else "replay_off"])
              .replace("{mastery_rule}", t["mastery_on" if a.mastery else "mastery_off"])
              .replace("{level_rule}", level_rule)
              .replace("{feedback_rule}", t["feedback_explain" if a.feedback == "explain" else "feedback_short"])
              .replace("{hints_rule}", t["hints_on" if a.hints else "hints_off"])
              .replace("{summary_rule}", t["summary_on" if a.summary else "summary_off"]))
        rules.append("- " + r)
    rules.append("- " + t["time_" + a.time])
    rules.append("- " + t["lives_on" if a.lives else "lives_off"])
    block("learning", [t["learning_intro"]] + rules)

    src = {"none": "content_source_none", "pasted": "content_source_pasted", "file": "content_source_file"}[a.source]
    block("content", [t["content_intro"]] + ["- " + r for r in t["content"]] + ["- " + t[src]])
    block("gamerules", ["- " + r for r in g["rules"]])

    theme = t["theme_note"].replace("{theme}", a.theme) if a.theme else ""
    block("look", ["- " + r.replace("{palette}", t["palettes"][a.look]).replace("{theme_note}", theme)
                   for r in t["look_rules"]])
    block("tech", [t["tech_intro"]] + ["- " + r.replace("{game_id}", a.game) for r in t["tech"]])
    block("output", ["- " + r for r in t["output"]])
    if a.source == "pasted":
        out.append(t["headings"]["source"] + ":")
        out.append(t["source_heading_pasted"])
        out.append(a.notes or t["source_none"])
    elif a.source == "file":
        out.append(t["headings"]["source"] + ":")
        out.append("(attached file)" if a.lang == "en" else "(lisatud fail)")
    return "\n".join(out).rstrip() + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lang", choices=["en", "et"], default="en")
    p.add_argument("--game", choices=GAMES, required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--level", choices=["intro", "inter", "adv", "prof"], default="intro")
    p.add_argument("--levels", type=int, default=3)
    p.add_argument("--items", type=int, default=8)
    p.add_argument("--difficulty", choices=["easy", "medium", "hard", "adaptive"], default="medium")
    p.add_argument("--game-language", dest="game_language", default=None, help="et, en, or any language name (default: same as --lang)")
    p.add_argument("--no-mastery", dest="mastery", action="store_false")
    p.add_argument("--no-replay", dest="replay", action="store_false")
    p.add_argument("--feedback", choices=["short", "explain"], default="explain")
    p.add_argument("--hints", action="store_true")
    p.add_argument("--time", choices=["off", "relaxed", "tight"], default="off")
    p.add_argument("--lives", action="store_true")
    p.add_argument("--look", choices=["light", "dark", "contrast"], default="light")
    p.add_argument("--theme", default="")
    p.add_argument("--no-summary", dest="summary", action="store_false")
    p.add_argument("--no-progress", dest="progress", action="store_false")
    p.add_argument("--scoreboard", action="store_true")
    p.add_argument("--source", choices=["none", "pasted", "file"], default="none")
    p.add_argument("--notes", default="")
    sys.stdout.write(build(p.parse_args()))


if __name__ == "__main__":
    main()
