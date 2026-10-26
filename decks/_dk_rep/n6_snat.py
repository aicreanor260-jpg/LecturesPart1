# -*- coding: utf-8 -*-
"""2.6: Source NAT — путь пакета, таблица NAT, режимы, ответный трафик (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 72

CSS = """<style>
.n6sn-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.6);border-radius:12px;box-shadow:0 0 18px rgba(58,160,255,.3)}
.n6sn-t{position:absolute;font:500 16px/1.25 "Golos Text",sans-serif;color:#e6eefc;white-space:nowrap}
.n6sn-h{position:absolute;font:800 22px/1.1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6sn-hd{position:absolute;font:700 16px/1.2 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6sn-s{position:absolute;font:500 11px/1.25 "Golos Text",sans-serif;color:#c8d6ee;white-space:nowrap}
.n6sn-f{position:absolute;box-sizing:border-box;border-radius:7px;font:500 13px/1.18 "Golos Text",sans-serif;color:#111;padding:5px 0 0 58px;white-space:nowrap}
.n6sn-f b{font-weight:700}
.n6sn-tb{position:absolute;border-collapse:collapse;font:500 13px/1.2 "Golos Text",sans-serif;color:#e6eefc}
.n6sn-tb td,.n6sn-tb th{border:1px solid rgba(120,170,240,.3);text-align:center;height:24px;padding:0 4px;font-weight:500}
.n6sn-tb th{height:38px;font-size:13px}
.n6sn-ok{color:#5ce06a}
.n6sn-m{position:absolute;box-sizing:border-box;height:42px;border-radius:9px 9px 0 0;font:800 19px/42px Montserrat,sans-serif;color:#111;padding-left:66px;white-space:nowrap}
.n6sn-m span{position:absolute;right:14px;top:0;font:500 12px/1.2 "Golos Text",sans-serif;padding-top:6px;text-align:center}
.n6sn-li{position:absolute;font:500 13px/1.25 "Golos Text",sans-serif;color:#e6eefc;white-space:nowrap}
.n6sn-li i{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 8px 0 -16px;vertical-align:1px}
.n6sn-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6sn-fl{stroke-dasharray:12 8;animation:n6snd 1s linear infinite}
@keyframes n6snd{to{stroke-dashoffset:-40}}
</style>"""


def P(x, y, w, h, st=""):
    return '<div class="n6sn-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"></div>' % (x, y, w, h, st)


def T(x, y, t, cls="n6sn-t", st=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, st, t)


def F(x, y, w, h, col, ico, t1, t2):
    return ('<div class="n6sn-f" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"><b>%s</b><br>%s</div>' % (x, y, w, h, col, t1, t2)
            + img(ico, "left:%dpx;top:%dpx;width:30px" % (x + 16, y + (h - 30) // 2)))


def SV(body):
    return '<svg class="n6sn-sv" viewBox="0 0 1672 941">' + body + '</svg>'


def A(d, end, col, cls="n6sn-fl"):
    x, y = end
    return ('<path class="%s" d="%s" stroke="%s" stroke-width="4" fill="none" style="filter:drop-shadow(0 0 4px %s)"/>'
            '<path d="M%d %dl-16-10v20z" fill="%s"/>' % (cls, d, col, col, x, y, col))


Y, O, B, G = "#ffd84a", "#ff7a58", "#78c8ff", "#8cf07a"

TOPROW = ('<div class="step">'
          + P(14, 98, 380, 335, "border-color:#4ce0a0") + img("n6_snat_sh.png", "left:33px;top:106px;width:49px")
          + T(98, 110, "Trusted <span style='font-weight:600;font-size:20px'>— доверенная сеть</span>", "n6sn-h")
          + T(100, 143, "Частные IP-адреса<br>&nbsp;&nbsp;&nbsp;&nbsp;(локальная сеть)", st="font-size:16px")
          + img("n6_snat_pcs.png", "left:72px;top:198px;width:260px")
          + T(68, 387, "Устройство отправляет пакет<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;в Интернет")
          + P(1278, 98, 380, 335, "border-color:#ff5a5a;background:linear-gradient(160deg,rgba(90,20,30,.7),rgba(30,8,14,.9))")
          + img("n6_snat_ush.png", "left:1288px;top:106px;width:49px")
          + T(1342, 110, "<span style='font-size:20px'>Untrusted</span> <span style='font-weight:600;font-size:18px'>— недоверенная сеть</span>", "n6sn-h")
          + T(1452, 145, "Интернет<br>(публичные сети)", st="text-align:center;margin-left:-14px")
          + img("n6_snat_cloud.png", "left:1348px;top:192px;width:197px") + img("n6_snat_xsrv.png", "left:1508px;top:288px;width:84px")
          + T(1488, 399, "Внешний сервер")
          + '</div>')

BOXES = ('<div class="step">'
         + P(572, 98, 198, 86, "border-color:#b77bff") + img("n6_snat_i1.png", "left:588px;top:110px;width:49px")
         + T(643, 115, "Проверка правила", "n6sn-hd", "font-size:13px") + T(643, 138, "Соответствует ли пакет<br>правилу SNAT?", "n6sn-s")
         + P(784, 98, 162, 86) + img("n6_snat_i2.png", "left:792px;top:108px;width:46px")
         + T(840, 108, "Object-group<br>частных адресов", "n6sn-hd", "font-size:12px") + T(840, 141, "Определяет, какие<br>внутренние адреса<br>подлежат трансляции", "n6sn-s", "font-size:10px")
         + P(960, 98, 180, 86, "border-color:#4ce060") + img("n6_snat_i3.png", "left:973px;top:110px;width:54px")
         + T(1036, 113, "Пул публичных<br>адресов", "n6sn-hd", "font-size:12px") + T(1036, 147, "Из него выбирается<br>публичный IP", "n6sn-s", "font-size:10px")
         + SV('<path d="M745 186L790 234" stroke="#e070ff" stroke-width="3" fill="none"/><path d="M836 186V230" stroke="#5cd2ff" stroke-width="3" fill="none"/>'
              '<path d="M976 186V200L900 234" stroke="#5ce06a" stroke-width="3" fill="none"/>')
         + img("n6_snat_rt.png", "left:768px;top:238px;width:139px")
         + T(762, 332, "Маршрутизатор<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SNAT", "n6sn-hd", "font-size:18px")
         + '</div>')

BEFORE = ('<div class="step">' + P(360, 188, 293, 192)
          + T(378, 194, "До SNAT:<br>источник — частный IP:порт<br>назначение — сервер", "n6sn-hd")
          + T(412, 250, "Адрес назначения не меняется", st="font-size:13px;color:#c8d6ee")
          + F(373, 273, 267, 43, Y, "n6_snat_user.png", "Источник", "Частный IP:порт")
          + F(373, 324, 267, 45, B, "n6_snat_sicon.png", "Назначение", "Публичный IP:порт (сервер)")
          + SV('<path d="M330 290H360" stroke="#3ab8ff" stroke-width="4"/>' + A("M655 290H750", (764, 290), "#3ab8ff")) + '</div>')

AFTER = ('<div class="step">' + P(1018, 188, 294, 192)
         + T(1050, 196, "После SNAT:<br>источник — публичный IP:порт<br>назначение — сервер", "n6sn-hd")
         + T(1088, 252, "Адрес назначения не меняется", st="font-size:13px;color:#c8d6ee")
         + F(1032, 273, 267, 43, O, "n6_snat_user.png", "Источник", "Публичный IP:порт")
         + F(1032, 324, 267, 45, B, "n6_snat_sicon.png", "Назначение", "Публичный IP:порт (сервер)")
         + SV(A("M905 290H1006", (1014, 290), "#3ab8ff") + A("M1312 290H1350", (1360, 290), "#3ab8ff")
              + '<path d="M1450 285V345H1505" stroke="#ff7a3a" stroke-width="3" fill="none"/>') + '</div>')

ROWS = [("Частный_IP1:порт1", "Публичный_IP1:портA"), ("Частный_IP2:порт2", "Публичный_IP2:портB"), ("Частный_IP3:порт3", "Публичный_IP1:портC")]
TABLE = ('<div class="step">' + P(428, 390, 816, 180)
         + T(757, 393, "Таблица NAT", "n6sn-h", "font-size:24px")
         + '<table class="n6sn-tb" style="left:444px;top:424px;width:785px"><tr><th>Частный IP:порт<br>(внутренний)</th><th style="width:30px"></th>'
           '<th>Публичный IP:порт<br>(внешний)</th><th>Адрес назначения<br>(сервер)</th><th>Состояние</th></tr>'
         + "".join('<tr><td>%s</td><td>&harr;</td><td>%s</td><td>Сервер_IP:порт</td><td class="n6sn-ok">Активна</td></tr>' % r for r in ROWS)
         + '<tr><td>…</td><td></td><td>…</td><td>…</td><td>…</td></tr></table></div>')


def mode(x, w, col, ico, title, note, bullets, bx, dot, pics, svg):
    s = P(x, 586, w, 172, "border-color:%s;background:linear-gradient(160deg,rgba(40,34,20,.75),rgba(10,12,24,.9))" % col)
    s += '<div class="n6sn-m" style="left:%dpx;top:586px;width:%dpx;background:%s">%s<span>%s</span></div>' % (x, w, col, title, note)
    s += img(ico, "left:%dpx;top:590px;width:36px" % (x + 14))
    s += "".join('<div class="n6sn-li" style="left:%dpx;top:%dpx"><i style="background:%s"></i>%s</div>' % (bx, by, dot, t) for by, t in bullets)
    return s + "".join(img(*p) for p in pics) + SV(svg)


MODES = ('<div class="step">' + T(32, 556, "Режимы трансляции Source NAT", "n6sn-h")
         + mode(20, 538, Y, "n6_snat_m1.png", "1.&nbsp; Статический SNAT", "<br>Постоянная связка 1:1",
                [(640, "Каждому частному адресу<br>соответствует свой<br>фиксированный публичный IP."),
                 (698, "Используется, когда нужен<br>постоянный публичный адрес<br>(например, публикация сервисов).")], 337, Y,
                [("n6_snat_mon.png", "left:38px;top:662px;width:50px"), ("n6_snat_mrt.png", "left:128px;top:658px;width:69px"),
                 ("n6_snat_mgl.png", "left:243px;top:660px;width:44px")],
                '<path d="M90 686H126" stroke="#8cf07a" stroke-width="3" marker-end=""/><path d="M200 686H240" stroke="#ff7a58" stroke-width="3"/>')
         + T(38, 718, "Частный_IP_A", st="font-size:13px") + T(215, 710, "Публичный_IP_A", st="font-size:13px")
         + '</div><div class="step">'
         + mode(568, 536, O, "n6_snat_m2.png", "2. Динамический SNAT", "<br>Свободный публичный IP из пула",
                [(645, "Публичный IP временно<br>выделяется из пула<br>на время соединения."),
                 (701, "Один активный пользователь<br>на один публичный IP<br>в каждый момент времени.")], 902, O,
                [("n6_snat_pcs3.png", "left:583px;top:633px;width:49px"), ("n6_snat_mrt2.png", "left:666px;top:658px;width:71px"),
                 ("n6_snat_gls.png", "left:803px;top:653px;width:34px")],
                '<path d="M632 660H650V700H666M632 735H650V700" stroke="#5cd2ff" stroke-width="2.5" fill="none"/>'
                '<path d="M737 690H758" stroke="#ffd84a" stroke-width="3"/>'
                '<rect x="758" y="656" width="102" height="94" rx="6" stroke="#5cd2ff" stroke-width="1.5" stroke-dasharray="5 4" fill="none"/>')
         + T(778, 636, "Пул публичных IP", "n6sn-s") + '</div><div class="step">'
         + mode(1114, 538, G, "n6_snat_m3.png", "3. PAT", "Много частных узлов используют<br>один публичный IP через разные порты",
                [(645, "Многие частные узлы<br>используют один публичный IP<br>через разные порты."),
                 (703, "Отличаются номерами портов<br>в таблице NAT (перегрузка<br>по портам).")], 1446, G,
                [("n6_snat_pcs4.png", "left:1128px;top:638px;width:59px"), ("n6_snat_mrt3.png", "left:1220px;top:653px;width:74px"),
                 ("n6_snat_mgl3.png", "left:1336px;top:658px;width:44px")],
                '<path d="M1187 655L1222 680M1187 692H1222M1187 735L1222 700" stroke="#e070ff" stroke-width="2.5"/>'
                '<path class="n6sn-fl" d="M1296 683H1326" stroke="#ffd84a" stroke-width="3"/>')
         + T(1306, 704, "Один публичный IP<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;много портов", "n6sn-hd", "font-size:12px") + '</div>')

BACK = ('<div class="step">' + P(14, 776, 1644, 156)
        + img("n6_snat_sh2.png", "left:28px;top:786px;width:26px") + T(58, 790, "Ответный трафик из Интернета", "n6sn-hd")
        + img("n6_snat_bsrv.png", "left:86px;top:818px;width:76px") + T(46, 885, "Внешний сервер<br>(источник не меняется)", st="font-size:13px")
        + P(330, 784, 268, 138) + T(348, 790, "Ответ приходит на публичный адрес", "n6sn-hd", "font-size:13px")
        + F(340, 812, 248, 40, B, "n6_snat_sicon.png", "Источник", "Публичный IP:порт (сервер)")
        + F(340, 860, 248, 52, O, "n6_snat_user.png", "Назначение", "Публичный IP:порт<br>(адрес маршрутизатора)")
        + P(730, 776, 218, 50) + img("n6_snat_find.png", "left:743px;top:780px;width:39px")
        + T(794, 780, "NAT находит запись", "n6sn-hd", "font-size:12px") + T(794, 796, "и меняет адрес назначения<br>на частный", "n6sn-s")
        + img("n6_snat_brt.png", "left:793px;top:828px;width:84px") + T(775, 885, "Маршрутизатор<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SNAT", "n6sn-hd", "font-size:15px")
        + P(988, 784, 288, 138) + T(1006, 790, "После обратной трансляции (для ответа)", "n6sn-hd", "font-size:13px")
        + F(998, 812, 266, 40, B, "n6_snat_sicon.png", "Источник", "Публичный IP:порт (сервер)")
        + F(998, 860, 266, 52, Y, "n6_snat_user.png", "Назначение", "Частный IP:порт<br>(исходное устройство)")
        + P(1378, 784, 268, 138, "border-color:#4ce060") + img("n6_snat_sh3.png", "left:1388px;top:788px;width:34px")
        + T(1444, 790, "Ответ получает устройство,<br>начавшее соединение", "n6sn-hd", "font-size:13px")
        + img("n6_snat_bpcs.png", "left:1403px;top:828px;width:239px")
        + SV(A("M162 852H306", (316, 852), "#ff5a4a") + A("M600 858H772", (782, 858), "#ff5a4a")
             + A("M880 858H968", (978, 858), "#5ce06a") + A("M1278 858H1356", (1366, 858), "#5ce06a")
             + '<path d="M780 818V834" stroke="#5cd2ff" stroke-width="3"/>') + '</div>')

HTML = (CSS + bg("bgk_net")
        + '<div class="step">' + T(836, 75, "Исходящая трансляция: замена частного адреса источника на публичный при выходе в Интернет.", st="font-size:17px;color:#b9d2f5;transform:translateX(-50%)") + '</div>'
        + TOPROW + BOXES + BEFORE + AFTER + TABLE + MODES + BACK)
