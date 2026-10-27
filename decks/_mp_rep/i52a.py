# -*- coding: utf-8 -*-
"""pptx: LSP Ping — обнаружение ошибки на LSR7 — вёрстка поверх bgk_16."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 206

CSS = """<style>
.i52-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i52-t{position:absolute;font:500 21px/1.42 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i52-n{position:absolute;font:900 27px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i52-lb{position:absolute;height:38px;border-radius:5px;font:700 22px/34px "Golos Text",sans-serif;color:#13306e;text-align:center;
 box-sizing:border-box;padding:0 12px}
.i52-num{position:absolute;width:66px;height:66px;border-radius:50%;background:#a9dccb;font:900 34px/66px "Golos Text",sans-serif;
 color:#13306e;text-align:center}
.i52-dash{stroke-dasharray:12 8;animation:i52d 1.2s linear infinite}
@keyframes i52d{to{stroke-dashoffset:-20}}
.i52-fly{animation:i52f 3s ease-in-out infinite}
@keyframes i52f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def card(x, w, n, title, text):
    return '<div class="step">' + \
        '<div class="i52-p" style="left:%dpx;top:612px;width:%dpx;height:202px;border-width:2px"></div>' % (x, w) + \
        '<div class="i52-num" style="left:%dpx;top:626px">%d.</div>' % (x + 26, n) + \
        '<div class="i52-t" style="left:%dpx;top:642px;font:900 24px/1 Golos Text;color:#13306e">%s</div>' % (x + 112, title) + \
        '<div class="i52-t" style="left:%dpx;top:686px">%s</div>' % (x + 112, text) + '</div>'


SVG = ('<svg style="position:absolute;left:0;top:0" width="1672" height="941"><defs>'
       '<marker id="i52g" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="20" refX="14" refY="10" orient="auto">'
       '<path d="M0,0 L20,10 L0,20z" style="fill:#14866a"/></marker>'
       '<marker id="i52s" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="12" refY="9" orient="auto">'
       '<path d="M0,0 L18,9 L0,18z" style="fill:#7f8590"/></marker>'
       '<marker id="i52k" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
       '<path d="M0,0 L16,8 L0,16z" style="fill:#13306e"/></marker>'
       '<marker id="i52r" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="12" refY="9" orient="auto">'
       '<path d="M0,0 L18,9 L0,18z" style="fill:#f2694a"/></marker></defs>'
       '<path d="M282,276 L282,256 L770,256 M900,256 L1386,256 L1386,276" style="fill:none;stroke:#13306e;stroke-width:2.5"/>'
       '<line class="i52-dash" x1="248" y1="402" x2="456" y2="402" style="stroke:#14866a;stroke-width:5" marker-end="url(#i52g)"/>'
       '<line class="i52-dash" x1="612" y1="402" x2="832" y2="402" style="stroke:#14866a;stroke-width:5" marker-end="url(#i52g)"/>'
       '<line x1="988" y1="402" x2="1206" y2="402" style="stroke:#7f8590;stroke-width:4;stroke-dasharray:14 9" marker-end="url(#i52s)"/>'
       '<line x1="1356" y1="402" x2="1424" y2="402" style="stroke:#13306e;stroke-width:3" marker-end="url(#i52k)"/>'
       '<text x="1097" y="422" text-anchor="middle" style="fill:#e2342b;font:900 44px Golos Text,sans-serif">✕</text>'
       '<path class="i52-dash" d="M944,484 C944,520 920,528 900,528 M462,524 C360,524 280,510 220,470" '
       'style="fill:none;stroke:#f2694a;stroke-width:3.5" marker-end="url(#i52r)"/>'
       '<path d="M940,286 L932,300 L948,300z" style="fill:#f9d0c4;stroke:#e2342b;stroke-width:2"/>'
       '</svg>')

HTML = CSS + bg("bgk_16") + "".join([
    '<div class="step">',
    '<div class="i52-p" style="left:44px;top:220px;width:1584px;height:376px"></div>',
    SVG,
    '<div class="i52-t" style="left:790px;top:230px;font:900 28px/1.4 Golos Text;color:#13306e">LSP1</div>',
    img("i52a_rt.png", "left:104px;top:348px;width:142px"),
    img("i52a_rt.png", "left:466px;top:348px;width:142px"),
    img("i52a_gray.png", "left:1212px;top:348px;width:146px"),
    img("i52a_cloud.png", "left:1420px;top:340px;width:192px"),
    '<div class="i52-n" style="left:104px;top:450px">LSR1</div><div class="i52-n" style="left:466px;top:452px">LSR4</div>',
    '<div class="i52-n" style="left:842px;top:452px">LSR7</div><div class="i52-n" style="left:1214px;top:452px">LSR8</div>',
    '<div class="i52-lb i52-fly" style="left:316px;top:348px;background:#c4ecd2;border:2px solid #2e9a62">105</div>',
    '<div class="i52-lb i52-fly" style="left:684px;top:348px;background:#c4ecd2;border:2px solid #2e9a62">177</div>',
    '<div class="i52-lb" style="left:1062px;top:348px;background:#f9b5a6;border:2px solid #e2342b">210</div>',
    '</div>',
    '<div class="step">',
    img("i52a_red.png", "left:842px;top:348px;width:142px"),
    '<div class="i52-lb" style="left:770px;top:282px;height:44px;line-height:40px;background:#f9d0c4;border:2px solid #e2342b;font-size:20px;'
    'border-radius:12px;padding:0 16px">Метка: 177&nbsp; |&nbsp; DA: 127.0.0.1&nbsp; |&nbsp; FEC: 105.0.0.0</div>',
    '<div class="i52-lb" style="left:626px;top:434px;background:#c4ecd2;border:2px solid #2e9a62;border-radius:12px">Echo Request</div>',
    '<div class="i52-t" style="left:600px;top:440px;font:900 22px/1 Golos Text;color:#2e9a62">⟷</div>',
    '</div>',
    '<div class="step">',
    '<div class="i52-lb" style="left:464px;top:506px;height:44px;line-height:40px;background:#f9d0c4;border:2px solid #e2342b;border-radius:10px">'
    'Echo Reply: <span style="color:#b01a14">информация об ошибке</span></div>',
    '<div class="i52-t" style="left:420px;top:558px;font-size:20px">Ответ возвращается по IP-маршруту; он может отличаться от пути запроса.</div>',
    '</div>',
    card(44, 470, 1, "Сбой продвижения", "В этом примере LSR7 не может<br>продолжить передачу по LSP1."),
    card(526, 512, 2, "Локальная обработка запроса", "После снятия MPLS-заголовка<br>адрес DA = 127.0.0.1 направляет<br>"
         "запрос локальному обработчику<br>LSP Ping."),
    card(1048, 484, 3, "Сообщение об ошибке", "LSR7 обрабатывает Echo Request<br>и отправляет Echo Reply узлу LSR1<br>"
         "с кодом обнаруженной ошибки."),
    '<div class="step">',
    '<div class="i52-t" style="left:44px;top:830px;width:1356px;height:76px;background:#fbd8cc;border:2px solid #e2342b;border-radius:16px;'
    'box-sizing:border-box;padding-left:92px;font:500 20px/72px Golos Text"><b style="color:#d0281f">Пример обработки диагностического '
    'запроса:</b> обычный MPLS-пакет при ошибке не обязан переходить на IP-продвижение.</div>',
    '<div class="i52-num" style="left:68px;top:846px;width:46px;height:46px;background:#e2342b;color:#fff;font:900 30px/46px Golos Text">!</div>',
    '</div>',
])
