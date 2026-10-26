# -*- coding: utf-8 -*-
"""2.6: NTP — история, иерархия источников, где нужно точное время, как работает (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.n6nt-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.6);border-radius:14px;box-shadow:0 0 20px rgba(58,160,255,.3)}
.n6nt-t{position:absolute;font:500 15px/1.25 "Golos Text",sans-serif;color:#e6eefc;white-space:nowrap}
.n6nt-h{position:absolute;font:800 26px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6nt-b{position:absolute;font:700 17px/1.2 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6nt-s{position:absolute;font:500 12.5px/1.2 "Golos Text",sans-serif;color:#c8d6ee;white-space:nowrap}
.n6nt-col{position:absolute;box-sizing:border-box;height:34px;border-radius:7px;font:800 19px/34px "Golos Text",sans-serif;color:#111;text-align:center}
.n6nt-box{position:absolute;box-sizing:border-box;border:1.5px solid rgba(92,190,255,.45);border-radius:10px;background:rgba(10,24,52,.6)}
.n6nt-r{position:absolute;box-sizing:border-box;width:314px;height:68px;border-radius:9px;padding:6px 0 0 70px;color:#111}
.n6nt-r b{display:block;font:800 15px/1.05 Montserrat,sans-serif}
.n6nt-r span{display:block;font:500 11.5px/1.12 "Golos Text",sans-serif;margin-top:2px}
.n6nt-nu{position:absolute;width:34px;height:34px;border-radius:50%;font:800 20px/34px Montserrat,sans-serif;color:#fff;text-align:center}
.n6nt-tbl{position:absolute;border-collapse:collapse;font:500 13px "Golos Text",sans-serif;color:#e6eefc}
.n6nt-tbl td{border-bottom:1px solid rgba(120,170,240,.3);height:33px;padding:0 10px}
.n6nt-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6nt-fl{stroke-dasharray:8 7;animation:n6ntd 1.1s linear infinite}
@keyframes n6ntd{to{stroke-dashoffset:-30}}
.n6nt-wv{stroke-dasharray:240;animation:n6ntw 3s linear infinite}
@keyframes n6ntw{from{stroke-dashoffset:240}to{stroke-dashoffset:0}}
</style>"""


def P(x, y, w, h, st=""):
    return '<div class="n6nt-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"></div>' % (x, y, w, h, st)


def T(x, y, t, cls="n6nt-t", st=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, st, t)


def SV(b):
    return '<svg class="n6nt-sv" viewBox="0 0 1672 941">' + b + '</svg>'


HEAD = ('<div class="step">' + P(28, 112, 1615, 104, "background:linear-gradient(90deg,rgba(16,40,90,.7),rgba(6,14,36,.2))")
        + T(54, 114, "Network Time Protocol", st="font:600 32px/1 'Golos Text',sans-serif;color:#8cb4ff")
        + T(54, 154, "NTP — это клиент-серверный протокол, который распространяет точное время<br>от эталонных источников через NTP-серверы к клиентам в сети.",
            st="font-size:21px;color:#dbe6fa") + '</div>')

HIST = ('<div class="step">' + P(28, 232, 314, 384) + img("n6_ntp_hclk.png", "left:43px;top:243px;width:49px")
        + T(110, 251, "История", "n6nt-h")
        + SV('<path d="M50 316V512" stroke="#4a5a80" stroke-width="2"/><circle cx="50" cy="318" r="5" fill="none" stroke="#ffd84a" stroke-width="2"/>'
             '<circle cx="50" cy="413" r="5" fill="none" stroke="#ff7a58" stroke-width="2"/><circle cx="50" cy="512" r="5" fill="none" stroke="#b97bff" stroke-width="2"/>')
        + img("n6_ntp_cal.png", "left:73px;top:298px;width:59px") + img("n6_ntp_doc.png", "left:73px;top:388px;width:59px")
        + img("n6_ntp_gear.png", "left:73px;top:495px;width:59px")
        + T(145, 301, "Конец 1970-х:", "n6nt-b", "color:#ffd84a") + T(145, 322, "Дэвид Миллс начал<br>разработку NTP.")
        + T(145, 390, "NTPv1–v3", "n6nt-b", "color:#ff8a5a") + T(145, 412, "Развитие алгоритмов,<br>повышение точности<br>и масштабируемости.")
        + T(145, 498, "NTPv4 —<br>современная версия<br>протокола.", "n6nt-b", "color:#c890ff")
        + T(145, 562, "Широко используется<br>и активно поддерживается.", st="font-size:14px") + '</div>')

SRC = ('<div class="step">' + P(352, 232, 942, 384)
       + '<div class="n6nt-col" style="left:373px;top:252px;width:272px;background:#ffd84a">Источники времени</div>'
       + '<div class="n6nt-col" style="left:702px;top:252px;width:228px;background:#ff7a58">NTP-серверы</div>'
       + '<div class="n6nt-col" style="left:985px;top:252px;width:282px;background:#78c8ff">Клиенты сети</div>'
       + T(655, 252, "&#10095;&#10095;&#10095;", st="font-size:22px;color:#5cd2ff") + T(940, 252, "&#10095;&#10095;&#10095;", st="font-size:22px;color:#5cd2ff")
       + '<div class="n6nt-box" style="left:374px;top:298px;width:268px;height:134px"></div>'
       + '<div class="n6nt-box" style="left:374px;top:443px;width:268px;height:156px"></div>'
       + img("n6_ntp_atomc.png", "left:383px;top:303px;width:114px") + img("n6_ntp_atom.png", "left:503px;top:313px;width:49px")
       + T(508, 368, "Атомные часы", "n6nt-b") + T(508, 392, "Высокоточные<br>эталоны времени", "n6nt-s", "font-size:13px")
       + img("n6_ntp_sats.png", "left:388px;top:453px;width:114px") + img("n6_ntp_dish.png", "left:508px;top:463px;width:89px")
       + img("n6_ntp_tower.png", "left:393px;top:528px;width:49px")
       + T(444, 528, "GPS", "n6nt-b") + T(444, 550, "Глобальные<br>спутниковые<br>системы", "n6nt-s", "font-size:13px")
       + img("n6_ntp_s1.png", "left:718px;top:293px;width:106px") + img("n6_ntp_s2.png", "left:718px;top:386px;width:106px")
       + img("n6_ntp_s3.png", "left:718px;top:478px;width:106px")
       + T(832, 320, "Сервер 1<br>(источник 1)") + T(832, 407, "Сервер 2<br>(источник 2)") + T(832, 500, "Сервер 3<br>(источник 3)")
       + img("n6_ntp_mon.png", "left:1018px;top:298px;width:74px") + img("n6_ntp_lap.png", "left:1088px;top:318px;width:84px")
       + img("n6_ntp_srv.png", "left:1198px;top:308px;width:74px") + img("n6_ntp_rt.png", "left:1008px;top:408px;width:119px")
       + img("n6_ntp_cam.png", "left:1133px;top:418px;width:69px") + img("n6_ntp_ph.png", "left:1213px;top:423px;width:49px")
       + T(982, 518, "Компьютеры и сетевые устройства", "n6nt-b") + T(985, 550, "Клиенты синхронизируют свои часы,<br>обращаясь к нескольким NTP-серверам.")
       + SV('<g stroke="#5cd2ff" stroke-width="2" fill="none" style="filter:drop-shadow(0 0 3px #5cd2ff)">'
            '<path class="n6nt-fl" d="M642 345H676V335H712M676 345V430H712M642 490H676V520H712M676 430V520"/>'
            '<path class="n6nt-fl" d="M912 330H944V340H1010M944 340V430H1000M912 415H944M912 510H944V430M944 380H1012"/></g>')
       + '</div>')

NEED = [("#ffd84a", "Безопасности<br>и аутентификации", "Корректная работа сертификатов,<br>протоколов и журналов доступа."),
        ("#ff7a58", "Журналов событий", "Точные и согласованные записи<br>для анализа и расследований."),
        ("#b97bff", "Согласованности данных", "Единое время в распределённых<br>системах и базах данных."),
        ("#7ef06a", "Финансов", "Корректная отметка времени<br>в транзакциях и торговых системах."),
        ("#78c8ff", "Телекоммуникаций и науки", "Синхронизация сетей, измерений<br>и научных экспериментов.")]
NY = [276, 360, 435, 510, 585]

RIGHT = ('<div class="step">' + P(1304, 232, 344, 434) + T(1322, 242, "Точное время нужно для", "n6nt-h", "font-size:23px")
         + "".join('<div class="n6nt-r" style="left:1320px;top:%dpx;background:%s;box-shadow:0 0 12px %s"><b>%s</b><span>%s</span></div>' % (y, c, c, t, s)
                   + img("n6_ntp_r%d.png" % (i + 1), "left:1328px;top:%dpx;width:50px" % (y + 8))
                   for i, (y, (c, t, s)) in enumerate(zip(NY, NEED))) + '</div>')


def step_box(x, w, col, n, title, note):
    return (P(x, 676, w, 208) + '<div class="n6nt-nu" style="left:%dpx;top:688px;background:%s;box-shadow:0 0 12px %s">%s</div>' % (x + 62 if n == "1" else x + 22, col, col, n)
            + T(x + (112 if n == "1" else 72), 686, title, "n6nt-b", "font-size:14px") + T(x + 24, 834, note, "n6nt-s"))


HOW = (P(28, 628, 1265, 50, "border-radius:14px 14px 0 0;border-bottom:0") + img("n6_ntp_hgear.png", "left:43px;top:638px;width:49px")
       + T(110, 644, "Как работает", "n6nt-h"))

H1 = ('<div class="step">' + HOW + step_box(44, 397, "#3aa0ff", "1", "Клиент обращается<br>к нескольким серверам времени",
                                           "Клиент отправляет запросы одновременно<br>к нескольким NTP-серверам.")
      + img("n6_ntp_lap1.png", "left:83px;top:743px;width:134px") + img("n6_ntp_srvs1.png", "left:333px;top:723px;width:64px")
      + SV('<g stroke="#5cd2ff" stroke-width="2.5" fill="none"><path class="n6nt-fl" d="M218 768L325 742M218 785H325M218 800L325 830"/></g>') + '</div>')

H2 = ('<div class="step">' + step_box(456, 380, "#b97bff", "2", "Сравнение источников помогает<br>выбрать стабильное время",
                                     "Клиент сравнивает полученные ответы<br>и выбирает наиболее надёжные источники<br>(с учётом их стабильности).")
      + '<table class="n6nt-tbl" style="left:484px;top:726px;width:330px;border:1px solid rgba(120,170,240,.35)">'
        '<tr><td>Сервер 1</td><td style="color:#5ce06a;font-size:20px">&#10004;</td><td style="width:180px"></td></tr>'
        '<tr><td>Сервер 2</td><td style="color:#ff9a2a;font-size:20px">&#9888;</td><td></td></tr>'
        '<tr><td>Сервер 3</td><td style="color:#5ce06a;font-size:20px">&#10004;</td><td></td></tr></table>'
      + SV('<path class="n6nt-wv" d="M630 742q10-3 20 0t20 0t20 0t20 0t20 0t20 0t20 0t20 0t20 0" stroke="#5cd2ff" stroke-width="2" fill="none"/>'
           '<path class="n6nt-wv" d="M630 775q5-9 10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0t10 0" stroke="#ff9a2a" stroke-width="2" fill="none"/>'
           '<path class="n6nt-wv" d="M630 808q10-3 20 0t20 0t20 0t20 0t20 0t20 0t20 0t20 0t20 0" stroke="#5cd2ff" stroke-width="2" fill="none"/>'
           '<path d="M622 730V826" stroke="rgba(120,170,240,.35)"/>') + '</div>')

H3 = ('<div class="step">' + step_box(853, 379, "#6ee07a", "3", "Сетевая задержка и джиттер<br>учитываются при синхронизации", "")
      + img("n6_ntp_lap3.png", "left:893px;top:733px;width:84px") + img("n6_ntp_srv3.png", "left:1133px;top:723px;width:69px")
      + T(1012, 726, "Запрос (t1)", st="font-size:13px") + T(1018, 776, "Ответ (t4)", st="font-size:13px")
      + T(1114, 738, "t2", st="font-size:12px") + T(1114, 762, "t3", st="font-size:12px")
      + SV('<g stroke="#e6eefc" stroke-width="2" fill="none"><path class="n6nt-fl" d="M972 750H1104M1104 770H982"/></g>'
           '<path d="M1110 750l-10-5v10zM976 770l10-5v10z" style="fill:#e6eefc"/>')
      + '<div class="n6nt-box" style="left:866px;top:804px;width:174px;height:72px;border-color:#5ce06a;background:rgba(20,60,30,.6)"></div>'
      + img("n6_ntp_dly.png", "left:873px;top:818px;width:39px")
      + T(924, 810, "Сетевая задержка", "n6nt-b", "font-size:12px;color:#8cf07a") + T(924, 828, "Время в пути<br>туда и обратно", "n6nt-s", "font-size:10px")
      + T(924, 856, "оценивается и учитывается.", "n6nt-s", "font-size:8.5px")
      + '<div class="n6nt-box" style="left:1051px;top:804px;width:170px;height:72px"></div>'
      + img("n6_ntp_jit.png", "left:1053px;top:820px;width:59px")
      + T(1115, 810, "Джиттер", "n6nt-b", "font-size:12px") + T(1115, 828, "Изменчивость<br>задержки в сети,", "n6nt-s", "font-size:10px")
      + T(1115, 856, "влияет на стабильность.", "n6nt-s", "font-size:8.5px") + '</div>')

H4 = ('<div class="step">' + step_box(1242, 406, "#ff7a58", "4", "Клиент синхронизирует часы<br>с выбранными источниками",
                                     "Клиент корректирует свои часы,<br>постепенно подстраиваясь к стабильным<br>источникам (фильтрация и усреднение).")
      + img("n6_ntp_lap4.png", "left:1293px;top:733px;width:149px") + img("n6_ntp_srvs4.png", "left:1533px;top:698px;width:59px")
      + SV('<g stroke="#5cd2ff" stroke-width="2.5" fill="none"><path class="n6nt-fl" d="M1442 770L1528 722M1442 780H1528M1442 792L1528 820"/></g>'
           '<g style="fill:#5cd2ff"><path d="M454 760l-12-7v14zM848 760l-12-7v14zM1240 760l-12-7v14z"/></g>') + '</div>')

FOOT = ('<div class="step">' + P(28, 894, 1615, 40, "border-radius:10px") + img("n6_ntp_udp.png", "left:88px;top:896px;width:32px")
        + T(148, 903, "<b style='font-weight:800'>NTP</b> использует UDP-порт 123", st="font-size:16px")
        + SV('<path d="M446 900V928" stroke="rgba(120,170,240,.4)"/>') + img("n6_ntp_bsh.png", "left:535px;top:892px;width:40px")
        + T(634, 897, "Аутентификация и обновления помогают защитить синхронизацию", "n6nt-b", "font-size:13.5px")
        + T(634, 915, "NTPv4 поддерживает опциональную аутентификацию сообщений. Правильная настройка и регулярные обновления важны для точности и безопасности.",
            "n6nt-s", "font-size:12px") + '</div>')

HTML = CSS + bg("bgk_globe") + HEAD + HIST + SRC + RIGHT + H1 + H2 + H3 + H4 + FOOT
