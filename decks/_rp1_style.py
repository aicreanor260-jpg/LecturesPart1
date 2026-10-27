# -*- coding: utf-8 -*-
"""Тема деки RIP 2.5.1 под инфографики автора: светлый мятный фон с листвой, белые панели,
тёмно-зелёные заголовки Unbounded, бирюзовые акценты, пастельные розовый и сиреневый."""


BG = """<svg id="rpbg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>
<radialGradient id="rpbgA" cx="25%" cy="20%" r="80%"><stop offset="0" stop-color="#f7fdf9"/><stop offset=".6" stop-color="#e3f6ec"/><stop offset="1" stop-color="#cdeedd"/></radialGradient>
<radialGradient id="rpglo" r=".5"><stop offset="0" stop-color="#bdf0da" stop-opacity=".9"/><stop offset="1" stop-color="#bdf0da" stop-opacity="0"/></radialGradient>
<radialGradient id="rpglo2" r=".5"><stop offset="0" stop-color="#ffd9e6" stop-opacity=".55"/><stop offset="1" stop-color="#ffd9e6" stop-opacity="0"/></radialGradient>
<path id="rpleaf" d="M0 0 C 30 -40 90 -50 130 -20 C 90 10 40 20 0 0 Z"/>
<g id="rpspray"><path d="M0 0 C 40 -80 70 -170 60 -260" fill="none" stroke="#3aa57f" stroke-width="4" stroke-linecap="round"/>
<use href="#rpleaf" transform="translate(14 -40) rotate(-60) scale(.8)" fill="#5cc49b"/><use href="#rpleaf" transform="translate(30 -80) rotate(-140) scale(.75)" fill="#3fae86"/>
<use href="#rpleaf" transform="translate(48 -130) rotate(-50) scale(.7)" fill="#7ad6b0"/><use href="#rpleaf" transform="translate(56 -175) rotate(-150) scale(.6)" fill="#4cbb92"/>
<use href="#rpleaf" transform="translate(60 -225) rotate(-75) scale(.55)" fill="#8fe0bf"/></g></defs>
<rect width="1600" height="900" fill="url(#rpbgA)"/><circle cx="1250" cy="380" r="520" fill="url(#rpglo)"/><circle cx="180" cy="820" r="380" fill="url(#rpglo2)"/>
<g opacity=".07" stroke="#0f5c47"><path d="M0 120H1600M0 300H1600M0 480H1600M0 660H1600M200 0V900M500 0V900M800 0V900M1100 0V900M1400 0V900"/></g>
<path d="M0 790 C 300 720 520 760 760 800 S 1250 740 1600 770 V900 H0Z" fill="#bfe9d4"/><path d="M0 840 C 260 800 600 830 900 860 S 1400 820 1600 835 V900 H0Z" fill="#a8dfc4"/>
<use href="#rpspray" transform="translate(30 905) scale(.85)"/><use href="#rpspray" transform="translate(90 905) scale(-.6 .6)"/>
<use href="#rpspray" transform="translate(1570 905) scale(-.85 .85)"/><use href="#rpspray" transform="translate(1500 905) scale(.6)"/></svg>"""


def css():
    return r"""
:root{--bg0:#e9f7f0;--cy:#2bb38a;--cy2:#0f5c47;--mg:#c2588f;--mg2:#d77aa8;--lm:#2f9d4f;--am:#c98a00;--rd:#d6336c;
 --ink:#123d33;--soft:#3d6b5f;--dim:#6c8d83;--line:rgba(43,179,138,.35);
 --panel:rgba(255,255,255,.66);--fd:"Unbounded","Golos Text",sans-serif;--r:24px;--r2:16px}
body{background:#e9f7f0;color:var(--ink)}
#bg,#bgimg,#bgfx{display:none}
#rpbg{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.head{padding-left:0;margin-bottom:10px}.head::before{display:none}
.head .eb{font:800 clamp(11px,.85vw,15px)/1 "Golos Text",sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#2bb38a;margin-bottom:10px}
h1.t{font-family:var(--fd);font-weight:800;text-transform:none;color:#0f5c47;text-shadow:none;letter-spacing:-.01em;
 font-size:clamp(22px,2.6vw,46px)!important;line-height:1.08}
h1.t em,h1.t em.v{color:#0f5c47;font-style:normal;text-shadow:none}
p.sub{color:var(--soft);font-weight:500;font-size:clamp(14px,1.15vw,21px)}
.c,.q{background:var(--panel)!important;border:1.5px solid rgba(255,255,255,.95)!important;border-radius:var(--r);
 box-shadow:0 26px 50px -30px rgba(15,92,71,.4),inset 0 1px 0 #fff!important;backdrop-filter:blur(12px)}
.c::before{display:none}
.c.cy{border-color:#8fd3bf!important}.c.mg{border-color:#f0b6d2!important}.c.lm{border-color:#9fdcae!important}
.c.am{border-color:#f2d27c!important}.c.rd{border-color:#f3a3bd!important}
.ch h3{font-family:var(--fd);font-weight:800;text-transform:none;color:#0f5c47}
.c p,ul.li li,.ir span:last-child{color:var(--ink)!important}
.c p b,.c li b,.ir b{color:#0f3d30}
ul.li li::before{background:var(--cy);box-shadow:none;border-radius:50%;transform:none}
ul.li.mg li::before{background:var(--mg)}ul.li.lm li::before{background:var(--lm)}
.tag{background:#e3f6ee;border-color:#8fd3bf;color:#16775f}
.tag.v{background:#f9e3ef;border-color:#f0b6d2;color:#a53d74}.tag.g{background:#e6f6e1;border-color:#9fdcae;color:#2b7a3d}
.tag.y{background:#fff3cf;border-color:#f2d27c;color:#8a6300}.tag.r{background:#ffe2ea;border-color:#f3a3bd;color:#a8264f}
.foot{background:#e3f6ee;border-color:#8fd3bf;color:var(--ink)}
.tw{background:#fff;border-color:#bfe6d6}.tw th{background:#dff3ec;color:#17463a;border-bottom-color:#8fd3bf}
.tw td{color:var(--ink);border-top-color:#d5eee5}
pre.cli{background:#0e231e;border-color:#2c8f80;color:#d7f5ea}
pre.cli .k{color:#9dff8a}pre.cli .p{color:#7fc7b6}
.clih{color:#1d6b4a}
.mt-t,.fl-edge{color:var(--ink)}
.pic{border:2px solid #bfe6d6;box-shadow:0 10px 30px rgba(30,100,80,.18);background:#fff}
.pic img{background:#fff}
.rppanel,.scene .figwrap{background:rgba(255,255,255,.66);border:1.5px solid rgba(255,255,255,.95);border-radius:var(--r);padding:10px;
 box-shadow:0 26px 50px -30px rgba(15,92,71,.4);backdrop-filter:blur(12px)}
.scene .figwrap .rppanel{border:0;box-shadow:none;padding:0;background:none}
svg.rpfig{max-height:62vh}
.g2 svg.rpfig,.g21 svg.rpfig,.g12 svg.rpfig{max-height:60vh}
.scbar{background:rgba(255,255,255,.92);border:2px solid #bfe6d6}
.scbar button{background:linear-gradient(160deg,#4fc3a6,#1f9a7e);color:#fff;box-shadow:none}
.scbar button.sec{background:#e3f6ee;color:#16775f;border:1px solid #8fd3bf}
.scbar .pos,.scbar .cap b{color:#16775f}.scbar .cap{color:var(--ink)}
.dots i{background:#cfe9df}.dots i.on{background:var(--cy);box-shadow:none}
.opts button{background:#f3fbf7;border-color:#bfe6d6;color:var(--ink)}
.opts button:hover{background:#e3f6ee;color:#0f3d30;border-color:#1f9a7e}
.opts button.good{background:#dcf5e2;color:#14532d;border-color:#2f9d4f}
.opts button.bad{background:#ffe2ea;color:#7a1636;border-color:#d6336c}
.q .qt{color:#0f3d30}.ex,.note{color:var(--soft)}
.inrow input{background:#fff;color:#0f3d30;border-color:#8fd3bf}
.inrow button{background:linear-gradient(160deg,#4fc3a6,#1f9a7e);color:#fff}
.inrow button.sec{background:#e3f6ee;color:#16775f}
.score{color:#16775f}
.cover{align-items:flex-start;text-align:left;margin:auto 0 auto 3vw;flex:0 1 auto;background:rgba(255,255,255,.88);
 border:2px solid #bfe6d6;border-radius:24px;padding:34px 46px;box-shadow:0 18px 50px rgba(30,100,80,.22)}
.cover .big{font-family:var(--fd);font-weight:900;text-transform:none;color:#1d6b4a;text-shadow:none;font-size:clamp(40px,6vw,104px)}
.cover .big em{color:#2a9b6c;text-shadow:none}
.cover .lead{color:var(--soft)}.cover .meta,.cover .tags{justify-content:flex-start}
#hud{background:rgba(255,255,255,.72);border-top:1.5px solid rgba(255,255,255,.9);backdrop-filter:blur(12px)}
#hud button{background:#e3f6ee;border-color:#8fd3bf;color:#16775f}
#hud #count{color:#16775f}#hud #sname{color:var(--soft)}
#prog{background:linear-gradient(90deg,#4fc3a6,#d77aa8);box-shadow:none}
#toc{background:rgba(240,250,245,.97)}#toc h2{color:#1d6b4a;font-family:var(--fd)}
.tocit{background:#fff;border-color:#bfe6d6;color:var(--ink)}.tocit i{color:#1f9a7e}
.q .qt{font-size:clamp(15px,1.3vw,25px)!important}
.opts button{font-size:clamp(14px,1.15vw,22px)!important;padding:10px 14px}
.inrow input,.inrow button{font-size:clamp(14px,1.05vw,20px)!important}
.score{font-size:clamp(14px,1.1vw,20px)}
.rp32{grid-template-columns:3fr 2fr}
.rp32 svg.rpfig{max-height:64vh}
/* формат RIPv2 */
.rpfmt{background:#fff;border:2px solid #bfe6d6;border-radius:14px;padding:10px 14px}
.rpbits{display:grid;grid-template-columns:1fr 1fr 2fr;font:800 clamp(13px,1vw,19px)/1.4 var(--m);color:#17463a}
.rpbits span:last-child{text-align:right}.rpbits span:nth-child(3){grid-column:3}
.rpbits{grid-template-columns:repeat(4,1fr)}
.rprow{display:grid;grid-template-columns:repeat(4,1fr)}
.rpf{border:2px solid #17463a;margin:-1px;text-align:center;padding:7px 4px;font:800 clamp(13px,1.05vw,20px)/1.2 var(--f);color:#17463a}
.rpf-h,.rps.h{background:#ffe7c9}.rpf-a,.rps.a{background:#f9d3da}.rpf-r,.rps.r{background:#d8e7fb}
.rpstrip{display:grid;grid-template-columns:repeat(12,1fr);margin-top:10px}
.rps{border:1.5px solid #17463a;margin:-.75px;text-align:center;padding:4px 2px;font:700 clamp(10px,.72vw,14px)/1.2 var(--f);color:#17463a}
/* тренажёр CLI в светлой теме */
.th-rp1 .cs-side{background:#fff;border:2px solid #bfe6d6;outline:0;border-radius:16px;box-shadow:0 8px 24px rgba(30,100,80,.12)}
.th-rp1 .cs-h{color:#1d6b4a}.th-rp1 .cs-task{color:var(--ink)}.th-rp1 .cs-task b{color:#16775f}
.th-rp1 .cs-btns button{border:2px solid #16775f;border-radius:10px;background:#1f9a7e;color:#fff;box-shadow:none}
.th-rp1 .cs-btns button.alt{background:#f9e3ef;color:#a53d74;border-color:#d77aa8}
.th-rp1 .cs-btns button.sec{background:#e3f6ee;color:#16775f}
.th-rp1 .cs-res .ok{color:#1d7a3a}.th-rp1 .cs-res .no{color:#c0264f}.th-rp1 .cs-res .exp{color:#a06a00}
.th-rp1 .cs-term{border:2px solid #2c8f80;outline:0;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(30,100,80,.18)}
"""


SPLIT = r"""
/* схема + текст pptx: схема слева сверху, под ней первая колонка текста, справа — остальные; без обрезки */
.sc:has(> .step svg.rpfig):has(> .g.grow){display:grid;grid-template-columns:minmax(0,57fr) minmax(0,43fr);
 grid-template-rows:auto auto minmax(0,1fr);column-gap:20px;row-gap:12px;overflow:hidden;align-content:start}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.head{grid-column:1/-1}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.step{grid-column:1;grid-row:2;min-height:0}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow{display:contents}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow>.col{display:flex;flex-direction:column;gap:12px;min-height:0}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow>.col:nth-child(1){grid-column:1;grid-row:3}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow>.col:nth-child(n+2){grid-column:2;grid-row:2/4}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow>.col:nth-child(3){grid-row:3/4}
.sc:has(> .step svg.rpfig):has(> .g.grow)>.g.grow>.col:nth-child(2):not(:last-child){grid-row:2/3}
.sc:has(> .step svg.rpfig):has(> .g.grow) svg.rpfig{max-height:52vh}
.sc:has(> .step svg.rpfig):has(> .g3.grow) svg.rpfig{max-height:40vh}
.th-rp1 .c p,.th-rp1 ul.li li,.th-rp1 .ir span{font-size:clamp(13px,1.08vw,20px)!important;line-height:1.45}
.th-rp1 .ch h3{font-size:clamp(14px,1.2vw,22px)!important;line-height:1.15}
.th-rp1 pre.cli{font-size:clamp(11px,.92vw,17px)!important;line-height:1.45}
.th-rp1 .c{padding:clamp(10px,1vw,18px) clamp(12px,1.2vw,22px)}
.c p b,.c li b{color:#0f5c47}
.th-rp1 .sc>.g.grow{align-content:center}
.th-rp1 .sc:has(.clisim)>.g.grow,.th-rp1 .sc:has(.clisim){align-content:stretch}
"""
