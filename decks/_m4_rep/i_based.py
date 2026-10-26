import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _kr import css, defs, cloud_at
W, H, TOP = 1672, 941, 138
P = "m4x-bas"
CSS = css(P) + ("<style>.%s-n{position:absolute;width:58px;height:58px;box-sizing:border-box;border-radius:50%%;border:3px solid #f0c75e;"
                "box-shadow:0 0 14px rgba(240,199,94,.6),inset 0 0 10px rgba(240,199,94,.25);background:rgba(6,34,26,.7);"
                "font:800 36px/50px 'Playfair Display',serif;color:#f6d36a;text-align:center}"
                ".%s-r{position:absolute;font:700 25px/1 'Playfair Display',serif;font-variant-numeric:lining-nums;color:#f6ebc8;text-align:center;width:80px;margin-left:-40px;text-shadow:0 2px 5px #000}"
                ".%s-tx{position:absolute;font:500 19.8px/26.7px 'Golos Text',sans-serif;color:#f4ecd2;text-shadow:0 1px 4px rgba(0,0,0,.7)}"
                "</style>") % (P, P, P)

def rt(cx, cy):
    return img("sub_router.png", "left:%dpx;top:%dpx;width:122px;height:72px" % (cx - 61, cy - 36))

def card(n, x, y, w, h, nx, ny, tx, ty, text):
    return ('<div class="step"><div class="%s-pn" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
            '<div class="%s-n" style="left:%dpx;top:%dpx">%d</div><div class="%s-tx" style="left:%dpx;top:%dpx">%s</div></div>'
            % (P, x, y, w, h, P, nx - 29, ny - 29, n, P, tx, ty, text))

wires = ('<svg class="%s-sv" viewBox="0 0 1672 941">%s<g fill="none" stroke="#f4ecd2" stroke-width="1.6" stroke-dasharray="8 6" opacity=".9">'
         '<path d="M985 245L836 362"/><path d="M1043 282V362"/><path d="M1102 248L1252 362"/></g>'
         '<g fill="none" stroke="#f6d36a" stroke-width="4" filter="url(#%s-gl)">'
         '<path d="M612 406H748" marker-end="url(#%s-ah)"/><path d="M872 406H980" marker-end="url(#%s-ah)"/>'
         '<path d="M1102 406H1212" marker-end="url(#%s-ah)"/><path d="M1334 406H1440" marker-end="url(#%s-ah)"/></g></svg>' % ((P, defs(P)) + (P,) * 5))
HTML = CSS + bg() + "".join([
    card(1, 20, 187, 396, 186, 58, 226, 107, 214, "Маршрут — запись<br>сегмента пути от шлюза<br>к шлюзу, определяющая<br>направление передачи<br>IP-пакетов."),
    card(2, 20, 395, 396, 212, 58, 435, 107, 423, "Устройство маршрутизации<br>переадресует пакеты<br>в подсеть назначения<br>на основе маршрутов<br>и поддерживает таблицу<br>IP-маршрутизации."),
    '<div class="step">' + wires + rt(1043, 222) + rt(812, 397) + rt(1043, 397) + rt(1274, 397) +
    '<div class="%s-r" style="left:1046px;top:160px">R4</div><div class="%s-r" style="left:811px;top:447px">R1</div>'
    '<div class="%s-r" style="left:1043px;top:447px">R2</div><div class="%s-r" style="left:1274px;top:447px">R3</div>' % ((P,) * 4) +
    cloud_at(P, 522, 408, 168, "Сеть N", 27) + cloud_at(P, 1548, 408, 196, "Сеть M", 27) + '</div>',
    '<div class="step">' + img("based_cube.png", "left:660px;top:360px;width:60px;height:50px") +
    '<div class="%s-t" style="left:684px;top:306px;font-size:20px;line-height:26px">IP-пакет</div>' % P +
    '<svg class="%s-sv" viewBox="0 0 1672 941"><path d="M707 337H758" stroke="#f0c75e" stroke-width="1.3"/><path d="M707 337V348" stroke="#f0c75e" stroke-width="1.3"/><circle cx="707" cy="337" r="3" fill="#f0c75e"/></svg></div>' % P,
    '<div class="step"><div class="%s-lb" style="left:756px;top:478px;width:110px;height:43px">Шлюз</div>'
    '<div class="%s-lb" style="left:948px;top:475px;width:192px;height:52px;line-height:21px">Промежуточный<br>маршрутизатор</div>'
    '<div class="%s-lb" style="left:1196px;top:475px;width:178px;height:52px;line-height:21px">Последний<br>маршрутизатор</div></div>' % ((P,) * 3),
    card(3, 433, 572, 395, 172, 473, 611, 519, 596, "Шлюз и промежуточный<br>маршрутизатор выбирают путь<br>по адресу назначения<br>и пересылают пакет<br>следующему узлу."),
    card(4, 843, 572, 408, 172, 882, 611, 933, 596, "Промежуточный<br>маршрутизатор выбирает<br>наилучший путь по своей<br>таблице: исходящий интерфейс<br>и адрес следующего узла."),
    card(5, 1267, 572, 389, 172, 1305, 611, 1353, 596, "Последний маршрутизатор<br>выполняет адресацию<br>уровня 2 и передаёт пакет<br>хосту назначения."),
    '<div class="step"><div class="%s-pn" style="left:578px;top:863px;width:515px;height:49px;border-radius:25px"></div>'
    '<div class="%s-t" style="left:578px;top:870px;width:515px;text-align:center;font:500 28px/34px \'Playfair Display\',serif;color:#f6ebc8">Передача на основе маршрута</div>'
    '<svg class="%s-sv" viewBox="0 0 1672 941"><path d="M600 843H822M848 843H1070" stroke="#f0c75e" stroke-width="1.3" opacity=".8"/>'
    '<path d="M835 833L845 843L835 853L825 843z" fill="none" stroke="#f0c75e" stroke-width="2"/></svg></div>' % ((P,) * 3),
])
