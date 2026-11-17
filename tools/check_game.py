#!/usr/bin/env python3
"""Automatic checks for a generated Mängulabor game (phase 1 quality gate).

Checks: outside links and risky calls, contrast, shuffled order across reloads,
and (for quiz games) the position of the correct answer.
Usage: python3 tools/check_game.py game.html [--game quiz] [--runs 6] [--json]
Needs: pip install playwright, and Chrome (path in CHROME).
"""
import argparse, json, re, sys, os, collections
from playwright.sync_api import sync_playwright

CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
START_RE = re.compile(r"^(start|play|begin|alusta|mängi|hakka pihta|alusta mängu|let'?s go)\b", re.I)
NEXT_RE = re.compile(r"(next|continue|edasi|järgmine|jätka)", re.I)

RISKY = [
    (r"https?://", "outside address (http/https)"),
    (r"(?<![\w.])//[a-z0-9.-]+\.[a-z]{2,}/", "protocol-relative address"),
    (r"\bfetch\s*\(", "fetch call"), (r"XMLHttpRequest", "XMLHttpRequest"),
    (r"\bWebSocket\b", "WebSocket"), (r"sendBeacon", "sendBeacon"),
    (r"\beval\s*\(", "eval"), (r"new\s+Function\s*\(", "new Function"),
    (r"window\.open\s*\(", "window.open"), (r"document\.cookie", "cookies"),
    (r"<form[^>]*\baction=", "form with action"), (r"<iframe", "iframe"),
    (r"<script[^>]*\bsrc=", "external script"), (r"<link[^>]*\bhref=", "link tag"),
    (r"@import", "CSS @import"), (r"\bimport\s*\(", "dynamic import"),
]

CONTRAST_JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if(!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
  const lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
  const blend = (top, bot) => ({r: top.r*top.a+bot.r*(1-top.a), g: top.g*top.a+bot.g*(1-top.a), b: top.b*top.a+bot.b*(1-top.a), a:1});
  const bgOf = el => { const layers=[]; let n=el, unknown=false;
    while(n && n.nodeType===1){ const cs=getComputedStyle(n); if(cs.backgroundImage && cs.backgroundImage!=='none') unknown=true;
      const c=parse(cs.backgroundColor); if(c && c.a>0) { layers.push(c); if(c.a>=0.99) break; } n=n.parentElement; }
    let base={r:255,g:255,b:255,a:1}; for(let i=layers.length-1;i>=0;i--) base=blend(layers[i],base); return {c:base, unknown}; };
  const res=[]; const seen=new Set();
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(walker.nextNode()){ const t=walker.currentNode; const txt=t.textContent.trim(); if(!txt) continue;
    const el=t.parentElement; if(!el||seen.has(el)) continue; seen.add(el);
    if(['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)) continue;
    const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
    const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) continue;
    let fg=parse(cs.color); if(!fg) continue; const op=parseFloat(cs.opacity); const bg=bgOf(el);
    if(fg.a<1) fg=blend(fg,bg.c);
    const L1=lum(fg), L2=lum(bg.c); const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size=parseFloat(cs.fontSize); const bold=parseInt(cs.fontWeight)>=700; const large=size>=24||(bold&&size>=18.66);
    res.push({text:txt.slice(0,40), ratio:Math.round(ratio*100)/100, need:large?3:4.5, unknownBg:bg.unknown, size});
  }
  return res;
}
"""

SNAPSHOT_JS = """() => { const vis = e => { const cs=getComputedStyle(e); const r=e.getBoundingClientRect(); return cs.display!=='none'&&cs.visibility!=='hidden'&&r.width>0&&r.height>0; };
  return document.body.innerText.replace(/\\s+/g,' ').trim(); }"""

BUTTONS_JS = """() => { const vis = e => { const cs=getComputedStyle(e); const r=e.getBoundingClientRect(); return cs.display!=='none'&&cs.visibility!=='hidden'&&r.width>0&&r.height>0; };
  return Array.from(document.querySelectorAll('button,[role=button],[role=option],input[type=button],label')).filter(vis).map(e => (e.innerText||e.value||'').trim()); }"""

OPTIONS_JS = """() => { const vis = e => { const cs=getComputedStyle(e); const r=e.getBoundingClientRect(); return cs.display!=='none'&&cs.visibility!=='hidden'&&r.width>0&&r.height>0; };
  const groups = new Map();
  for (const b of document.querySelectorAll('button,[role=button],[role=option],[role=radio],label')) { if(!vis(b)) continue; const p=b.parentElement; if(!groups.has(p)) groups.set(p,[]); groups.get(p).push(b); }
  let best=null; for (const [p,l] of groups) { if(l.length>=3 && l.length<=6 && (!best || l.length>=best.length)) best=l; }
  if(!best) return null; best.forEach((b,i)=>b.setAttribute('data-ml-opt',i)); return best.map(b=>(b.innerText||'').trim()); }"""


def static_scan(src):
    found = []
    for rx, name in RISKY:
        for m in re.finditer(rx, src, re.I):
            ctx = src[max(0, m.start() - 20):m.end() + 30].replace("\n", " ")
            # allow the XML/SVG namespace string, which is not a network address
            if name.startswith("outside") and "w3.org" in ctx:
                continue
            found.append("%s: ...%s..." % (name, ctx))
            break
    return found


def extract_items(src):
    i = src.lower().find("questions")
    if i < 0:
        return []
    m = re.search(r"[\[{]", src[i:])
    if not m:
        return []
    start = i + m.start()
    depth, j, q = 0, start, None
    while j < len(src):
        ch = src[j]
        if q:
            if ch == "\\": j += 1
            elif ch == q: q = None
        elif ch in "\"'`": q = ch
        elif ch in "[{": depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0: break
        j += 1
    return src[start:j + 1]


def start_game(page):
    page.wait_for_timeout(150)
    for _ in range(3):
        btns = page.locator("button:visible")
        clicked = False
        for k in range(btns.count()):
            t = (btns.nth(k).inner_text() or "").strip()
            if START_RE.search(t):
                btns.nth(k).click(); page.wait_for_timeout(150); clicked = True; break
        if not clicked:
            break


def contrast_report(page, label, bad):
    for r in page.evaluate(CONTRAST_JS):
        if r["ratio"] < r["need"]:
            bad.append("[%s] %.2f:1 (needs %s) %r%s" % (label, r["ratio"], r["need"], r["text"], " (bg image, unsure)" if r["unknownBg"] else ""))


def run(path, game, runs):
    src = open(path, encoding="utf-8").read()
    res = collections.OrderedDict()
    scan = static_scan(src)
    res["outside_links_and_risky_calls"] = ("FAIL", scan) if scan else ("PASS", [])
    bad_requests, console_errors = [], []
    items_text = extract_items(src)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        ctx = br.new_context(viewport={"width": 390, "height": 800})
        page = ctx.new_page()
        page.on("request", lambda r: bad_requests.append(r.url) if not re.match(r"^(file|data|blob|about):", r.url) else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))
        url = "file://" + os.path.abspath(path)
        snaps, positions, contrast_bad = [], [], []
        items = []
        if items_text:
            try:
                page.goto(url); items = page.evaluate("(" + items_text + ")")
            except Exception:
                items = []
        flat = []
        def walk(o):
            if isinstance(o, dict):
                if "correct" in o and "question" in o: flat.append(o)
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(items)
        for run_i in range(runs):
            ctx.clear_cookies()
            page.goto(url); page.evaluate("() => { try { localStorage.clear() } catch(e) {} }"); page.goto(url)
            page.wait_for_timeout(200)
            if run_i == 0: contrast_report(page, "start screen", contrast_bad)
            start_game(page)
            snaps.append(page.evaluate(SNAPSHOT_JS))
            if run_i == 0: contrast_report(page, "game screen", contrast_bad)
            if game == "quiz" and flat:
                for qn in range(10):
                    opts = page.evaluate(OPTIONS_JS)
                    if not opts: break
                    body = page.evaluate(SNAPSHOT_JS)
                    item = next((it for it in flat if it["question"] in body), None)
                    if item:
                        norm = lambda s: re.sub(r"^[A-Da-d1-4][\).:]\s*", "", s).replace("✔", "").strip()
                        idx = next((i for i, o in enumerate(opts) if norm(o).lower() == item["correct"].strip().lower()), None)
                        if idx is not None: positions.append(idx)
                    page.locator("[data-ml-opt='0']").first.click(); page.wait_for_timeout(120)
                    if run_i == 0 and qn == 0: contrast_report(page, "after answering", contrast_bad)
                    nxt = page.locator("button:visible").filter(has_text=NEXT_RE)
                    if nxt.count() == 0: break
                    nxt.first.click(); page.wait_for_timeout(120)
        br.close()
    res["no_network_requests_at_runtime"] = ("FAIL", sorted(set(bad_requests))) if bad_requests else ("PASS", [])
    res["no_script_errors"] = ("FAIL", console_errors[:3]) if console_errors else ("PASS", [])
    res["contrast"] = ("FAIL", contrast_bad[:8]) if contrast_bad else ("PASS", [])
    distinct = len(set(snaps))
    if runs >= 3:
        res["order_varies_between_reloads"] = ("PASS", ["%d different first screens in %d loads" % (distinct, len(snaps))]) if distinct > 1 else ("FAIL", ["identical first screen in all %d loads (not shuffled, or inconclusive)" % len(snaps)])
    if game == "quiz":
        if len(positions) >= 12:
            c = collections.Counter(positions)
            n = len(positions); top = max(c.values()) / n
            detail = ["correct-answer positions over %d questions: %s" % (n, dict(sorted(c.items())))]
            ok = top <= 0.5 and len(c) >= 3
            res["correct_answer_position"] = ("PASS" if ok else "FAIL", detail)
        else:
            res["correct_answer_position"] = ("INCONCLUSIVE", ["only %d questions could be matched to the data block" % len(positions)])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--game", default="")
    ap.add_argument("--runs", type=int, default=6); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = run(a.file, a.game, a.runs)
    ok = all(v[0] == "PASS" for v in res.values())
    if a.json:
        print(json.dumps({"file": a.file, "pass": ok, "checks": {k: {"result": v[0], "details": v[1]} for k, v in res.items()}}, ensure_ascii=False))
    else:
        for k, (s, d) in res.items():
            print("%-34s %s" % (k, s))
            for line in d: print("    " + line)
        print("OVERALL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
