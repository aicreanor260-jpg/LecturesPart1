# -*- coding: utf-8 -*-
"""Тема деки «OSPF 2.5 (по pptx)»: светлый кавай как на инфографиках автора — облачный фон, белые карточки
с розово-голубой обводкой, заголовки сжатым сверхжирным гротеском с розовым акцентом."""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&'
         'family=Golos+Text:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap">')


def css(bg, cover):
    return r"""
:root{--cy:#2f8fe8;--cy2:#1f6fd0;--cyd:#9fd0ff;--mg:#ff4f9a;--mg2:#ff86bb;--lm:#2fae6a;--am:#e8a400;--rd:#ff4f6a;--or:#ff8a3d;
 --ink:#1f1a33;--soft:#5a5374;--dim:#8a84a2;--line:rgba(255,79,154,.28);
 --panel:rgba(255,255,255,.93);--fd:"Oswald","Arial Narrow",sans-serif;--r:20px;--r2:14px}
body{background:#fdf3f8;color:var(--ink)}
#bg{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%s)}
#bgfx{background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,.55))!important}
#bgfx::after{display:none}
.head{padding-left:0}.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:700;color:#14101f;text-shadow:none;letter-spacing:-.005em;line-height:.95;
 font-size:clamp(24px,3vw,54px)}
h1.t em,h1.t em.v{color:var(--mg);text-shadow:none}
p.sub{color:var(--soft)}
.c,.q{background:var(--panel)!important;border:2.5px solid #ffc2dc!important;border-radius:20px!important;
 box-shadow:0 6px 0 rgba(255,79,154,.18),0 10px 26px rgba(120,80,160,.12)!important;color:var(--ink)}
.c.cy{border-color:#b9dcff!important;box-shadow:0 6px 0 rgba(47,143,232,.18),0 10px 26px rgba(80,120,160,.12)!important}
.c.lm{border-color:#bfe9cf!important}.c.am{border-color:#ffe2a0!important}.c.rd{border-color:#ffb3c0!important}
.c::before{display:none}
.c p,.c li{color:var(--ink)}
.c b,.c strong,.c p b,.c li b,.foot b,.q b{color:#d6337d!important;font-weight:800}
.c.cy b,.c.cy p b,.c.cy li b{color:var(--cy2)!important}
.c p,ul.li li{font-size:clamp(15px,1.42vw,28px)!important;line-height:1.4}
ul.li li::before{background:var(--mg)!important}
.foot span{color:var(--ink)}
.ch h3{font-family:var(--fd);font-weight:700;color:#14101f;letter-spacing:.01em}
.num{background:var(--mg)!important;color:#fff!important;box-shadow:none!important}
.tag{background:#fff;color:var(--ink);border:2px solid #ffc2dc}
.foot{background:rgba(255,255,255,.92);color:var(--ink);border:2px solid #ffe2a0;border-radius:16px}
.foot i{background:#ffd23a;color:#14101f}
.tw table{color:var(--ink)}.tw th{background:#ffe3f0;color:#14101f}.tw td{border-color:#f3d6e6}
.tw{background:#fff;border:2px solid #ffc2dc;border-radius:14px}
pre.cli{background:#1d1b2b;color:#f2f2f2;border:2px solid #ffc2dc;border-radius:14px}
pre.cli .p{color:#9a93b8}pre.cli .k{color:#ffd1e6;font-weight:700}
.clih{color:var(--soft)}
.pic{border:3px solid #fff;border-radius:18px;box-shadow:0 8px 26px rgba(120,80,160,.18)}
.dkrep .repc,.o5rep .repc{background:none!important;border-radius:18px!important;box-shadow:0 8px 30px rgba(120,80,160,.22)!important;color:#1f1a33}
.dkrep .repc img,.o5rep .repc img{-webkit-mask:none!important;mask:none!important}
.figwrap.o5panel,.scene .figwrap{background:rgba(255,255,255,.95);border:2.5px solid #ffc2dc;border-radius:20px;padding:10px;
 box-shadow:0 6px 0 rgba(255,79,154,.16)}
svg.o5fig text{font-family:"Golos Text",sans-serif}
.scbar{background:rgba(255,255,255,.95)!important;border:2px solid #ffc2dc!important;border-radius:14px;color:var(--ink)}
.scbar .cap b{color:var(--ink)}
.opts button{background:#fff;color:var(--ink);border:2px solid #ffc2dc}
.inrow input{background:#fff;color:var(--ink);border:2px solid #b9dcff}
.inrow button,.scbar button{background:var(--mg);color:#fff;border:0}
.inrow button.sec,.scbar button.sec{background:#fff;color:var(--ink);border:2px solid #ffc2dc}
.ex,.note{color:var(--ink)}
.qt{color:var(--ink)!important;font-size:clamp(15px,1.3vw,25px)!important}
.opts button{font-size:clamp(14px,1.1vw,21px)!important}
.cover .big{font-family:var(--fd);color:#14101f;text-shadow:4px 4px 0 #ffc2dc}
.cover .big em{color:var(--mg)}
.cover{background:rgba(255,255,255,.86);border:3px solid #ffc2dc;border-radius:26px;padding:34px 46px;margin:auto 4vw auto auto;max-width:56vw}
.cover .lead{color:var(--ink)}
#hud{background:rgba(255,255,255,.94);color:var(--ink);border-top:2px solid #ffc2dc}
#hud button{color:var(--ink)}
#toc{background:rgba(255,250,253,.98);color:var(--ink)}
.tocit{color:var(--ink)}
/* тренажёр CLI на светлом фоне */
.clisim .cs-side{background:rgba(255,255,255,.95);border:2.5px solid #ffc2dc;outline:0;border-radius:18px}
.clisim .cs-term{border:2.5px solid #ffc2dc;outline:0;border-radius:18px;overflow:hidden}
.clisim .cs-btns button{border:0;border-radius:10px;background:var(--mg);color:#fff}
.clisim .cs-btns button.alt{background:#2fae6a}.clisim .cs-btns button.sec{background:#fff;color:var(--ink);border:2px solid #ffc2dc}
.clisim .cs-res .ok{color:#1f8a4c}.clisim .cs-res .no{color:#d6243f}.clisim .cs-res .exp{color:#a36b00}
.clisim .cs-task b{color:#d6337d}
""" % (bg, cover)
