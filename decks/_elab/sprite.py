# -*- coding: utf-8 -*-
"""Иконки устройств эмулятора: объёмные коммутатор, маршрутизатор, ПК, сервер из деки главы 7 (они же в svg-atlas),
перекрашенные из бирюзы атласа в палитру HUD эмулятора. Маршрутизатор — коралловый, остальное — циан."""
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "..", "glava7-application.html")

CYAN = {"#2b9f8f": "#3fb7c0", "#247b70": "#1b5f67", "#267c71": "#1d656d", "#26867a": "#227079", "#27877a": "#237480",
        "#2a9183": "#2a8790", "#28c7b2": "#6fe3ea", "#00d2b6": "#6fe3ea", "#5dd1c2": "#9af0f4", "#d3dedc": "#e6fbfc", "#cfe1df": "#d9f7f9"}
CORAL = {"#2b9f8f": "#d4574f", "#247b70": "#7e2a27", "#267c71": "#8a2e2a", "#26867a": "#9b3833", "#2a9183": "#b4443e",
         "#28c7b2": "#ff8a80", "#5dd1c2": "#ffb4ad", "#d3dedc": "#ffe6e2", "#cfe1df": "#ffe6e2"}
VIOLET = dict((k, v) for k, v in CYAN.items())
VIOLET.update({"#2b9f8f": "#9b7de0", "#247b70": "#4b3486", "#267c71": "#523a8f", "#26867a": "#5c4299", "#28c7b2": "#c79bff",
               "#2a9183": "#7a5cc4", "#5dd1c2": "#dcc6ff"})
# id в эмуляторе ← (символ главы 7, палитра)
ICONS = {"ic-switch": ("rp-switch", CYAN), "ic-stack": ("rp-s2u", CYAN), "ic-router": ("rp-router", CORAL),
         "ic-pc": ("rp-pc", CYAN), "ic-server": ("rp-server", CYAN), "ic-docker": ("rp-pc", VIOLET)}


def recolor(t, pal):
    return re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: pal.get(m.group(0).lower(), m.group(0)), t)


def sprite():
    s = open(SRC, encoding="utf-8").read()
    out = []
    for new, (old, pal) in ICONS.items():
        m = re.search(r'<symbol id="' + old + r'"[\s\S]*?</symbol>', s)
        if not m:
            raise SystemExit("нет символа " + old + " в glava7-application.html")
        out.append(recolor(m.group(0).replace('id="' + old + '"', 'id="' + new + '"', 1), pal))
    return '<svg id="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>' + "".join(out) + "</defs></svg>"
