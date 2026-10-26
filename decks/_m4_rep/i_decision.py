import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _kr import css, defs
W, H, TOP = 1672, 941, 240
P = "m4x-dec"
CSS = css(P) + ("<style>.%s-pt{position:absolute;box-sizing:border-box;border:2px solid rgba(240,199,94,.7);border-radius:14px;"
                "background:rgba(8,40,30,.35);box-shadow:0 0 16px rgba(240,199,94,.22),inset 0 0 20px rgba(240,199,94,.07)}"
                ".%s-nt{position:absolute;font:700 22px/1 'Golos Text',sans-serif;color:#f4ecd2;text-align:center;text-shadow:0 1px 4px #000}"
                ".%s-rn{position:absolute;font:800 24px/1 'Playfair Display',serif;color:#fff;text-align:center;width:60px;margin-left:-30px;text-shadow:0 2px 4px #000}"
                ".%s-lb{font-size:18.5px;line-height:22px;border-radius:10px}"
                "</style>") % ((P,) * 4)

def dev(f, x, y, w, h):
    return img(f, "left:%dpx;top:%dpx;width:%dpx;height:%dpx" % (x, y, w, h))

def rt(cx, cy):
    return img("sub_router.png", "left:%dpx;top:%dpx;width:150px;height:88px" % (cx - 75, cy - 48))

def lab(x, y, w, h, text):
    return '<div class="%s-lb %s-lb" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>' % (P, P, x, y, w, h, text)

def bd(cx, cy, n):
    return '<div class="%s-bd" style="left:%dpx;top:%dpx;width:60px">%d</div>' % (P, cx - 30, cy - 12, n)

def svg(body):
    return '<svg class="%s-sv" viewBox="0 0 1672 941">%s</svg>' % (P, body)

def gold(d):
    return '<path d="%s" fill="none" stroke="#f6d36a" stroke-width="4.5" filter="url(#%s-gl)" marker-end="url(#%s-ah)"/>' % (d, P, P)

def ptr(d):
    return '<path d="%s" fill="none" stroke="#f0c75e" stroke-width="1.6"/>' % d

TEXT = ("Когда узел отправляет пакет другому<br>узлу, он использует свою таблицу<br>маршрутизации, чтобы определить<br>направление передачи. Если IP-адрес<br>"
        "назначения находится в другой сети,<br>пакет пересылается на шлюз по<br>умолчанию — интерфейс маршрутизатора.<br>"
        "Получив пакет, маршрутизатор выполняет<br>поиск в своей таблице маршрутизации<br>и определяет исходящий интерфейс.<br>"
        "Маршрутизаторы выбирают маршрут<br>и обеспечивают доставку пакетов<br>между сетями. Эффективность доставки<br>"
        "зависит от передачи пакетов по наиболее<br>оптимальному пути.")
white = ('<g fill="none" stroke="#f4ecd2" stroke-width="1.8">'
         '<path d="M572 503L634 503" marker-start="url(#%(p)s-ahs)" marker-end="url(#%(p)s-ahs)"/>'
         '<path d="M582 612L650 548" marker-start="url(#%(p)s-ahs)" marker-end="url(#%(p)s-ahs)"/>'
         '<path d="M1436 482L1552 376" marker-start="url(#%(p)s-ahs)" marker-end="url(#%(p)s-ahs)"/>'
         '<path d="M1440 540L1552 632" marker-start="url(#%(p)s-ahs)" marker-end="url(#%(p)s-ahs)"/></g>' % {"p": P})
HTML = CSS + bg() + "".join([
    '<div class="step"><div class="%s-pn" style="left:24px;top:258px;width:444px;height:429px;border-radius:12px"></div>'
    '<div class="%s-t" style="left:47px;top:278px;font-size:19.2px;line-height:25.9px">%s</div></div>' % (P, P, TEXT),
    '<div class="step"><div class="%s-pt" style="left:483px;top:248px;width:407px;height:456px"></div>'
    '<div class="%s-pt" style="left:1231px;top:248px;width:417px;height:456px"></div>'
    '<div class="%s-nt" style="left:483px;width:407px;top:260px">Сеть 192.168.10.0/24</div>'
    '<div class="%s-nt" style="left:1231px;width:417px;top:260px">Сеть 192.168.20.0/24</div>' % ((P,) * 4) +
    svg(defs(P) + white) +
    dev("dec_monitor_l.png", 512, 332, 96, 70) + dev("dec_server_l.png", 500, 458, 70, 92) + dev("dec_laptop_l.png", 512, 598, 96, 78) +
    dev("dec_switch_l.png", 636, 466, 94, 80) + dev("dec_switch_r.png", 1345, 470, 97, 75) + dev("dec_server_r.png", 1530, 482, 70, 92) +
    dev("dec_laptop_r.png", 1520, 300, 92, 88) + dev("dec_monitor_r.png", 1525, 605, 87, 85) +
    rt(868, 497) + rt(1195, 497) +
    '<div class="%s-rn" style="left:868px;top:512px">R1</div><div class="%s-rn" style="left:1195px;top:512px">R2</div></div>' % (P, P),
    '<div class="step">' + svg(gold("M1546 513H1448")) + bd(1600, 473, 1) + lab(1518, 401, 123, 52, "Адрес<br>назначения") + svg(ptr("M1560 453L1572 466")) + '</div>',
    '<div class="step">' + svg(gold("M1346 508H1262")) + bd(1398, 458, 2) + lab(1295, 378, 128, 52, "Шлюз по<br>умолчанию") + svg(ptr("M1360 430L1366 458")) + '</div>',
    '<div class="step">' + svg(gold("M1140 499H1068")) + bd(1218, 450, 3) + lab(1115, 363, 130, 55, "Поиск<br>маршрута") + svg(ptr("M1190 418L1200 440")) +
    img("dec_cube.png", "left:1000px;top:475px;width:56px;height:47px") +
    '<div class="%s-t" style="left:988px;top:530px;font-size:19px;line-height:22px">IP-пакет</div>' % P +
    lab(940, 431, 178, 32, "Оптимальный путь") + svg(ptr("M1028 463L1028 474")) + '</div>',
    '<div class="step">' + svg(gold("M990 499H926") + gold("M818 499H732")) + bd(898, 450, 4) + lab(803, 364, 127, 55, "Исходящий<br>интерфейс") + svg(ptr("M850 419L860 442")) + '</div>',
    '<div class="step">' + svg(gold("M668 462L604 358")) + bd(700, 455, 5) + '</div>',
    '<div class="step">' + bd(592, 325, 6) + lab(633, 309, 144, 34, "Доставка узлу") + svg(ptr("M633 330L612 345")) + '</div>',
])
