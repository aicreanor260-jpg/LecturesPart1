# -*- coding: utf-8 -*-
"""pptx: MPLS-метка — стек LIFO и таблица значений — вёрстка поверх bgk_27."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg

W, H, TOP = 1672, 941, 100

CSS = """<style>
.i16-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i16-h{position:absolute;font:800 36px/1 "Golos Text",sans-serif;color:#13306e}
.i16-t{position:absolute;font:500 22px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i16-c{position:absolute;font:600 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i16-row{position:absolute;display:flex;border:2px solid #1d3f8a;border-left:8px solid #8cbde6;border-right:8px solid #8cbde6;border-radius:4px;overflow:hidden}
.i16-row div{font:600 20px/48px "Golos Text",sans-serif;color:#13306e;text-align:center;border-left:2px solid #1d3f8a}
.i16-row div:first-child{border-left:0}
.i16-rg{position:absolute;background:#ccefea;border-radius:16px}
.i16-v{position:absolute;font:800 28px/54px "Golos Text",sans-serif;color:#13306e;text-align:center;border-radius:8px}
.i16-tb{position:absolute;border-collapse:collapse;font:500 19.5px/30.3px "Golos Text",sans-serif;color:#1d2a44}
.i16-tb th{background:#13306e;color:#fff;font-weight:700;line-height:36px;font-size:22px}
.i16-tb td{border-bottom:1px solid #fff}
.i16-tb tr:nth-child(odd) td{background:#d9f0ec}.i16-tb tr:nth-child(even) td{background:#eef8f5}
.i16-tb td:first-child{text-align:center;font-weight:700;color:#13306e}
.i16-tb td+td,.i16-tb th+th{border-left:2px solid #13306e;padding-left:26px}
.i16-tb td+td+td{padding-left:24px}
.i16-up{animation:i16u 2.4s ease-in-out infinite}
@keyframes i16u{0%,100%{transform:translate(0,0)}50%{transform:translate(4px,-6px)}}
</style>"""

ROWS = [("0", "IPv4 Explicit NULL", "Снять метку; при S=1 продолжить пересылку по IPv4."),
        ("1", "Router Alert", "Передать пакет на локальную обработку."),
        ("2", "IPv6 Explicit NULL", "Снять метку; при S=1 продолжить пересылку по IPv6."),
        ("3", "Implicit NULL", "Сигнал снять метку (PHP); в пакете не передаётся."),
        ("4", "MPLS Network Actions", "Индикатор сетевых действий MPLS."),
        ("7", "Entropy Label Indicator (ELI)", "Указывает на следующую метку энтропии."),
        ("5–6, 8–12", "Не назначены", "Значения служебного диапазона без назначения."),
        ("13", "Generic Associated Channel Label", "Указывает на связанный служебный канал."),
        ("14", "OAM Alert", "Обработка пакетов OAM."),
        ("15", "Extension Label (XL)", "Расширение пространства служебных меток."),
        ("16–1 048 575", "Обычные метки", "Используются для продвижения трафика MPLS.")]

HTML = CSS + bg("bgk_27") + "".join([
    '<div class="step">',
    '<div class="i16-p" style="left:168px;top:106px;width:754px;height:302px"></div>',
    '<div class="i16-h" style="left:196px;top:120px">Стек меток: принцип LIFO</div>',
    '<div class="i16-t" style="left:196px;top:166px;width:700px">Последняя добавленная метка обрабатывается первой.<br>'
    'Операции выполняются с верхней меткой стека.</div>',
    '<div class="i16-c" style="left:376px;top:238px;width:346px">Стек MPLS-меток</div>',
    '<div class="i16-row" style="left:378px;top:262px;width:346px;height:12px;border:2px solid #1d3f8a;border-bottom:0;border-radius:4px 4px 0 0"></div>',
    '<div class="i16-row" style="left:198px;top:280px;width:700px">'
    '<div style="width:170px;background:#cfe0f6">Заголовок L2</div><div style="width:178px;background:#f7845f">Верхняя метка</div>'
    '<div style="width:170px;background:#fbd56a">Нижняя метка</div><div style="flex:1;background:#fff">IP-пакет</div></div>',
    '<div class="i16-c" style="left:420px;top:340px;width:110px">S = 0</div>',
    '<div class="i16-c" style="left:586px;top:340px;width:110px">S = 1</div>',
    '<div class="i16-up" style="position:absolute;left:380px;top:336px"><svg width="40" height="60"><path d="M6 56 L28 12" '
    'style="stroke:#13306e;stroke-width:5"/><path d="M34 0 L16 14 L34 22Z" style="fill:#13306e"/></svg></div>',
    '<div class="i16-c" style="left:418px;top:372px;width:200px;text-align:left;font-size:22px">Push / Swap / Pop</div>',
    '</div>',
    '<div class="step">',
    '<div class="i16-p" style="left:936px;top:106px;width:604px;height:302px"></div>',
    '<div class="i16-h" style="left:960px;top:120px">Диапазоны значений</div>',
    '<div class="i16-rg" style="left:954px;top:174px;width:568px;height:76px"></div>',
    '<div class="i16-v" style="left:966px;top:186px;width:138px;background:#f7845f">0 –15</div>',
    '<div class="i16-t" style="left:1116px;top:198px;width:400px">— базовые служебные метки.</div>',
    '<div class="i16-rg" style="left:954px;top:264px;width:568px;height:128px"></div>',
    '<div class="i16-v" style="left:966px;top:278px;width:176px;background:#fbd56a;font-size:26px">16–1 048 575</div>',
    '<div class="i16-t" style="left:1154px;top:286px;width:360px;font-size:20.5px">— обычные метки; выделяются, например, LDP и MP-BGP, '
    'а также другими механизмами MPLS.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i16-p" style="left:226px;top:422px;width:1224px;height:492px"></div>',
    '<div class="i16-h" style="left:252px;top:436px">Таблица значений MPLS-меток</div>',
    '<table class="i16-tb" style="left:246px;top:482px;width:1184px"><tr><th style="width:178px">Значение</th><th style="width:382px">Название</th>'
    '<th>Назначение</th></tr>',
    "".join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in ROWS),
    '</table>',
    '<div class="i16-t" style="left:254px;top:876px;width:600px;font-size:16.5px">Служебные значения: реестр IANA, 2026.</div>',
    '</div>',
])
