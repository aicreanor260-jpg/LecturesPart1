# -*- coding: utf-8 -*-
"""pptx: пример — минимизируем максимальную загрузку — вёрстка поверх bgk_31."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i60-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i60-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i60-pl{position:absolute;border-radius:10px;font:700 21px/40px "Golos Text",sans-serif;color:#13306e;text-align:center;white-space:nowrap}
.i60-tg{position:absolute;border-radius:8px;font:700 18px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;padding:4px 10px}
.i60-lt{position:absolute;font:900 24px/1 "Golos Text";color:#13306e}
.i60-sp{position:absolute;font:600 17px/1 "Golos Text";color:#1d2a44;white-space:nowrap}
.i60-res{position:absolute;font:600 26px/1.45 "Golos Text",sans-serif;color:#13306e;white-space:pre}
.i60-mx{position:absolute;border-radius:12px;font:900 44px/80px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i60-vs{position:absolute;width:0;border-left:2px solid #9aa8b8}
.i60-flow{stroke-dasharray:10 8;animation:i60d 1.2s linear infinite}
@keyframes i60d{to{stroke-dashoffset:-18}}
</style>"""


def rt(x, y):
    return img("i60a_rt.png", "left:%dpx;top:%dpx;width:80px" % (x, y))


def graph(ox, top_c, bot_c, top_tag, bot_tag, tb, bb):
    """ox — смещение варианта; линии inline-SVG, узлы — вырезки."""
    def ln(x1, y1, x2, y2, c):
        return ('<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:6" marker-end="url(#i60m%s)"/>'
                % (x1 + ox, y1, x2 + ox, y2, c, c[1:]))
    svg = ('<svg class="ab" style="left:0;top:0;width:1672px;height:941px;overflow:visible" viewBox="0 0 1672 941">'
           '<defs>' + "".join('<marker id="i60m%s%d" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto">'
                              '<path d="M0,0L5,2.5L0,5z" style="fill:%s"/></marker>' % (c[1:], ox, c) for c in (top_c, bot_c)) + '</defs>'
           + ln(258, 457, 446, 446, top_c) + ln(530, 448, 718, 462, top_c)
           + ln(228, 498, 324, 554, bot_c) + ln(408, 565, 566, 565, bot_c) + ln(648, 550, 734, 504, bot_c)
           + '</svg>').replace('marker-end="url(#i60m%s)"' % top_c[1:], 'marker-end="url(#i60m%s%d)"' % (top_c[1:], ox)) \
        .replace('marker-end="url(#i60m%s)"' % bot_c[1:], 'marker-end="url(#i60m%s%d)"' % (bot_c[1:], ox))
    return "".join([
        svg,
        rt(176 + ox, 440), rt(452 + ox, 418), rt(726 + ox, 440), rt(330 + ox, 538), rt(570 + ox, 538),
        '<div class="i60-lt" style="left:%dpx;top:414px">A</div>' % (206 + ox),
        '<div class="i60-lt" style="left:%dpx;top:388px">B</div>' % (482 + ox),
        '<div class="i60-lt" style="left:%dpx;top:414px">C</div>' % (758 + ox),
        '<div class="i60-lt" style="left:%dpx;top:512px">D</div>' % (356 + ox),
        '<div class="i60-lt" style="left:%dpx;top:512px">E</div>' % (602 + ox),
        '<div class="i60-sp" style="left:%dpx;top:463px">155 Мбит/с</div>' % (310 + ox),
        '<div class="i60-sp" style="left:%dpx;top:463px">155 Мбит/с</div>' % (572 + ox),
        '<div class="i60-sp" style="left:%dpx;top:548px">100 Мбит/с</div>' % (204 + ox),
        '<div class="i60-sp" style="left:%dpx;top:577px">100 Мбит/с</div>' % (440 + ox),
        '<div class="i60-sp" style="left:%dpx;top:548px">100 Мбит/с</div>' % (682 + ox),
        '<div class="i60-tg" style="left:%dpx;top:385px;background:%s">%s</div>' % (284 + ox, tb, top_tag),
        '<div class="i60-tg" style="left:%dpx;top:500px;background:%s">%s</div>' % (430 + ox, bb, bot_tag),
    ])


HTML = CSS + bg("bgk_31") + "".join([
    '<div class="step">',
    '<div class="i60-p" style="left:100px;top:156px;width:1472px;height:146px"></div>',
    '<div class="i60-pl" style="left:120px;top:174px;width:218px;background:#f8a890">Поток 1: 50 Мбит/с</div>',
    '<div class="i60-t" style="left:350px;top:180px;font-weight:900">•</div>',
    '<div class="i60-pl" style="left:376px;top:174px;width:214px;background:#a8e2cc">Поток 2: 40 Мбит/с</div>',
    '<div class="i60-t" style="left:600px;top:180px;font-weight:900">•</div>',
    '<div class="i60-pl" style="left:626px;top:174px;width:218px;background:#fbd772">Поток 3: 30 Мбит/с</div>',
    '<div class="i60-t" style="left:126px;top:226px;color:#13306e"><b style="font-weight:800">Верхний путь A–B–C: 155 Мбит/с</b> на канал, меньшая метрика.<br>'
    '<b style="font-weight:800">Нижний A–D–E–C: 100 Мбит/с</b> на канал.</div>',
    '<div class="i60-vs" style="left:874px;top:178px;height:104px"></div>',
    '<div class="i60-pl" style="left:908px;top:170px;width:644px;height:78px;background:#dceef0"></div>',
    '<div class="i60-t" style="left:932px;top:190px;font:italic 400 32px/1 Times New Roman;color:#13306e">K =</div>',
    '<div class="i60-t" style="left:1010px;top:176px;width:410px;text-align:center;color:#13306e">суммарная скорость потоков в канале</div>',
    '<div style="position:absolute;left:1010px;top:208px;width:408px;border-top:2px solid #13306e"></div>',
    '<div class="i60-t" style="left:1010px;top:212px;width:410px;text-align:center;color:#13306e">пропускная способность канала</div>',
    '<div class="i60-t" style="left:1428px;top:194px;font:400 30px/1 Times New Roman;color:#13306e">× 100%</div>',
    '<div class="i60-pl" style="left:1060px;top:256px;width:342px;height:42px;background:#f8b8a6;font:800 23px/42px Golos Text;padding-left:30px;box-sizing:border-box">Ограничение: K ≤ 65%</div>',
    img("i60a_excl.png", "left:1075px;top:256px;width:42px"),
    '</div>',
    # вариант 1
    '<div class="step">',
    '<div class="i60-p" style="left:150px;top:318px;width:680px;height:426px"></div>',
    '<div class="i60-pl" style="left:170px;top:328px;width:640px;background:#f8c4b4;font:700 24px/42px Golos Text">Вариант 1 • порядок 1 → 2 → 3</div>',
    graph(0, "#ef6a48", "#4aa8ec", "Потоки 1 + 2:<br>90 Мбит/с", "Поток 3:<br>30 Мбит/с", "#f8a890", "#bfe2f8"),
    '<div class="i60-pl" style="left:172px;top:622px;width:290px;height:102px;background:#dceef0"></div>',
    '<div class="i60-res" style="left:192px;top:640px">Верх:  90 / 155 ≈ 58%\nНиз:   30 / 100 = 30%</div>',
    '<div class="i60-vs" style="left:480px;top:642px;height:62px"></div>',
    '<div class="i60-mx" style="left:510px;top:634px;width:296px;background:#f8a890">max K ≈ 58%</div>',
    '</div>',
    # вариант 2
    '<div class="step">',
    '<div class="i60-p" style="left:842px;top:318px;width:680px;height:426px"></div>',
    '<div class="i60-pl" style="left:862px;top:328px;width:640px;background:#bfe8d8;font:700 24px/42px Golos Text">Вариант 2 • порядок 2 → 3 → 1</div>',
    graph(694, "#2ab478", "#f2c420", "Потоки 2 + 3:<br>70 Мбит/с", "Поток 1:<br>50 Мбит/с", "#a8e2cc", "#fbd772"),
    '<div class="i60-pl" style="left:864px;top:622px;width:290px;height:102px;background:#dceef0"></div>',
    '<div class="i60-res" style="left:886px;top:640px">Верх:  70 / 155 ≈ 45%\nНиз:   50 / 100 = 50%</div>',
    '<div class="i60-vs" style="left:1160px;top:642px;height:62px"></div>',
    '<div class="i60-mx" style="left:1188px;top:620px;width:304px;height:66px;line-height:66px;background:#a8e2cc">max K = 50%</div>',
    img("i60a_ok.png", "left:1194px;top:688px;width:50px"),
    '<div class="i60-t" style="left:1252px;top:696px;font:800 20px/1 Golos Text;color:#1f7a3a">Лучшее распределение</div>',
    '</div>',
    # итог
    '<div class="step">',
    '<div class="i60-p" style="left:236px;top:756px;width:1200px;height:162px"></div>',
    img("i60a_bulb.png", "left:253px;top:763px;width:69px"),
    '<div class="i60-t" style="left:334px;top:778px;font:800 22px/1 Golos Text;color:#13306e">'
    'Оба варианта соблюдают 65%. Во втором максимальная загрузка ниже: 50% вместо 58%.</div>',
    img("i60a_warn.png", "left:253px;top:833px;width:69px"),
    '<div class="i60-t" style="left:334px;top:838px;font-size:19px">Все три потока на верхнем пути:<br>'
    '<b style="font-weight:800;color:#13306e">120 / 155 ≈ 77% — недопустимо.</b></div>',
    '<div class="i60-vs" style="left:656px;top:842px;height:50px"></div>',
    img("i60a_tgt.png", "left:673px;top:833px;width:71px"),
    '<div class="i60-t" style="left:756px;top:834px;font-size:17px"><b style="font-weight:800;color:#13306e">min(max K)</b> — выбрать распределение<br>'
    'с минимальной загрузкой самого<br>загруженного канала.</div>',
    '<div class="i60-vs" style="left:1090px;top:842px;height:50px"></div>',
    img("i60a_list.png", "left:1106px;top:833px;width:68px"),
    '<div class="i60-t" style="left:1184px;top:840px;font-size:14px">Потоки не делятся между путями;<br>порядок размещения влияет<br>на результат.</div>',
    '</div>',
])
