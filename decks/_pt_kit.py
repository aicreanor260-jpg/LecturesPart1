# -*- coding: utf-8 -*-
"""Общие блоки дек по pptx (комплект 2026-11: ACL, WAN, WAN-2, мониторинг, STP) на движке коммутации:
консоль/конфигурация/синтаксис, инфографика автора во весь слайд, рисунок pptx в панели, авто-подгонка кегля,
тренажёр «разложи по группам» и общий сборщик HTML."""
import base64
import io
import os
import re

from _sw_lib import slide, _esc

HERE = os.path.dirname(os.path.abspath(__file__))


def b64(adir, name, ext="webp"):
    with open(os.path.join(HERE, adir, name + "." + ext), "rb") as fh:
        return "data:image/%s;base64,%s" % (ext, base64.b64encode(fh.read()).decode())


_PROMPT = re.compile(r"^(\S+?(?:\([^)]*\))?#)(.*)$")


def conf(lines, title="Конфигурация"):
    """Команды: приглашение приглушено, команда выделена; [[…]] — подсветка как в pptx; прочие строки — как есть."""
    out = []
    for ln in lines:
        m = _PROMPT.match(ln)
        if m and not ln.startswith("#"):
            s = '<span class="p">%s</span><span class="k">%s</span>' % (_esc(m.group(1)), _esc(m.group(2)))
        else:
            s = _esc(ln)
        out.append(s.replace("[[", '<span class="h">').replace("]]", "</span>"))
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<pre class="cli">%s</pre>' % (t, "\n".join(out))


def term(lines, title=""):
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    body = "\n".join(_esc(l).replace("[[", '<span class="h">').replace("]]", "</span>") for l in lines)
    return '%s<pre class="cli term">%s</pre>' % (t, body)


def syn(lines, title="Синтаксис"):
    body = "\n".join(re.sub(r"\*([^*]+)\*", r"<i>\1</i>", _esc(l)) for l in lines)
    t = '<div class="clih">%s</div>' % title if title else ""
    return '%s<pre class="cli syn">%s</pre>' % (t, body)


def info(adir, name, label):
    """Инфографика автора во весь слайд сразу за своим слайдом pptx."""
    slide("Инфографика · " + re.sub("<[^>]+>", "", label),
          '<div class="ptbleed"><img src="%s" alt="" loading="lazy"></div>' % b64(adir, name))


def pic(adir, name, cap=""):
    """Рисунок pptx (схема) в панели деки."""
    c = '<div class="ptcap">%s</div>' % cap if cap else ""
    return '<div class="ptpic"><img src="%s" alt="" loading="lazy">%s</div>' % (b64(adir, name), c)


def table(headers, rows, cls=""):
    from _sw_lib import table as T
    return T(headers, rows, "pttw " + cls)


# ---------------------------------------------------------------- живая консоль (движок — свой *_cli.js)
def sim(deck, pool, console="Console · Eltex ESR", send="Отправить пакет"):
    return (
        '<div class="clisim" data-deck="%s" data-pool="%s">'
        '<div class="cs-side"><div class="cs-h">Задание</div><div class="cs-task"></div>'
        '<div class="cs-btns"><button data-cs="new">↻ Обновить задание</button><button data-cs="check">Проверить</button>'
        '<button data-cs="send" class="alt">%s</button><button data-cs="sol" class="sec">Решение</button></div>'
        '<div class="cs-res"></div><pre class="cli cs-sol" style="display:none"></pre></div>'
        '<div class="cs-term"><div class="cs-bar"><i></i><i></i><i></i><span>%s</span></div>'
        '<div class="cs-out"></div><label class="cs-in"><span class="cs-pr"></span>'
        '<input type="text" spellcheck="false" autocomplete="off" placeholder="введите команду и нажмите Enter"></label></div></div>'
    ) % (deck, ",".join(str(i) for i in pool), send, console)


def js(name):
    with io.open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------- тренажёр «разложи по группам»
def sorter(sid, groups, items, task_text):
    """groups — [название, ...]; items — [(текст, индекс верной группы), ...]. Клик по карточке, затем по группе."""
    import json
    import random
    rnd = random.Random(sid)
    its = list(items)
    rnd.shuffle(its)
    chips = "".join('<button class="srt-it" data-g="%d">%s</button>' % (g, t) for t, g in its)
    bins = "".join('<div class="srt-bin" data-g="%d"><div class="srt-h">%s</div><div class="srt-b"></div></div>' % (i, g)
                   for i, g in enumerate(groups))
    return ('<div class="srt" data-srt="%s"><div class="srt-task">%s</div><div class="srt-pool">%s</div>'
            '<div class="srt-bins" style="grid-template-columns:repeat(%d,1fr)">%s</div>'
            '<div class="inrow"><button data-srt="check">Проверить</button><button class="sec" data-srt="reset">Сначала</button>'
            '<button class="sec" data-srt="show">Показать ответ</button><span class="srt-res"></span></div></div>'
            % (sid, task_text, chips, len(groups), bins))


SORT_JS = r"""
(function(){
  document.querySelectorAll('.srt').forEach(function(box){
    var pool=box.querySelector('.srt-pool'), sel=null, res=box.querySelector('.srt-res');
    function clear(){box.querySelectorAll('.srt-it').forEach(function(c){c.classList.remove('ok','no');});res.textContent='';}
    box.addEventListener('click',function(e){
      var it=e.target.closest('.srt-it'), bin=e.target.closest('.srt-bin'), b=e.target.closest('[data-srt]');
      if(b&&b.tagName==='BUTTON'){
        var a=b.dataset.srt;
        if(a==='reset'){box.querySelectorAll('.srt-it').forEach(function(c){c.classList.remove('ok','no','sel');pool.appendChild(c);});res.textContent='';}
        if(a==='show'){box.querySelectorAll('.srt-it').forEach(function(c){box.querySelector('.srt-bin[data-g="'+c.dataset.g+'"] .srt-b').appendChild(c);c.classList.remove('no','sel');c.classList.add('ok');});res.textContent='Ответ показан';}
        if(a==='check'){var ok=0,n=0;box.querySelectorAll('.srt-b .srt-it').forEach(function(c){n++;var y=c.closest('.srt-bin').dataset.g===c.dataset.g;c.classList.toggle('ok',y);c.classList.toggle('no',!y);if(y)ok++;});
          var left=pool.querySelectorAll('.srt-it').length;res.textContent='Верно '+ok+' из '+(n+left)+(left?' · не разложено: '+left:'')+(ok===n+left?' — отлично!':'');}
        return;
      }
      if(it){ if(sel) sel.classList.remove('sel'); sel=(sel===it)?null:it; if(sel) sel.classList.add('sel'); clear(); return; }
      if(bin&&sel){ bin.querySelector('.srt-b').appendChild(sel); sel.classList.remove('sel'); sel=null; clear(); return; }
      if(e.target.closest('.srt-pool')&&sel){ pool.appendChild(sel); sel.classList.remove('sel'); sel=null; }
    });
  });
})();
"""

# ---------------------------------------------------------------- авто-подгонка
FIT_JS = r"""
(function(){
  var stage=document.getElementById('stage');
  function fit(s){
    var sc=s.querySelector(':scope>.sc'); if(!sc||s.querySelector('.ptbleed')) return;
    var grow=!s.querySelector('.clisim,.scene');
    s.querySelectorAll('pre.cli.fitw').forEach(function(p){p.classList.remove('fitw','wrapw');p.style.removeProperty('--pw');});
    var inner=[].slice.call(s.querySelectorAll('.tw,pre.cli,.sc>.grow,.sc>.grow>.col'));
    function over(){
      if(sc.scrollHeight>sc.clientHeight+2) return true;
      for(var i=0;i<inner.length;i++){var e=inner[i]; if(e.clientHeight&&e.scrollHeight>e.clientHeight+2) return true;}
      return false;
    }
    function set(f){s.style.setProperty('--fz',f.toFixed(3));s.style.setProperty('--fm',Math.min(f,1.2).toFixed(3));}
    s.classList.add('ptfit');
    var f=1; set(f);
    if(over()){while(f>0.6&&over()){f-=0.04;set(f);}}
    else if(grow){while(f<1.75&&!over()){f+=0.04;set(f);} if(over()){f-=0.04;set(f);}}
    s.querySelectorAll('pre.cli').forEach(function(p){
      if(p.scrollWidth<=p.clientWidth+1) return;
      var fs=parseFloat(getComputedStyle(p).fontSize), min=Math.max(11,fs*0.62), k=0;
      p.classList.add('fitw');
      while(p.scrollWidth>p.clientWidth+1&&k<40&&fs>min){fs*=0.96;p.style.setProperty('--pw',fs+'px');k++;}
      if(p.scrollWidth>p.clientWidth+1) p.classList.add('wrapw');
    });
    s.classList.remove('ptfit');
  }
  var obs=new MutationObserver(function(m){ if(m.some(function(x){return x.target.classList&&x.target.classList.contains('slide')&&x.target.classList.contains('on');})) cur(); });
  function cur(){var s=document.querySelector('.slide.on'); if(s){ fit(s); obs.takeRecords(); }}
  obs.observe(stage,{subtree:true,attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',function(){clearTimeout(window.__fitT);window.__fitT=setTimeout(cur,120);});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(cur);
  setTimeout(cur,60);
  window.PT_FIT=cur;
})();
"""

# общие правила, не зависящие от темы (кегль через --fz, подгонка консоли, сцены, рисунки, сортировка)
BASE_CSS = r"""
.c p,ul.li li,.ir span{font-size:calc(clamp(15px,1.42vw,28px)*var(--fz,1))!important;line-height:1.42}
.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) .c p,.slide>.sc>.g.grow:not(.g2):not(.g3):not(.g12):not(.g21) ul.li li{font-size:calc(clamp(17px,1.7vw,33px)*var(--fz,1))!important}
.step>p,.col>p{font:600 calc(clamp(14px,1.25vw,24px)*var(--fz,1))/1.4 var(--f);margin:0}
.foot{font-size:calc(clamp(15px,1.35vw,26px)*var(--fz,1))!important}
.tw table{font-size:calc(clamp(14px,1.25vw,24px)*var(--fz,1))!important}
pre.cli{font-size:calc(clamp(13px,1.2vw,23px)*var(--fm,1))!important;white-space:pre;overflow-x:auto}
pre.cli.term{font-size:calc(clamp(12px,1.05vw,20px)*var(--fm,1))!important}
pre.cli.fitw{font-size:var(--pw)!important}
pre.cli.wrapw{white-space:pre-wrap!important;overflow-wrap:anywhere}
.q .qt{font-size:calc(clamp(15px,1.35vw,26px)*var(--fz,1))!important}
.opts button{font-size:calc(clamp(14px,1.25vw,24px)*var(--fz,1))!important}
.ex{font-size:calc(clamp(13px,1.15vw,22px)*var(--fz,1))!important}
.note{font-size:calc(clamp(13px,1.1vw,21px)*var(--fz,1))!important}
.inrow input{font-size:calc(clamp(14px,1.2vw,23px)*var(--fz,1))!important}
.inrow button{font-size:calc(clamp(12px,1vw,19px)*var(--fz,1))!important}
.ptfit,.ptfit *{transition:none!important}
.col>.col{flex:1 1 auto;min-height:0}
.col>.scene,.scene{flex:1 1 auto;min-height:0}
.scene .figwrap{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}
svg.flowfig{flex:1 1 auto;width:100%;height:100%;min-height:0;max-height:none}
.ptbleed{position:absolute;inset:0 0 54px 0;display:flex;align-items:center;justify-content:center;padding:clamp(8px,1.2vw,22px)}
.ptbleed img{max-width:100%;max-height:100%;object-fit:contain}
.slide.on .ptbleed img{animation:ptpic .75s cubic-bezier(.22,.7,.3,1) both}
@keyframes ptpic{from{opacity:0;transform:translateY(24px) scale(.96)}to{opacity:1;transform:none}}
.ptpic{flex:1 1 auto;min-height:min(30vh,260px);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px}
.ptpic img{width:100%;height:auto;max-width:100%;max-height:calc(100vh - 190px);min-height:0;object-fit:contain;background:#fff;border-radius:10px;padding:8px}
.slide.on .ptpic img{animation:ptpic .7s cubic-bezier(.22,.7,.3,1) .15s both}
.ptcap{margin-top:6px;font:700 calc(clamp(12px,1vw,18px)*var(--fz,1))/1.3 var(--f)}
.ptol{margin:6px 0 0 1.5em;display:flex;flex-direction:column;gap:6px}
.ptol li{font-size:calc(clamp(15px,1.42vw,28px)*var(--fz,1));line-height:1.42;font-weight:700}
.srt{display:flex;flex-direction:column;gap:12px}
.srt-task{font:700 calc(clamp(15px,1.35vw,26px)*var(--fz,1))/1.35 var(--f)}
.srt-pool{display:flex;flex-wrap:wrap;gap:8px;min-height:52px;padding:8px;border:2px dashed currentColor;border-radius:12px;opacity:.95}
.srt-bins{display:grid;gap:12px}
.srt-bin{border-radius:14px;padding:8px;min-height:120px;cursor:pointer}
.srt-h{font:800 calc(clamp(14px,1.25vw,24px)*var(--fz,1))/1.2 var(--f);margin-bottom:8px;text-align:center}
.srt-b{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.srt-it{font:700 calc(clamp(13px,1.1vw,21px)*var(--fz,1))/1.2 var(--f);padding:8px 12px;border-radius:10px;cursor:pointer;transition:transform .15s}
.srt-it.sel{transform:translateY(-3px) scale(1.04);outline:3px solid #ffd23a}
.srt-it.ok{background:#c9f2b8!important;border-color:#2f8a3a!important}
.srt-it.no{background:#ffc9c0!important;border-color:#c0392b!important;animation:shake .35s}
.srt-res{font:800 calc(clamp(14px,1.2vw,22px)*var(--fz,1))/1.2 var(--f);margin-left:8px}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?%s&display=swap">')


# ---------------------------------------------------------------- смысловые блоки вместо сплошного текста
# Длинный абзац (> LONG символов) делится по границам предложений и перечислений на блоки по 1–2 предложения.
# Текст pptx не меняется ни на букву — меняется только подача (каждый блок с акцентной полосой слева).
LONG, CHUNK = 200, 150
_PARA = re.compile(r"<p>(.*?)</p>", re.S)
_CUT = re.compile(r"(?:(?<=[.!?])|(?<=[.!?]»)|(?<=[.!?]\)))\s+(?=(?:<[^>]+>)*[А-ЯЁA-Z«(])"   # конец предложения
                  r"|(?<=;)\s*(?=(?:<[^>]+>)*(?:\d+[.)]|[А-ЯЁA-Z]))"                    # «…;2. …» — пункты перечисления
                  r"|(?<=:)\s*(?=(?:<[^>]+>)*\d+[.)]\s)")                              # «…: 1. …»


def _plain(s):
    return re.sub(r"<[^>]+>", "", s)


def _balanced(s):
    return all(len(re.findall(r"<%s\b" % t, s)) == len(re.findall(r"</%s>" % t, s)) for t in ("b", "i", "span", "em"))


def _split_para(h):
    if len(_plain(h)) <= LONG:
        return None
    parts, last = [], 0
    for m in _CUT.finditer(h):
        parts.append(h[last:m.start()])
        last = m.end()
    parts.append(h[last:])
    parts = [x.strip() for x in parts if x.strip()]
    if len(parts) < 2:
        return None
    chunks, cur = [], ""
    for x in parts:
        cur = (cur + " " + x).strip() if cur else x
        if len(_plain(cur)) >= CHUNK and _balanced(cur):
            chunks.append(cur)
            cur = ""
    if cur:
        if chunks and (len(_plain(cur)) < 60 or not _balanced(cur)):
            chunks[-1] += " " + cur
        else:
            chunks.append(cur)
    if len(chunks) < 2 or not all(_balanced(c) for c in chunks):
        return None
    return "".join('<p class="ptb">%s</p>' % c for c in chunks)


_LI = re.compile(r"<li>(.*?)</li>", re.S)


def blocks(html):
    def rep(m):
        r = _split_para(m.group(1))
        return r if r else m.group(0)

    def rep_li(m):   # длинный пункт списка — пункт и под ним блоки
        r = _split_para(m.group(1))
        return "<li>%s</li>" % r if r else m.group(0)
    return _LI.sub(rep_li, _PARA.sub(rep, html))


BASE_CSS += r"""
p.ptb{border-left:5px solid var(--cy);padding:3px 0 3px 12px!important;margin:0!important}
p.ptb+p.ptb,p+p.ptb,p.ptb+p{margin-top:9px!important}
"""


def build(out, title, body_cls, fonts, theme_css, slides, extra_js="", out_env="PT_OUT"):
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _dk_kit
    import _dk_cli
    css = CSS + _dk_kit.CSS + _dk_cli.CSS + BASE_CSS + theme_css
    js = JS + _dk_kit.JS + SORT_JS + extra_js + FIT_JS
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>%s</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"%s\">\n"
        '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n" % (title, fonts, css, body_cls, "\n".join(blocks(s) for s in slides), _sw_build.HUD, js))
    # одинаковые картинки (схема pptx на нескольких слайдах) — один раз в словаре, src подставляет скрипт
    uris = re.findall(r'src="(data:image/[^"]+)"', html)
    rep = {u: "i%d" % k for k, u in enumerate(sorted({u for u in uris if uris.count(u) > 1}, key=uris.index))}
    if rep:
        for u, k in rep.items():
            html = html.replace('src="%s"' % u, 'data-pt="%s" src="data:image/gif;base64,R0lGODlhAQABAAAAACw="' % k)
        store = "<script>(function(){var M={%s};document.querySelectorAll('img[data-pt]').forEach(function(i){i.src=M[i.dataset.pt];});})();</script>" % (
            ",".join('%s:"%s"' % (k, u) for u, k in rep.items()))
        html = html.replace("</body>", store + "\n</body>", 1)
    path = os.environ.get(out_env) or os.path.join(HERE, out)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (path, len(slides), os.path.getsize(path) / 1048576.0))
