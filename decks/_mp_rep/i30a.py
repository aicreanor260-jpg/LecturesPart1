# -*- coding: utf-8 -*-
"""pptx: LDP — Label Mapping и упорядоченное распределение меток. Фон bgk_15 (Порко и Джина в самолёте справа внизу)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 52

CSS = """<style>
.i30-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i30-h{position:absolute;font:900 31px/1 "Rubik",sans-serif;color:#13306e;letter-spacing:.01em}
.i30-t{position:absolute;font:500 20px/1.25 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i30-n{position:absolute;font:800 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i30-zone{position:absolute;background:#c6ece4;border-radius:22px}
.i30-bar{position:absolute;background:#c6ece4;border-radius:14px;font:600 21px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i30-lm{position:absolute;background:#f8846b;color:#fff;font:600 19px/32px "Golos Text",sans-serif;padding:0 18px;border-radius:7px}
.i30-pk{position:absolute;display:flex;height:40px;border:2px solid #1d3f8a;border-radius:3px 12px 3px 3px;overflow:hidden;font:600 21px/36px "Golos Text",sans-serif}
.i30-pk b{background:#f2694a;color:#1d1d1d;padding:0 16px;font-weight:600}.i30-pk i{background:#fff;color:#1d3f8a;padding:0 24px;font-style:normal}
.i30-cl{position:absolute;background:#fff;border:2px solid #1d3f8a;border-radius:50%/50%;font:600 21px/52px "Golos Text",sans-serif;
 color:#13306e;text-align:center;width:160px;height:52px}
.i30-tb{position:absolute;border-collapse:collapse;font:500 21px/1 "Golos Text",sans-serif;color:#1d2a44;background:#fff}
.i30-tb th{background:#d6ebfb;font-weight:600;color:#13306e;height:34px;border:1px solid #1d3f8a}
.i30-tb td{text-align:center;height:32px;border:1px solid #1d3f8a}
.i30-pill{position:absolute;background:#c6ece4;border-radius:16px;font:600 21px/1.15 "Golos Text",sans-serif;color:#13306e;padding:10px 24px}
.i30-fly{animation:i30f 3s ease-in-out infinite}
@keyframes i30f{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""

SVG0 = ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
        '<defs><marker id="i30r" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="#f2694a"/></marker>'
        '<marker id="i30b" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="#1f5fa8"/></marker></defs>')


def rt(x, y, name, w=118):
    return img("i30a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i30-n" style="left:%dpx;top:%dpx">%s</div>' % (x + w // 2 - 70, y + 82, name)


def pk(x, y, lab):
    return '<div class="i30-pk i30-fly" style="left:%dpx;top:%dpx"><b>%s</b><i>IP</i></div>' % (x, y, lab)


HTML = CSS + bg("bgk_15") + "".join([
    '<div class="step"><div class="i30-pill" style="left:828px;top:62px">Ordered Control +<br>Downstream on Demand</div></div>',
    # ---- блок 1
    '<div class="step">',
    '<div class="i30-p" style="left:38px;top:150px;width:1292px;height:276px"></div>',
    '<div class="i30-h" style="left:62px;top:164px">СНАЧАЛА — МЕТКА ОТ СОСЕДА НИЖЕ ПО ПОТОКУ</div>',
    '<div class="i30-zone" style="left:66px;top:198px;width:1234px;height:168px"></div>',
    '<div class="i30-bar" style="left:66px;top:376px;width:1234px">LSR2 объявляет метку вверх по потоку после получения метки снизу по потоку.</div>',
    SVG0 + '<line x1="608" y1="254" x2="300" y2="254" stroke="#f2694a" stroke-width="5" marker-end="url(#i30r)"/>'
    '<line x1="1078" y1="254" x2="752" y2="254" stroke="#f2694a" stroke-width="5" marker-end="url(#i30r)"/></svg>',
    rt(163, 212, "LSR1"), rt(615, 212, "LSR2"), rt(1085, 212, "LSR3"),
    '<div class="i30-lm" style="left:348px;top:214px">2. Label Mapping: 199</div>',
    '<div class="i30-lm" style="left:804px;top:214px">1. Label Mapping: 231</div>',
    '<div class="i30-t" style="left:420px;top:316px;width:520px">Получает метку 231 от LSR3,<br>затем назначает свою метку 199 для LSR1.</div>',
    '</div>',
    # ---- блок 2
    '<div class="step">',
    '<div class="i30-p" style="left:38px;top:440px;width:1292px;height:266px"></div>',
    '<div class="i30-h" style="left:62px;top:454px">LSP2 ГОТОВ: ДАННЫЕ ИДУТ ПО МЕТКАМ</div>',
    '<div class="i30-zone" style="left:66px;top:494px;width:974px;height:164px"></div>',
    '<div class="i30-bar" style="left:66px;top:664px;width:1180px">Несколько сетей могут использовать общий путь при одинаковой обработке.</div>',
    SVG0 + ''.join('<line x1="%d" y1="550" x2="%d" y2="550" stroke="#1f5fa8" stroke-width="4" marker-end="url(#i30b)"/>' % (a, b)
                   for a, b in [(246, 290), (446, 492), (612, 658), (804, 866)]) +
    '<line x1="228" y1="640" x2="890" y2="640" stroke="#1d3f8a" stroke-width="2"/><line x1="228" y1="628" x2="228" y2="652" stroke="#1d3f8a" stroke-width="2"/>'
    '<line x1="890" y1="628" x2="890" y2="652" stroke="#1d3f8a" stroke-width="2"/>'
    '<line x1="982" y1="540" x2="1068" y2="488" stroke="#1f5fa8" stroke-width="4" marker-end="url(#i30b)"/>'
    '<line x1="986" y1="550" x2="1080" y2="550" stroke="#1f5fa8" stroke-width="4" marker-end="url(#i30b)"/>'
    '<line x1="982" y1="562" x2="1074" y2="610" stroke="#1f5fa8" stroke-width="4" marker-end="url(#i30b)"/></svg>',
    rt(132, 510, "LSR1"), rt(500, 510, ""), rt(876, 510, "LSR3"),
    pk(300, 530, "199"), pk(668, 530, "231"),
    '<div class="i30-t" style="left:440px;top:596px;width:240px">Swap <b>199</b> → 231</div>',
    '<div class="i30-n" style="left:506px;top:629px;background:#c6ece4">LSP2</div>',
    '<div class="i30-cl" style="left:1086px;top:458px">132.100.0.0</div>',
    '<div class="i30-cl" style="left:1096px;top:522px">194.15.17.0</div>',
    '<div class="i30-cl" style="left:1096px;top:590px">201.25.10.0</div>',
    '</div>',
    # ---- таблицы
    '<div class="step">',
    '<div class="i30-p" style="left:38px;top:722px;width:458px;height:190px"></div>',
    '<div class="i30-h" style="left:62px;top:736px;font-size:25px">МАРШРУТЫ НА LSR1</div>',
    '<table class="i30-tb" style="left:64px;top:770px;width:414px"><tr><th>Сеть</th><th>Следующий хоп</th></tr>'
    '<tr><td>132.100.0.0</td><td>LSR2</td></tr><tr><td>194.15.17.0</td><td>LSR2</td></tr><tr><td>201.25.10.0</td><td>LSR2</td></tr></table>',
    '<div class="i30-p" style="left:508px;top:722px;width:612px;height:190px"></div>',
    '<div class="i30-h" style="left:530px;top:736px;font-size:25px">ЗАПИСЬ ПРОДВИЖЕНИЯ LSR2</div>',
    '<table class="i30-tb" style="left:530px;top:772px;width:570px"><tr><th>Входная метка</th><th>Выходная метка</th><th>Следующий хоп</th></tr>'
    '<tr><td>199</td><td>231</td><td>LSR3</td></tr></table>',
    '<div class="i30-t" style="left:530px;top:850px;width:560px;text-align:left;font-size:18px">Метки локальны: 231 может использоваться<br>'
    'на другом узле для другогло пути.</div>',
    '</div>',
])
