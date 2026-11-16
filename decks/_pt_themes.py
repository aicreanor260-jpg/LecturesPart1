# -*- coding: utf-8 -*-
"""Темы дек STP (пиксельный «Покемон»), LACP (фэнтези-арена) и «Масштабируемость сети» (космос) — по инфографикам и фонам автора."""
import re

from _pt_kit import FONT_LINK, b64

FONTS = {
    "stp": FONT_LINK % "family=Rubik:wght@700;800;900&family=Golos+Text:wght@500;600;700;800&family=JetBrains+Mono:wght@400;700",
    "lacp": FONT_LINK % "family=Rubik:wght@700;800;900&family=Nunito:wght@600;700;800;900&family=JetBrains+Mono:wght@400;700",
    "hier": FONT_LINK % "family=Exo+2:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700",
}

COMMON = r"""
#bg{display:none}#bgfx::after{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%(bg)s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%(cover)s)}
.head{padding-left:0;padding-top:6px}.head::before{display:none}
.c::before{display:none}
.c>.ch{display:none}
ul.li li{padding-left:1.4em!important}
ul.li li::before{transform:none!important;box-shadow:none!important}
.foot span{color:inherit!important}
.ptpic img{background:transparent;padding:0}
"""

STP = r"""
:root{--cy:#1f8f86;--ink:#14244d;--soft:#1d2d55;--f:"Golos Text",sans-serif;--fd:"Rubik",sans-serif;--r:12px;--r2:10px}
body{background:#5bb8e8;color:#14244d}
#bgfx{background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.18))!important}
h1.t{display:inline-flex;align-items:center;gap:.5em;font-family:var(--fd);font-weight:900;text-transform:none;color:#12235a!important;
 font-size:clamp(20px,2.3vw,42px)!important;line-height:1.15!important;background:#fff;border:4px solid #2aa198;border-radius:14px;
 padding:.25em .8em;box-shadow:0 5px 0 #17665f;text-shadow:none!important}
h1.t::before{content:"";flex:none;width:.9em;height:.9em;border-radius:50%;border:3px solid #12235a;
 background:linear-gradient(180deg,#e8393b 0 45%,#12235a 45% 55%,#fff 55%)}
h1.t em{font-style:normal;color:#1f8f86!important;text-shadow:none!important}
p.sub{display:inline-block;margin-top:8px;background:#c9f2e6;color:#12235a;border:3px solid #2aa198;border-radius:10px;padding:3px 14px;font-weight:800}
.c,.q{background:#fbfef6!important;border:4px solid #2aa198!important;border-radius:14px!important;box-shadow:0 6px 0 #17665f!important;color:#14244d}
.c.am{border-color:#f0a52b!important;box-shadow:0 6px 0 #a76a10!important;background:#fff8e6!important}
.c.lm{border-color:#59b84a!important;box-shadow:0 6px 0 #2f7a26!important}
.c.mg{border-color:#3f7fd6!important;box-shadow:0 6px 0 #234f8f!important;background:#f2f8ff!important}
.c p,ul.li li{color:#14244d!important;font-weight:600}.c b{color:#0d5f58!important}
ul.li li::before{background:#e8393b!important;border:2px solid #12235a;border-radius:50%!important;width:.6em!important;height:.6em!important;top:.45em!important}
.foot{border-radius:14px!important;background:#ffe6a6!important;color:#12235a!important;border:4px solid #f0a52b!important;font-weight:800}
.foot i{border-radius:50%!important;background:#f0a52b!important;color:#fff!important}
.tw{border-radius:12px!important;border:4px solid #2aa198!important;background:#fff!important;overflow:hidden}
.tw th{background:#2aa198!important;color:#fff!important}.tw td{color:#14244d!important;font-weight:600}
pre.cli{border-radius:12px!important;background:#10213f!important;color:#e6f6ff!important;border:4px solid #2aa198!important}
pre.cli .p{color:#7fd1c6!important}pre.cli .k{color:#ffe082!important}
.clih{color:#12235a!important}
.ptpic{background:#fff;border:4px solid #2aa198;border-radius:14px;box-shadow:0 6px 0 #17665f}
.ptbleed img{border-radius:14px;border:5px solid #fff;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.opts button{border-radius:10px!important;background:#fff!important;color:#14244d!important;border:3px solid #9fd8d0!important;font-weight:700}
.opts button.good{background:#d4f5c8!important;border-color:#59b84a!important}.opts button.bad{background:#ffd6d0!important;border-color:#e8393b!important}
.q .qt{color:#12235a!important;font-weight:800}.ex{color:#14244d!important;border-left-color:#2aa198!important}
.inrow input{border-radius:10px!important;background:#fff!important;color:#14244d!important;border:3px solid #9fd8d0!important}
.inrow button{border-radius:10px!important;background:#2aa198!important;color:#fff!important;border:0!important;font-weight:800}
.inrow button.sec{background:#fff!important;color:#14244d!important;border:2px solid #2aa198!important}
.note{color:#14244d!important}
.srt{background:#fbfef6;border:4px solid #2aa198;border-radius:14px;padding:14px;box-shadow:0 6px 0 #17665f;color:#14244d}
.srt-bin{background:#eaf8f4;border:3px dashed #2aa198}.srt-h{color:#12235a}.srt-it{background:#fff;border:3px solid #12235a;color:#12235a}
.cover{margin:auto;background:#fff;border:6px solid #2aa198;border-radius:22px;box-shadow:0 10px 0 #17665f;padding:34px 46px;max-width:min(1100px,86vw)}
.cover .big{font-family:var(--fd)!important;font-weight:900;color:#12235a!important;text-transform:none!important;font-size:clamp(32px,4.6vw,84px)!important;
 line-height:1.05!important;text-shadow:4px 4px 0 #c9f2e6!important}
.cover .big em{font-style:normal;color:#e8393b!important}
.cover .lead{color:#14244d!important;font-weight:700}
#hud{background:#12235a!important;border-top:4px solid #2aa198!important}
#hud button{border-radius:8px!important;background:#fff!important;color:#12235a!important;border:2px solid #2aa198!important;font-weight:800}
#hud #count{color:#ffe082!important}#hud #sname{color:#fff!important}
#prog{background:#e8393b!important}
.tag{background:#fff!important;color:#12235a!important;border:2px solid #2aa198!important;border-radius:8px!important;font-weight:800}
#toc{background:rgba(18,35,90,.96)!important}#toc h2{color:#fff!important}
.tocit{border-radius:10px!important;background:#fff!important;color:#12235a!important;border:2px solid #2aa198!important}
.cs-side{background:#fbfef6!important;border:4px solid #2aa198!important;outline:0!important;border-radius:14px!important}
.cs-h{color:#e8393b!important}.cs-task{color:#14244d!important}.cs-task b{color:#0d5f58!important;background:#e6faf5}
.cs-btns button{border-radius:8px!important;background:#ffe082!important;color:#12235a!important;border:2px solid #12235a!important}
.cs-btns button.alt{background:#a6e07a!important}.cs-btns button.sec{background:#fff!important}
.cs-term{border:4px solid #2aa198!important;outline:0!important;border-radius:12px!important;overflow:hidden}.cs-bar{background:#12235a!important}
.cs-res .ok{color:#2f7a26!important}.cs-res .no{color:#c0262a!important}
"""

LACP = r"""
:root{--cy:#2a5bd7;--ink:#2a1a08;--soft:#3a2810;--f:"Nunito",sans-serif;--fd:"Rubik",sans-serif;--r:14px;--r2:10px}
body{background:#2c8a7a;color:#2a1a08}
#bgfx{background:rgba(10,20,40,.12)!important}
h1.t{display:inline-block;font-family:var(--fd);font-weight:900;text-transform:uppercase;color:#ffd33a!important;
 font-size:clamp(20px,2.4vw,44px)!important;line-height:1.1!important;background:linear-gradient(180deg,#3b74e8,#1d48b8);border:4px solid #0f2a6e;
 border-radius:14px;padding:.2em .8em;box-shadow:0 6px 0 #0f2a6e,0 10px 20px rgba(0,0,0,.3);-webkit-text-stroke:2px #0f2a6e;paint-order:stroke fill;
 text-shadow:0 3px 0 #0f2a6e!important}
h1.t em{font-style:normal;color:#fff!important}
p.sub{display:inline-block;margin-top:8px;background:#f7e6bd;color:#2a1a08;border:3px solid #c9962e;border-radius:10px;padding:3px 14px;font-weight:800}
.c,.q{background:linear-gradient(180deg,#fbefcf,#f2dca4)!important;border:4px solid #c9962e!important;border-radius:16px!important;
 box-shadow:inset 0 0 0 2px #fff6dc,0 6px 0 #7a5410,0 12px 22px rgba(0,0,0,.25)!important;color:#2a1a08}
.c.am{border-color:#e0a21c!important}.c.mg{border-color:#7a4bd6!important}.c.lm{border-color:#3fae4a!important}
.c p,ul.li li{color:#2a1a08!important;font-weight:700}.c b{color:#1d48b8!important}
ul.li li::before{background:#ffd33a!important;border:2px solid #0f2a6e;border-radius:3px!important;width:.6em!important;height:.6em!important;top:.45em!important;transform:rotate(45deg)!important}
.foot{border-radius:14px!important;background:linear-gradient(180deg,#3b74e8,#1d48b8)!important;color:#fff!important;border:4px solid #0f2a6e!important;font-weight:800}
.foot i{border-radius:50%!important;background:#ffd33a!important;color:#0f2a6e!important}
.tw{border-radius:12px!important;border:4px solid #c9962e!important;background:#fff8e6!important;overflow:hidden}
.tw th{background:#1d48b8!important;color:#ffd33a!important}.tw td{color:#2a1a08!important;font-weight:700}
pre.cli{border-radius:12px!important;background:#0f1c3a!important;color:#e8f0ff!important;border:4px solid #c9962e!important}
pre.cli .p{color:#9fb6e8!important}pre.cli .k{color:#ffd33a!important}
.clih{color:#fff!important;text-shadow:0 2px 0 #0f2a6e}
.ptpic{background:#fff8e6;border:4px solid #c9962e;border-radius:16px;box-shadow:0 6px 0 #7a5410}
.ptbleed img{border-radius:16px;border:5px solid #c9962e;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.opts button{border-radius:10px!important;background:#fff8e6!important;color:#2a1a08!important;border:3px solid #c9962e!important;font-weight:800}
.opts button.good{background:#d4f5c8!important;border-color:#3fae4a!important}.opts button.bad{background:#ffd0c8!important;border-color:#d84a2a!important}
.q .qt{color:#0f2a6e!important;font-weight:900}.ex{color:#2a1a08!important;border-left-color:#1d48b8!important}
.inrow input{border-radius:10px!important;background:#fff!important;color:#2a1a08!important;border:3px solid #c9962e!important}
.inrow button{border-radius:10px!important;background:#1d48b8!important;color:#ffd33a!important;border:3px solid #0f2a6e!important;font-weight:900}
.inrow button.sec{background:#fff8e6!important;color:#2a1a08!important}
.note{color:#2a1a08!important}.score{color:#fff!important}
.srt{background:#fbefcf;border:4px solid #c9962e;border-radius:16px;padding:14px;box-shadow:0 6px 0 #7a5410;color:#2a1a08}
.srt-bin{background:#fff8e6;border:3px dashed #1d48b8}.srt-h{color:#1d48b8}.srt-it{background:#fff;border:3px solid #0f2a6e;color:#0f2a6e}
.cover{margin:auto;background:linear-gradient(180deg,#fbefcf,#f2dca4);border:6px solid #c9962e;border-radius:24px;box-shadow:0 10px 0 #7a5410;padding:34px 46px;max-width:min(1100px,86vw)}
.cover .big{font-family:var(--fd)!important;font-weight:900;color:#ffd33a!important;text-transform:uppercase!important;font-size:clamp(30px,4.4vw,80px)!important;
 line-height:1.05!important;-webkit-text-stroke:3px #0f2a6e;paint-order:stroke fill;text-shadow:0 6px 0 #0f2a6e!important}
.cover .big em{font-style:normal;color:#fff!important}
.cover .lead{color:#2a1a08!important;font-weight:800}
#hud{background:#0f2a6e!important;border-top:4px solid #c9962e!important}
#hud button{border-radius:8px!important;background:#ffd33a!important;color:#0f2a6e!important;border:2px solid #0f2a6e!important;font-weight:900}
#hud #count{color:#ffd33a!important}#hud #sname{color:#fff!important}
#prog{background:#ffd33a!important}
.tag{background:#fff8e6!important;color:#0f2a6e!important;border:2px solid #c9962e!important;border-radius:8px!important;font-weight:900}
#toc{background:rgba(15,42,110,.96)!important}#toc h2{color:#ffd33a!important}
.tocit{border-radius:10px!important;background:#fbefcf!important;color:#2a1a08!important;border:2px solid #c9962e!important}
.cs-side{background:#fbefcf!important;border:4px solid #c9962e!important;outline:0!important;border-radius:16px!important}
.cs-h{color:#1d48b8!important}.cs-task{color:#2a1a08!important}.cs-task b{color:#1d48b8!important;background:#fff8e6}
.cs-btns button{border-radius:8px!important;background:#ffd33a!important;color:#0f2a6e!important;border:2px solid #0f2a6e!important}
.cs-btns button.alt{background:#8fe07a!important}.cs-btns button.sec{background:#fff!important}
.cs-term{border:4px solid #c9962e!important;outline:0!important;border-radius:12px!important;overflow:hidden}.cs-bar{background:#1d48b8!important}
.cs-res .ok{color:#2f7a26!important}.cs-res .no{color:#c0262a!important}
"""

HIER = r"""
:root{--cy:#5fd0ff;--ink:#e6eeff;--soft:#c9d6f2;--f:"Exo 2",sans-serif;--fd:"Exo 2",sans-serif;--r:12px;--r2:10px}
body{background:#030712;color:#e6eeff}
#bgfx{background:linear-gradient(180deg,rgba(3,7,18,.45),rgba(3,7,18,.7))!important}
body:has(.slide.on.cover-slide) #bgfx{background:rgba(3,7,18,.25)!important}
h1.t{font-family:var(--fd);font-weight:500;text-transform:uppercase;letter-spacing:.22em;color:#f2f6ff!important;font-size:clamp(17px,1.9vw,34px)!important;
 line-height:1.25!important;text-shadow:0 0 18px rgba(95,208,255,.45)!important;border-bottom:1px solid rgba(95,208,255,.5);padding-bottom:.25em}
h1.t em{font-style:normal;color:#e8b65a!important;text-shadow:0 0 18px rgba(232,182,90,.6)!important}
p.sub{display:inline-block;margin-top:8px;color:#9fb3d9;letter-spacing:.08em;font-weight:500}
.c,.q{background:linear-gradient(160deg,rgba(14,24,48,.88),rgba(6,12,28,.92))!important;border:1px solid rgba(95,208,255,.4)!important;border-radius:12px!important;
 box-shadow:0 0 0 1px rgba(255,255,255,.04) inset,0 0 26px rgba(40,120,255,.18)!important;color:#e6eeff}
.c.am{border-color:rgba(232,182,90,.55)!important}.c.mg{border-color:rgba(170,120,255,.5)!important}.c.lm{border-color:rgba(110,230,170,.45)!important}
.c p,ul.li li{color:#dbe5ff!important;font-weight:400}.c b{color:#ffd58a!important;font-weight:600}
ul.li li::before{background:#5fd0ff!important;border-radius:50%!important;width:.45em!important;height:.45em!important;top:.55em!important;box-shadow:0 0 8px #5fd0ff!important}
.foot{border-radius:12px!important;background:rgba(232,182,90,.12)!important;color:#ffe2a8!important;border:1px solid rgba(232,182,90,.6)!important;font-weight:500}
.foot i{border-radius:50%!important;background:transparent!important;color:#e8b65a!important;border:1px solid #e8b65a}
.tw{border-radius:10px!important;border:1px solid rgba(95,208,255,.45)!important;background:rgba(6,12,28,.9)!important}
.tw th{background:rgba(95,208,255,.15)!important;color:#bfeaff!important;letter-spacing:.06em}.tw td{color:#dbe5ff!important}
pre.cli{border-radius:10px!important;background:rgba(2,6,16,.95)!important;color:#d6f3ff!important;border:1px solid rgba(95,208,255,.45)!important}
.ptpic{background:rgba(240,246,255,.96);border:1px solid rgba(95,208,255,.6);border-radius:12px;box-shadow:0 0 30px rgba(40,120,255,.25)}
.ptbleed img{border-radius:12px;border:1px solid rgba(95,208,255,.6);box-shadow:0 0 40px rgba(40,120,255,.35)}
.opts button{border-radius:10px!important;background:rgba(14,24,48,.9)!important;color:#e6eeff!important;border:1px solid rgba(95,208,255,.4)!important}
.opts button.good{background:rgba(60,200,130,.25)!important;border-color:#6ee6aa!important}.opts button.bad{background:rgba(255,90,90,.2)!important;border-color:#ff7a7a!important}
.q .qt{color:#f2f6ff!important;font-weight:600}.ex{color:#c9d6f2!important;border-left-color:#e8b65a!important}
.inrow input{border-radius:8px!important;background:rgba(2,6,16,.9)!important;color:#fff!important;border:1px solid rgba(95,208,255,.5)!important}
.inrow button{border-radius:8px!important;background:rgba(95,208,255,.2)!important;color:#bfeaff!important;border:1px solid #5fd0ff!important}
.inrow button.sec{background:transparent!important}
.note{color:#c9d6f2!important}
.srt{background:rgba(6,12,28,.9);border:1px solid rgba(95,208,255,.45);border-radius:12px;padding:14px;color:#e6eeff}
.srt-pool{color:#5fd0ff}.srt-bin{background:rgba(95,208,255,.06);border:1px dashed rgba(95,208,255,.6)}.srt-h{color:#e8b65a;letter-spacing:.08em}
.srt-it{background:rgba(14,24,48,.95);border:1px solid #5fd0ff;color:#e6eeff}
.srt-it.ok{color:#0a2a14!important}.srt-it.no{color:#3a0a0a!important}
.cover{margin:auto;text-align:center;align-items:center;background:rgba(3,7,18,.55);border:1px solid rgba(95,208,255,.45);border-radius:16px;padding:36px 50px;
 box-shadow:0 0 60px rgba(40,120,255,.25);max-width:min(1150px,88vw)}
.cover .big{font-family:var(--fd)!important;font-weight:300;letter-spacing:.14em;text-transform:uppercase!important;color:#f2f6ff!important;
 font-size:clamp(26px,3.8vw,70px)!important;line-height:1.15!important;text-shadow:0 0 30px rgba(95,208,255,.55)!important}
.cover .big em{font-style:normal;color:#e8b65a!important}
.cover .lead{color:#c9d6f2!important}
.tag{background:transparent!important;color:#bfeaff!important;border:1px solid rgba(95,208,255,.6)!important;border-radius:999px!important}
#hud{background:rgba(3,7,18,.92)!important;border-top:1px solid rgba(95,208,255,.4)!important}
#hud button{border-radius:8px!important;background:transparent!important;color:#bfeaff!important;border:1px solid rgba(95,208,255,.5)!important}
#hud #count{color:#e8b65a!important}#hud #sname{color:#c9d6f2!important}
#prog{background:linear-gradient(90deg,#5fd0ff,#e8b65a)!important}
#toc{background:rgba(3,7,18,.96)!important}#toc h2{color:#f2f6ff!important;letter-spacing:.2em}
.tocit{border-radius:8px!important;background:rgba(14,24,48,.9)!important;color:#dbe5ff!important;border:1px solid rgba(95,208,255,.35)!important}
.tocit i{color:#e8b65a!important}
"""


def css(key, adir):
    t = {"stp": STP, "lacp": LACP, "hier": HIER}[key]
    body = re.sub(r"%(?!\()", "%%", COMMON)
    return body % {"bg": b64(adir, "bg_main"), "cover": b64(adir, "bg_cover")} + t
