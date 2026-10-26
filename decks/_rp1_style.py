# -*- coding: utf-8 -*-
"""Тема деки RIP 2.5.1 под инфографики автора: светлый мятный фон с листвой, белые панели,
тёмно-зелёные заголовки Unbounded, бирюзовые акценты, пастельные розовый и сиреневый."""


def css(bg, cover):
    return r"""
:root{--bg0:#eef8f3;--cy:#1f9a7e;--cy2:#16775f;--mg:#c2588f;--mg2:#d77aa8;--lm:#2f9d4f;--am:#c98a00;--rd:#d6336c;
 --ink:#17463a;--soft:#2f5a4e;--dim:#6c8d83;--line:rgba(31,154,126,.35);
 --panel:rgba(255,255,255,.90);--fd:"Unbounded","Golos Text",sans-serif;--r:18px;--r2:12px}
body{background:#eef8f3;color:var(--ink)}
#bg{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(@@BG@@) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(@@CV@@)}
#bgfx{background:linear-gradient(180deg,rgba(255,255,255,.25),rgba(232,248,240,.35))!important}
#bgfx::after{display:none}
.head{padding-left:0}.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:900;text-transform:none;color:#1d6b4a;text-shadow:none;letter-spacing:-.01em;
 font-size:clamp(20px,2.3vw,42px)!important;line-height:1.1}
h1.t em,h1.t em.v{color:#2a9b6c;text-shadow:none}
p.sub{color:var(--soft);font-weight:700}
.c,.q{background:var(--panel)!important;border:2px solid #bfe6d6!important;border-radius:var(--r);
 box-shadow:0 8px 24px rgba(30,100,80,.12)!important}
.c::before{display:none}
.c.cy{border-color:#8fd3bf!important}.c.mg{border-color:#f0b6d2!important}.c.lm{border-color:#9fdcae!important}
.c.am{border-color:#f2d27c!important}.c.rd{border-color:#f3a3bd!important}
.ch h3{font-family:var(--fd);font-weight:800;text-transform:none;color:#1d6b4a}
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
.rppanel,.scene .figwrap{background:rgba(255,255,255,.92);border:2px solid #bfe6d6;border-radius:var(--r);padding:8px;
 box-shadow:0 8px 24px rgba(30,100,80,.12)}
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
#hud{background:rgba(255,255,255,.94);border-top:2px solid #bfe6d6}
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
""".replace("@@BG@@", bg).replace("@@CV@@", cover)
