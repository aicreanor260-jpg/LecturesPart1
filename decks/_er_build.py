# -*- coding: utf-8 -*-
"""Сборка деки «Маршрутизаторы ESR» (2.3 доп.) строго по pptx «2_3» на движке коммутации:

    python _er_build.py        → marshrutizatory-esr.html

Стиль — лавандовое стекло инфографик автора (комплект «Маршрутизатор 2.3»): светлые стеклянные панели,
тёмно-синий текст, сине-фиолетовые акценты; фон — размытая инфографика. Деку marshrutizatory.html не трогает."""
import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402
import _er_intro  # noqa: E402

OUT = "marshrutizatory-esr.html"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;800&'
         'family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap">')


def b64(name):
    with open(os.path.join(HERE, "_er_assets", name + ".webp"), "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


THEME = r"""
:root{--bg0:#e9e8fb;--cy:#2f6bff;--cy2:#5a4bff;--mg:#8a3ad6;--mg2:#c03ad6;--lm:#18a75a;--am:#d98a00;--rd:#e23b5a;
 --ink:#141a5c;--soft:#3e4688;--dim:#6a70a8;--line:rgba(90,90,220,.28);
 --panel:linear-gradient(160deg,rgba(255,255,255,.86),rgba(240,240,255,.78));
 --fd:"Unbounded","Golos Text",sans-serif;--r:18px;--r2:12px}
body{background:#e9e8fb;color:var(--ink)}
#bg{display:none}#bgfx::after{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%s)}
#bgfx{background:linear-gradient(180deg,rgba(255,255,255,.30),rgba(235,235,255,.45))!important}
body:has(.slide.on.cover-slide) #bgfx{background:linear-gradient(90deg,rgba(255,255,255,.88) 35%%,rgba(255,255,255,.2))!important}
.head::before{background:linear-gradient(180deg,#2f6bff,#8a3ad6);box-shadow:none}
h1.t{font-family:var(--fd);font-weight:800;text-transform:none;color:#10145a;text-shadow:none;letter-spacing:-.01em;
 font-size:clamp(20px,2.3vw,42px)}
h1.t em,h1.t em.v{color:#5a4bff;text-shadow:none;background:linear-gradient(90deg,#2f6bff,#8a3ad6);-webkit-background-clip:text;
 background-clip:text;-webkit-text-fill-color:transparent}
p.sub{color:var(--soft)}
.c,.q{background:var(--panel)!important;border:1.5px solid rgba(255,255,255,.95)!important;border-radius:18px;
 box-shadow:0 10px 30px rgba(70,60,190,.16),inset 0 1px 0 #fff!important;backdrop-filter:blur(10px);color:var(--ink)}
.c::before{display:none}
.c p,.c li,.ch h3,.qt{color:var(--ink)!important}
.c b,.c strong{color:#2a3ad0!important;-webkit-text-fill-color:#2a3ad0!important;background:none!important}
.c p,ul.li li,.ir span{font-size:clamp(15px,1.5vw,30px)!important;line-height:1.42}
.ch h3{font-size:clamp(15px,1.45vw,28px)!important}
pre.cli{font-size:clamp(13px,1.25vw,24px)!important;white-space:pre-wrap;overflow-wrap:anywhere}
pre.cli.term{font-size:clamp(11px,1.02vw,20px)!important;white-space:pre;overflow-x:auto}
.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) .c p,.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) ul.li li{font-size:clamp(17px,1.85vw,36px)!important}
.ch h3{font-family:"Golos Text",sans-serif;font-weight:800}
.c.cy{border-left:6px solid #2f6bff!important}.c.mg{border-left:6px solid #8a3ad6!important}
.c.lm{border-left:6px solid #18a75a!important}.c.am{border-left:6px solid #e89a10!important}.c.rd{border-left:6px solid #e23b5a!important}
ul.li li::before{background:#5a4bff!important;box-shadow:none!important}
pre.cli{background:#141838!important;color:#e6e9ff;border:1.5px solid #5a62c8!important;border-radius:12px}
pre.cli .p{color:#8f97cc}pre.cli .k{color:#9fd0ff;font-weight:700}
pre.cli.syn{background:rgba(255,255,255,.9)!important;color:#141a5c;border-color:#b9b6f0!important;font-weight:700}
.clih{color:#3e4688!important;font-weight:800}
pre.cli.erhl{border:3px solid #e23b5a!important;margin-top:-4px}
.pic{border:1.5px solid #fff;border-radius:18px;box-shadow:0 12px 34px rgba(70,60,190,.22);background:transparent}
.pic img{background:transparent}
.figwrap.erpanel,.scene .figwrap{background:linear-gradient(160deg,rgba(255,255,255,.8),rgba(238,238,255,.7));
 border:1.5px solid #fff;border-radius:18px;box-shadow:0 10px 30px rgba(70,60,190,.16);padding:8px}
.scbar{background:rgba(255,255,255,.88)!important;border:1.5px solid #fff!important;border-radius:14px;color:var(--ink)}
.scbar .cap,.scbar .pos{color:var(--ink)!important}
.scbar button,.opts button,.inrow button{background:linear-gradient(90deg,#2f6bff,#6a4cff)!important;color:#fff!important;border:0!important}
.scbar button.sec,.inrow button.sec{background:rgba(90,75,255,.12)!important;color:#2a3ad0!important}
.opts button{background:rgba(255,255,255,.9)!important;color:var(--ink)!important;border:1.5px solid #c9c5f5!important}
.opts button.ok{background:#d9f7e5!important;border-color:#18a75a!important}.opts button.no{background:#ffe0e6!important;border-color:#e23b5a!important}
.inrow input{background:#fff!important;color:var(--ink)!important;border:1.5px solid #c9c5f5!important}
.tag{background:rgba(255,255,255,.9)!important;color:#2a3ad0!important;border:1.5px solid #c9c5f5!important}
.foot{background:rgba(255,255,255,.88)!important;color:var(--ink)!important;border-color:#c9c5f5!important}
.ex,.note{color:var(--soft)!important}
.cover{background:none}
.cover .big{font-family:var(--fd);color:#10145a;text-shadow:none;text-transform:none}
.cover .big em{color:#5a4bff;text-shadow:none}
.cover .lead{color:#2a3070}
#hud{background:linear-gradient(0deg,rgba(255,255,255,.96),rgba(255,255,255,.75));color:var(--ink)}
#hud button{color:var(--ink)!important}
#toc{background:rgba(245,245,255,.97);color:var(--ink)}
.tw table{background:rgba(255,255,255,.92);color:var(--ink)}
.tw th{background:linear-gradient(90deg,#2f6bff,#4aa3ff)!important;color:#fff!important}
.tw td{color:var(--ink)!important;border-color:#dcdaf7!important}
.ertw.ctr td{text-align:center}
.ertw table{font-size:clamp(15px,1.45vw,28px)!important}
.cs-side{background:var(--panel)!important;border:1.5px solid #fff!important;outline:0!important;border-radius:18px;box-shadow:0 10px 30px rgba(70,60,190,.16)!important}
.cs-task{color:var(--ink)!important}.cs-task b{color:#2a3ad0!important}
.cs-h{color:#5a4bff!important}
.cs-btns button{background:linear-gradient(90deg,#2f6bff,#6a4cff)!important;color:#fff!important;border:0!important;border-radius:10px}
.cs-btns button.alt{background:#18a75a!important}.cs-btns button.sec{background:rgba(90,75,255,.12)!important;color:#2a3ad0!important}
.cs-res .ok{color:#108a48!important}.cs-res .no{color:#d0284a!important}
.cs-term{border:1.5px solid #5a62c8!important;outline:0!important;border-radius:14px;overflow:hidden}
/* окна программ, ICMP, этапы AAA */
.erwin{max-width:1040px;width:100%%;margin:auto;background:#fff;color:#111;border:1px solid #8a8fc0;border-radius:10px;box-shadow:0 14px 40px rgba(60,50,170,.25);
 font:500 clamp(14px,1.35vw,26px)/1.4 "Golos Text",sans-serif;overflow:hidden}
.erw-t{display:flex;justify-content:space-between;padding:8px 14px;background:#f2f2fa;font-weight:700}
.erw-b{padding:12px 18px}.erw-b p{margin:8px 0}
.erw-tab{display:inline-block;border:1px solid #aaa;border-bottom:0;padding:2px 10px}
.erw-r{margin:6px 0}.erw-r.dis{color:#999}
.erw-r i.o,.pt-rad i.o{display:inline-block;width:13px;height:13px;border:1.5px solid #555;border-radius:50%%;margin-right:7px;vertical-align:-1px}
i.o.on{background:radial-gradient(#222 40%%,#fff 45%%)}
.erw-g{border:1px solid #ccc;padding:6px 14px;margin:4px 0}
.erw-row{display:flex;justify-content:space-between;margin:5px 0}.erw-row i{font-style:normal;border:1px solid #888;padding:0 18px;letter-spacing:.3em}
.erw-f{display:flex;justify-content:space-between;align-items:center;margin-top:8px}.erw-f.r{justify-content:flex-end;gap:10px}
.erw-f u,.pt-bt u,.pt-f u{text-decoration:none;border:1px solid #888;padding:3px 16px;background:#eee}
i.x{display:inline-block;width:13px;height:13px;border:1.5px solid #555;margin-right:7px}
.putty{max-width:1300px}.pt{display:grid;grid-template-columns:1fr 2.2fr;gap:12px}
.pt-l{font-size:.85em}.pt-c.on{background:#2f6bff;color:#fff}.pt-h{font-weight:700}.pt-h.c{text-align:center}
.putty fieldset{border:1px solid #bbb;padding:6px 10px;margin:6px 0}.putty legend{font-size:.9em}
.pt-2{display:flex;gap:10px}.pt-2 label{flex:1}.pt-2 .sm{flex:0 0 90px}
i.in{display:block;font-style:normal;border:1px solid #888;min-height:1.5em;padding:0 6px;background:#fff}
.pt-rad{display:flex;gap:14px;align-items:center;flex-wrap:wrap}.pt-list{flex:1;border:1px solid #888;min-height:5em;padding:2px 6px}
.pt-bt{display:flex;flex-direction:column;gap:5px}.pt-f{grid-column:1/-1;display:flex;justify-content:space-between}.pt-f span{display:flex;gap:8px}
.ericmp{display:flex;flex-direction:column;align-items:center;gap:0;font:700 clamp(13px,1.2vw,22px)/1.25 "Golos Text",sans-serif}
.ei-row{display:flex}.ei-row span{border:1.5px solid #6a70a8;background:rgba(255,255,255,.92);padding:8px 14px;text-align:center;color:#141a5c}
.ei-row span.hl{background:#dde4ff;color:#1a2a9a;font-weight:800}.ei-msg{margin-top:-1.5px}
.ei-msg .w{min-width:220px}.ei-msg .w2{min-width:400px}
.ersteps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:stretch;flex:1}
.ersteps .es{height:100%%;background:var(--panel);border:1.5px solid #fff;border-radius:18px;padding:22px;box-shadow:0 10px 30px rgba(70,60,190,.16)}
.ersteps u{display:inline-block;text-decoration:none;background:linear-gradient(90deg,#2f6bff,#6a4cff);color:#fff;font:800 clamp(14px,1.2vw,22px)/1 var(--f);
 padding:9px 18px;border-radius:12px}
.ersteps b{display:block;margin:16px 0 10px;font:800 clamp(18px,2vw,38px)/1.2 var(--f);color:#10145a}
.ersteps p{font:600 clamp(16px,1.7vw,32px)/1.45 var(--f);color:#2a3070}
.qt{font-size:clamp(15px,1.45vw,28px)!important;line-height:1.35}
.opts button{font-size:clamp(14px,1.3vw,25px)!important;padding:.45em .8em!important}
.inrow input,.inrow button{font-size:clamp(14px,1.2vw,23px)!important;padding:.4em .8em!important}
.ex{font-size:clamp(13px,1.15vw,22px)!important}
.cs-task{font-size:clamp(16px,1.5vw,29px)!important}.cs-btns button{font-size:clamp(13px,1.1vw,21px)!important}
.cs-out,.cs-in{font-size:clamp(14px,1.25vw,24px)!important}
svg.erfig text{font-family:"Golos Text",sans-serif}
"""


# общие градиенты/фильтры SVG — один раз на видимом уровне: ссылки из слайдов в display:none не рисуются
GDEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">%s</svg>'


def build():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _dk_kit
    import _dk_cli
    import _er_deck
    import _er_final
    import _er_fig

    del L.SL[:]
    _er_final.cover()
    _er_deck.build()
    _er_final.tail()
    slides = list(L.SL)
    css = CSS + _dk_kit.CSS + _dk_cli.CSS + THEME % (b64("bg_main"), b64("bg_cover")) + _er_intro.CSS
    with io.open(os.path.join(HERE, "_er_cli.js"), encoding="utf-8") as fh:
        cli_js = fh.read()
    js = JS + _dk_kit.JS + cli_js
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>Маршрутизаторы Eltex ESR — лекция</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-esr\">\n"
        '%s<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n" % (FONTS, css, GDEFS % _er_fig.defs(), "\n".join(slides), _sw_build.HUD, js))
    out = os.environ.get("ER_OUT") or os.path.join(HERE, OUT)
    with io.open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (out, len(slides), os.path.getsize(out) / 1048576.0))


if __name__ == "__main__":
    build()
