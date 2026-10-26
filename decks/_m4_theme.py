# -*- coding: utf-8 -*-
"""Тема деки 2.4 «Маршрутизация»: изумрудная ночь и золото — как инфографики комплекта «Маршрутизатор 2.4»."""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Playfair+Display:wght@700;800;900&family=Golos+Text:wght@400;600;700;800&'
         'family=JetBrains+Mono:wght@400;700&display=swap">')

# цвета движка коммутации (неон) → золото/изумруд деки
HUES = [(170, 215, 44, .85), (216, 262, 160, .8), (263, 320, 12, .9)]


def css(bg, cover):
    return r"""
:root{
--bg0:#04110c;--bg1:#071a13;--bg2:#0b2a20;
--cy:#f0c75e;--cy2:#ffe39a;--cyd:#8a6a1e;
--mg:#3fd6b0;--mg2:#8ff0d4;
--lm:#9be37a;--am:#f0c75e;--rd:#ff7a5c;--or:#ffae5c;
--ink:#fbf3dc;--soft:#d6cfae;--dim:#a39c7d;
--line:rgba(240,199,94,.32);
--panel:linear-gradient(160deg,rgba(10,44,33,.86),rgba(4,22,16,.92));
--r:14px;--r2:10px;
--fd:"Playfair Display",Georgia,serif;
--gold:linear-gradient(180deg,#fff2c2 0%,#f0c75e 45%,#b8862a 100%);
}
body{background:#04110c}
#bg{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(@BG@) center bottom/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(@CV@)}
#bgfx{background:linear-gradient(180deg,rgba(4,17,12,.15),rgba(4,17,12,.45))!important}
#bgfx::after{display:none}
.head{padding-left:0}
.head::before{display:none}
h1.t{font-family:var(--fd);font-weight:900;text-transform:uppercase;letter-spacing:.02em;line-height:1.08;
 background:var(--gold);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 2px 0 rgba(0,0,0,.6)) drop-shadow(0 0 18px rgba(240,199,94,.35));text-shadow:none}
h1.t em,h1.t em.v{font-style:normal;background:linear-gradient(180deg,#d9fff2,#3fd6b0);-webkit-background-clip:text;
 background-clip:text;color:transparent;text-shadow:none}
.head::after{content:"";display:block;width:min(420px,40%);height:2px;margin-top:8px;
 background:linear-gradient(90deg,#f0c75e,rgba(240,199,94,0))}
p.sub{color:var(--soft)}
.c,.q{background:var(--panel)!important;border:1.5px solid rgba(240,199,94,.55)!important;border-radius:12px;
 box-shadow:0 0 0 1px rgba(0,0,0,.4),0 10px 30px rgba(0,0,0,.45),inset 0 0 24px rgba(240,199,94,.06)!important}
.c::before{display:none}
.ch h3{font-family:var(--fd);font-weight:800;color:var(--cy2);letter-spacing:.01em}
.c b,.q b{color:var(--cy2)}
.tw table th{background:rgba(240,199,94,.16)!important;color:var(--cy2)!important}
.tw{border-color:rgba(240,199,94,.4)!important}
pre.cli{background:rgba(2,12,9,.92)!important;border:1.5px solid rgba(240,199,94,.45)!important}
pre.cli .p{color:#8fa89a}pre.cli .k{color:#ffe39a}
.cover{align-items:flex-start}
.cover .big{font-family:var(--fd);font-weight:900;text-transform:uppercase;background:var(--gold);-webkit-background-clip:text;
 background-clip:text;color:transparent;filter:drop-shadow(0 3px 0 rgba(0,0,0,.6)) drop-shadow(0 0 30px rgba(240,199,94,.35))}
.cover .big em{font-style:normal;background:linear-gradient(180deg,#d9fff2,#3fd6b0);-webkit-background-clip:text;background-clip:text;color:transparent}
#hud{background:linear-gradient(0deg,rgba(4,17,12,.97),rgba(4,17,12,.7))}
#toc{background:rgba(4,17,12,.97)}
#prog{background:linear-gradient(90deg,#b8862a,#ffe39a)!important}
.scene .figwrap,.figwrap.m4p{background:linear-gradient(160deg,rgba(9,40,30,.9),rgba(3,18,13,.94));
 border:1.5px solid rgba(240,199,94,.55);border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.45);padding:8px}
.scbar{border:1.5px solid rgba(240,199,94,.5)!important;background:rgba(4,22,16,.94)!important;border-radius:10px}
svg.m4 text{font-family:"Golos Text",sans-serif}
.dkrep .repc{background:none!important;border-radius:10px!important;box-shadow:0 10px 30px rgba(0,0,0,.5)!important}
.frm span{border-color:#2a1e06!important;box-shadow:0 0 0 1px rgba(240,199,94,.5),3px 3px 0 rgba(0,0,0,.45)}
.fl-dev{background:rgba(255,248,226,.96)!important;border-color:#8a6a1e!important;box-shadow:0 0 14px rgba(240,199,94,.35)!important}
.fl-edge i{color:var(--cy)}
.m4tbl td.hl,.m4tbl tr.hl td{background:rgba(240,199,94,.22)!important;color:#fff}
.m4row{display:flex;gap:12px;align-items:stretch}.m4row>*{flex:1 1 0;min-width:0}
.m4note{font:600 clamp(12px,.95vw,18px)/1.4 var(--f);color:var(--soft)}
.cs-side,.cs-term{border:1.5px solid rgba(240,199,94,.55)!important;outline:0!important;border-radius:12px}
.cs-btns button{border:2px solid #2a1e06!important;border-radius:8px;background:var(--cy)}
.ct textarea{border-color:var(--cy)}
""".replace("@BG@", bg).replace("@CV@", cover)

EXTRA = r"""
.m4tree{display:flex;flex-direction:column;align-items:center;gap:2px;font:700 clamp(12px,1vw,19px)/1.3 var(--f)}
.m4tree i{font-style:normal;color:var(--cy);font-size:20px;line-height:1}
.m4tree b{color:var(--cy2);font-size:.85em}
.m4n{padding:9px 14px;border:1.5px solid rgba(240,199,94,.6);border-radius:10px;background:rgba(4,22,16,.92);text-align:center;max-width:420px}
.m4n.q{border-radius:40px;border-color:var(--mg);color:var(--mg2)}
.m4n.rd{border-color:var(--rd);color:#ffb3a3}
.m4br{display:flex;gap:16px;justify-content:center;align-items:flex-start;width:100%}
.m4br>div{display:flex;flex-direction:column;align-items:center;gap:2px;flex:1 1 0;min-width:0}
"""

EXTRA += r"""
.slide>.sc{padding-top:10px}
h1.t{padding:4px 0 2px;font-size:clamp(20px,2.3vw,44px)!important}
.c p,ul.li li,ol.li li{font-size:clamp(14px,1.36vw,27px)!important;line-height:1.38}
ol.li{padding-left:1.4em;display:flex;flex-direction:column;gap:6px}
.tw table{font-size:clamp(14px,1.2vw,23px)!important}
pre.cli{font-size:clamp(12px,1.05vw,20px)!important}
.figwrap.m4p svg,.scene .figwrap svg{width:100%;height:auto;max-height:64vh}
"""

EXTRA += r"""
.head{margin-top:10px}
h1.t{line-height:1.25!important;overflow:visible}
.th-m4 .g2{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
.th-m4 .g12{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
"""

EXTRA += r"""
.mt-t{font-size:clamp(14px,1.15vw,22px)!important;color:var(--cy2)!important}
.m4tbl td,.m4tbl th{padding:6px 10px!important}
"""

EXTRA += r"""
pre.cli.term{font-size:clamp(10px,.82vw,16px)!important;overflow-x:auto;white-space:pre}
"""

EXTRA += r"""
pre.cli.term.wide{font-size:clamp(10px,.9vw,18px)!important}
"""
