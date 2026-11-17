#!/usr/bin/env python3
"""Check that js/prompt.js (the web page) gives exactly the same prompt text as tools/build_prompt.py.

Runs many random option sets in headless Chrome. Usage: python3 tools/test_parity.py [count]
"""
import os, random, sys, types
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_prompt as bp

CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
TOPICS = ["Photosynthesis", "Fotosüntees", 'He said "stop" & <left>', "SQL {joins} {topic}", "Õun, ööbik; ž š"]
NOTES = ["", "Short notes.", "Line one\nLine two with {game_name} and {topic} inside.\n\n  indented"]


def rand_opts(r):
    lang = r.choice(["en", "et"])
    gl = r.choice([None, "et", "en", "Spanish", "Estonian", "eesti keel"])
    source = r.choice(["none", "pasted", "file"])
    return dict(lang=lang, game=r.choice(bp.GAMES), topic=r.choice(TOPICS), level=r.choice(["intro", "inter", "adv", "prof"]),
                levels=r.randint(1, 5), items=r.choice([5, 8, 10, 15]), difficulty=r.choice(["easy", "medium", "hard", "adaptive"]),
                game_language=gl, mastery=r.random() < .5, replay=r.random() < .5, feedback=r.choice(["short", "explain"]),
                hints=r.random() < .5, time=r.choice(["off", "relaxed", "tight"]), lives=r.random() < .5,
                look=r.choice(["light", "dark", "contrast"]), theme=r.choice(["", "space", "mets"]),
                summary=r.random() < .5, progress=r.random() < .5, scoreboard=r.random() < .5,
                source=source, notes=r.choice(NOTES) if source == "pasted" else "")


def to_js(o):
    d = dict(o); d["gameLanguage"] = d.pop("game_language") or o["lang"]
    return d


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    r = random.Random(7)
    cases = [rand_opts(r) for _ in range(n)]
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = br.new_page()
        page.goto("file://" + os.path.join(ROOT, "index.html"))
        for i, o in enumerate(cases):
            py = bp.build(types.SimpleNamespace(**o))
            js = page.evaluate("o => window.MangulaborPrompt.build(o).text", to_js(o))
            if py != js:
                bad += 1
                if bad <= 3:
                    a, b = py.splitlines(), js.splitlines()
                    k = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
                    print("MISMATCH case %d %s\n  py: %r\n  js: %r" % (i, o, a[k:k + 1], b[k:k + 1]))
        br.close()
    print("%d of %d option sets identical" % (n - bad, n))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
