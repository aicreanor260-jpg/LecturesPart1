# -*- coding: utf-8 -*-
"""pptx: RSVP-TE — исходная схема сети и выбор пути по полосе. Фон bgk_13 (Гранмамаре справа)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 118

CSS = """<style>
.i37-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i37-h{position:absolute;font:800 36px/1 "Golos Text",sans-serif;color:#13306e}
.i37-t{position:absolute;font:500 20px/1.25 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i37-m{position:absolute;background:#d6ebfb;border-radius:8px;font:600 19px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;padding:6px 0}
.i37-n{position:absolute;background:#d6ebfb;border-radius:10px;font:800 25px/1.1 "Golos Text",sans-serif;color:#13306e;text-align:center;padding:6px 0}
.i37-n small{display:block;font:500 18px/1.2 "Golos Text",sans-serif}
.i37-tb{position:absolute;border-collapse:collapse;font:500 20px/1 "Golos Text",sans-serif;color:#1d2a44;background:#fdf8ea}
.i37-tb th{background:#d6ebfb;color:#13306e;font-weight:600;height:42px;border:1px solid #9ec3e6}
.i37-tb td{height:46px;border:1px solid #9ec3e6;text-align:center}
.i37-tb td:first-child{text-align:left;padding-left:30px}
.i37-flow{stroke-dasharray:14 10;animation:i37d 1.2s linear infinite}
@keyframes i37d{to{stroke-dashoffset:-24}}
</style>"""

SVG = ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
       '<path d="M390,388 C410,362 440,366 470,368 L740,368" stroke="#8b9db8" stroke-width="6" fill="none"/>'
       '<path d="M752,368l-20,-10v20z" fill="#8b9db8"/>'
       '<path d="M892,368 L1210,368 C1250,370 1280,380 1300,392" stroke="#ef5a4e" stroke-width="6" fill="none"/>'
       '<path d="M1252,368l-20,-10v20z" fill="#ef5a4e"/>'
       '<path d="M390,440 C410,490 420,532 470,532 L630,532 M740,532 L938,532 M1046,532 L1220,532 C1260,532 1270,470 1300,440" '
       'stroke="#7be08f" stroke-width="16" fill="none" opacity=".45"/>'
       '<path d="M390,440 C410,490 420,532 470,532 L630,532 M740,532 L938,532 M1046,532 L1220,532 C1260,532 1270,470 1300,440" '
       'stroke="#22a052" stroke-width="5" fill="none"/>'
       '<path class="i37-flow" d="M470,532 L630,532 M740,532 L938,532 M1046,532 L1220,532" stroke="#e9ffe9" stroke-width="2" fill="none"/>'
       '<path d="M600,532l-20,-10v20z M910,532l-20,-10v20z M1220,532l-20,-10v20z" fill="#22a052"/></svg>')

HTML = CSS + bg("bgk_13") + "".join([
    '<div class="step">',
    '<div class="i37-p" style="left:186px;top:126px;width:1290px;height:52px;border-radius:14px"></div>',
    '<div class="i37-t" style="left:186px;top:138px;width:1290px;font:800 24px/1.2 Golos Text,sans-serif;color:#13306e">'
    'RSVP-TE устанавливает LSP в MPLS-сети, распределяет метки и резервирует ресурсы пути.</div>',
    '<div class="i37-t" style="left:186px;top:188px;width:1290px;color:#fff;font-size:22px;text-shadow:0 1px 4px #0a2a5c,0 0 10px #0a3a7c">'
    'MPLS Traffic Engineering: выбор пути с учётом доступной полосы и заданных ограничений.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i37-p" style="left:204px;top:230px;width:1268px;height:390px"></div>',
    '<div class="i37-h" style="left:234px;top:248px">Исходная схема сети</div>',
    '<div class="i37-t" style="left:706px;top:244px;width:660px;height:48px;background:#f8956f;border-radius:24px;'
    'font:800 28px/48px Golos Text,sans-serif;color:#13306e">LER1 → LER2 &nbsp;•&nbsp; Требуется 100 Мбит/с</div>',
    SVG,
    img("i37a_rt.png", "left:272px;top:365px;width:123px"), img("i37a_rt.png", "left:778px;top:318px;width:117px"),
    img("i37a_rt.png", "left:1288px;top:368px;width:120px"), img("i37a_rt.png", "left:626px;top:486px;width:117px"),
    img("i37a_rt.png", "left:932px;top:486px;width:117px"),
    '<div class="i37-n" style="left:258px;top:450px;width:140px">LER1<small>Входной</small></div>',
    '<div class="i37-n" style="left:1284px;top:450px;width:144px">LER2<small>Выходной</small></div>',
    '<div class="i37-n" style="left:770px;top:396px;width:136px">LSR3</div>',
    '<div class="i37-n" style="left:618px;top:564px;width:132px">LSR1</div>',
    '<div class="i37-n" style="left:928px;top:564px;width:132px">LSR2</div>',
    '<div class="i37-m" style="left:510px;top:308px;width:170px">Метрика 10<br>200 Мбит/с</div>',
    '<div class="i37-m" style="left:1012px;top:308px;width:174px">Метрика 10<br><span style="color:#d63b2f">40 Мбит/с</span></div>',
    '<div class="i37-m" style="left:452px;top:462px;width:136px">Метрика 20<br>150 Мбит/с</div>',
    '<div class="i37-m" style="left:756px;top:462px;width:166px">Метрика 20<br>150 Мбит/с</div>',
    '<div class="i37-m" style="left:1070px;top:462px;width:168px">Метрика 20<br>150 Мбит/с</div>',
    '<div class="i37-m" style="left:1000px;top:378px;width:224px;background:#fbc9c2;font-weight:800;color:#c0302a;font-size:20px">'
    '<span style="display:inline-block;width:30px;height:30px;border-radius:50%;background:#d63b2f;color:#fff;vertical-align:middle;'
    'margin-right:8px;line-height:30px">!</span>40 &lt; 100 —<br>недостаточно</div>',
    '<div class="i37-t" style="left:752px;top:580px;width:176px;height:32px;background:#1f8a5e;border-radius:16px;color:#fff;'
    'font:700 18px/32px Golos Text,sans-serif">Выбранный путь</div>',
    '</div>',
    '<div class="step">',
    '<div class="i37-p" style="left:250px;top:634px;width:1214px;height:156px"></div>',
    '<table class="i37-tb" style="left:270px;top:642px;width:1178px"><tr><th>Путь</th><th style="width:226px">Метрика</th>'
    '<th style="width:318px">Мин. доступная полоса</th><th style="width:262px">Результат</th></tr>'
    '<tr><td>LER1 → LSR3 → LER2</td><td>20</td><td>40 Мбит/с</td>'
    '<td style="background:#fbd4d0;color:#c0302a;font-weight:800">Не подходит</td></tr>'
    '<tr><td>LER1 → LSR1 → LSR2 → LER2</td><td>60</td><td>150 Мбит/с</td>'
    '<td style="background:#cdeec8;color:#1d7a3a;font-weight:800">Подходит</td></tr></table>',
    '</div>',
    '<div class="step">',
    '<div class="i37-p" style="left:334px;top:806px;width:754px;height:104px;background:#dff5e3"></div>',
    img("i37a_ok.png", "left:350px;top:818px;width:82px"),
    '<div class="i37-t" style="left:450px;top:822px;text-align:left;font-size:22px"><span style="font:800 29px Golos Text,sans-serif;color:#13306e">'
    'Выбираем нижний путь:</span><br>на каждом участке можно зарезервировать 100 Мбит/с.</div>',
    '<div class="i37-p" style="left:1106px;top:802px;width:406px;height:110px;background:#fdf0c8"></div>',
    img("i37a_bulb.png", "left:1118px;top:814px;width:74px"),
    '<div class="i37-t" style="left:1202px;top:814px;text-align:left;font-size:17px">Доступная полоса — ресурс<br>для резервирования TE,<br>'
    'а не текущая свободная скорость<br>интерфейса.</div>',
    '</div>',
])
