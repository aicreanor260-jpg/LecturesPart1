# -*- coding: utf-8 -*-
"""pptx: Таблицы MPLS — сигнальные протоколы LDP / RSVP-TE — вёрстка поверх bgk_23."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 104

CSS = """<style>
.i18-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i18-t{position:absolute;font:500 22px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i18-hd{position:absolute;border-radius:14px}
.i18-big{position:absolute;font:900 50px/1 "Golos Text",sans-serif;color:#13306e}
.i18-sm{position:absolute;font:500 17px/1.2 "Golos Text",sans-serif;color:#1d2a44}
.i18-sm b{display:block;font:800 21px/1.5 "Golos Text",sans-serif;color:#13306e}
.i18-c{position:absolute;font:600 19px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i18-tb{position:absolute;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;background:#fff}
.i18-tb div{font:700 19px/34px "Golos Text",sans-serif;color:#13306e;text-align:center;border-bottom:3px solid #1d3f8a}
.i18-tb span{display:block;height:22px;border-bottom:2px solid #1d3f8a;background:linear-gradient(90deg,transparent 33%,#1d3f8a 33%,#1d3f8a calc(33% + 2px),transparent calc(33% + 2px),transparent 66%,#1d3f8a 66%,#1d3f8a calc(66% + 2px),transparent calc(66% + 2px))}
.i18-tb span:last-child{border-bottom:0}
.i18-ex{position:absolute;font:900 34px/1 "Golos Text",sans-serif;color:#1d7a6a}
.i18-ar{position:absolute;height:4px;background:#1f8fd8}
.i18-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:9px solid transparent;border-left:13px solid #1f8fd8;border-right:0}
.i18-ra{position:absolute;height:3px;background:#e2332a}
.i18-ra::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #e2332a;border-right:0}
.i18-flow{animation:i18f 2.4s ease-in-out infinite}
@keyframes i18f{0%,100%{opacity:1}50%{opacity:.45}}
</style>"""


def tb(x, y, w, head, col):
    return '<div class="i18-tb" style="left:%dpx;top:%dpx;width:%dpx"><div style="background:%s">%s</div><span></span><span></span></div>' % (
        x, y, w, col, head)


HTML = CSS + bg("bgk_23") + "".join([
    '<div class="step"><div style="position:absolute;left:100px;top:106px;width:1000px;text-align:left;font:800 32px/1.2 Rubik,sans-serif;color:#fffbe8;text-shadow:0 2px 0 #1550a8,0 3px 8px rgba(10,40,90,.5)">Сигнальные протоколы и формирование таблиц</div></div>',
    '<div class="step">',
    '<div class="i18-p" style="left:100px;top:158px;width:1146px;height:94px"></div>',
    '<div class="i18-t" style="left:126px;top:168px;width:1100px;font:600 28px/1.32 Golos Text,sans-serif;color:#13306e">'
    'Сигнальные протоколы обмениваются информацией о метках<br>и участвуют в формировании таблиц MPLS на каждом LSR.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i18-p" style="left:100px;top:268px;width:570px;height:438px"></div>',
    '<div class="i18-hd" style="left:114px;top:276px;width:542px;height:74px;background:#ccefea"></div>',
    '<div class="i18-big" style="left:134px;top:288px">LDP</div>',
    '<div class="i18-sm" style="left:272px;top:288px;width:380px">Label Distribution Protocol<b>Протокол распределения меток</b></div>',
    '<div class="i18-t" style="left:134px;top:354px;width:520px">Согласует метки для классов FEC<br>между соседними маршрутизаторами.<br>'
    'LSP обычно следует маршрутам IGP.</div>',
    img("i18a_rt.png", "left:144px;top:466px;width:108px"), img("i18a_rt.png", "left:330px;top:466px;width:108px"),
    img("i18a_rt.png", "left:516px;top:466px;width:108px"),
    '<div class="i18-ex i18-flow" style="left:258px;top:484px">⇄</div><div class="i18-ex i18-flow" style="left:444px;top:484px">⇄</div>',
    '<div class="i18-c" style="left:130px;top:556px;width:500px">Обмен соответствиями FEC ↔ метка</div>',
    tb(240, 596, 288, "Метки и FEC", "#c7ead9"),
    '</div>',
    '<div class="step">',
    '<div class="i18-p" style="left:684px;top:268px;width:634px;height:438px"></div>',
    '<div class="i18-hd" style="left:698px;top:276px;width:606px;height:74px;background:#fbd6cc"></div>',
    '<div class="i18-big" style="left:712px;top:290px;font-size:46px">RSVP-TE</div>',
    '<div class="i18-sm" style="left:926px;top:290px;width:380px;font-size:15px">Resource Reservation Protocol — Traffic Engineering'
    '<b style="font-size:18px">RSVP с расширениями для MPLS TE</b></div>',
    '<div class="i18-t" style="left:714px;top:354px;width:560px">Сигнализирует LSP с учётом<br>заданного пути и требований к ресурсам.<br>'
    'Поддерживает резервирование ресурсов.</div>',
    '<div style="position:absolute;left:770px;top:500px;width:450px;height:48px;background:linear-gradient(90deg,rgba(242,105,74,.15),rgba(242,105,74,.4))"></div>',
    '<div class="i18-c" style="left:872px;top:462px;width:206px;height:30px;background:#f9b8a8;border-radius:8px;line-height:30px">LSP (заданный путь)</div>',
    img("i18a_g.png", "left:1120px;top:444px;width:62px"),
    '<div class="i18-c" style="left:1186px;top:448px;width:140px;font-size:13px;text-align:left;line-height:1.15">Требуемая<br>полоса пропускания</div>',
    img("i18a_rt.png", "left:734px;top:490px;width:102px"), img("i18a_rt.png", "left:936px;top:490px;width:102px"),
    img("i18a_rt.png", "left:1148px;top:490px;width:102px"),
    '<div class="i18-ra i18-flow" style="left:840px;top:528px;width:90px"></div><div class="i18-ra i18-flow" style="left:1042px;top:528px;width:100px"></div>',
    '<div class="i18-c" style="left:788px;top:568px;width:400px">Сигнализация выбранного LSP</div>',
    tb(840, 602, 324, "Параметры LSP и метки", "#f9b8a8"),
    '</div>',
    '<div class="step">',
    '<div class="i18-p" style="left:228px;top:718px;width:908px;height:178px"></div>',
    '<div class="i18-c" style="left:248px;top:728px;width:400px;text-align:left;font:900 27px/1 Rubik,sans-serif">РЕЗУЛЬТАТ НА LSR</div>',
    img("i18a_docs.png", "left:338px;top:760px;width:114px"), '<div class="i18-ar" style="left:508px;top:792px;width:52px"></div>',
    img("i18a_db.png", "left:610px;top:754px;width:82px"), '<div class="i18-ar" style="left:746px;top:792px;width:62px"></div>',
    img("i18a_tb.png", "left:874px;top:758px;width:118px"),
    '<div class="i18-c" style="left:282px;top:830px;width:240px;font-weight:500">Служебный обмен</div>',
    '<div class="i18-c" style="left:540px;top:830px;width:240px;font-weight:500">База меток (LIB)</div>',
    '<div class="i18-c" style="left:798px;top:830px;width:300px;font-weight:500">Таблица продвижения (LFIB)</div>',
    '<div class="i18-c" style="left:240px;top:868px;width:888px;font-weight:500;font-size:17.5px">'
    'На основе полученных меток и маршрутов формируются записи для пересылки пакетов.</div>',
    '</div>',
])
