# -*- coding: utf-8 -*-
"""Тема деки MPLS 2.9 — как инфографики комплекта: голубое небо Гибли, кремовые панели с синей рамкой,
белые заголовки с синей обводкой, оранжевые метки."""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@600;700;800;900&'
         'family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap">')


def css(bg, cover):
    return r"""
:root{--fd:"Rubik","Arial Black",sans-serif;
--ink:#1d2a44;--soft:#3e5175;--dim:#5d6f90;--cy:#1f63c6;--cy2:#2f7be0;--mg:#e8742c;--mg2:#f29a55;
--lm:#2f9e5b;--am:#d99a0b;--rd:#d9363e;--line:#1f63c6;--panel:rgba(255,250,238,.96);--r:14px;--r2:10px}
body{background:#4aa8f0;color:var(--ink)}
#bg{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%s)}
#bgfx{background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(20,70,140,.10))!important}
#bgfx::after{display:none}
.head{padding-left:0}.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:900;text-transform:none;color:#fff;letter-spacing:0;line-height:1.08;
 font-size:clamp(22px,2.5vw,46px);
 text-shadow:0 3px 0 #1550a8,3px 0 0 #1550a8,-3px 0 0 #1550a8,0 -3px 0 #1550a8,2px 2px 0 #1550a8,-2px 2px 0 #1550a8,
 2px -2px 0 #1550a8,-2px -2px 0 #1550a8,0 7px 14px rgba(10,40,90,.35)}
h1.t em,h1.t em.v{color:#ffe38a;text-shadow:inherit}
p.sub{display:inline-block;background:rgba(255,250,238,.94);color:var(--ink);padding:5px 14px;border-radius:999px;
 border:2px solid #1f63c6;margin-top:10px}
.c,.q{background:var(--panel)!important;border:2.5px solid #1f63c6!important;border-radius:14px!important;color:var(--ink);
 box-shadow:0 6px 0 rgba(21,80,168,.25),0 10px 26px rgba(10,40,90,.18)!important}
.c::before{display:none}
.c.am{border-color:#e8742c!important}.c.lm{border-color:#2f9e5b!important}.c.rd{border-color:#d9363e!important}
.c.mg{border-color:#e8742c!important}
.c p,.c li,ul.li li{color:var(--ink)}
.c p b,.c li b,.ir b,.c b{color:#123a7a!important}
.mpfs{display:contents}
.tw.mt td,.tw.mt th,.tw td,.tw th{font-family:"Golos Text",sans-serif!important}
.tw table{font-size:clamp(13px,1.08vw,21px)!important}
.mpfr{display:flex;align-items:center;justify-content:center;gap:10px;margin:6px 0;font:700 clamp(15px,1.3vw,26px)/1.2 "Golos Text",sans-serif;color:var(--ink)}
.mpfr i{font-family:Georgia,serif}
.mpfr .fr{display:inline-flex;flex-direction:column;text-align:center}
.mpfr .fr span:first-child{border-bottom:2px solid var(--ink);padding:0 6px}
.mpformula{align-items:center}
.mpfs1 .c p,.mpfs1 ul.li li{font-size:clamp(17px,1.85vw,36px)!important}
.mpfs2 .c p,.mpfs2 ul.li li{font-size:clamp(16px,1.55vw,30px)!important}
.mpfs3 .c p,.mpfs3 ul.li li{font-size:clamp(14px,1.3vw,26px)!important}
.mpfs4 .c p,.mpfs4 ul.li li{font-size:clamp(13px,1.12vw,22px)!important;line-height:1.36}
.ch h3{font-family:var(--fd);font-weight:800;text-transform:none;color:#fff;background:#1f63c6;padding:4px 12px;border-radius:8px}
.tw{background:rgba(255,255,255,.97);border:2.5px solid #1f63c6;border-radius:12px;overflow:hidden}
.tw table{color:var(--ink);border-collapse:collapse;width:100%%}
.tw th{background:#1f63c6!important;color:#fff!important;text-align:left;padding:7px 10px}
.tw td{border-top:1px solid #c9d8ef;padding:7px 10px;color:var(--ink)}
.tw tr:nth-child(even) td{background:#f3f8ff}
.tw b{color:#123a7a}
.mt-t{color:#fff!important;background:#1f63c6;display:inline-block;padding:3px 10px;border-radius:8px 8px 0 0;margin-top:6px}
.mt-n{color:var(--ink)!important;background:rgba(255,250,238,.94);border-radius:8px;padding:5px 10px}
.mtgrid{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px}
.mtgrid .tw table{font-size:clamp(10px,.74vw,14px)!important;table-layout:fixed}
.mtgrid .tw th,.mtgrid .tw td{padding:3px 5px!important;word-break:break-word}
.figwrap.mppanel,.scene .figwrap{background:linear-gradient(180deg,#fffaf0,#fff3dc);border:2.5px solid #1f63c6;
 border-radius:14px;padding:8px;box-shadow:0 6px 0 rgba(21,80,168,.25)}
svg.mpfig{width:100%%;height:auto;display:block}
svg.mpfig text{font-family:"Golos Text",sans-serif}
.scbar{background:rgba(255,250,238,.97)!important;border:2.5px solid #1f63c6!important;border-radius:12px!important;color:var(--ink)}
.scbar button{background:#1f63c6!important;color:#fff!important;border:0!important}
.scbar button.sec{background:#e8742c!important}
.scbar .cap b,.scbar .pos{color:var(--ink)!important}
.scbar .dots i{background:#c9d8ef}.scbar .dots i.on{background:#e8742c}
.pic.mppic{border:3px solid #fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 0 rgba(21,80,168,.3),0 14px 30px rgba(10,40,90,.3);
 align-self:center;max-height:100%%;display:flex}
.pic.mppic img{display:block;max-height:calc(100vh - 190px);width:auto;max-width:100%%;object-fit:contain;margin:auto}
ul.li li::marker,ul.li li::before{color:#e8742c}
ul.li.nb li::before{display:none!important}
ul.li.nb li{padding-left:0!important}
.foot{background:rgba(255,250,238,.96)!important;border:2px solid #1f63c6!important;color:var(--ink)!important;border-radius:12px}
.foot i{background:#e8742c!important;color:#fff!important}
.cover{background:rgba(255,250,238,.93);border:3px solid #1f63c6;border-radius:22px;padding:32px 44px;
 box-shadow:0 8px 0 rgba(21,80,168,.3);max-width:860px;margin:auto 0 auto 3vw;flex:0 1 auto}
.cover .big{font-family:var(--fd);font-weight:900;color:#1f63c6;text-transform:none;text-shadow:none;line-height:1}
.cover .big em{color:#e8742c;font-style:normal}
.cover .lead{color:var(--ink)}
.tag{background:#1f63c6!important;color:#fff!important;border:0!important}
.tag.v{background:#e8742c!important}.tag.g{background:#2f9e5b!important}.tag.y{background:#d99a0b!important}
.q .qt{color:var(--ink)}
.opts button,.inrow button{background:#fff;color:var(--ink);border:2px solid #1f63c6}
.opts button.good{background:#d6f3e0!important;border-color:#2f9e5b!important}
.opts button.bad{background:#ffe0e0!important;border-color:#d9363e!important}
.inrow input{background:#fff;color:var(--ink);border:2px solid #1f63c6}
.ex,.note{color:var(--ink)!important}
#hud{background:rgba(255,250,238,.96)!important;border-top:2.5px solid #1f63c6;color:var(--ink)}
#hud button{background:#1f63c6!important;color:#fff!important;border:0!important}
#hud .hint,#hud #count,#hud #sname{color:var(--ink)!important}
#toc{background:rgba(232,243,255,.98)!important;color:var(--ink)}
#toc h2,.tocit{color:var(--ink)!important}
.tocit{background:#fff!important;border:1.5px solid #1f63c6!important}
#prog{background:#e8742c!important}
""" % (bg, cover)
