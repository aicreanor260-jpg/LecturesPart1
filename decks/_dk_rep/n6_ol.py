# -*- coding: utf-8 -*-
"""NAT: Outside local — внешний локальный адрес (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img as _img

FADE = ";-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)"


def img(f, st):
    return _img(f, st)

W, H, TOP = 1672, 941, 245

GLOBE = ('<svg viewBox="0 0 64 64" style="width:100%;height:100%"><g fill="none" stroke="#5cd2ff" stroke-width="3.4">'
         '<circle cx="32" cy="32" r="26"/><ellipse cx="32" cy="32" rx="11" ry="26"/><path d="M6 32h52M10 19h44M10 45h44M32 6v52"/></g></svg>')
DOC = ('<svg viewBox="0 0 64 64" style="width:100%;height:100%"><g fill="none" stroke="#b77bff" stroke-width="3.4" stroke-linejoin="round">'
       '<path d="M16 6h22l12 12v40H16z"/><path d="M38 6v12h12M24 30h18M24 38h18M24 46h12"/></g></svg>')

CSS = """<style>
.n6ol-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6ol-ic{position:absolute;box-sizing:border-box;border-radius:14px;padding:16px;background:rgba(10,30,70,.85)}
.n6ol-h{position:absolute;font:800 27px/1.1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6ol-t{position:absolute;white-space:nowrap;font:400 22px/1.42 "Golos Text",sans-serif;color:#b9d2f5}
.n6ol-l{position:absolute;text-align:center;font:700 21px/1.25 "Golos Text",sans-serif;color:#fff;width:240px}
.n6ol-l span{display:block;font-weight:400;font-size:18px;color:#b9d2f5}
.n6ol-ip{position:absolute;box-sizing:border-box;border:2px solid #b77bff;border-radius:8px;background:rgba(40,20,90,.7);
  font:600 26px/1 "Golos Text",sans-serif;color:#fff;padding:10px 8px;white-space:nowrap}
.n6ol-ip span{display:block;font:400 13px/1 "Golos Text",sans-serif;color:#b9d2f5;margin-top:8px}
.n6ol-ol{position:absolute;box-sizing:border-box;border:2px solid #b77bff;border-radius:14px;background:rgba(50,30,140,.85);
  box-shadow:0 0 22px rgba(183,123,255,.55);padding:10px 22px}
.n6ol-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6ol-wire .fl{fill:none;stroke:#5cd2ff;stroke-width:4;filter:drop-shadow(0 0 6px #3aa0ff);stroke-dasharray:14 8;animation:n6old 1s linear infinite}
@keyframes n6old{to{stroke-dashoffset:-44}}
.n6ol-pk{position:absolute;width:22px;height:14px;border-radius:3px;background:#5cd2ff;box-shadow:0 0 12px #5cd2ff;
  animation:n6olp 3.2s linear infinite}
@keyframes n6olp{0%{transform:translate(0,0);opacity:0}8%{opacity:1}48%{transform:translate(300px,0)}52%{transform:translate(330px,0)}
  92%{opacity:1}100%{transform:translate(600px,0);opacity:0}}
</style>"""


def panel(y, h, ico, icc, title, text):
    return ('<div class="step"><div class="n6ol-p" style="left:64px;top:%dpx;width:638px;height:%dpx"></div>'
            '<div class="n6ol-ic" style="left:90px;top:%dpx;width:112px;height:112px;border:2px solid %s;box-shadow:0 0 18px %s">%s</div>'
            '<div class="n6ol-h" style="left:240px;top:%dpx">%s</div>'
            '<div class="n6ol-t" style="left:240px;top:%dpx;width:462px;font-size:21px">%s</div></div>'
            % (y, h, y + 30, icc, icc, ico, y + 32, title, y + 70, text))


HTML = CSS + bg("bgk_globe") + "".join([
    panel(270, 168, GLOBE, "#5cd2ff", "Определение",
          "Адрес внешнего устройства таким,<br>каким его видит внутренняя сеть."),
    panel(461, 252, DOC, "#b77bff", "Короткое пояснение",
          "В простой схеме он совпадает<br>с адресом сервера. Если NAT<br>преобразует и адрес внешнего устройства,<br>"
          "Outside local и Outside global могут<br>различаться."),
    # схема
    '<div class="step">'
    + img("n6_ol_pc.png", "left:735px;top:478px;width:203px")
    + img("n6_ol_rt.png", "left:1060px;top:443px;width:202px")
    + img("n6_ol_srv.png", "left:1418px;top:435px;width:184px")
    + '<svg class="n6ol-wire"><path class="fl" d="M890 556H1050M1262 556H1410"/>'
      '<path d="M1040 546l14 10-14 10M1398 546l14 10-14 10" fill="none" stroke="#5cd2ff" stroke-width="4"/></svg>'
    + '<div class="n6ol-pk" style="left:895px;top:549px"></div>'
    + '<div class="n6ol-l" style="left:724px;top:626px">Компьютер<span>Внутренняя локальная<br>сеть</span></div>'
    + '<div class="n6ol-l" style="left:1042px;top:622px">Маршрутизатор<span>NAT</span></div>'
    + '<div class="n6ol-l" style="left:1385px;top:628px">Веб-сервер<span>В Интернете</span></div></div>',
    # пакет
    '<div class="step"><div class="n6ol-p" style="left:822px;top:263px;width:268px;height:177px;border-radius:12px"></div>'
    '<div style="position:absolute;left:834px;top:276px;font:400 17px/1 \'Golos Text\',sans-serif;color:#b9d2f5">Пакет (до выхода через NAT)</div>'
    '<div style="position:absolute;left:840px;top:309px;width:234px;height:116px;box-sizing:border-box;border:2px solid #5cd2ff;'
    'border-radius:10px;background:rgba(10,40,80,.7);box-shadow:0 0 14px rgba(92,210,255,.5)"></div>'
    '<div style="position:absolute;left:858px;top:323px;font:500 18px/1 \'Golos Text\',sans-serif;color:#fff">Назначение:</div>'
    '<div class="n6ol-ip" style="left:846px;top:348px;width:222px">203.0.113.20<span>(учебный адрес TEST-NET-3)</span></div>'
    '<svg class="n6ol-wire"><path d="M965 446v30q0 40 30 60" fill="none" stroke="#5cd2ff" stroke-width="3"/>'
    '<path d="M957 482l8-12 8 12M988 528l10 10 2-14" fill="none" stroke="#5cd2ff" stroke-width="3"/></svg></div>',
    '<div class="step"><svg class="n6ol-wire"><path d="M1062 368L1124 340" stroke="#b77bff" stroke-width="3"/>'
    '<circle cx="1062" cy="368" r="5" style="fill:#b77bff"/></svg>'
    '<div class="n6ol-ol" style="left:1122px;top:301px;width:226px;height:103px">'
    '<div style="font:800 25px/1.1 Montserrat,sans-serif;color:#fff">Outside local</div>'
    '<div style="font:400 16px/1.3 \'Golos Text\',sans-serif;color:#d8c8ff;margin-top:6px">Адрес сайта, видимый<br>компьютеру</div></div></div>',
    # итог
    '<div class="step"><div class="n6ol-p" style="left:46px;top:751px;width:1584px;height:148px"></div>'
    '<div class="n6ol-ic" style="left:73px;top:768px;width:114px;height:108px;border:2px solid #5cd2ff;box-shadow:0 0 18px #3aa0ff">' + GLOBE + '</div>'
    '<div style="position:absolute;left:223px;top:778px;width:2px;height:90px;background:#5cd2ff"></div>'
    '<div style="position:absolute;left:262px;top:800px;font:700 35px/1 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
    'Адрес внешнего сервера в представлении внутренней сети.</div></div>',
])
