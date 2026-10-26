# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 112

CSS = """<style>
.m4x-sea-p{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.6);border-radius:14px;
  background:linear-gradient(180deg,rgba(14,70,52,.6),rgba(5,32,24,.82));box-shadow:0 0 18px rgba(240,199,94,.2),inset 0 0 30px rgba(0,0,0,.35)}
.m4x-sea-b{position:absolute;box-sizing:border-box;border:2px solid #f0c75e;border-radius:22px;background:linear-gradient(180deg,rgba(16,86,64,.92),rgba(6,48,36,.94));
  box-shadow:0 0 16px rgba(63,214,176,.35),0 0 10px rgba(240,199,94,.35)}
.m4x-sea-r{border-color:#ff6a4a;background:linear-gradient(180deg,rgba(120,26,18,.92),rgba(70,12,8,.95));box-shadow:0 0 18px rgba(255,90,60,.5)}
.m4x-sea-pill{position:absolute;box-sizing:border-box;border:1.5px solid #f0c75e;border-radius:16px;background:rgba(6,56,42,.95);text-align:center;
  font:700 22px/26px "Golos Text",sans-serif;color:#f6e3a0;box-shadow:0 0 10px rgba(63,214,176,.4)}
.m4x-sea-t{position:absolute;font:500 21px/24px "Golos Text",sans-serif;color:#f4efdc}
.m4x-sea-c{text-align:center;font-size:19px;line-height:23px}
.m4x-sea-ph{position:absolute;text-align:center;font:800 22px/1 "Playfair Display",serif;text-transform:uppercase;white-space:nowrap;
  background:linear-gradient(180deg,#fff0b8,#e8b84a 55%,#b88a2a);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-sea-ip{position:absolute;font:800 25px/1 "Playfair Display",serif;color:#f0c75e;white-space:nowrap}
.m4x-sea-ip2{font-size:24px;color:#f6e3a0}
.m4x-sea-s{position:absolute;font:500 17px/21px "Golos Text",sans-serif;color:#f1ead2}
.m4x-sea-title{position:absolute;left:0;width:1672px;top:25px;text-align:center;font:900 62px/1 "Playfair Display",serif;text-transform:uppercase;
  background:linear-gradient(180deg,#fff0b8,#e8b84a 55%,#b88a2a);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-sea-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.m4x-sea-sv .a{fill:none;stroke:#e8b84a;stroke-width:2.5;marker-end:url(#m4xsea)}
.m4x-sea-sv .g{fill:none;stroke:#e8b84a;stroke-width:2.5}
.m4x-sea-sv .dg{fill:rgba(10,70,52,.92);stroke:#f0c75e;stroke-width:2.5;filter:drop-shadow(0 0 8px rgba(240,199,94,.45))}
</style>"""

DEFS = '<defs><marker id="m4xsea" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#f0c75e"/></marker></defs>'


def im(n, x, y, w):
    return img("i_search_%s.png" % n, "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def svg(body):
    return '<svg class="m4x-sea-sv" viewBox="0 0 1672 941">' + DEFS + body + '</svg>'


def box(x, y, x2, y2, red=False):
    return '<div class="m4x-sea-b%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (" m4x-sea-r" if red else "", x, y, x2 - x, y2 - y)


def txt(x, y, s, cls="", w=None):
    st = "left:%dpx;top:%dpx" % (x, y)
    if w:
        st += ";width:%dpx;margin-left:-%dpx" % (w, w // 2)
    return '<div class="m4x-sea-t %s" style="%s">%s</div>' % (cls, st, s)


def pill(cx, cy, w, s, red=False):
    extra = ";border-color:#ff6a4a;background:rgba(90,16,10,.95);color:#ffd9cf" if red else ""
    return '<div class="m4x-sea-pill" style="left:%dpx;top:%dpx;width:%dpx;height:29px%s">%s</div>' % (cx - w // 2, cy - 14, w, extra, s)


def hexa(pts):
    return '<polygon class="dg" points="%s"/>' % " ".join("%d,%d" % p for p in pts)


def diamond(cx, cy, w=290, h=100):
    return hexa([(cx - w // 2, cy), (cx - w // 2 + 55, cy - h // 2), (cx + w // 2 - 55, cy - h // 2), (cx + w // 2, cy), (cx + w // 2 - 55, cy + h // 2), (cx - w // 2 + 55, cy + h // 2)])


def flat(x, y, x2, y2):
    return hexa([(x, (y + y2) // 2), (x + 38, y), (x2 - 38, y), (x2, (y + y2) // 2), (x2 - 38, y2), (x + 38, y2)])


# левая колонка
L1 = ('<div class="step"><div class="m4x-sea-p" style="left:22px;top:148px;width:438px;height:444px;border-radius:20px"></div>'
      '<div class="m4x-sea-ph" style="left:22px;width:438px;top:161px">Пример иерархии префиксов</div>'
      + im("cl1", 70, 218, 140) + im("rt", 175, 320, 140) + im("cl2", 72, 424, 126) + im("cl3", 284, 424, 128)
      + svg('<path class="g" d="M140 298V340Q140 352 152 352H186M135 382V425M345 382V425" /><circle cx="140" cy="325" r="5" fill="#f0c75e"/><circle cx="137" cy="400" r="4" fill="#f0c75e"/><circle cx="345" cy="400" r="4" fill="#f0c75e"/>')
      + '<div class="m4x-sea-ip" style="left:219px;top:227px">10.1.0.0/16</div>'
      + '<div class="m4x-sea-s" style="left:219px;top:253px">Родительская сеть<br>(маршрут 1-го уровня)</div>'
      + '<div class="m4x-sea-ip m4x-sea-ip2" style="left:0;width:270px;text-align:center;top:498px">10.1.1.0/24</div>'
      + '<div class="m4x-sea-s m4x-sea-c" style="left:0;width:270px;top:523px">Дочерняя подсеть<br>(маршрут 2-го уровня)</div>'
      + '<div class="m4x-sea-ip m4x-sea-ip2" style="left:212px;width:270px;text-align:center;top:499px">10.1.2.0/24</div>'
      + '<div class="m4x-sea-s m4x-sea-c" style="left:212px;width:270px;top:524px">Дочерняя подсеть<br>(маршрут 2-го уровня)</div></div>')
L2 = ('<div class="step"><div class="m4x-sea-p" style="left:22px;top:600px;width:438px;height:112px;border-radius:20px"></div>'
      + im("cl4", 68, 610, 132)
      + '<div class="m4x-sea-ip" style="left:218px;top:623px">0.0.0.0/0</div>'
      + '<div class="m4x-sea-s" style="left:218px;top:651px">Маршрут по умолчанию<br>(суперсеть)</div></div>')

GLOBE = '<div class="step">' + im("globe", 1180, 95, 492) + '</div>'

S1 = ('<div class="step">' + box(642, 123, 1030, 187) + im("mon", 673, 133, 55)
      + txt(760, 143, "IP-адрес назначения", "", None).replace("21px", "23px") + svg('<path class="a" d="M837 187V224"/>') + '</div>')
S2 = ('<div class="step">' + box(677, 226, 997, 298) + im("mag1", 702, 238, 56)
      + txt(786, 237, "Поиск совпадения<br>в таблице") + svg('<path class="a" d="M677 262H628V312M997 262H1045V312"/>') + '</div>')
S3 = ('<div class="step">' + svg(diamond(628, 380)) + im("doc", 610, 332, 38)
      + txt(628, 364, "Окончательный<br>маршрут 1-го уровня?", "m4x-sea-c", 290)
      + svg('<path class="a" d="M628 432V448M628 479V507"/>') + pill(628, 464, 78, "Да")
      + box(492, 511, 763, 570) + im("pl1", 512, 522, 48) + txt(574, 529, "Переслать пакет").replace("21px", "22px") + '</div>')
S4 = ('<div class="step">' + svg(diamond(1045, 380)) + im("net", 1025, 332, 40)
      + txt(1045, 364, "Родительский<br>маршрут 1-го уровня?", "m4x-sea-c", 290)
      + svg('<path class="a" d="M1045 430V433M1045 461V472"/>') + pill(1045, 447, 76, "Да")
      + box(870, 474, 1219, 542) + im("mag2", 893, 483, 52) + txt(962, 483, "Проверить дочерние<br>маршруты 2-го уровня")
      + svg('<path class="a" d="M1045 542V584"/>') + '</div>')
S5 = ('<div class="step">' + svg(flat(908, 586, 1177, 642)) + im("node", 933, 595, 42) + txt(986, 604, "Подсеть совпала?").replace("21px", "19px")
      + svg('<path class="a" d="M908 614H869V646M1177 614H1295V644"/>') + pill(869, 662, 76, "Да")
      + svg('<path class="a" d="M869 677V694"/>')
      + box(750, 696, 1002, 755) + im("pl2", 768, 707, 48) + txt(825, 715, "Переслать пакет").replace("21px", "22px") + '</div>')
S6 = ('<div class="step">' + svg(flat(1165, 646, 1503, 718)) + im("glob", 1193, 664, 44) + txt(1250, 659, "Суперсеть или<br>маршрут по умолчанию?").replace("21px", "19px")
      + svg('<path class="a" d="M1165 682H1147V717M1503 682H1522V716"/>') + pill(1147, 734, 74, "Да") + pill(1522, 733, 78, "Нет", True)
      + svg('<path class="a" d="M1147 748V766M1522 748V767"/>')
      + box(1032, 768, 1286, 826) + im("pl3", 1048, 778, 50) + txt(1106, 786, "Переслать пакет").replace("21px", "22px")
      + box(1393, 769, 1651, 826, True) + im("x", 1413, 779, 44) + txt(1470, 785, "Отбросить пакет").replace("21px", "22px") + '</div>')

HTML = CSS + bg() + "".join([GLOBE, L1, L2, S1, S2, S3, S4, S5, S6])
