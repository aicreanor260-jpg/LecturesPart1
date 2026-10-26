# -*- coding: utf-8 -*-
"""NAT: Outside global — внешний глобальный адрес (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img as _img

W, H, TOP = 1672, 941, 262

FADE = (";-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)"
        ";mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)")


def img(f, st):
    return _img(f, st)


GLOBE = ('<svg viewBox="0 0 64 64" style="width:100%;height:100%"><g fill="none" stroke="#5cd2ff" stroke-width="2.6">'
         '<circle cx="32" cy="32" r="26"/><ellipse cx="32" cy="32" rx="11" ry="26"/><path d="M6 32h52M10 19h44M10 45h44M32 6v52"/></g></svg>')
RACK = ('<svg viewBox="0 0 64 64" style="width:100%;height:100%"><g fill="none" stroke="#5cd2ff" stroke-width="3.2">'
        '<rect x="10" y="6" width="44" height="14" rx="4"/><rect x="10" y="25" width="44" height="14" rx="4"/>'
        '<rect x="10" y="44" width="44" height="14" rx="4"/><path d="M18 13h4M18 32h4M18 51h4"/></g></svg>')

CSS = """<style>
.n6og-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6og-lb{position:absolute;box-sizing:border-box;text-align:center;font:600 21px/1.35 "Golos Text",sans-serif;color:#fff;
  display:flex;align-items:center;justify-content:center;background:rgba(8,20,50,.85);border:1.5px solid rgba(92,190,255,.55);border-radius:12px}
.n6og-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6og-wire .fl{fill:none;stroke:#5cd2ff;stroke-width:4;filter:drop-shadow(0 0 6px #3aa0ff);stroke-dasharray:14 8;animation:n6ogd 1s linear infinite}
@keyframes n6ogd{to{stroke-dashoffset:-44}}
.n6og-ip{position:absolute;box-sizing:border-box;border:2.5px solid #5cd2ff;border-radius:14px;background:rgba(10,30,80,.9);
  box-shadow:0 0 26px rgba(92,210,255,.7);font:700 40px/1 "Golos Text",sans-serif;color:#fff;padding:16px 20px;white-space:nowrap;
  animation:n6ogg 2.4s ease-in-out infinite}
@keyframes n6ogg{50%{box-shadow:0 0 40px rgba(92,210,255,1)}}
</style>"""

HTML = CSS + bg("bgk_globe") + "".join([
    # определение
    '<div class="step"><div class="n6og-p" style="left:80px;top:281px;width:734px;height:208px"></div>'
    '<div class="n6og-p" style="left:102px;top:300px;width:168px;height:168px;padding:20px;border-radius:12px">' + GLOBE + '</div>'
    '<div style="position:absolute;left:304px;top:310px;font:700 30px/1.3 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
    'Адрес внешнего сервера<br>в его собственной сети —<br><span style="font-weight:400;color:#b9d2f5">тот, по которому к нему<br>'
    'обращаются извне.</span></div></div>',
    # адрес сервера
    '<div class="step">' + img("n6_og_srv.png", "left:1195px;top:275px;width:267px")
    + '<div class="n6og-ip" style="left:880px;top:285px">203.0.113.20*</div>'
    '<svg class="n6og-wire"><path d="M1160 355l60 38" stroke="#5cd2ff" stroke-width="3"/></svg>'
    '<div style="position:absolute;left:880px;top:385px;font:400 17px/1.4 \'Golos Text\',sans-serif;color:#b9d2f5;white-space:nowrap">'
    '*Учебный адрес TEST-NET-3;<br>используется в примерах<br>и не маршрутизируется<br>в Интернете.</div></div>',
    # схема
    '<div class="step"><div class="n6og-p" style="left:32px;top:520px;width:1612px;height:385px;border-radius:18px"></div>'
    '<div style="position:absolute;left:64px;top:540px;font:700 29px/1 \'Golos Text\',sans-serif;color:#fff">Схема работы</div>'
    '<div style="position:absolute;left:64px;top:582px;width:360px;height:1px;background:rgba(92,190,255,.4)"></div>'
    + img("n6_og_pc.png", "left:62px;top:612px;width:274px")
    + img("n6_og_rt.png", "left:383px;top:612px;width:239px")
    + img("n6_og_cl.png", "left:692px;top:608px;width:210px")
    + img("n6_og_srv2.png", "left:972px;top:572px;width:176px")
    + '<svg class="n6og-wire"><path class="fl" d="M282 686H380L408 712M598 686H682M900 686H962"/>'
      '<path d="M398 700l12 14-16 2M676 676l14 10-14 10M956 676l14 10-14 10" fill="none" stroke="#5cd2ff" stroke-width="4"/></svg>'
    + '<div class="n6og-lb" style="left:54px;top:783px;width:290px;height:78px">Клиент<br>во внутренней сети</div>'
    '<div class="n6og-lb" style="left:375px;top:790px;width:293px;height:62px">NAT-маршрутизатор</div>'
    '<div class="n6og-lb" style="left:892px;top:782px;width:305px;height:76px">Внешний сервер<br>(в Интернете)</div></div>',
    # вывод
    '<div class="step"><svg class="n6og-wire"><path d="M1128 631L1180 588H1268" fill="none" stroke="#b77bff" stroke-width="3"/>'
    '<circle cx="1128" cy="631" r="7" style="fill:#b77bff"/></svg>'
    '<div style="position:absolute;left:1266px;top:548px;width:354px;height:172px;box-sizing:border-box;border:2.5px solid #b77bff;'
    'border-radius:16px;background:rgba(40,22,100,.85);box-shadow:0 0 24px rgba(183,123,255,.6);padding:16px 26px;'
    'font:400 26px/1.32 \'Golos Text\',sans-serif;color:#fff"><span style="font:800 27px Montserrat,sans-serif">Outside global</span> —<br>'
    'это адрес <b>назначения</b><br>сервера, видимый<br>во внешней сети.</div></div>',
    '<div class="step"><div class="n6og-p" style="left:1219px;top:750px;width:410px;height:122px;border:2.5px solid #5cd2ff"></div>'
    '<div style="position:absolute;left:1242px;top:772px;width:62px;height:78px">' + RACK + '</div>'
    '<div style="position:absolute;left:1328px;top:772px;width:1.5px;height:78px;background:#5cd2ff"></div>'
    '<div style="position:absolute;left:1354px;top:776px;font:700 27px/1.3 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
    'Реальный адрес<br>внешнего сервера.</div></div>',
])
