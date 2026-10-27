# -*- coding: utf-8 -*-
"""pptx: проверка FEC и возврат Echo Reply — вёрстка поверх bgk_02."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 140

CSS = """<style>
.i51-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i51-t{position:absolute;font:500 21px/1.2 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i51-n{position:absolute;font:900 24px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center;width:180px}
.i51-n small{font-size:20px;font-weight:500}
.i51-num{position:absolute;width:50px;height:50px;border-radius:50%;color:#fff;font:900 30px/50px "Golos Text",sans-serif;text-align:center}
.i51-dash{stroke-dasharray:12 8;animation:i51d 1.2s linear infinite}
@keyframes i51d{to{stroke-dashoffset:20}}
.i51-fly{animation:i51f 3s ease-in-out infinite}
@keyframes i51f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def rt(x, name, sub=""):
    s = "<br><small>%s</small>" % sub if sub else ""
    return img("i45a_rt.png", "left:%dpx;top:372px;width:100px" % x) + \
        '<div class="i51-n" style="left:%dpx;top:450px">%s%s</div>' % (x - 40, name, s)


def card(x, w, n, col, title, text, fs=21):
    return '<div class="step">' + \
        '<div class="i51-p" style="left:%dpx;top:636px;width:%dpx;height:198px;border-width:2px"></div>' % (x, w) + \
        '<div class="i51-num" style="left:%dpx;top:646px;background:%s">%d</div>' % (x + 26, col, n) + \
        '<div class="i51-t" style="left:%dpx;top:656px;font:900 23px/1 Golos Text;color:#13306e">%s</div>' % (x + 102, title) + \
        '<div class="i51-t" style="left:%dpx;top:700px;font-size:%dpx">%s</div>' % (x + 42 if n == 1 else x + 96, fs, text) + '</div>'


SVG = ('<svg style="position:absolute;left:0;top:0" width="1672" height="941"><defs>'
       '<marker id="i51r" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="12" refY="9" orient="auto">'
       '<path d="M0,0 L18,9 L0,18z" style="fill:#f2694a"/></marker>'
       '<marker id="i51k" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
       '<path d="M0,0 L16,8 L0,16z" style="fill:#13306e"/></marker>'
       '<marker id="i51b" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
       '<path d="M0,0 L16,8 L0,16z" style="fill:#1f63c6"/></marker></defs>'
       '<path d="M468,350 L468,332 L626,332 M1048,332 L1186,332 L1186,350" style="fill:none;stroke:#13306e;stroke-width:2"/>'
       '<line class="i51-dash" x1="520" y1="406" x2="650" y2="406" style="stroke:#f2694a;stroke-width:6" marker-end="url(#i51r)"/>'
       '<line class="i51-dash" x1="766" y1="406" x2="896" y2="406" style="stroke:#f2694a;stroke-width:6" marker-end="url(#i51r)"/>'
       '<line class="i51-dash" x1="1012" y1="406" x2="1114" y2="406" style="stroke:#f2694a;stroke-width:6" marker-end="url(#i51r)"/>'
       '<line x1="1230" y1="404" x2="1270" y2="404" style="stroke:#13306e;stroke-width:3" marker-end="url(#i51k)"/>'
       '<path class="i51-dash" d="M1182,534 L1182,560 L920,560 M752,560 L462,560 L462,532" style="fill:none;stroke:#1f63c6;stroke-width:3" '
       'marker-end="url(#i51b)"/>'
       '<path d="M760,560 C740,540 760,516 790,520 C800,500 840,496 860,512 C880,500 910,510 912,530 C936,536 932,572 910,578 '
       'L782,580 C756,580 748,566 760,560z" style="fill:#e8f5fd;stroke:#1f63c6;stroke-width:2.5"/>'
       '</svg>')

HTML = CSS + bg("bgk_02") + "".join([
    '<div class="step">',
    '<div class="i51-p" style="left:256px;top:146px;width:1220px;height:82px;border-radius:16px"></div>',
    '<div class="i51-t" style="left:256px;top:160px;width:1220px;text-align:center;font:600 22px/1.32 Golos Text,sans-serif;color:#13306e">'
    'Конечный узел LSR8 проверяет, что указанный в Echo Request FEC соответствует завершению<br>проверяемого LSP на этом узле. '
    'При успешной проверке он формирует Echo Reply с кодом результата.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i51-p" style="left:302px;top:238px;width:1134px;height:386px"></div>',
    '<div class="i51-t" style="left:302px;top:254px;width:1134px;text-align:center;font:900 30px/1 Golos Text;color:#13306e">'
    'Запрос — по проверяемому LSP; ответ — по IP</div>',
    '<div style="position:absolute;left:398px;top:310px;width:842px;height:140px;background:#c4e8e0;border-radius:24px"></div>',
    SVG,
    '<div class="i51-t" style="left:640px;top:318px;font-size:20px;font-weight:600;color:#13306e">Проверяемый однонаправленный LSP</div>',
    '<div class="i51-t i51-fly" style="left:752px;top:354px;font-weight:700;color:#e2342b">Echo Request + FEC</div>',
    rt(416, "LSR1", "Инициатор<br>проверки"), rt(660, "LSR"), rt(906, "LSR"), rt(1124, "LSR8", "Конечный узел<br>LSP"),
    '<div class="i51-t" style="left:1280px;top:370px;width:142px;height:68px;background:#fbefc4;border:2px solid #1d3f8a;border-radius:6px;'
    'box-sizing:border-box;text-align:center;font:600 21px/1.2 Golos Text;color:#13306e;padding-top:6px">Проверка<br>'
    'FEC <span style="color:#22a33a;font-weight:900">✓</span></div>',
    '</div>',
    '<div class="step">',
    '<div class="i51-t" style="left:788px;top:543px;font:700 23px/1 Golos Text;color:#13306e">IP-сеть</div>',
    '<div class="i51-t" style="left:696px;top:590px;font-weight:700;color:#1f63c6">Echo Reply: UDP в IP-пакете</div>',
    '</div>',
    card(254, 384, 1, "#4fb08a", "Проверка назначения",
         "Узел проверяет FEC<br>и возвращает код результата:<br>достижение узла само по себе<br>ещё не означает успех теста."),
    card(650, 394, 2, "#f2694a", "Обратный маршрут",
         "В рассматриваемом режиме<br>ответ идёт по обычной<br>IP-маршрутизации. Обратный<br>LSP не требуется, но нужна<br>"
         "IP-достижимость LSR1.", 19),
    card(1056, 380, 3, "#3d8fe6", "Если ответа нет",
         "Возможен сбой LSP,<br>обратного IP-пути или<br>обработки запроса.<br><span style='font-size:16px'>Для локализации используют<br>"
         "LSP Traceroute и дополнительные<br>проверки.</span>", 18),
    '<div class="step">',
    '<div class="i51-t" style="left:244px;top:842px;width:1186px;height:76px;background:#f5d24a;border:2px solid #1f63c6;border-radius:12px;'
    'box-sizing:border-box;text-align:center;font:700 24px/1.25 Golos Text,sans-serif;color:#13306e;padding-top:8px">'
    '<b style="font-weight:900">Успешный Echo Reply</b> подтверждает результат конкретной проверки.<br>Отсутствие ответа требует диагностики.</div>',
    img("i51a_bulb.png", "left:340px;top:848px;width:62px"),
    '</div>',
])
