# -*- coding: utf-8 -*-
"""Сборка деки «Списки контроля доступа (ACL)» строго по pptx «ACL» на движке коммутации:

    python _acl_build.py        → spiski-dostupa-acl.html

Стиль — ретро-окна инфографик автора (комплект «ACL»): бежевая бумага, окна с тёмно-бирюзовыми заголовками
и кнопками «_ □ ×», синие / красные / горчичные / зелёные шапки панелей, пиксельный шрифт заголовков.
Инфографики автора — во весь слайд сразу за своим слайдом pptx (как в деке ESR)."""
import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

OUT = "spiski-dostupa-acl.html"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&'
         'family=Golos+Text:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap">')


def b64(name):
    with open(os.path.join(HERE, "_acl_assets", name + ".webp"), "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


# три кнопки окна «_ □ ×» — как на инфографиках
WINBTN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 78 22'>"
          "<g fill='%23d9d2c0' stroke='%23111' stroke-width='2'><rect x='1' y='1' width='22' height='20'/>"
          "<rect x='28' y='1' width='22' height='20'/><rect x='55' y='1' width='22' height='20'/></g>"
          "<path d='M6 16h12' stroke='%23111' stroke-width='3'/><rect x='33' y='6' width='12' height='10' fill='none' stroke='%23111' stroke-width='2.5'/>"
          "<path d='M60 6l12 10M72 6L60 16' stroke='%23111' stroke-width='3'/></svg>")

THEME = r"""
:root{--bg0:#d6ccb2;--cy:#1f4a44;--cy2:#2e6b60;--mg:#a8473b;--mg2:#c0574a;--lm:#2f7a3a;--am:#b8933a;--rd:#a8473b;
 --ink:#1d1d1b;--soft:#2f2d27;--dim:#5e594b;--line:#1d1d1b;
 --panel:#faf3e0;--fd:"Press Start 2P","Golos Text",monospace;--f:"Golos Text","Segoe UI",sans-serif;--r:0px;--r2:0px}
body{background:#d6ccb2;color:var(--ink)}
#bg{display:none}#bgfx::after{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%(bg)s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%(cover)s)}
#bgfx{background:none!important}
/* ---- заголовок слайда: окно с тёмно-бирюзовой шапкой и кнопками ---- */
.head{padding-left:0}.head::before{display:none}
h1.t{display:inline-flex;align-items:center;gap:18px;font-family:var(--fd);font-weight:400;text-transform:none;letter-spacing:0;
 font-size:clamp(14px,1.55vw,29px)!important;line-height:1.35!important;color:#fff;text-shadow:3px 3px 0 #0d2622;
 background:#1f4a44;border:3px solid #1d1d1b;box-shadow:6px 6px 0 rgba(0,0,0,.5);padding:.55em .8em .5em}
h1.t::after{content:"";flex:none;width:78px;height:22px;background:url("%(btn)s") center/contain no-repeat}
h1.t em,h1.t em.v{font-style:normal;color:#ffd75e;text-shadow:3px 3px 0 #0d2622}
p.sub{display:inline-block;margin-top:10px;background:#faf3e0;color:#1d1d1b;border:3px solid #1d1d1b;box-shadow:4px 4px 0 rgba(0,0,0,.4);
 padding:6px 14px;font-weight:700}
/* ---- панели: ретро-окна ---- */
.c,.q{background:#faf3e0!important;border:3px solid #1d1d1b!important;border-radius:0!important;box-shadow:6px 6px 0 rgba(0,0,0,.45)!important}
.c::before{display:none}
.c{padding:0 0 14px!important}
.c>*{margin-left:clamp(12px,1.1vw,20px);margin-right:clamp(12px,1.1vw,20px)}
.c>:first-child{margin-top:14px}
.c>.ch{margin:0 0 12px!important;padding:7px 12px;background:#1f4a44;border-bottom:3px solid #1d1d1b;display:flex;align-items:center;gap:10px}
.c>.ch::after{content:"";margin-left:auto;flex:none;width:66px;height:19px;background:url("%(btn)s") center/contain no-repeat}
.c>.ch h3{color:#fff!important;font:900 clamp(14px,1.3vw,25px)/1.15 "Golos Text",sans-serif!important;text-transform:uppercase;letter-spacing:.03em}
.c.cy>.ch{background:#2a4f6d}.c.mg>.ch,.c.rd>.ch{background:#a8473b}.c.lm>.ch{background:#2f6b3f}
.c.am>.ch{background:#b8933a}.c.am>.ch h3{color:#1d1d1b!important}
.c.cy,.c.mg,.c.lm,.c.am,.c.rd{box-shadow:6px 6px 0 rgba(0,0,0,.45)!important;border-color:#1d1d1b!important}
.c p,ul.li li,.ir span{color:#26241e!important;font-size:calc(clamp(15px,1.42vw,28px)*var(--fz,1))!important;line-height:1.42}
.step>p,.col>p{font:600 calc(clamp(14px,1.25vw,24px)*var(--fz,1))/1.4 "Golos Text",sans-serif;color:#26241e;margin:0}
.step>p+p{margin-top:6px}
.c b,.c strong{color:#000!important}
.c p+p{margin-top:8px}
.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) .c p,.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) ul.li li{font-size:calc(clamp(17px,1.7vw,33px)*var(--fz,1))!important}
ul.li li::before{background:#1f4a44!important;box-shadow:2px 2px 0 rgba(0,0,0,.35)!important;border-radius:0;transform:none!important;width:10px!important;height:10px!important}
ul.li.mg li::before{background:#a8473b!important}ul.li.lm li::before{background:#2f6b3f!important}
.num{border-radius:0!important;background:#faf3e0!important;color:#1d1d1b!important;border:2px solid #1d1d1b;box-shadow:2px 2px 0 rgba(0,0,0,.4)!important;font-family:var(--fd)!important;font-size:12px!important}
.tag{border-radius:0!important;background:#fff!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 rgba(0,0,0,.35)}
.tag.v{background:#f3c9c0!important}.tag.g{background:#cfe8c4!important}.tag.y{background:#ffe7a0!important}.tag.r{background:#f3c9c0!important}
/* ---- сноски: горчичная плашка как внизу инфографик ---- */
.foot{border-radius:0!important;background:#e8b84a!important;color:#1d1d1b!important;border:3px solid #1d1d1b!important;box-shadow:5px 5px 0 rgba(0,0,0,.45);
 font-size:calc(clamp(15px,1.35vw,26px)*var(--fz,1))!important}
.foot i{border-radius:0!important;background:#faf3e0!important;color:#1d1d1b!important;border:2px solid #1d1d1b}
.foot.warn{background:#e9a091!important}.foot.ok{background:#b9dca8!important}.foot.note{background:#c9d6e6!important}
/* ---- таблицы ---- */
.tw{border-radius:0!important;border:3px solid #1d1d1b!important;box-shadow:5px 5px 0 rgba(0,0,0,.4);background:#fff!important}
.tw table{font-size:calc(clamp(14px,1.25vw,24px)*var(--fz,1))!important}
.tw th{background:#1f4a44!important;color:#fff!important;border-bottom:3px solid #1d1d1b!important}
.tw td{color:#1d1d1b!important;border-top:2px solid #d9cfb4!important}
.tw tr.hi td{background:#d7ecc9!important}.tw tr.hl td{background:#f6dcd5!important}
.tw td.pm{color:#2f6b3f!important;font-weight:800}.tw td.dn{color:#a8473b!important;font-weight:800}
/* ---- консоль: тёмный терминал ---- */
pre.cli{border-radius:0!important;background:#14201d!important;color:#e6f2d8!important;border:3px solid #1d1d1b!important;
 box-shadow:5px 5px 0 rgba(0,0,0,.45)!important;font-size:calc(clamp(13px,1.2vw,23px)*var(--fm,1))!important;white-space:pre;overflow-x:auto}
pre.cli.term{font-size:calc(clamp(12px,1.05vw,20px)*var(--fm,1))!important;white-space:pre;overflow-x:auto}
pre.cli.fitw{font-size:var(--pw)!important}
pre.cli.wrapw{white-space:pre-wrap!important;overflow-wrap:anywhere}
pre.cli .p{color:#8fb9a6!important}pre.cli .k{color:#ffe082!important;font-weight:700}
pre.cli .h{background:rgba(255,224,130,.28)}
pre.cli.syn{background:#fff!important;color:#1d1d1b!important}
pre.cli.syn i{color:#a8473b;font-style:italic}
.clih{color:#1d1d1b!important;font:900 clamp(11px,.85vw,16px)/1 "Golos Text",sans-serif!important;letter-spacing:.08em;text-transform:uppercase}
/* ---- сцены ---- */
.scene .figwrap,.figwrap.aclpanel{background:#faf3e0;border:3px solid #1d1d1b;box-shadow:6px 6px 0 rgba(0,0,0,.45);border-radius:0;padding:8px}
.scbar{background:#1f4a44!important;border:3px solid #1d1d1b!important;border-radius:0!important;box-shadow:5px 5px 0 rgba(0,0,0,.45)}
.scbar .cap{color:#fff!important;font-size:clamp(14px,1.25vw,24px)!important}.scbar .cap b{color:#ffd75e!important}
.scbar .pos{color:#ffd75e!important}
.scbar button{border-radius:0!important;background:#faf3e0!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 #000!important}
.scbar button.sec{background:#d9d2c0!important}
.dots i{border-radius:0!important;background:#5f8d84!important}.dots i.on{background:#ffd75e!important;box-shadow:none!important}
/* ---- тест и задачи ---- */
.q{padding:0 0 14px!important}
.q>*{margin-left:16px;margin-right:16px}
.q .qt{margin:0 0 12px!important;padding:9px 14px;background:#2a4f6d;color:#fff!important;border-bottom:3px solid #1d1d1b;
 font-size:calc(clamp(15px,1.35vw,26px)*var(--fz,1))!important;line-height:1.35}
.opts button{border-radius:0!important;background:#fff!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;
 box-shadow:2px 2px 0 rgba(0,0,0,.4);font-size:calc(clamp(14px,1.25vw,24px)*var(--fz,1))!important}
.opts button:hover{background:#fff3c4!important}
.opts button.good{background:#cfe8c4!important;border-color:#2f6b3f!important}.opts button.bad{background:#f3c9c0!important;border-color:#a8473b!important}
.ex{color:#26241e!important;border-left-color:#1f4a44!important;font-size:calc(clamp(13px,1.15vw,22px)*var(--fz,1))!important}
.score{color:#1d1d1b!important;font-family:var(--fd)!important;font-size:13px!important}
.inrow input{border-radius:0!important;background:#fff!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;font-size:calc(clamp(14px,1.2vw,23px)*var(--fz,1))!important}
.inrow button{border-radius:0!important;background:#1f4a44!important;color:#fff!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 #000;font-size:calc(clamp(12px,1vw,19px)*var(--fz,1))!important}
.inrow button.sec{background:#faf3e0!important;color:#1d1d1b!important}
.note{color:#26241e!important;font-size:calc(clamp(13px,1.1vw,21px)*var(--fz,1))!important}.note b.ok{color:#2f6b3f!important}.note b.no{color:#a8473b!important}
/* ---- титул ---- */
.cover{flex:0 1 auto;margin:auto;align-items:stretch;text-align:center;gap:0;background:#faf3e0;border:4px solid #1d1d1b;
 box-shadow:12px 12px 0 rgba(0,0,0,.5);padding:0;max-width:1350px;width:92%%}
.cover .cvh{display:flex;align-items:center;gap:14px;background:#1f4a44;color:#fff;border-bottom:4px solid #1d1d1b;padding:12px 16px;
 font:900 clamp(13px,1.1vw,21px)/1 "Golos Text",sans-serif;letter-spacing:.12em;text-transform:uppercase}
.cover .cvh::after{content:"";margin-left:auto;width:96px;height:27px;background:url("%(btn)s") center/contain no-repeat}
.cover .cvb{padding:clamp(22px,3vw,56px) clamp(20px,3vw,60px);display:flex;flex-direction:column;align-items:center;gap:22px}
.cover .big{font-family:var(--fd)!important;font-weight:400;color:#1f4a44!important;text-transform:none!important;
 font-size:clamp(24px,3.8vw,68px)!important;line-height:1.3!important;text-shadow:5px 5px 0 rgba(0,0,0,.15)!important}
.cover .big em{font-style:normal;color:#a8473b!important;text-shadow:5px 5px 0 rgba(0,0,0,.15)!important}
.cover .lead{color:#26241e!important;font-weight:700}
.cover .tags{justify-content:center}
/* ---- HUD и содержание ---- */
#hud{background:#1f4a44!important;border-top:3px solid #1d1d1b!important}
#hud button{border-radius:0!important;background:#faf3e0!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 #000}
#hud button:hover{background:#ffd75e!important}
#hud #count{color:#ffd75e!important}#hud #sname{color:#f2ecdc!important}#hud .hint{color:rgba(255,255,255,.65)!important}
#prog{background:#ffd75e!important;box-shadow:none!important}
#toc{background:rgba(214,204,178,.97)!important}
#toc h2{color:#1f4a44!important;font-family:var(--fd)!important;font-size:clamp(14px,1.4vw,26px)!important}
.tocit{border-radius:0!important;background:#faf3e0!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 rgba(0,0,0,.35)}
.tocit:hover{background:#ffd75e!important}.tocit i{color:#a8473b!important}
/* ---- инфографика автора во весь слайд ---- */
.aclbleed{position:absolute;inset:0 0 54px 0;display:flex;align-items:center;justify-content:center;padding:clamp(8px,1.2vw,22px)}
.aclbleed img{max-width:100%%;max-height:100%%;object-fit:contain;border:4px solid #1d1d1b;box-shadow:12px 12px 0 rgba(0,0,0,.45);background:#faf3e0}
.slide.on .aclbleed img{animation:aclpic .75s cubic-bezier(.22,.7,.3,1) both}
@keyframes aclpic{from{opacity:0;transform:translateY(24px) scale(.96)}to{opacity:1;transform:none}}
/* ---- тренажёр CLI ---- */
.cs-side{background:#faf3e0!important;border:3px solid #1d1d1b!important;outline:0!important;border-radius:0!important;box-shadow:6px 6px 0 rgba(0,0,0,.45)!important}
.cs-h{color:#1f4a44!important;font-family:var(--fd)!important;font-size:clamp(11px,.95vw,17px)!important}
.cs-task{color:#1d1d1b!important;font-size:clamp(15px,1.4vw,27px)!important}.cs-task b{color:#000!important;background:#ffe7a0}
.cs-btns button{border-radius:0!important;background:#ffd75e!important;color:#1d1d1b!important;border:2px solid #1d1d1b!important;box-shadow:2px 2px 0 #000!important}
.cs-btns button.alt{background:#9fd28c!important}.cs-btns button.sec{background:#fff!important}
.cs-res .ok{color:#2f6b3f!important}.cs-res .no{color:#a8473b!important}.cs-res .exp{color:#7a5d00!important}
.cs-term{border:3px solid #1d1d1b!important;outline:0!important;border-radius:0!important;box-shadow:6px 6px 0 rgba(0,0,0,.45)!important}
.cs-bar{background:#1f4a44!important}.cs-bar i{border-radius:0!important;background:#d9d2c0!important;border:2px solid #111}
.cs-out,.cs-in{font-size:clamp(13px,1.15vw,22px)!important}
.cs-send>div{border-bottom-color:rgba(0,0,0,.2)!important}
"""

GDEFS = ""

# авто-подгонка: текст растёт, пока слайд заполнен без прокрутки (или ужимается, если не влезает);
# консоль и конфигурации ужимаются по ширине, чтобы строки не переносились
FIT_JS = r"""
(function(){
  var stage=document.getElementById('stage');
  function fit(s){
    var sc=s.querySelector(':scope>.sc'); if(!sc||s.querySelector('.aclbleed')) return;
    var grow=!s.querySelector('.clisim,.scene');
    s.querySelectorAll('pre.cli.fitw').forEach(function(p){p.classList.remove('fitw','wrapw');p.style.removeProperty('--pw');});
    var inner=[].slice.call(s.querySelectorAll('.tw,pre.cli,.sc>.grow,.sc>.grow>.col'));
    function over(){
      if(sc.scrollHeight>sc.clientHeight+2) return true;
      for(var i=0;i<inner.length;i++){var e=inner[i]; if(e.clientHeight&&e.scrollHeight>e.clientHeight+2) return true;}
      return false;
    }
    function set(f){s.style.setProperty('--fz',f.toFixed(3));s.style.setProperty('--fm',Math.min(f,1.2).toFixed(3));}
    var f=1; set(f);
    if(over()){while(f>0.62&&over()){f-=0.04;set(f);}}
    else if(grow){while(f<1.75&&!over()){f+=0.04;set(f);} if(over()){f-=0.04;set(f);}}
    s.querySelectorAll('pre.cli').forEach(function(p){
      if(p.scrollWidth<=p.clientWidth+1) return;
      var fs=parseFloat(getComputedStyle(p).fontSize), min=Math.max(11,fs*0.62), k=0;
      p.classList.add('fitw');
      while(p.scrollWidth>p.clientWidth+1&&k<40&&fs>min){fs*=0.96;p.style.setProperty('--pw',fs+'px');k++;}
      if(p.scrollWidth>p.clientWidth+1) p.classList.add('wrapw');
    });
  }
  function cur(){var s=document.querySelector('.slide.on'); if(s) fit(s);}
  new MutationObserver(function(m){ if(m.some(function(x){return x.target.classList&&x.target.classList.contains('slide')&&x.target.classList.contains('on');})) cur(); })
    .observe(stage,{subtree:true,attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',function(){clearTimeout(window.__fitT);window.__fitT=setTimeout(cur,120);});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(cur);
  setTimeout(cur,60);
  window.ACL_FIT=cur;
})();
"""


def build():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _dk_kit
    import _dk_cli
    import _acl_deck
    import _acl_final
    import _acl_fig

    del L.SL[:]
    _acl_final.cover()
    _acl_deck.build()
    _acl_final.tail()
    slides = list(L.SL)
    css = (CSS + _dk_kit.CSS + _dk_cli.CSS
           + THEME % {"bg": b64("bg_main"), "cover": b64("bg_cover"), "btn": WINBTN} + _acl_fig.CSS + _acl_final.CSS)
    with io.open(os.path.join(HERE, "_acl_cli.js"), encoding="utf-8") as fh:
        cli_js = fh.read()
    js = JS + _dk_kit.JS + cli_js + FIT_JS
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>Списки контроля доступа ACL — лекция</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-acl\">\n"
        '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n" % (FONTS, css, "\n".join(slides), _sw_build.HUD, js))
    out = os.environ.get("ACL_OUT") or os.path.join(HERE, OUT)
    with io.open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (out, len(slides), os.path.getsize(out) / 1048576.0))


if __name__ == "__main__":
    build()
