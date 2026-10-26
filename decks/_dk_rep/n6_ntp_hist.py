# -*- coding: utf-8 -*-
"""2.6: протокол сетевого времени — история, иерархия источников, зачем точное время (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 100

CSS = """<style>
.n6nh-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.6);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6nh-sub{position:absolute;font:700 31px/1 "Golos Text",sans-serif;color:#8cb4ff;white-space:nowrap}
.n6nh-tb{position:absolute;box-sizing:border-box;height:46px;border-radius:12px;font:800 20px/46px Montserrat,sans-serif;color:#111;padding-left:72px;white-space:nowrap}
.n6nh-nu{position:absolute;width:44px;height:44px;border-radius:50%;background:#0c1630;border:2px solid;font:800 22px/40px Montserrat,sans-serif;
  color:#fff;text-align:center;box-sizing:border-box}
.n6nh-t{position:absolute;font:500 18px/1.2 "Golos Text",sans-serif;color:#e6eefc;white-space:nowrap}
.n6nh-h{position:absolute;font:800 22px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6nh-c{position:absolute;box-sizing:border-box;border-radius:12px;overflow:hidden}
.n6nh-ct{position:absolute;font:700 19px/1.1 "Golos Text",sans-serif;color:#111;white-space:nowrap}
.n6nh-dv{position:absolute;box-sizing:border-box;height:46px;border-radius:7px;border:1.5px solid rgba(140,190,255,.4);background:rgba(16,30,60,.85);
  font:500 15px/1.15 "Golos Text",sans-serif;color:#e6eefc;padding-left:14px;display:flex;align-items:center}
.n6nh-tag{position:absolute;box-sizing:border-box;height:36px;border-radius:7px;background:#ff7a58;border:1.5px solid #ffb090;
  font:700 18px/33px "Golos Text",sans-serif;color:#111;text-align:center;box-shadow:0 0 16px rgba(255,122,88,.6)}
.n6nh-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6nh-fl{stroke-dasharray:10 8;animation:n6nhd 1.1s linear infinite}
@keyframes n6nhd{to{stroke-dashoffset:-36}}
.n6nh-ar{position:absolute;font:800 30px/1 sans-serif;color:#3ad8ff;text-shadow:0 0 10px #3ad8ff}
</style>"""

STAGES = [(30, 340, "#ffd84a", "1", "Ранние компьютеры", "Время задавали операторы<br>вручную", "n6_ntp_hist_c1.png", (35, 285, 337)),
          (383, 308, "#ff7a58", "2", "1950–1960-е", "Операционные системы<br>получили функции работы<br>со временем", "n6_ntp_hist_c2.png", (383, 312, 309)),
          (701, 309, "#b97bff", "3", "Рост сетей", "Компьютерам понадобилась<br>синхронизация часов", "n6_ntp_hist_c3.png", (703, 290, 309)),
          (1019, 270, "#7ef06a", "4", "NTP", "Сетевой протокол<br>синхронизации времени", "n6_ntp_hist_c4.png", (1058, 292, 174)),
          (1301, 344, "#9cdcff", "5", "Сегодня", "GPS и атомные часы служат<br>точными источниками<br>времени", "n6_ntp_hist_c5.png", (1303, 306, 339))]


def stage(x, w, col, n, title, text, pic, pp):
    return ('<div class="step"><div class="n6nh-p" style="left:%dpx;top:168px;width:%dpx;height:326px"></div>' % (x, w)
            + img(pic, "left:%dpx;top:%dpx;width:%dpx" % pp)
            + '<div class="n6nh-tb" style="left:%dpx;top:184px;width:%dpx;background:%s;box-shadow:0 0 16px %s">%s</div>' % (x + 16, w - 34, col, col, title)
            + '<div class="n6nh-nu" style="left:%dpx;top:185px;border-color:%s">%s</div>' % (x + 20, col, n)
            + '<div class="n6nh-t" style="left:%dpx;top:240px">%s</div>' % (x + 32, text)
            + ('<div class="n6nh-ar" style="left:%dpx;top:312px">&#10140;</div>' % (x - 22) if x > 40 else "") + '</div>')


DEV = ["Компьютеры", "Ноутбуки", "Серверы", "Сетевые<br>устройства", "IoT-устройства"]
DY = [578, 638, 698, 758, 828]

CHAIN = ('<div class="step"><div class="n6nh-p" style="left:28px;top:512px;width:1012px;height:402px"></div>'
         '<div class="n6nh-h" style="left:48px;top:533px">GPS / атомные часы → NTP-серверы → компьютеры и сетевые устройства</div>'
         '<div class="n6nh-c" style="left:48px;top:583px;width:248px;height:120px;background:#ffd84a"></div>'
         + img("n6_ntp_hist_earth.png", "left:140px;top:640px;width:156px") + img("n6_ntp_hist_sat.png", "left:58px;top:593px;width:82px")
         + '<div class="n6nh-ct" style="left:156px;top:603px">GPS</div>'
         '<div class="n6nh-c" style="left:48px;top:718px;width:248px;height:178px;background:#bfe6ff"></div>'
         + img("n6_ntp_hist_lab.png", "left:58px;top:790px;width:238px") + img("n6_ntp_hist_atom.png", "left:62px;top:728px;width:66px")
         + '<div class="n6nh-ct" style="left:146px;top:740px">Атомные<br>часы</div>'
         + img("n6_ntp_hist_cluster.png", "left:378px;top:618px;width:274px")
         + '<div class="n6nh-tag" style="left:436px;top:588px;width:200px">NTP-серверы</div>'
         + "".join(img("n6_ntp_hist_d%d.png" % (i + 1), "left:785px;top:%dpx;width:91px" % DY[i]) for i in range(5))
         + "".join('<div class="n6nh-dv" style="left:883px;top:%dpx;width:136px">%s</div>' % (DY[i] + 4, DEV[i]) for i in range(5))
         + '<svg class="n6nh-sv" viewBox="0 0 1672 941"><g stroke="#3ad8ff" stroke-width="3" fill="none" style="filter:drop-shadow(0 0 4px #3ad8ff)">'
           '<path class="n6nh-fl" d="M296 622C340 622 330 700 400 706M296 800C340 800 330 712 400 712"/>'
           + "".join('<path class="n6nh-fl" d="M650 720C700 720 700 %d 764 %d"/>' % (y + 26, y + 26) for y in DY) + '</g>'
         + "".join('<path d="M776 %dl-14-8v16z" style="fill:#3ad8ff"/>' % (y + 26) for y in DY)
         + '<path d="M410 709l-14-8v16z" style="fill:#3ad8ff"/></svg></div>')

WHY = [(1068, 576, "#ffd84a", "w1", "Безопасность", (1078, 593), (1148, 608, 169)),
       (1338, 576, "#ff7a58", "w2", "Согласованность<br>данных", (1350, 593), (1448, 630, 159)),
       (1068, 682, "#b97bff", "w3", "Аутентификация", (1080, 698), (1148, 723, 164)),
       (1338, 682, "#7ef06a", "w4", "Финансы", (1350, 698), (1430, 745, 187)),
       (1068, 790, "#9cdcff", "w5", "Телеком", (1083, 803), (1150, 842, 172)),
       (1338, 790, "#ffd84a", "w6", "Научные<br>исследования", (1348, 798), (1440, 858, 177))]

WHYP = ('<div class="step"><div class="n6nh-p" style="left:1050px;top:512px;width:594px;height:402px"></div>'
        '<div class="n6nh-h" style="left:1076px;top:530px;font-size:31px">Зачем нужно точное время?</div>'
        + "".join('<div class="n6nh-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"></div>' % (x, y, 262 if x < 1300 else 284, 98 if y < 790 else 108, c)
                  + img("n6_ntp_hist_%s.png" % k, "left:%dpx;top:%dpx;width:%dpx" % (ix, iy, {"w1": 49, "w2": 52, "w3": 44, "w4": 47, "w5": 54, "w6": 59}[k]))
                  + img("n6_ntp_hist_%sp.png" % k, "left:%dpx;top:%dpx;width:%dpx" % pp)
                  + '<div class="n6nh-ct" style="left:%dpx;top:%dpx;font-size:18px">%s</div>' % (x + 74, y + 12, t)
                  for x, y, c, k, t, (ix, iy), pp in WHY) + '</div>')

HTML = (CSS + bg("bgk_space")
        + '<div class="step"><div class="n6nh-sub" style="left:66px;top:113px">Единое время для компьютеров, сетей и всего мира</div></div>'
        + "".join(stage(*s) for s in STAGES) + CHAIN + WHYP)
