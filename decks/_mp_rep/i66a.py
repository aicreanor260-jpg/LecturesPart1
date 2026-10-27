# -*- coding: utf-8 -*-
"""pptx: Проблемы пересылки MPLS — сложности настройки и плоскости управления, фон bgk_11."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i66-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i66-h{position:absolute;font:900 29px/1.05 "Rubik",sans-serif;color:#13306e}
.i66-t{position:absolute;font:500 19px/1.18 "Golos Text",sans-serif;color:#1d2a44}
.i66-li{position:absolute;padding-left:36px;font:500 18.3px/1.18 "Golos Text",sans-serif;color:#1d2a44}
.i66-li::before{content:"";position:absolute;left:0;top:5px;width:16px;height:16px;border-radius:50%;background:var(--c)}
.i66-ft{position:absolute;border-radius:12px;font:800 24px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center;display:flex;align-items:center;justify-content:center}
.i66-lb{position:absolute;border:2px solid #1d3f8a;border-radius:4px;font:700 19px/30px "Golos Text",sans-serif;color:#13306e;padding:0 8px}
.i66-lsp{position:absolute;border:2px solid #1d3f8a;border-radius:4px;font:800 20px/36px "Golos Text",sans-serif;color:#13306e;padding:0 12px}
.i66-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e}
.i66-env{animation:i66f 2.8s ease-in-out infinite}
@keyframes i66f{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
</style>"""


def li(x, y, col, text):
    return '<div class="i66-li" style="left:%dpx;top:%dpx;--c:%s">%s</div>' % (x, y, col, text)


def rt(x, y, w=78):
    return img("i66a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


M = ('<marker id="i66m%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="%s" markerHeight="%s" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>')

HTML = CSS + bg("bgk_11") + "".join([
    '<div class="step">',
    '<div class="i66-p" style="left:162px;top:156px;width:1346px;height:88px"></div>',
    '<div class="i66-t" style="left:162px;top:170px;width:1346px;text-align:center;font:600 24px/1.3 Golos Text,sans-serif;color:#13306e">'
    'Метки настраиваются статически или распределяются динамически.<br>Основные сложности связаны с управлением сетью и её масштабированием.</div>',
    '</div>',
    # 1
    '<div class="step">',
    '<div class="i66-p" style="left:162px;top:256px;width:458px;height:452px"></div>',
    img("i66a_n1.png", "left:175px;top:268px;width:73px"),
    '<div class="i66-h" style="left:272px;top:268px">Статическое<br>распределение</div>',
    img("i66a_eng.png", "left:183px;top:328px;width:139px"),
    '<div style="position:absolute;left:356px;top:418px;width:200px;height:4px;background:#1d3f8a"></div>',
    rt(318, 390), rt(422, 390), rt(526, 390),
    '<div class="i66-lb" style="left:334px;top:356px;background:#f27a64">100</div>',
    '<div class="i66-lb" style="left:436px;top:356px;background:#f6c34d">200</div>',
    '<div class="i66-lb" style="left:538px;top:356px;background:#79d6b4">300</div>',
    li(186, 488, "#f2694a", "Ручная настройка меток на устройствах"),
    li(186, 520, "#f2694a", "При изменении топологии конфигурацию<br>нужно обновлять"),
    li(186, 572, "#f2694a", "Рост сети увеличивает трудоёмкость<br>и риск ошибок"),
    '<div class="i66-ft" style="left:178px;top:638px;width:428px;height:52px;background:#f7836c">Сложно масштабировать</div>',
    '</div>',
    # 2
    '<div class="step">',
    '<div class="i66-p" style="left:630px;top:256px;width:438px;height:452px"></div>',
    img("i66a_n2.png", "left:645px;top:268px;width:73px"),
    '<div class="i66-h" style="left:740px;top:268px">Динамическое<br>распределение</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' +
    M % ("a", 6, 6, "#1d3f8a") + '</defs>'
    '<path d="M790 372 L816 366" style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:5 4" marker-end="url(#i66ma)"/>'
    '<path d="M732 410 L752 392" style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:5 4" marker-start="url(#i66ma)"/>'
    '<path d="M892 366 L912 372" style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:5 4" marker-start="url(#i66ma)"/>'
    '<path d="M950 392 L968 410" style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:5 4" marker-end="url(#i66ma)"/>'
    '<path d="M782 440 L830 440 M872 440 L930 440" style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:5 4" marker-start="url(#i66ma)" marker-end="url(#i66ma)"/>'
    '</svg>',
    rt(820, 340), rt(703, 410), rt(933, 410),
    '<div class="i66-env" style="position:absolute;left:0;top:0">',
    img("i66a_env.png", "left:750px;top:364px;width:40px"), img("i66a_env.png", "left:914px;top:364px;width:40px"),
    img("i66a_env.png", "left:832px;top:432px;width:40px"), '</div>',
    li(656, 486, "#5fcfa6", "LDP использует маршруты IGP,<br>а не рассчитывает TE-путь"),
    li(656, 538, "#5fcfa6", "Нужно поддерживать соседства,<br>сеансы и таблицы меток"),
    li(656, 590, "#5fcfa6", "Служебный обмен расходует полосу,<br>CPU и память"),
    '<div class="i66-ft" style="left:648px;top:640px;width:404px;height:52px;background:#86dcc0;font-size:22px">Автоматизация требует ресурсов</div>',
    '</div>',
    # 3
    '<div class="step">',
    '<div class="i66-p" style="left:1078px;top:256px;width:430px;height:452px"></div>',
    img("i66a_n3.png", "left:1093px;top:268px;width:73px"),
    '<div class="i66-h" style="left:1194px;top:280px">Traffic Engineering</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' +
    M % ("r", 4, 4, "#f2694a") + M % ("g", 4, 4, "#3fb894") + '</defs>'
    '<path d="M1196 396 Q1220 364 1268 362 L1388 362" style="fill:none;stroke:#f2694a;stroke-width:6" marker-end="url(#i66mr)"/>'
    '<path d="M1196 408 Q1220 434 1268 434 L1388 434" style="fill:none;stroke:#3fb894;stroke-width:6" marker-end="url(#i66mg)"/>'
    '</svg>',
    rt(1110, 374, 90), rt(1404, 340, 72), rt(1404, 412, 72),
    '<div class="i66-lsp" style="left:1270px;top:344px;background:#f7836c">LSP A</div>',
    '<div class="i66-lsp" style="left:1270px;top:416px;background:#86dcc0">LSP B</div>',
    '<div class="i66-n" style="left:1134px;top:448px">LER</div>',
    li(1104, 486, "#f6b73c", "RSVP-TE добавляет сигнализацию<br>и состояние для LSP"),
    li(1104, 538, "#f6b73c", "Много туннелей усложняет настройку<br>и сопровождение"),
    li(1104, 590, "#f6b73c", "Распределение нагрузки требует<br>подходящих механизмов и настроек"),
    '<div class="i66-ft" style="left:1098px;top:640px;width:398px;height:60px;background:#f8cd4f;font-size:22px">Больше возможностей —<br>сложнее управление</div>',
    '</div>',
    # учитывать
    '<div class="step">',
    '<div class="i66-p" style="left:234px;top:722px;width:1346px;height:92px;border-radius:14px"></div>',
    '<div class="i66-h" style="left:256px;top:752px;font-size:28px">Что важно учитывать</div>',
    '<div style="position:absolute;left:594px;top:740px;width:2px;height:56px;background:#7aa3d8"></div>',
    '<div style="position:absolute;left:1058px;top:740px;width:2px;height:56px;background:#7aa3d8"></div>',
    img("i66a_db.png", "left:616px;top:740px;width:68px"),
    '<div class="i66-t" style="left:698px;top:738px;font-size:16.5px;line-height:1.3">Объём служебной нагрузки зависит<br>от протокола, числа соседей, туннелей<br>и настроек.</div>',
    img("i66a_gear.png", "left:1084px;top:738px;width:68px"),
    '<div class="i66-t" style="left:1170px;top:738px;font-size:16.5px;line-height:1.3">Балансировка нагрузки в MPLS возможна;<br>её поддержка и способ реализации зависят<br>от технологии и оборудования.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i66-p" style="left:338px;top:828px;width:1060px;height:98px;background:#1f63c6;border-color:#174ea0;border-radius:14px"></div>',
    img("i66a_tgt.png", "left:391px;top:843px;width:86px"),
    '<div style="position:absolute;left:510px;top:846px;width:3px;height:62px;background:#fff"></div>',
    '<div class="i66-h" style="left:538px;top:838px;font:800 31px/1.22 Golos Text,sans-serif;color:#fff">Задача: уменьшить сложность управления,<br>сохранив гибкость и отказоустойчивость.</div>',
    '</div>',
])
