# -*- coding: utf-8 -*-
"""pptx: MPLS-метка — формат заголовка — вёрстка поверх bgk_01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg

W, H, TOP = 1672, 941, 116

CSS = """<style>
.i15-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i15-h{position:absolute;font:800 34px/1 "Golos Text",sans-serif;color:#13306e}
.i15-t{position:absolute;font:500 23px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i15-t b{font-weight:800;color:#13306e}
.i15-row{position:absolute;display:flex;border:2px solid #1d3f8a;border-radius:8px;overflow:hidden}
.i15-row div{font:700 20px/46px "Golos Text",sans-serif;color:#13306e;text-align:center;border-left:2px solid #1d3f8a}
.i15-row div:first-child{border-left:0}
.i15-fmt div{font:800 25px/48px "Golos Text",sans-serif}
.i15-c{position:absolute;font:500 19px/1 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i15-br{position:absolute;height:12px;border:2px solid #1d3f8a;border-top:0}
.i15-tag{display:inline-block;font:800 22px/34px "Golos Text",sans-serif;color:#13306e;padding:0 18px;border-radius:9px;margin-bottom:4px}
.i15-d{position:absolute;font:500 18.5px/1.3 "Golos Text",sans-serif;color:#1d2a44;width:500px}
.i15-pulse{animation:i15p 2.6s ease-in-out infinite}
@keyframes i15p{0%,100%{filter:none}50%{filter:brightness(1.08)}}
</style>"""

HTML = CSS + bg("bgk_01") + "".join([
    '<div class="step">',
    '<div class="i15-p" style="left:224px;top:122px;width:1116px;height:200px"></div>',
    '<div class="i15-t" style="left:248px;top:132px;width:1080px"><b>MPLS-метка (MPLS Label)</b> — короткий идентификатор фиксированной длины: '
    '<b>20 бит.</b><br>Она имеет локальное значение и связывает пакет с FEC в соответствующем контексте меток.</div>',
    '<div class="i15-t" style="left:248px;top:201px;width:1080px">Одному FEC могут соответствовать несколько входящих меток.<br>'
    'Каждая метка в своём контексте обозначает один FEC.</div>',
    '<div class="i15-t" style="left:250px;top:268px;width:1064px;height:40px;background:#fbc0b0;border-radius:10px;padding-left:18px;'
    'font:800 23px/40px Golos Text,sans-serif;color:#13306e">Значение метки: 20 бит.&nbsp; Весь&nbsp; MPLS-заголовок: 32 бита = 4 байта.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i15-p" style="left:224px;top:332px;width:1116px;height:160px"></div>',
    '<div class="i15-h" style="left:248px;top:344px">Где расположен MPLS-заголовок</div>',
    '<div class="i15-row" style="left:250px;top:390px;width:1064px">'
    '<div style="width:240px;background:#bcdcfa">Заголовок L2</div><div style="width:336px;background:#f7a99a">MPLS-заголовок • 4 байта</div>'
    '<div style="width:226px;background:#a9e3d6">IP-заголовок</div><div style="flex:1;background:#fbe7a6">Данные</div></div>',
    '<div class="i15-br" style="left:474px;top:450px;width:580px"></div>',
    '<div class="i15-c" style="left:524px;top:458px;width:490px;white-space:nowrap;background:#fdf8ea;font-weight:600;font-size:18px">Между заголовками канального и сетевого уровней</div>',
    '</div>',
    '<div class="step">',
    '<div class="i15-p" style="left:224px;top:506px;width:1116px;height:166px"></div>',
    '<div class="i15-h" style="left:248px;top:516px">Формат MPLS-заголовка</div>',
    '<div class="i15-br" style="left:266px;top:562px;width:1034px;height:16px;border-top:0;border-bottom:0;border-left:2px solid #1d3f8a"></div>',
    '<div style="position:absolute;left:266px;top:568px;width:1034px;height:2px;background:#1d3f8a"></div>',
    '<div class="i15-c" style="left:710px;top:556px;width:180px;background:#fdf8ea;font-weight:700;color:#13306e">32 бита (4 байта)</div>',
    '<div class="i15-row i15-fmt i15-pulse" style="left:264px;top:586px;width:1038px">'
    '<div style="width:584px;background:#f7a99a">Label</div><div style="width:124px;background:#a9e3d6">TC</div>'
    '<div style="width:52px;background:#fbe7a6">S</div><div style="flex:1;background:#a8d2f8">TTL</div></div>',
    '<div class="i15-c" style="left:458px;top:648px;width:200px">20 бит</div>',
    '<div class="i15-c" style="left:850px;top:648px;width:120px">3 бита</div>',
    '<div class="i15-c" style="left:948px;top:648px;width:100px">1 бит</div>',
    '<div class="i15-c" style="left:1104px;top:648px;width:120px">8 бит</div>',
    '</div>',
    '<div class="step">',
    '<div class="i15-p" style="left:242px;top:684px;width:1088px;height:232px"></div>',
    '<div class="i15-d" style="left:264px;top:696px"><span class="i15-tag" style="background:#f7a99a">Label — 20 бит</span><br>'
    '&nbsp;Значение MPLS-метки: от 0 до 1 048 575.</div>',
    '<div class="i15-d" style="left:786px;top:696px"><span class="i15-tag" style="background:#a9e3d6">TC — 3 бита</span><br>'
    '&nbsp;Класс трафика: используется для применения<br>&nbsp;политик QoS, в том числе при перегрузке.</div>',
    '<div class="i15-d" style="left:264px;top:784px"><span class="i15-tag" style="background:#fbd56a">S — 1 бит</span><br>'
    '&nbsp;Признак дна стека. S = 1 — последняя, нижняя метка;<br>&nbsp;S = 0 — ниже есть ещё метка.</div>',
    '<div class="i15-d" style="left:786px;top:784px"><span class="i15-tag" style="background:#a8d2f8">TTL — 8 бит</span><br>'
    '&nbsp;Время жизни. Ограничивает число переходов,<br>&nbsp;выполняя роль, аналогичную TTL в IP-пакетах.</div>',
    '<div style="position:absolute;left:262px;top:878px;width:1048px;height:2px;background:#1d3f8a"></div>',
    '<div class="i15-c" style="left:262px;top:886px;width:1048px;font:700 15.5px/1 Golos Text,sans-serif;color:#13306e">'
    'MPLS поддерживает стек из нескольких меток; каждой соответствует отдельный 4-байтовый заголовок.</div>',
    '</div>',
])
