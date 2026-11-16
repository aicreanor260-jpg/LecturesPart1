# -*- coding: utf-8 -*-
"""Тема «Скуби-Ду» для дек «Глобальная сеть» и «WAN на основе Ethernet» — по инфографикам автора:
ночной лес / фиолетовый ретро-фон с цветами, кремовые карточки с толстой салатовой рамкой, фиолетовые надписи,
жёлтые заголовки с фиолетовым контуром, оранжевые цветочки-маркеры, бирюзовая плашка внизу."""
from _pt_kit import FONT_LINK, b64

FONTS = FONT_LINK % ("family=Rubik:wght@700;800;900&family=Nunito:wght@600;700;800;900&family=JetBrains+Mono:wght@400;700")

_CSS = r"""
:root{--bg0:#2a1460;--cy:#4b2a8a;--cy2:#6a3fc0;--mg:#e2701a;--mg2:#f59a2c;--lm:#7fb51e;--am:#f0a21c;--rd:#d8452f;
 --ink:#2a1460;--soft:#3a2a66;--dim:#6a5a96;--line:#b9dd4f;--panel:#fdf8e3;
 --fd:"Rubik","Nunito",sans-serif;--f:"Nunito","Segoe UI",sans-serif;--r:22px;--r2:14px}
body{background:#2a1460;color:var(--ink)}
#bg{display:none}#bgfx::after{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%(bg)s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%(cover)s)}
body:has(.slide.on .ptbleed) #bgimg{background-image:url(%(alt)s)}
#bgfx{background:none!important}
body:has(.slide.on .ptbleed) #bgfx{background:rgba(20,8,50,.55)!important}
/* ---- заголовок: жёлтый «мультяшный» с фиолетовым контуром ---- */
.head{padding-left:0;padding-top:6px}.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:900;text-transform:none;letter-spacing:.005em;color:#ffe23a!important;
 font-size:clamp(22px,2.7vw,50px)!important;line-height:1.2!important;-webkit-text-stroke:2px #2a0f55;paint-order:stroke fill;
 text-shadow:4px 4px 0 #2a0f55,0 0 22px rgba(0,0,0,.45)!important}
h1.t em,h1.t em.v{font-style:normal;color:#c8f05a!important;text-shadow:4px 4px 0 #2a0f55!important}
p.sub{display:inline-block;margin-top:8px;background:#fdf8e3;color:#2a1460;border:4px solid #b9dd4f;border-radius:999px;padding:4px 16px;font-weight:800}
/* ---- карточки ---- */
.c,.q{background:#fdf8e3!important;border:5px solid #b9dd4f!important;border-radius:22px!important;box-shadow:0 7px 0 #2a0f55,0 12px 26px rgba(0,0,0,.35)!important;color:#2a1460}
.c::before{display:none}
.c>.ch{display:inline-flex;align-self:flex-start;margin-bottom:10px;background:linear-gradient(180deg,#e0f57c,#bfe24e);border:3px solid #2a0f55;border-radius:999px;padding:5px 18px}
.c>.ch h3{color:#2a1460!important;font:900 clamp(15px,1.4vw,27px)/1.1 var(--fd)!important;text-transform:none}
.c.cy{border-color:#b9dd4f!important}.c.mg{border-color:#f59a2c!important}.c.mg>.ch{background:linear-gradient(180deg,#ffc06a,#f59a2c)}
.c.lm{border-color:#8fd14f!important}.c.am{border-color:#ffd23a!important}.c.am>.ch{background:linear-gradient(180deg,#fff08a,#ffd23a)}
.c.rd{border-color:#ff8a6a!important}.c.rd>.ch{background:linear-gradient(180deg,#ffb39a,#ff8a6a)}
.c p,ul.li li,.ir span{color:#2a1460!important;font-weight:700}
.c b,.c strong{color:#5a1fa8!important}
ul.li li{padding-left:1.55em!important}
ul.li li::before{content:"✿"!important;background:none!important;box-shadow:none!important;transform:none!important;width:auto!important;height:auto!important;
 left:0!important;top:-.05em!important;color:#f08a1c;font-size:1.15em;line-height:1}
.num{border-radius:50%%!important;background:#ffd23a!important;color:#2a1460!important;border:3px solid #2a0f55;box-shadow:none!important}
.tag{border-radius:999px!important;background:#fdf8e3!important;color:#2a1460!important;border:3px solid #b9dd4f!important;font-weight:800}
.tag.v{border-color:#f59a2c!important}.tag.g{border-color:#8fd14f!important}.tag.y{border-color:#ffd23a!important}.tag.r{border-color:#ff8a6a!important}
/* ---- нижняя плашка: бирюзовая с жёлтым текстом ---- */
.foot{border-radius:22px!important;background:#1d8f95!important;color:#ffe23a!important;border:4px solid #b9dd4f!important;box-shadow:0 6px 0 #2a0f55;font-weight:900}
.foot i{border-radius:50%%!important;background:#ffd23a!important;color:#2a1460!important}
.foot span{color:inherit!important}
.foot.warn{background:#c0442e!important;color:#fff!important}.foot.ok{background:#3f8f2a!important;color:#fff!important}.foot.note{background:#5a2fa0!important;color:#fff!important}
/* ---- таблицы ---- */
.tw{border-radius:18px!important;border:5px solid #b9dd4f!important;box-shadow:0 6px 0 #2a0f55;background:#fdf8e3!important;overflow:hidden}
.tw th{background:#4b2a8a!important;color:#ffe23a!important;font-weight:900}
.tw td{color:#2a1460!important;border-top:2px solid #e3dcb8!important;font-weight:700}
.tw tr.hl td{background:#f2ecc8!important}
/* ---- консоль ---- */
pre.cli{border-radius:16px!important;background:#1d1240!important;color:#efe9ff!important;border:4px solid #b9dd4f!important;box-shadow:0 6px 0 #2a0f55!important}
pre.cli .p{color:#a99ad8!important}pre.cli .k{color:#ffe23a!important;font-weight:700}
pre.cli.syn{background:#fdf8e3!important;color:#2a1460!important}pre.cli.syn i{color:#c0442e}
.clih{color:#ffe23a!important;font:900 clamp(11px,.85vw,16px)/1 var(--f)!important;letter-spacing:.06em;text-transform:uppercase;text-shadow:2px 2px 0 #2a0f55}
/* ---- рисунки pptx ---- */
.ptpic{background:#fdf8e3;border:5px solid #b9dd4f;border-radius:22px;box-shadow:0 7px 0 #2a0f55}
.ptpic img{background:transparent;padding:0}
.ptcap{color:#2a1460}
.ptbleed img{border-radius:18px;border:5px solid #b9dd4f;box-shadow:0 10px 0 #2a0f55,0 18px 40px rgba(0,0,0,.5)}
/* ---- сцены ---- */
.scene .figwrap{background:#fdf8e3;border:5px solid #b9dd4f;border-radius:22px;box-shadow:0 7px 0 #2a0f55}
.scbar{background:#4b2a8a!important;border:4px solid #b9dd4f!important;border-radius:18px!important}
.scbar .cap{color:#fff!important;font-weight:800}.scbar .cap b{color:#ffe23a!important}.scbar .pos{color:#ffe23a!important}
.scbar button{border-radius:999px!important;background:#ffd23a!important;color:#2a1460!important;border:3px solid #2a0f55!important;font-weight:900}
.scbar button.sec{background:#fdf8e3!important}
/* ---- тест и задачи ---- */
.q{padding:14px 16px!important}
.q .qt{color:#2a1460!important;font-weight:900}
.opts button{border-radius:14px!important;background:#fff!important;color:#2a1460!important;border:3px solid #d9cfa0!important;font-weight:800}
.opts button:hover{border-color:#b9dd4f!important;background:#fbffe8!important}
.opts button.good{background:#d8f5c4!important;border-color:#3f8f2a!important}.opts button.bad{background:#ffd5cc!important;border-color:#c0442e!important}
.ex{color:#2a1460!important;border-left-color:#f08a1c!important;font-weight:700}
.score{color:#ffe23a!important}
.inrow input{border-radius:12px!important;background:#fff!important;color:#2a1460!important;border:3px solid #d9cfa0!important}
.inrow button{border-radius:999px!important;background:#4b2a8a!important;color:#ffe23a!important;border:3px solid #2a0f55!important;font-weight:900}
.inrow button.sec{background:#fdf8e3!important;color:#2a1460!important}
.note{color:#2a1460!important;font-weight:700}.note b.ok{color:#2f7a1f!important}.note b.no{color:#c0442e!important}
/* ---- сортировка ---- */
.srt{background:#fdf8e3;border:5px solid #b9dd4f;border-radius:22px;padding:14px 16px;box-shadow:0 7px 0 #2a0f55;color:#2a1460}
.srt-pool{color:#b9a86a}
.srt-bin{background:#f2ecd0;border:3px dashed #4b2a8a}
.srt-h{color:#4b2a8a}
.srt-it{background:#fff;border:3px solid #4b2a8a;color:#2a1460}
.srt-res{color:#2a1460}
/* ---- титул ---- */
.cover{flex:0 1 auto;margin:auto 0 auto 4vw;align-items:flex-start;text-align:left;max-width:min(980px,60vw);background:rgba(253,248,227,.94);
 border:6px solid #b9dd4f;border-radius:28px;box-shadow:0 9px 0 #2a0f55,0 20px 50px rgba(0,0,0,.5);padding:34px 42px}
.cover .big{font-family:var(--fd)!important;font-weight:900;text-transform:none!important;color:#ffe23a!important;
 font-size:clamp(34px,5vw,92px)!important;line-height:1!important;-webkit-text-stroke:3px #2a0f55;paint-order:stroke fill;text-shadow:6px 6px 0 #2a0f55!important}
.cover .big em{font-style:normal;color:#c8f05a!important}
.cover .lead{color:#2a1460!important;font-weight:800}
.cover .tags{justify-content:flex-start}
/* ---- HUD ---- */
#hud{background:#2a1460!important;border-top:4px solid #b9dd4f!important}
#hud button{border-radius:999px!important;background:#ffd23a!important;color:#2a1460!important;border:3px solid #2a0f55!important;font-weight:900}
#hud #count{color:#ffe23a!important}#hud #sname{color:#efe9ff!important}#hud .hint{color:rgba(255,255,255,.6)!important}
#prog{background:#b9dd4f!important;box-shadow:none!important}
#toc{background:rgba(42,20,96,.97)!important}
#toc h2{color:#ffe23a!important;font-family:var(--fd)!important}
.tocit{border-radius:14px!important;background:#fdf8e3!important;color:#2a1460!important;border:3px solid #b9dd4f!important;font-weight:800}
.tocit i{color:#e2701a!important}
/* ---- тренажёр CLI ---- */
.cs-side{background:#fdf8e3!important;border:5px solid #b9dd4f!important;outline:0!important;border-radius:22px!important;box-shadow:0 7px 0 #2a0f55!important}
.cs-h{color:#4b2a8a!important;font-family:var(--fd)!important}
.cs-task{color:#2a1460!important;font-weight:800}.cs-task b{color:#5a1fa8!important;background:#efffc0}
.cs-btns button{border-radius:999px!important;background:#ffd23a!important;color:#2a1460!important;border:3px solid #2a0f55!important}
.cs-btns button.alt{background:#a6e07a!important}.cs-btns button.sec{background:#fff!important}
.cs-res .ok{color:#2f7a1f!important}.cs-res .no{color:#c0442e!important}
.cs-term{border:5px solid #b9dd4f!important;outline:0!important;border-radius:18px!important;overflow:hidden;box-shadow:0 7px 0 #2a0f55!important}
.cs-bar{background:#4b2a8a!important}
"""


def css(adir):
    return _CSS % {"bg": b64(adir, "bg_main"), "cover": b64(adir, "bg_cover"), "alt": b64(adir, "bg_alt")}
