// Assembles a Mängulabor prompt from the prompt texts in data/prompts.js.
// Mirrors tools/build_prompt.py (the two must give the same text; tools/test_parity.py checks this).
(function () {
  "use strict";

  var NAMES = {
    en: { et: "Estonian", en: "English" },
    et: { et: "eesti keel", en: "inglise keel" }
  };

  function gameLanguageName(o) {
    var g = o.gameLanguage || o.lang;
    return g === "et" || g === "en" ? NAMES[o.lang][g] : g;
  }

  function isEstonian(o) {
    var g = o.gameLanguage || o.lang;
    return g === "et" || ["estonian", "eesti keel", "eesti"].indexOf(g.trim().toLowerCase()) >= 0;
  }

  var CATALOGUE = ["quiz", "flashcards", "memory", "typeanswer", "sort", "sequence"];

  // Accepts an array of ids (or one id); returns the ids in catalogue order, without duplicates.
  function gameList(v) {
    var ids = Array.isArray(v) ? v : [v];
    return CATALOGUE.filter(function (x) { return ids.indexOf(x) >= 0; });
  }

  function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

  // o: { lang, games (array, one to three ids), mixStyle ("all" or "turns"), topic, level, levels, items, difficulty, gameLanguage, mastery, replay,
  //      feedback, hints, time, lives, look, theme, summary, progress, scoreboard, source, notes }
  // Returns { blocks: [{ key, heading, lines: [] }], text }
  function build(o) {
    var t = window.MANGULABOR_PROMPTS[o.lang];
    var ids = gameList(o.games || o.game);
    if (ids.length < 1 || ids.length > 3) throw new Error("choose one to three game types");
    var mix = ids.length > 1;
    var games = ids.map(function (i) { return t.games[i]; });
    var g = games[0];
    var names = games.map(function (x) { return x.name; }).join(", ");
    var levels = clamp(parseInt(o.levels, 10) || 1, 1, 5);
    var steps = [];
    for (var i = 0; i < levels; i++) steps.push((i + 1) + " = " + t.ladder[i]);
    steps = steps.join("; ");
    var gl = gameLanguageName(o);
    var note = isEstonian(o) ? t.standard_lang_note.et : "";
    var blocks = [];

    function block(key, lines) {
      blocks.push({ key: key, heading: t.headings[key], lines: lines });
    }

    block("role", [t.role]);
    block("learner", [t.learner.split("{level_text}").join(t.levels_text[o.level])
      .split("{topic}").join(o.topic).split("{game_language}").join(gl)
      .split("{standard_lang_note}").join(note)]);
    var gameLine = mix ? t.game_line_mix : t.game_line;
    block("game", [gameLine.split("{game_name}").join(g.name).split("{n}").join(String(ids.length)).split("{game_names}").join(names)
      .split("{levels}").join(String(levels)).split("{items}").join(String(o.items))
      .split("{difficulty_text}").join(t.difficulty_text[o.difficulty])]);
    block("progress", [t[o.progress ? "progress_on" : "progress_off"], t[o.scoreboard ? "scoreboard_on" : "scoreboard_off"]]);

    var levelRule;
    if (!mix) {
      levelRule = g.level_rule ? g.level_rule.split("{items}").join(String(o.items))
        : t.level_rule_default.split("{ladder_steps}").join(steps);
    } else {
      var parts = [];
      if (games.some(function (x) { return !x.level_rule; })) parts.push(t.level_rule_default.split("{ladder_steps}").join(steps));
      var special = games.filter(function (x) { return x.level_rule; });
      if (special.length) {
        parts.push(t.level_rule_mix_suffix + " " + special.map(function (x) {
          return x.name + ": " + x.level_rule.split("{items}").join(String(o.items));
        }).join(" "));
      }
      levelRule = parts.join(" ");
    }
    var rules = t.learning.map(function (r) {
      return "- " + r.split("{replay_rule}").join(t[o.replay ? "replay_on" : "replay_off"])
        .split("{mastery_rule}").join(t[o.mastery ? "mastery_on" : "mastery_off"])
        .split("{level_rule}").join(levelRule)
        .split("{feedback_rule}").join(t[o.feedback === "explain" ? "feedback_explain" : "feedback_short"])
        .split("{hints_rule}").join(t[o.hints ? "hints_on" : "hints_off"])
        .split("{summary_rule}").join(t[o.summary ? "summary_on" : "summary_off"]);
    });
    rules.push("- " + t["time_" + o.time]);
    rules.push("- " + t[o.lives ? "lives_on" : "lives_off"]);
    block("learning", [t.learning_intro].concat(rules));

    var srcKey = { none: "content_source_none", pasted: "content_source_pasted", file: "content_source_file" }[o.source];
    block("content", [t.content_intro].concat(t.content.map(function (r) { return "- " + r; }), ["- " + t[srcKey]]));
    if (mix) {
      var style;
      if (o.mixStyle === "turns") {
        var turns = [];
        for (var k = 0; k < levels; k++) turns.push((o.lang === "en" ? "level" : "tase") + " " + (k + 1) + " = " + games[k % games.length].name);
        style = t.mix_style_turns.split("{turns}").join(turns.join(", ")).split("{items}").join(String(o.items));
      } else {
        style = t.mix_style_all.split("{game_names}").join(names).split("{items}").join(String(o.items));
      }
      block("mix", t.mix_common.map(function (r) { return "- " + r.split("{mix_style_rule}").join(style); }));
      games.forEach(function (x, n) {
        blocks.push({ key: "gamerules_" + (n + 1), heading: t.gamerules_n.split("{n}").join(String(n + 1)).split("{game_name}").join(x.name),
          lines: x.rules.map(function (r) { return "- " + r; }) });
      });
    } else {
      block("gamerules", g.rules.map(function (r) { return "- " + r; }));
    }

    var theme = o.theme ? t.theme_note.split("{theme}").join(o.theme) : "";
    block("look", t.look_rules.map(function (r) {
      return "- " + r.split("{palette}").join(t.palettes[o.look]).split("{theme_note}").join(theme);
    }));
    block("tech", [t.tech_intro].concat(t.tech.map(function (r) { return "- " + r.split("{game_id}").join(ids.join("-")); })));
    block("output", t.output.map(function (r) { return "- " + r; }));

    var tail = [];
    if (o.source === "pasted") {
      tail = [t.source_heading_pasted, o.notes || t.source_none];
      block("source", tail);
    } else if (o.source === "file") {
      block("source", [o.lang === "en" ? "(attached file)" : "(lisatud fail)"]);
    }

    var parts = [];
    blocks.forEach(function (b) { parts.push(b.heading + ":"); b.lines.forEach(function (l) { parts.push(l); }); parts.push(""); });
    var text = parts.join("\n").replace(/\s+$/, "") + "\n";
    return { blocks: blocks, text: text };
  }

  window.MangulaborPrompt = { build: build };
})();
