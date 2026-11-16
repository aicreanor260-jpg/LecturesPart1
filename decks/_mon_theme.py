# -*- coding: utf-8 -*-
"""Тема «Черепашки» для деки «Мониторинг и управление» — по инфографикам автора: бирюзово-зелёный комикс-фон с точками,
жёлтые панели с толстым чёрным контуром, красные наклонные ленты с жёлтыми буквами, зелёные акценты."""
from _pt_kit import FONT_LINK

FONTS = FONT_LINK % ("family=Rubik:ital,wght@0,700;0,800;0,900;1,800;1,900&family=Nunito:wght@600;700;800;900&family=JetBrains+Mono:wght@400;700")

CSS = r"""
:root{--bg0:#0f6e68;--cy:#e2241e;--cy2:#ff4a3a;--mg:#e2241e;--lm:#3fae2a;--am:#ffd21a;--rd:#e2241e;
 --ink:#111;--soft:#1d1d1d;--dim:#444;--line:#111;--panel:#fff6b8;--fd:"Rubik","Nunito",sans-serif;--f:"Nunito","Segoe UI",sans-serif;--r:14px;--r2:10px}
body{background:#0f6e68;color:#111}
#bg{display:none}#bgfx::after{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;
 background:radial-gradient(circle at 50% 45%,rgba(190,255,120,.35),transparent 55%),
  repeating-conic-gradient(from 0deg at 50% 45%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg),
  radial-gradient(rgba(0,0,0,.18) 22%,transparent 24%) 0 0/14px 14px,
  linear-gradient(160deg,#21b3a4,#0f7a70 55%,#0b5a54)}
body:has(.slide.on.cover-slide) #bgimg{background:radial-gradient(circle at 50% 50%,#ffe14a 0,#ff9a1a 18%,transparent 40%),
  repeating-conic-gradient(from 0deg at 50% 50%,#ffd21a 0 7deg,#ff8a1a 7deg 14deg)}
#bgfx{background:none!important}
.head{padding-left:0;padding-top:6px}.head::before{display:none}
h1.t{display:inline-block;font-family:var(--fd);font-style:italic;font-weight:900;text-transform:uppercase;letter-spacing:.01em;
 font-size:clamp(20px,2.3vw,44px)!important;line-height:1.15!important;color:#ffe21a!important;background:#e2241e;
 padding:.12em .7em .16em;border:4px solid #111;transform:skew(-8deg);box-shadow:6px 6px 0 #111;-webkit-text-stroke:1.5px #111;paint-order:stroke fill;
 text-shadow:3px 3px 0 #111!important}
h1.t em,h1.t em.v{font-style:italic;color:#c8ff4a!important;text-shadow:3px 3px 0 #111!important}
p.sub{display:inline-block;margin-top:10px;background:#fff6b8;color:#111;border:3px solid #111;border-radius:8px;padding:4px 14px;font-weight:800;box-shadow:4px 4px 0 #111}
.c,.q{background:#fff6b8!important;border:4px solid #111!important;border-radius:14px!important;box-shadow:6px 6px 0 #111!important;color:#111}
.c::before{display:none}
.c>.ch{display:inline-flex;align-self:flex-start;margin-bottom:10px;background:#e2241e;border:3px solid #111;padding:4px 16px;transform:skew(-8deg);box-shadow:3px 3px 0 #111}
.c>.ch h3{color:#ffe21a!important;font:900 italic clamp(14px,1.3vw,25px)/1.1 var(--fd)!important;text-transform:uppercase;text-shadow:2px 2px 0 #111}
.c.cy>.ch{background:#1f7fd8}.c.lm>.ch{background:#3fae2a}.c.am>.ch{background:#ff8a1a}.c.mg>.ch,.c.rd>.ch{background:#e2241e}
.c.cy{background:#e8fbff!important}.c.lm{background:#effcd8!important}
.c p,ul.li li,.ir span{color:#111!important;font-weight:700}
.c b,.c strong{color:#c0170f!important}
ul.li li{padding-left:1.5em!important}
ul.li li::before{background:#ffd21a!important;border:2px solid #111;border-radius:50%!important;box-shadow:none!important;transform:none!important;width:.6em!important;height:.6em!important;top:.42em!important}
.num{border-radius:50%!important;background:#ffd21a!important;color:#111!important;border:3px solid #111}
.tag{border-radius:8px!important;background:#fff!important;color:#111!important;border:3px solid #111!important;font-weight:900;box-shadow:2px 2px 0 #111}
.tag.v{background:#ffd0cc!important}.tag.g{background:#d6f5b8!important}.tag.y{background:#fff08a!important}.tag.r{background:#ffb3ad!important}
.foot{border-radius:12px!important;background:#ffd21a!important;color:#111!important;border:4px solid #111!important;box-shadow:5px 5px 0 #111;font-weight:900}
.foot i{border-radius:50%!important;background:#e2241e!important;color:#fff!important;border:2px solid #111}
.foot span{color:inherit!important}
.foot.warn{background:#ff8a80!important}.foot.ok{background:#a6e07a!important}.foot.note{background:#9fdcff!important}
.tw{border-radius:12px!important;border:4px solid #111!important;box-shadow:5px 5px 0 #111;background:#fff!important;overflow:hidden}
.tw th{background:#e2241e!important;color:#ffe21a!important;font-weight:900}
.tw td{color:#111!important;border-top:2px solid #ddd!important;font-weight:700}
.tw tr.hl td{background:#fff6b8!important}
pre.cli{border-radius:12px!important;background:#10241f!important;color:#e6ffe6!important;border:4px solid #111!important;box-shadow:5px 5px 0 #111!important}
pre.cli .p{color:#7fd1a8!important}pre.cli .k{color:#ffe21a!important;font-weight:700}
pre.cli .h{background:rgba(255,226,26,.3)}
pre.cli.syn{background:#fff!important;color:#111!important}pre.cli.syn i{color:#c0170f}
.clih{color:#fff!important;font:900 italic clamp(11px,.85vw,16px)/1 var(--fd)!important;text-transform:uppercase;text-shadow:2px 2px 0 #111;letter-spacing:.04em}
.ptpic{background:#fff;border:4px solid #111;border-radius:14px;box-shadow:6px 6px 0 #111}
.ptpic img{background:transparent;padding:0}
.ptcap{color:#111}
.ptbleed img{border-radius:14px;border:5px solid #111;box-shadow:10px 10px 0 #111}
.scene .figwrap{background:#fff6b8;border:4px solid #111;border-radius:14px;box-shadow:6px 6px 0 #111}
.scbar{background:#e2241e!important;border:4px solid #111!important;border-radius:12px!important}
.scbar .cap{color:#fff!important;font-weight:800}.scbar .cap b{color:#ffe21a!important}.scbar .pos{color:#ffe21a!important}
.scbar button{border-radius:8px!important;background:#ffd21a!important;color:#111!important;border:3px solid #111!important;font-weight:900}
.q{padding:14px 16px!important}
.q .qt{color:#111!important;font-weight:900}
.opts button{border-radius:10px!important;background:#fff!important;color:#111!important;border:3px solid #111!important;font-weight:800;box-shadow:2px 2px 0 #111}
.opts button:hover{background:#fff08a!important}
.opts button.good{background:#c8f5a8!important}.opts button.bad{background:#ffc0b8!important}
.ex{color:#111!important;border-left-color:#e2241e!important;font-weight:700}
.score{color:#111!important}
.inrow input{border-radius:8px!important;background:#fff!important;color:#111!important;border:3px solid #111!important}
.inrow button{border-radius:8px!important;background:#e2241e!important;color:#ffe21a!important;border:3px solid #111!important;font-weight:900;box-shadow:2px 2px 0 #111}
.inrow button.sec{background:#fff!important;color:#111!important}
.note{color:#111!important;font-weight:700}.note b.ok{color:#1f7a14!important}.note b.no{color:#c0170f!important}
.srt{background:#fff6b8;border:4px solid #111;border-radius:14px;padding:14px 16px;box-shadow:6px 6px 0 #111;color:#111}
.srt-pool{color:#7a6a20}.srt-bin{background:#fff;border:3px dashed #111}.srt-h{color:#c0170f}
.srt-it{background:#fff;border:3px solid #111;color:#111;box-shadow:2px 2px 0 #111}
.cover{flex:0 1 auto;margin:auto;align-items:center;text-align:center;max-width:min(1100px,86vw);background:#fff6b8;border:6px solid #111;border-radius:18px;
 box-shadow:12px 12px 0 #111;padding:34px 44px;transform:rotate(-1deg)}
.cover .big{font-family:var(--fd)!important;font-style:italic;font-weight:900;text-transform:uppercase!important;color:#ffe21a!important;
 font-size:clamp(34px,5.2vw,96px)!important;line-height:1!important;-webkit-text-stroke:3px #111;paint-order:stroke fill;text-shadow:7px 7px 0 #e2241e!important}
.cover .big em{font-style:italic;color:#7fe03a!important}
.cover .lead{color:#111!important;font-weight:800}
#hud{background:#111!important;border-top:4px solid #ffd21a!important}
#hud button{border-radius:8px!important;background:#ffd21a!important;color:#111!important;border:2px solid #111!important;font-weight:900}
#hud #count{color:#ffd21a!important}#hud #sname{color:#fff!important}
#prog{background:#e2241e!important;box-shadow:none!important}
#toc{background:rgba(15,110,104,.97)!important}
#toc h2{color:#ffe21a!important;font-family:var(--fd)!important;font-style:italic}
.tocit{border-radius:10px!important;background:#fff6b8!important;color:#111!important;border:3px solid #111!important;font-weight:800}
.tocit i{color:#e2241e!important}
.cs-side{background:#fff6b8!important;border:4px solid #111!important;outline:0!important;border-radius:14px!important;box-shadow:6px 6px 0 #111!important}
.cs-h{color:#c0170f!important;font-family:var(--fd)!important;font-style:italic}
.cs-task{color:#111!important;font-weight:800}.cs-task b{color:#c0170f!important;background:#fff}
.cs-btns button{border-radius:8px!important;background:#ffd21a!important;color:#111!important;border:3px solid #111!important;box-shadow:2px 2px 0 #111}
.cs-btns button.alt{background:#a6e07a!important}.cs-btns button.sec{background:#fff!important}
.cs-res .ok{color:#1f7a14!important}.cs-res .no{color:#c0170f!important}
.cs-term{border:4px solid #111!important;outline:0!important;border-radius:12px!important;overflow:hidden;box-shadow:6px 6px 0 #111!important}
.cs-bar{background:#e2241e!important}
"""
