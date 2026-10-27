# -*- coding: utf-8 -*-
"""pptx: туннель 2 — расчёт пути, резервирование, выбор трафика — вёрстка поверх bgk_24."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 152

CSS = """<style>
.i58-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i58-h{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i58-t{position:absolute;font:500 21px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i58-num{position:absolute;width:56px;height:56px;border-radius:50%;background:#13306e;color:#fff;font:900 32px/56px "Rubik";text-align:center}
.i58-n{position:absolute;font:800 26px/1 "Golos Text",sans-serif;color:#13306e;width:120px;text-align:center}
.i58-pl{position:absolute;border-radius:16px;font:500 19px/36px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i58-ar{position:absolute;height:4px;background:#1d3f6e;color:#1d3f6e}
.i58-ar::after{content:"";position:absolute;right:-4px;top:-8px;border:10px solid transparent;border-left:16px solid currentColor;border-right:0}
.i58-bx{position:absolute;border-radius:12px}
.i58-k{position:absolute;font:500 16px/1.2 "Golos Text",sans-serif;color:#1d2a44;text-align:center;width:130px}
.i58-ks{position:absolute;width:0;height:130px;border-left:1px solid #9aa8b8}
.i58-pulse{animation:i58p 2.4s ease-in-out infinite}
@keyframes i58p{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}
</style>"""


def rt(x, f):
    return img(f, "left:%dpx;top:300px;width:124px" % x)


NODES = [(348, "i58a_rr.png", "LER5", "Заданные концы", "#f8b8a6", 316, 186),
         (638, "i58a_rb.png", "LSR4", "Найдены автоматически", "#c6ecdc", 570, 252),
         (916, "i58a_rb.png", "LSR2", "Найдены автоматически", "#c6ecdc", 852, 250),
         (1200, "i58a_rr.png", "LER2", "Заданные концы", "#f8b8a6", 1168, 190)]

KEYS = [(866, "i58a_k1.png", "IP-адреса<br>источника<br>и назначения"), (1020, "i58a_k2.png", "Протокол<br>и TCP/UDP-<br>порты"),
        (1170, "i58a_k3.png", "Входной<br>интерфейс"), (1310, "i58a_k4.png", "")]

HTML = CSS + bg("bgk_24") + "".join([
    '<div class="step">',
    '<div class="i58-p" style="left:168px;top:158px;width:1336px;height:400px"></div>',
    '<div class="i58-num" style="left:190px;top:178px">1</div>',
    '<div class="i58-h" style="left:272px;top:176px;font-size:40px">Автоматический расчёт пути</div>',
    '<div class="i58-t" style="left:272px;top:222px;font-size:23px">Администратор задаёт LER5 → LER2 и требуемую полосу.</div>',
    '<div style="position:absolute;left:418px;top:280px;width:834px;height:26px;border:3px solid #1f5a7a;border-bottom:0;border-radius:14px 14px 0 0"></div>',
    '<div class="i58-pl" style="left:632px;top:258px;width:406px;height:46px;background:#bfe8d8;font:800 30px/46px Golos Text">Туннель 2&nbsp; •&nbsp; 36 Мбит/с</div>',
    "".join(rt(x, f) + '<div class="i58-n" style="left:%dpx;top:388px">%s</div>' % (x + 2, n)
            + '<div class="i58-pl" style="left:%dpx;top:414px;width:%dpx;background:%s">%s</div>' % (px, pw, c, s)
            for x, f, n, s, c, px, pw in NODES),
    '<div class="i58-ar i58-pulse" style="left:474px;top:340px;width:154px"></div>',
    '<div class="i58-ar" style="left:760px;top:340px;width:146px"></div>',
    '<div class="i58-ar" style="left:1036px;top:340px;width:152px"></div>',
    '</div>',
    '<div class="step">',
    '<div class="i58-t" style="left:168px;top:468px;width:1336px;text-align:center;font-size:22px">'
    'LER5 рассчитывает путь с учётом ограничений; RSVP-TE сигнализирует LSP и резервирует ресурсы.</div>',
    '<div class="i58-bx" style="left:246px;top:503px;width:1178px;height:42px;background:#dfeef3"></div>',
    img("i58a_bulb.png", "left:263px;top:504px;width:44px"),
    '<div class="i58-t" style="left:320px;top:514px;font-size:18px">Задание только концов — пример динамического расчёта; '
    'loose-маршрут может задавать и промежуточные опорные узлы.</div>',
    '</div>',
    # 2
    '<div class="step">',
    '<div class="i58-p" style="left:226px;top:574px;width:602px;height:350px"></div>',
    '<div class="i58-num" style="left:242px;top:584px;width:48px;height:48px;line-height:48px;font-size:28px">2</div>',
    '<div class="i58-h" style="left:312px;top:590px;font-size:29px">Сколько полосы резервировать</div>',
    '<div class="i58-bx" style="left:246px;top:634px;width:278px;height:94px;background:#a9daf2"></div>',
    '<div class="i58-bx" style="left:534px;top:634px;width:274px;height:94px;background:#fbd772"></div>',
    img("i58a_db1.png", "left:276px;top:646px;width:61px"), img("i58a_db2.png", "left:563px;top:646px;width:64px"),
    '<div class="i58-t" style="left:350px;top:648px;font:800 26px/1.25 Golos Text;color:#13306e">Туннель 1:<br>10 Мбит/с</div>',
    '<div class="i58-t" style="left:642px;top:648px;font:800 26px/1.25 Golos Text;color:#13306e">Туннель 2:<br>36 Мбит/с</div>',
    '<div class="i58-t" style="left:270px;top:738px;font-size:19px">Величину задаёт администратор, опираясь на измерения<br>и прогноз трафика.</div>',
    '<div class="i58-bx" style="left:246px;top:790px;width:562px;height:58px;background:#dfeef3"></div>',
    img("i58a_chart.png", "left:278px;top:798px;width:49px"),
    '<div class="i58-t" style="left:354px;top:798px;font-size:16px">Некоторые реализации поддерживают автоматическую<br>корректировку резерва по измерениям.</div>',
    '<div class="i58-bx" style="left:246px;top:858px;width:562px;height:56px;background:#f9cfc6"></div>',
    img("i58a_warn.png", "left:263px;top:868px;width:49px"),
    '<div class="i58-t" style="left:326px;top:867px;font-size:14px;color:#a8221a">Резерв RSVP-TE — учёт ресурсов.<br>'
    'Он сам по себе не задаёт ограничение скорости и не гарантирует QoS.</div>',
    '</div>',
    # 3
    '<div class="step">',
    '<div class="i58-p" style="left:840px;top:574px;width:606px;height:350px"></div>',
    '<div class="i58-num" style="left:856px;top:584px;width:48px;height:48px;line-height:48px;font-size:28px">3</div>',
    '<div class="i58-h" style="left:924px;top:590px;font-size:29px">Какой трафик пойдёт в туннель</div>',
    '<div class="i58-t" style="left:862px;top:638px;font-size:17px">На входном LER5 настраивают направление трафика в ТЕ-туннель.</div>',
    "".join(img(f, "left:%dpx;top:670px;width:%dpx" % (x, 101 if x != 1310 else 104))
            + ('<div class="i58-k" style="left:%dpx;top:742px">%s</div>' % (x - 14, t) if t else "") for x, f, t in KEYS),
    '<div class="i58-ks" style="left:990px;top:672px"></div><div class="i58-ks" style="left:1146px;top:672px"></div>'
    '<div class="i58-ks" style="left:1288px;top:672px"></div>',
    '<div class="i58-bx" style="left:858px;top:812px;width:570px;height:44px;background:#dfeef3"></div>',
    img("i58a_gear.png", "left:873px;top:816px;width:39px"),
    '<div class="i58-t" style="left:930px;top:825px;font-size:15px">Конкретные способы выбора зависят от оборудования и настроек.</div>',
    '<div class="i58-bx" style="left:858px;top:862px;width:570px;height:54px;background:#bfe8d8"></div>',
    img("i58a_ok.png", "left:868px;top:865px;width:52px"),
    '<div class="i58-t" style="left:936px;top:874px;font:800 21px/1.2 Golos Text;color:#13306e">Создать туннель ≠ направить в него пакеты.</div>',
    '</div>',
])
