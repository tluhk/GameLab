// Mängulabor page: reads the form, builds the prompt live, shows it, copies it.
(function () {
  "use strict";

  var I18N = window.MANGULABOR_I18N;
  var GAMES = window.MANGULABOR_GAMES;
  var lang = "en";

  function $(id) { return document.getElementById(id); }
  function t(key) { var d = I18N[lang]; return d && d[key] !== undefined ? d[key] : (I18N.en[key] || key); }

  function detectLang() {
    try { var s = localStorage.getItem("mangulabor:lang"); if (s === "et" || s === "en") return s; } catch (e) { /* storage blocked */ }
    var n = (navigator.language || "en").toLowerCase();
    return n.indexOf("et") === 0 ? "et" : "en";
  }

  function saveLang() {
    try { localStorage.setItem("mangulabor:lang", lang); } catch (e) { /* storage blocked: fine */ }
  }

  function applyText() {
    document.documentElement.lang = lang;
    document.title = t("app.name") + " – " + t("app.name.english");
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n]"), function (el) { el.textContent = t(el.getAttribute("data-i18n")); });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-placeholder]"), function (el) { el.setAttribute("placeholder", t(el.getAttribute("data-i18n-placeholder"))); });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-aria]"), function (el) { el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria"))); });
    Array.prototype.forEach.call(document.querySelectorAll(".langbtn"), function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang)); });
  }

  function renderGames() {
    var box = $("games");
    var selected = Array.prototype.map.call(box.querySelectorAll("input:checked"), function (i) { return i.value; });
    box.innerHTML = "";
    GAMES.forEach(function (g) {
      var label = document.createElement("label");
      label.className = "game";
      var input = document.createElement("input");
      input.type = "checkbox"; input.name = "game"; input.value = g.id;
      if (selected.indexOf(g.id) >= 0) input.checked = true;
      var body = document.createElement("span");
      body.className = "game-body";
      body.innerHTML = '<span class="game-name"></span><span class="game-desc"></span><span class="game-trains"></span>';
      body.querySelector(".game-name").textContent = t("game." + g.id + ".name");
      body.querySelector(".game-desc").textContent = t("game." + g.id + ".desc");
      body.querySelector(".game-trains").textContent = t("game.trains") + " " + t("game." + g.id + ".trains");
      label.appendChild(input); label.appendChild(body);
      box.appendChild(label);
    });
  }

  function readOptions() {
    var games = Array.prototype.map.call($("games").querySelectorAll("input:checked"), function (i) { return i.value; });
    var gl = $("gamelang").value;
    var gameLanguage = gl === "page" ? lang : (gl === "other" ? $("gamelang-other").value.trim() : gl);
    return {
      lang: lang, games: games, mixStyle: (document.querySelector("input[name=mixstyle]:checked") || {}).value || "all", topic: $("topic").value.trim(), level: $("level").value,
      levels: $("levels").value, items: $("items").value, difficulty: $("difficulty").value,
      gameLanguage: gameLanguage, mastery: $("mastery").value === "1", replay: $("replay").checked,
      feedback: $("feedback").value, hints: $("hints").checked, time: $("time").value, lives: $("lives").checked,
      look: $("look").value, theme: $("theme").value.trim(), summary: $("summary").checked,
      progress: $("progress").checked, scoreboard: $("scoreboard").checked,
      source: (document.querySelector("input[name=source]:checked") || {}).value || "none",
      notes: $("notes").value.trim()
    };
  }

  var currentText = "";

  function limitGames() {
    var boxes = $("games").querySelectorAll("input");
    var count = $("games").querySelectorAll("input:checked").length;
    Array.prototype.forEach.call(boxes, function (i) { i.disabled = count >= 3 && !i.checked; });
    $("mix-max").textContent = count >= 3 ? t("mix.max") : "";
    $("mixbox").hidden = count < 2;
  }

  function update() {
    limitGames();
    var o = readOptions();
    var gl = $("gamelang").value;
    $("gamelang-other-wrap").hidden = gl !== "other";
    $("notes-wrap").hidden = o.source !== "pasted";
    $("notice").hidden = o.source === "none";
    $("filesteps").hidden = o.source !== "file";

    var missing = [];
    if (!o.topic) missing.push(t("need.topic"));
    if (!o.level) missing.push(t("need.level"));
    if (!o.games.length) missing.push(t("need.game"));
    if (gl === "other" && !o.gameLanguage) missing.push(t("need.language"));
    if (o.source === "pasted" && !o.notes) missing.push(t("need.notes"));

    if (missing.length) {
      currentText = "";
      $("prompt-ready").hidden = true;
      $("prompt-empty").hidden = false;
      $("prompt-empty").textContent = (o.topic || o.level || o.games.length ? t("prompt.needed") + " " + missing.join(", ") : t("prompt.empty"));
      $("copy-status").textContent = "";
      return;
    }

    var res = window.MangulaborPrompt.build(o);
    currentText = res.text;
    $("prompt-empty").hidden = true;
    $("prompt-ready").hidden = false;
    var words = res.text.trim().split(/\s+/).length;
    $("stats").textContent = t("prompt.stats").replace("{words}", String(words)).replace("{chars}", String(res.text.length));
    var pv = $("preview");
    pv.innerHTML = "";
    res.blocks.forEach(function (b) {
      var sec = document.createElement("section");
      var h = document.createElement("h4"); h.textContent = b.heading;
      var pre = document.createElement("pre"); pre.textContent = b.lines.join("\n");
      sec.appendChild(h); sec.appendChild(pre); pv.appendChild(sec);
    });
    $("fallback").value = currentText;
  }

  function copy() {
    var status = $("copy-status");
    status.className = "status";
    function ok() { status.textContent = t("prompt.copied"); $("fallback-wrap").hidden = true; }
    function fail() { status.className = "status fail"; status.textContent = t("prompt.copyfail"); $("fallback-wrap").hidden = false; $("fallback").focus(); $("fallback").select(); }
    function legacy() {
      var ta = $("fallback"); $("fallback-wrap").hidden = false; ta.value = currentText; ta.focus(); ta.select();
      var done = false;
      try { done = document.execCommand("copy"); } catch (e) { done = false; }
      if (done) ok(); else fail();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(currentText).then(ok, legacy);
    } else { legacy(); }
  }

  function setLang(l) {
    lang = l; saveLang(); applyText(); renderGames(); bindGames(); update();
  }

  function bindGames() {
    Array.prototype.forEach.call($("games").querySelectorAll("input"), function (i) { i.addEventListener("change", update); });
  }

  function init() {
    lang = detectLang();
    applyText(); renderGames(); bindGames(); update();
    Array.prototype.forEach.call(document.querySelectorAll(".langbtn"), function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    ["topic", "level", "levels", "items", "difficulty", "gamelang", "gamelang-other", "mastery", "feedback", "time", "look", "theme", "notes",
      "replay", "hints", "lives", "summary", "progress", "scoreboard"].forEach(function (id) {
      $(id).addEventListener("input", update); $(id).addEventListener("change", update);
    });
    Array.prototype.forEach.call(document.querySelectorAll("input[name=source], input[name=mixstyle]"), function (r) { r.addEventListener("change", update); });
    $("copy").addEventListener("click", copy);
  }

  window.MangulaborApp = { readOptions: readOptions };
  init();
})();
