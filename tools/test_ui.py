#!/usr/bin/env python3
"""Browser test of index.html: flow, both languages, copy, source mode, contrast, no outside requests.
Usage: python3 tools/test_ui.py [screenshot_dir]
"""
import os, re, sys, json
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_game

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "file://" + os.path.join(ROOT, "index.html")
shots = sys.argv[1] if len(sys.argv) > 1 else None
fails = []

def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" - " + str(detail)) if detail and not cond else ""))
    if not cond: fails.append(name)

def contrast(page, label):
    bad = [r for r in page.evaluate(check_game.CONTRAST_JS) if r["ratio"] < r["need"]]
    check("contrast " + label, not bad, bad[:3])

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=check_game.CHROME, args=["--no-sandbox"])
    for locale, width in (("en-US", 390), ("et-EE", 1100)):
        ctx = br.new_context(viewport={"width": width, "height": 900}, locale=locale, permissions=["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        reqs, errs = [], []
        page.on("request", lambda r: reqs.append(r.url) if not re.match(r"^(file|data|blob|about):", r.url) else None)
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.goto(URL)
        lang = "et" if locale.startswith("et") else "en"
        check("[%s] default language follows browser" % locale, page.evaluate("document.documentElement.lang") == lang)
        check("[%s] empty state shows no prompt" % locale, page.locator("#prompt-ready").is_hidden() and page.locator("#prompt-empty").is_visible())
        contrast(page, locale + " start")
        if shots: page.screenshot(path=os.path.join(shots, "%s-start.png" % lang), full_page=True)

        page.fill("#topic", "Fotosüntees" if lang == "et" else "Photosynthesis")
        check("[%s] still needs level and game" % locale, page.locator("#prompt-ready").is_hidden())
        page.select_option("#level", "inter")
        page.locator("label.game").nth(0).click()
        check("[%s] prompt appears" % locale, page.locator("#prompt-ready").is_visible())
        txt = page.evaluate("Array.from(document.querySelectorAll('#preview h4')).map(h=>h.textContent)")
        check("[%s] 10 sections without source" % locale, len(txt) == 10, txt)
        check("[%s] prompt language follows page" % locale, ("ÕPPEREEGLID" in txt) == (lang == "et"), txt)
        page.click("#copy")
        page.wait_for_timeout(200)
        clip = page.evaluate("navigator.clipboard.readText()")
        check("[%s] copy puts full prompt on clipboard" % locale, clip.startswith(("ROLL:", "ROLE:")) and "shuffle" in clip and "4.5:1" in clip or "4,5:1" in clip, clip[:60])
        check("[%s] copy confirmation shown" % locale, page.locator("#copy-status").inner_text().strip() != "")
        contrast(page, locale + " with prompt")

        # mixing game types
        check("[%s] mix box hidden with one game" % locale, page.locator("#mixbox").is_hidden())
        page.locator("label.game").nth(2).click()
        check("[%s] mix box shown with two games" % locale, page.locator("#mixbox").is_visible())
        heads = page.evaluate("Array.from(document.querySelectorAll('#preview h4')).map(h=>h.textContent)")
        check("[%s] mixed prompt has mix section and two game sections" % locale, len(heads) == 12 and heads[6] in ("MIXED GAME", "SEGAMÄNG"), heads)
        page.check("input[name=mixstyle][value=turns]")
        check("[%s] turns style changes prompt" % locale, "level 1 =" in page.locator("#preview").inner_text() or "tase 1 =" in page.locator("#preview").inner_text())
        page.locator("label.game").nth(4).click()
        check("[%s] fourth game blocked after three" % locale, page.locator("label.game input:disabled").count() == 3 and page.locator("#mix-max").inner_text().strip() != "")
        page.locator("label.game").nth(4).click()
        page.locator("label.game").nth(2).click()
        check("[%s] back to one game, nothing disabled" % locale, page.locator("label.game input:disabled").count() == 0 and page.locator("#mixbox").is_hidden())
        sbox = page.locator("details.more summary").bounding_box()
        check("[%s] More options toggle is large and shows description" % locale, sbox["height"] >= 56 and sbox["width"] > 300 and len(page.locator("details.more summary").inner_text()) > 40)

        # more options: source pasted
        page.click("details.more summary")
        page.check("input[name=source][value=pasted]")
        check("[%s] notice shown for pasted notes" % locale, page.locator("#notice").is_visible())
        check("[%s] needs notes" % locale, page.locator("#prompt-ready").is_hidden())
        page.fill("#notes", "Chlorophyll absorbs light.")
        check("[%s] SOURCE section appears" % locale, "Chlorophyll absorbs light." in page.locator("#preview").inner_text())
        page.check("input[name=source][value=file]")
        check("[%s] file steps shown" % locale, page.locator("#filesteps").is_visible() and page.locator("#notes-wrap").is_hidden())
        page.select_option("#gamelang", "other")
        check("[%s] other language needs a name" % locale, page.locator("#prompt-ready").is_hidden())
        page.fill("#gamelang-other", "Finnish")
        check("[%s] other language used" % locale, "Finnish" in page.locator("#preview").inner_text())
        contrast(page, locale + " more options open")
        if shots: page.screenshot(path=os.path.join(shots, "%s-filled.png" % lang), full_page=True)

        # switch language, game choice stays
        other = "en" if lang == "et" else "et"
        page.click(".langbtn[data-lang=%s]" % other)
        check("[%s] language switch works" % locale, page.evaluate("document.documentElement.lang") == other)
        check("[%s] game choice kept after switch" % locale, page.locator("label.game input:checked").count() == 1)
        check("[%s] topic kept after switch" % locale, page.input_value("#topic") != "")
        page.reload()
        check("[%s] language choice remembered" % locale, page.evaluate("document.documentElement.lang") == other)

        # keyboard: tab through to a game card and select with space
        page.fill("#topic", "x"); page.select_option("#level", "adv")
        page.focus("label.game input")
        page.keyboard.press("Space")
        check("[%s] game selectable by keyboard" % locale, page.locator("label.game input:checked").count() == 1)

        check("[%s] no requests to other sites" % locale, not reqs, reqs)
        check("[%s] no script errors" % locale, not errs, errs[:3])
        ctx.close()
    br.close()
print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
