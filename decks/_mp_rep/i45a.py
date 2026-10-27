# -*- coding: utf-8 -*-
"""pptx: как работает RSVP-TE и статические записи — вёрстка поверх bgk_17."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 100

CSS = """<style>
.i45-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i45-h{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i45-t{position:absolute;font:500 21px/1.22 "Golos Text",sans-serif;color:#1d2a44}
.i45-pill{position:absolute;border-radius:16px;font:700 19px/34px "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i45-n{position:absolute;font:900 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:60px}
.i45-ln{position:absolute;height:6px;transform-origin:0 50%;border-radius:3px}
.i45-num{position:absolute;width:52px;height:52px;border-radius:50%;color:#fff;font:900 32px/52px "Golos Text",sans-serif;text-align:center}
.i45-sh{position:absolute;height:40px;border-radius:20px;font:900 27px/40px "Golos Text",sans-serif;color:#13306e;padding:0 80px 0 70px}
.i45-ar{position:absolute;height:3px;background:#1b7a6a}
.i45-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1b7a6a;border-right:0}
.i45-pk{position:absolute;display:flex;height:42px;border:2px solid #1d3f8a;border-radius:3px;overflow:hidden;font:500 21px/38px "Golos Text",sans-serif}
.i45-pk b{background:#f2694a;color:#1d1d1d;padding:0 12px;font-weight:500}.i45-pk i{background:#fff;color:#1d3f8a;padding:0 18px;font-style:normal}
.i45-tb{position:absolute;border-collapse:collapse;font:500 19px/28px "Golos Text",sans-serif;color:#1d2a44;text-align:center;
 border:2px solid #1f63c6}
.i45-tb th{background:#d6ebfb;font-weight:700;border:1px solid #6aa6e0}.i45-tb td{background:#fdf8ea;border:1px solid #6aa6e0}
.i45-fly{animation:i45f 3s ease-in-out infinite}
@keyframes i45f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ln(x1, y1, x2, y2, c):
    import math
    d = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return '<div class="i45-ln" style="left:%dpx;top:%dpx;width:%dpx;background:%s;transform:rotate(%.1fdeg)"></div>' % (x1, y1 - 3, d, c, a)


def rt(x, y, name, nx, ny, w=104):
    return img("i45a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i45-n" style="left:%dpx;top:%dpx">%s</div>' % (nx - 30, ny, name)


def step(y, n, col, bgc, title, text):
    return '<div class="step">' + \
        '<div class="i45-sh" style="left:1150px;top:%dpx;background:%s">%s</div>' % (y + 4, bgc, title) + \
        '<div class="i45-num" style="left:1132px;top:%dpx;background:%s">%d</div>' % (y, col, n) + \
        '<div class="i45-t" style="left:1210px;top:%dpx;width:370px;font-size:17px">%s</div>' % (y + 46, text) + '</div>'


HTML = CSS + bg("bgk_17") + "".join([
    '<div class="step">',
    '<div class="i45-p" style="left:76px;top:108px;width:1520px;height:496px"></div>',
    '<div class="i45-h" style="left:104px;top:122px">RSVP-TE — сигнализация пути с ограничениями</div>',
    '<div class="i45-t" style="left:104px;top:166px;font-size:24px">RSVP-TE — расширение RSVP для инжиниринга трафика.</div>',
    '<div style="position:absolute;left:1110px;top:150px;width:2px;height:372px;background:#1d3f8a"></div>',
    '<div class="i45-pill" style="left:386px;top:202px;width:520px;background:#dcdfe6">Меньшая метрика • недостаточно свободной полосы</div>',
    ln(262, 300, 626, 266, "#b9bcc4"), ln(626, 266, 1000, 300, "#b9bcc4"),
    ln(262, 300, 474, 362, "#2fbf94"), ln(474, 362, 774, 362, "#2fbf94"), ln(774, 362, 1000, 300, "#2fbf94"),
    rt(208, 266, "R1", 260, 348), rt(582, 244, "R2", 626, 310, 92), rt(430, 330, "R3", 474, 398, 92),
    rt(730, 330, "R5", 774, 398, 92), rt(948, 266, "R4", 1000, 348),
    '<div class="i45-pill" style="left:386px;top:424px;width:520px;background:#bfe9d6">TE-туннель • больше метрика, достаточно ресурсов</div>',
    '</div>',
    '<div class="step">',
    '<div class="i45-ar i45-fly" style="left:308px;top:481px;width:648px;background:#1b8a77"></div>',
    '<div class="i45-t" style="left:470px;top:466px;width:310px;background:#fdf8ea;text-align:center;font-weight:600;color:#13306e">'
    'Path: R1 → R3 → R5 → R4</div>',
    '<div style="position:absolute;left:310px;top:511px;width:646px;height:3px;background:#f2694a"></div>',
    '<div style="position:absolute;left:306px;top:503px;border:9px solid transparent;border-right:13px solid #f2694a;border-left:0"></div>',
    '<div class="i45-t" style="left:470px;top:498px;width:310px;background:#fdf8ea;text-align:center;font-weight:600;color:#f2694a">'
    'Resv: R4 → R5 → R3 → R1</div>',
    '</div>',
    step(130, 1, "#20b48c", "#cdeee0", "Выбрать путь", "Входной маршрутизатор рассчитывает путь с ограничениями или использует заданный."),
    step(234, 2, "#f2694a", "#fbd3c8", "Path — вперёд", "Передаёт параметры запроса вдоль выбранного пути."),
    step(346, 3, "#20b48c", "#cdeee0", "Resv — обратно", "Согласует метки и резервирует запрошенные ресурсы."),
    step(456, 4, "#f2694a", "#fbd3c8", "Установить записи", "LSR формируют состояние для продвижения по туннелю."),
    '<div class="step">',
    '<div class="i45-t" style="left:104px;top:544px;width:1466px;height:52px;background:#c4e8e0;border-radius:12px;padding:12px 0 0 340px;'
    'box-sizing:border-box"><b>Сведения о ресурсах:</b> OSPF-TE / IS-IS-TE.&nbsp; RSVP-TE сигнализирует выбранный путь.</div>',
    img("i45a_db.png", "left:358px;top:548px;width:50px"),
    '<div style="position:absolute;left:422px;top:556px;width:2px;height:30px;background:#1d3f8a"></div>',
    '</div>',
    # ---- статика
    '<div class="step">',
    '<div class="i45-p" style="left:258px;top:614px;width:1070px;height:304px"></div>',
    '<div class="i45-h" style="left:284px;top:624px;font-size:31px">Статическое&nbsp; формирование таблиц</div>',
    '<div class="i45-t" style="left:284px;top:660px;font-size:20px">Администратор вручную задаёт входную метку, выходной интерфейс, '
    'следующий узел и действие.</div>',
    '<div class="i45-pk" style="left:434px;top:706px"><b>245</b><i>IP</i></div>',
    '<div class="i45-ar" style="left:562px;top:727px;width:36px"></div>',
    rt(604, 694, "R2", 648, 754, 88),
    '<div class="i45-ar i45-fly" style="left:700px;top:727px;width:192px"></div>',
    '<div class="i45-t" style="left:724px;top:700px;font-weight:700;font-size:19px;color:#13306e">Swap 245 → 256</div>',
    '<div class="i45-pk" style="left:904px;top:706px"><b>256</b><i>IP</i></div>',
    '<div class="i45-ar" style="left:1032px;top:727px;width:46px"></div>',
    rt(1084, 694, "R3", 1128, 754, 88),
    '<table class="i45-tb" style="left:312px;top:768px;width:964px"><tr><th>Узел</th><th>Входная метка</th><th>Действие</th>'
    '<th>Следующий узел</th></tr><tr><td>R2</td><td>245</td><td>Заменить на 256</td><td>R3</td></tr></table>',
    '<div class="i45-t" style="left:312px;top:836px;width:960px;height:32px;background:#c4e8e0;border-radius:8px;padding:4px 0 0 70px;'
    'box-sizing:border-box;font-size:18px">На R3 нужна согласованная запись для метки 256.</div>',
    '<div class="i45-t" style="left:338px;top:838px;width:28px;height:28px;border-radius:50%;background:#20a070;color:#fff;'
    'text-align:center;font:900 20px/28px Georgia">i</div>',
    '<div class="i45-t" style="left:312px;top:872px;width:960px;text-align:center;font-size:16px">Динамическое распределение меток '
    'для этих правил не требуется.<br>При изменении топологии согласованность поддерживает администратор.</div>',
    '</div>',
])
