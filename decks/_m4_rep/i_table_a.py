import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _kr import css, defs, cloud_box
W, H, TOP = 1672, 941, 90
P = "m4x-tba"
CSS = css(P) + ("<style>.%s-s{position:absolute;font:600 22px/1 'Playfair Display',serif;color:#f6ebc8;text-align:center;white-space:nowrap;margin-left:-100px;width:200px;text-shadow:0 2px 4px #000;font-variant-numeric:lining-nums}"
                ".%s-cell{position:absolute;font:600 26px/1 'Playfair Display',serif;color:#f6ebc8;text-align:center;white-space:nowrap;font-variant-numeric:lining-nums}"
                ".%s-hd{position:absolute;font:600 24px/26px 'Playfair Display',serif;color:#f6ebc8;text-align:center}"
                ".%s-ln{position:absolute;background:rgba(240,199,94,.8);box-shadow:0 0 6px rgba(240,199,94,.5)}"
                ".%s-hl{position:absolute;background:linear-gradient(180deg,rgba(240,199,94,.55),rgba(240,199,94,.32));box-shadow:0 0 14px rgba(240,199,94,.5)}"
                ".%s-cd{position:absolute;box-sizing:border-box;border-radius:14px;border:2px solid rgba(240,199,94,.8);background:rgba(10,38,28,.88);box-shadow:0 0 16px rgba(240,199,94,.3),inset 0 0 20px rgba(240,199,94,.1)}"
                ".%s-cd.b{border-color:#3fd6d0;background:rgba(8,48,48,.88);box-shadow:0 0 16px rgba(63,214,208,.35),inset 0 0 20px rgba(63,214,208,.12)}"
                ".%s-ct{position:absolute;font:800 27px/1 'Playfair Display',serif;color:#f6d36a}"
                ".%s-cx{position:absolute;font:500 20.5px/26px 'Golos Text',sans-serif;color:#f4ecd2;white-space:nowrap}"
                "</style>") % ((P,) * 9)


def lab(x, y, text, big=False):
    st = "font-size:26px;" if big else ""
    return '<div class="%s-s" style="left:%dpx;top:%dpx;%s">%s</div>' % (P, x, y - 11, st, text)


def rt(cx, cy):
    return img("tab_router.png", "left:%dpx;top:%dpx;width:120px;height:73px" % (cx - 60, cy - 37))


def svg(b):
    return '<svg class="%s-sv" viewBox="0 0 1672 941">%s</svg>' % (P, b)


def dots(pts):
    return "".join('<circle cx="%d" cy="%d" r="5" fill="#fff4c2" stroke="#f0c75e" stroke-width="2"/>' % p for p in pts)


wires = svg(defs(P) + '<g stroke="#f0c75e" stroke-width="3" filter="url(#%s-gl)"><path d="M398 236V340"/><path d="M336 408L232 483"/><path d="M460 408L565 483"/></g>' % P +
            dots([(397, 238), (397, 337), (335, 408), (231, 482), (460, 408), (565, 482)]))
COLS = [815, 1085, 1357, 1580]
ROWS = [168, 238, 290, 340, 390, 440, 490, 542]
DATA = [("11.0.0.0/8", "2.2.2.2", "Gi1/0/0"), ("13.0.0.0/8", "3.3.3.2", "Gi1/0/1"), ("14.0.0.0/8", "1.1.1.2", "Gi1/0/2"),
        ("...", "", ""), ("1.1.1.0/30", "1.1.1.1", "Gi1/0/2"), ("1.1.1.1/32", "127.0.0.1", "Gi1/0/2")]


def row(i):
    y0, y1 = ROWS[i + 1], ROWS[i + 2]
    out = ""
    for j, t in enumerate(DATA[i]):
        if t:
            cx = (COLS[j] + COLS[j + 1]) // 2 if t != "..." else 1185
            out += '<div class="%s-cell" style="left:%dpx;width:260px;margin-left:-130px;top:%dpx">%s</div>' % (P, cx, (y0 + y1) // 2 - 13, t)
    return out


grid = "".join('<div class="%s-ln" style="left:%dpx;top:168px;width:2px;height:374px"></div>' % (P, x - 1) for x in COLS[1:3]) + \
       "".join('<div class="%s-ln" style="left:815px;top:%dpx;width:765px;height:2px"></div>' % (P, y - 1) for y in ROWS[1:-1])

HTML = CSS + bg() + "".join([
    '<div class="step">' + wires + cloud_box(P, 313, 94, 175, 98) + cloud_box(P, 88, 512, 186, 76) + cloud_box(P, 514, 512, 186, 76) +
    rt(398, 193) + rt(398, 380) + rt(185, 514) + rt(604, 510) +
    lab(401, 141, "14.0.0.0/8", True) + lab(482, 198, "R4", True) + lab(469, 249, "1.1.1.2/30") +
    lab(458, 303, "Gi1/0/2") + lab(471, 328, "1.1.1.1/30") + lab(288, 371, "Gi1/0/0") + lab(271, 396, "2.2.2.1/30") +
    lab(513, 373, "Gi1/0/1") + lab(527, 400, "3.3.3.1/30") + lab(396, 441, "R2", True) +
    lab(175, 463, "2.2.2.2/30") + lab(270, 515, "R1", True) + lab(178, 564, "11.0.0.0/8", True) +
    lab(625, 463, "3.3.3.2/30") + lab(521, 515, "R3", True) + lab(607, 564, "13.0.0.0/8", True) + '</div>',
    '<div class="step"><div class="%s-pn" style="left:802px;top:112px;width:790px;height:446px;border-radius:24px"></div>'
    '<div class="%s-g" style="left:802px;width:790px;text-align:center;top:118px;font-size:34px;line-height:42px">Таблица маршрутизации R2</div>'
    '<div class="%s-hl" style="left:815px;top:238px;width:765px;height:52px"></div>%s'
    '<div class="%s-hd" style="left:815px;width:270px;top:190px">Назначение/маска</div>'
    '<div class="%s-hd" style="left:1085px;width:272px;top:177px">Следующий<br>маршрутизатор</div>'
    '<div class="%s-hd" style="left:1357px;width:223px;top:177px">Исходящий<br>интерфейс</div></div>' % ((P,) * 3 + (grid,) + (P,) * 3),
    '<div class="step">' + row(0) + row(1) + row(2) + '</div>',
    '<div class="step">' + row(3) + row(4) + row(5) + '</div>',
    '<div class="step"><div class="%s-pn" style="left:42px;top:604px;width:1588px;height:114px;border-radius:20px"></div>'
    '<div class="%s-t" style="left:42px;width:1588px;text-align:center;top:614px;font:500 23px/30.5px \'Playfair Display\',serif">'
    'Маршрутизатор передаёт пакеты на основе своей таблицы IP-маршрутизации. Таблица может содержать множество<br>'
    'записей, но включает не все известные маршруты, а только оптимальные. Маршрутизатор управляет информацией<br>'
    'о маршрутизации с помощью записей в таблице IP-маршрутизации.</div></div>' % (P, P),
    '<div class="step"><div class="%s-g" style="left:130px;width:1420px;text-align:center;top:723px;font-size:28px;line-height:36px;filter:drop-shadow(0 0 8px #000) drop-shadow(0 0 4px #000)">В таблице маршрутизации хранится следующая информация:</div>'
    '<div class="%s-ln" style="left:130px;top:743px;width:210px;height:2px"></div><div class="%s-ln" style="left:1322px;top:743px;width:220px;height:2px"></div></div>' % (P, P, P),
    '<div class="step"><div class="%s-cd" style="left:72px;top:766px;width:754px;height:146px"></div>' % P +
    img("tab_ic_tree.png", "left:92px;top:775px;width:124px;height:122px") +
    '<div class="%s-ct" style="left:245px;top:782px">Маршруты с прямым подключением</div>' % P +
    '<div class="%s-cx" style="left:245px;top:820px">Это сети, непосредственно подключенные<br>к интерфейсам маршрутизатора. Они добавляются<br>в таблицу маршрутизации автоматически.</div></div>' % P,
    '<div class="step"><div class="%s-cd b" style="left:850px;top:766px;width:754px;height:146px"></div>' % P +
    img("tab_ic_globe.png", "left:880px;top:775px;width:124px;height:122px") +
    '<div class="%s-ct" style="left:1036px;top:782px;color:#f3e3b0">Удалённые маршруты</div>' % P +
    '<div class="%s-cx" style="left:1036px;top:820px;font-size:19.5px">Это сети, расположенные за другими маршрутизаторами.<br>Для их достижения в таблице указывается следующий<br>маршрутизатор и исходящий интерфейс.</div></div>' % P,
])
