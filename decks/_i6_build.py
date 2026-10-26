# -*- coding: utf-8 -*-
"""Сборка деки «IP-сервисы: DHCP, NAT, NTP» строго по pptx «2.6» на движке дек 2.2:

    python -X utf8 _i6_build.py → ip-servisy-dhcp-nat-ntp.html

Общие модули (_dk_*, _sw_*) не меняются: тема «i6», титул/финал и CSS регистрируются здесь на лету.
Слайды — _i6_deck, схемы — _i6_fig, окна Wireshark — _i6_ws, финал — _i6_final, тренажёр ESR — _i6_cli.
Фоны — _i6_mkbg.py (в комплекте «NAT 2.6» нет папки ФОН)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _dk_build  # noqa: E402
import _dk_extra as X  # noqa: E402
import _dk_theme as T  # noqa: E402
import _i6_final  # noqa: E402
import _i6_fig  # noqa: E402
import _i6_ws  # noqa: E402
import _i6_cli  # noqa: E402

KEY = "i6"

CSS = r"""
:root{--fd:"Montserrat","Golos Text",sans-serif;--cy:#5cd2ff;--cy2:#9fe6ff;
 --panel:linear-gradient(160deg,rgba(16,38,86,.80),rgba(6,14,36,.90))}
body{background:#040a1e}
#bgfx{background:radial-gradient(1200px 700px at 50% 50%,transparent 50%,rgba(2,6,18,.6) 100%)!important}
.head{padding-left:0}
.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:800;letter-spacing:-.01em;color:#fff;text-shadow:0 0 18px rgba(92,190,255,.45)}
h1.t em,h1.t em.v{color:#7cc8ff;font-style:normal;text-shadow:0 0 18px rgba(92,190,255,.6)}
p.sub{color:#b9d2f5}
.c,.q{background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9))!important;border:1.5px solid rgba(92,190,255,.7)!important;
 border-radius:16px!important;box-shadow:0 0 18px rgba(58,160,255,.28),inset 0 0 26px rgba(58,160,255,.06)!important}
.c::before{display:none}
.c.mg{border-color:rgba(183,123,255,.8)!important}.c.lm{border-color:rgba(110,224,122,.75)!important}
.c.am{border-color:rgba(255,201,74,.8)!important}.c.rd{border-color:rgba(255,90,106,.8)!important}
.ch h3{font-family:var(--fd);font-weight:800}
.pic{border-radius:14px;border:1.5px solid rgba(92,190,255,.7);box-shadow:0 0 22px rgba(58,160,255,.35)}
.cover .big{font-family:var(--fd);font-weight:900;text-shadow:0 0 30px rgba(92,190,255,.55)}
.cover .big em{color:#7cc8ff;font-style:normal}
#hud{background:linear-gradient(0deg,rgba(4,10,30,.97),rgba(4,10,30,.7))}
#toc{background:rgba(4,10,30,.96)}
pre.cli{background:rgba(3,8,22,.92)!important;border:1.5px solid rgba(92,190,255,.6)!important;border-radius:12px!important}
pre.cli .k{color:#ffd36a}pre.cli .p{color:#7f9ccc}
.i6tbl table td,.i6tbl table th{font-size:clamp(12px,.92vw,17.5px)!important;line-height:1.3}
.i6mono td{font-family:var(--m)}
ol.i6ol{list-style:decimal;padding-left:1.4em}ol.i6ol li{padding-left:.2em;margin:.3em 0}
.i6scn .figwrap{background:linear-gradient(160deg,rgba(14,34,78,.82),rgba(5,13,34,.92));border:1.5px solid rgba(92,190,255,.75);
 border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35);padding:10px}
.i6scn svg{max-height:60vh}
.scbar{border:1.5px solid rgba(92,190,255,.6)!important;border-radius:12px}
.cs-side,.cs-term{border:1.5px solid rgba(92,190,255,.7)!important;outline:0!important;border-radius:14px}
"""

SCENE_CSS = """
.scene .figwrap{background:linear-gradient(160deg,rgba(14,34,78,.82),rgba(5,13,34,.92));border:1.5px solid rgba(92,190,255,.75);
 border-radius:16px;padding:10px}
"""


def register():
    T.THEMES[KEY] = {
        "title": "IP-сервисы: DHCP, NAT, NTP — лекция 2.6",
        "out": "ip-servisy-dhcp-nat-ntp.html",
        "adir": "_i6_assets",
        "fonts": T.FONT_LINK % ("family=Montserrat:wght@700;800;900&family=Golos+Text:wght@400;600;700;800&"
                                "family=JetBrains+Mono:wght@400;700"),
        "deck": "_i6_deck",
        "hues": [],
        "ovr": {},
        "css": CSS + _i6_fig.CSS + _i6_ws.CSS + _i6_cli.CSS + _i6_final.CSS,
    }
    T.SCENE_CSS[KEY] = SCENE_CSS
    X.i6_head = _i6_final.head
    X.i6_tail = _i6_final.tail
    # сцены SVG берут ПК из _dk_rep/crops/dev_<key>_pc.png — для 2.6 своих SVG-сцен на _sw_svg нет, но файл нужен
    crop = os.path.join(HERE, "_dk_rep", "crops", "dev_i6_pc.png")
    if not os.path.exists(crop):
        from PIL import Image
        Image.open(os.path.join(HERE, "_i6_assets", "dev", "laptop.png")).save(crop)


def build():
    register()
    import _dk_cli
    js0 = _dk_cli.JS
    _dk_cli.JS = js0 + "\n" + _i6_cli.JS + "\n" + _i6_final.JS
    try:
        _dk_build.build(KEY)
    finally:
        _dk_cli.JS = js0


if __name__ == "__main__":
    build()
