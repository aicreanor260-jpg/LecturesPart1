# -*- coding: utf-8 -*-
"""NAT и NAPT: пять этапов — перехват, перевод, отправка, обратный перевод, доставка (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 18

YEL, ORA, VIO, GRN, BLU = "#ffc94a", "#ff8a3d", "#b77bff", "#6ee07a", "#5cd2ff"

USER = ('<svg viewBox="0 0 24 24" style="width:26px;height:26px;flex:none"><circle cx="12" cy="8" r="5" style="fill:#0a1430"/>'
        '<path d="M2 23c1-6 5-8 10-8s9 2 10 8z" style="fill:#0a1430"/></svg>')
GLB = ('<svg viewBox="0 0 24 24" style="width:26px;height:26px;flex:none"><g fill="none" stroke="#0a1430" stroke-width="2">'
       '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.5" ry="10"/><path d="M2 12h20"/></g></svg>')

CSS = """<style>
.n6np-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.72),rgba(6,14,36,.86));
  border:1.5px solid rgba(92,190,255,.6);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6np-b{position:absolute;box-sizing:border-box;height:52px;border-radius:26px;display:flex;align-items:center;gap:16px;padding:0 26px 0 6px;
  font:800 27px/1 Montserrat,sans-serif;color:#0a1430;white-space:nowrap;box-shadow:0 0 18px rgba(255,255,255,.18)}
.n6np-b i{width:42px;height:42px;border-radius:50%;background:#0a1430;color:#fff;font:800 25px/42px Montserrat,sans-serif;
  text-align:center;font-style:normal}
.n6np-t{position:absolute;font:400 16px/1.3 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6np-s{position:absolute;font:400 16px/1.25 "Golos Text",sans-serif;color:#fff;text-align:center;white-space:nowrap}
.n6np-pk{position:absolute;box-sizing:border-box;border-radius:10px;background:rgba(8,18,44,.92);border:1.5px solid rgba(92,190,255,.6);padding:8px}
.n6np-ph{font:700 17px/1 "Golos Text",sans-serif;color:#fff;margin:2px 0 10px 4px;white-space:nowrap}
.n6np-ph span{font-weight:400;font-size:15px}
.n6np-r{display:flex;align-items:center;height:36px;border-radius:7px;margin-top:6px;overflow:hidden;font:700 16px/36px "Golos Text",sans-serif;
  color:#0a1430;white-space:nowrap}
.n6np-r .k{display:flex;align-items:center;gap:7px;padding-left:8px;width:138px;height:36px;font-size:14px}
.n6np-r .v{flex:1;height:36px;padding-left:10px;font-weight:500;font-size:15px;border-radius:7px}
.n6np-tb{position:absolute;border-collapse:collapse;font:400 15px/1 "Golos Text",sans-serif;color:#fff}
.n6np-tb td{border:1px solid rgba(92,190,255,.35);height:30px;text-align:center}
.n6np-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6np-wire .fl{fill:none;stroke:#5cd2ff;stroke-width:4;filter:drop-shadow(0 0 6px #3aa0ff);stroke-dasharray:14 8;animation:n6npd 1s linear infinite}
.n6np-wire .or{stroke:#ffb347;filter:drop-shadow(0 0 6px #ff8a3d)}
.n6np-wire .th{stroke-width:2.5}
@keyframes n6npd{to{stroke-dashoffset:-44}}
.n6np-ii{display:inline-block;width:22px;height:22px;border-radius:50%;border:2px solid #5cd2ff;color:#5cd2ff;font:700 13px/19px Montserrat;
  text-align:center;box-sizing:border-box;margin-right:12px;vertical-align:middle}
</style>"""


def badge(x, y, n, col, text):
    return '<div class="n6np-b" style="left:%dpx;top:%dpx;background:%s"><i>%s</i>%s</div>' % (x, y, col, n, text)


def row(ico, key, kc, val, vc):
    return ('<div class="n6np-r" style="background:%s"><div class="k">%s%s</div><div class="v" style="background:%s">%s</div></div>'
            % (kc, ico, key, vc, val))


def pkt(x, y, w, head, sub, r1, r2):
    return ('<div class="n6np-pk" style="left:%dpx;top:%dpx;width:%dpx"><div class="n6np-ph">%s <span>%s</span></div>%s%s</div>'
            % (x, y, w, head, sub, r1, r2))


SRC_LOC = row(USER, "Источник:", "#5cd2ff", "Локальный IP:порт", YEL)
DST_SRV = row(GLB, "Назначение:", VIO, "IP-адрес сервера:порт", "#c9a2ff")
SRC_PUB = row(USER, "Источник:", "#5cd2ff", "Публичный IP:порт", ORA)
SRC_SRV = row(GLB, "Источник:", VIO, "IP-адрес сервера:порт", "#c9a2ff")
DST_PUB = row(USER, "Назначение:", "#5cd2ff", "Публичный IP:порт", ORA)
DST_LOC = row(USER, "Назначение:", "#5cd2ff", "Локальный IP:порт", YEL)

INTRO = ('<div class="step"><div style="position:absolute;left:50px;top:30px;width:1560px;font:400 23px/1.35 \'Golos Text\',sans-serif;'
         'color:#b9d2f5">Преобразование сетевых адресов позволяет устройствам из локальной сети безопасно получать доступ в интернет,<br>'
         'используя ограниченный пул публичных IP-адресов.</div></div>')

S1 = ('<div class="step"><div class="n6np-p" style="left:20px;top:102px;width:530px;height:488px"></div>'
      + badge(34, 115, 1, YEL, "Перехват пакета")
      + '<div class="n6np-t" style="left:110px;top:173px">Устройство отправляет пакет<br>из локальной сети</div>'
      '<div class="n6np-p" style="left:42px;top:224px;width:278px;height:172px;border-radius:12px"></div>'
      '<div class="n6np-s" style="left:42px;top:232px;width:278px">Локальная сеть<br>(частные IP-адреса)</div>'
      + img("n6_napt_lap.png", "left:52px;top:280px;width:108px") + img("n6_napt_pcd.png", "left:186px;top:284px;width:92px")
      + '<div class="n6np-s" style="left:46px;top:370px;width:120px">Устройство 1</div>'
        '<div class="n6np-s" style="left:180px;top:370px;width:120px">Устройство 2</div>'
      + img("n6_napt_sw.png", "left:393px;top:298px;width:164px")
      + '<svg class="n6np-wire"><path class="fl th" d="M280 320Q360 320 400 340M320 386Q360 360 400 352M118 398V432"/></svg>'
      + pkt(40, 433, 414, "Исходный пакет", "(из локальной сети)", SRC_LOC, DST_SRV) + '</div>')

S2 = ('<div class="step"><div class="n6np-p" style="left:560px;top:102px;width:443px;height:488px"></div>'
      + badge(578, 115, 2, ORA, "Перевод адреса")
      + '<div class="n6np-t" style="left:655px;top:174px;line-height:1.36">Локальный IP:порт → публичный IP:порт<br>'
        'Порт может изменяться при NAPT (PAT)<br>Запись сохраняется в таблице NAT</div>'
      + img("n6_napt_rt.png", "left:680px;top:252px;width:255px")
      + '<div class="n6np-s" style="left:693px;top:252px;width:216px;font:700 18px/1.1 Golos Text;text-shadow:0 0 6px #000,0 0 3px #000">NAT<br><span style="font-size:15px">маршрутизатор</span></div>'
      + '<div class="n6np-s" style="left:710px;top:392px;width:200px">Публичный IP<br>(из пула адресов)</div>'
      '<svg class="n6np-wire"><path class="fl" d="M552 346H668"/><path d="M660 334l18 12-18 12z" style="fill:#5cd2ff"/></svg>'
      '<div class="n6np-p" style="left:583px;top:435px;width:448px;height:164px;border-width:2px;border-color:#5cd2ff"></div>'
      '<div class="n6np-s" style="left:583px;top:444px;width:448px;font:700 20px/1 \'Golos Text\'">Таблица NAT</div>'
      '<table class="n6np-tb" style="left:596px;top:472px;width:424px">'
      '<tr><td style="width:36px"></td><td>Локальный IP:порт</td><td style="width:62px"></td><td>Публичный IP:порт</td></tr>'
      '<tr><td><span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#ffc94a"></span></td><td>Локальный IP:порт</td><td>⟷</td><td>Публичный IP:порт</td></tr>'
      '<tr><td><span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#b77bff"></span></td><td>Локальный IP:порт</td><td>⟷</td><td>Публичный IP:порт</td></tr>'
      '<tr><td>…</td><td>…</td><td>⟷</td><td>…</td></tr></table></div>')

S3 = ('<div class="step"><div class="n6np-p" style="left:1013px;top:102px;width:640px;height:488px"></div>'
      + badge(1031, 115, 3, VIO, "Отправка в интернет")
      + '<div class="n6np-t" style="left:1104px;top:173px">Пакет с публичным адресом достигает<br>интернет-ресурса</div>'
      + img("n6_napt_cl.png", "left:1422px;top:130px;width:190px") + img("n6_napt_srv.png", "left:1340px;top:222px;width:305px")
      + '<div class="n6np-s" style="left:1490px;top:396px;width:165px">Интернет-ресурс<br>(сервер)</div>'
      + pkt(1020, 258, 324, "Пакет после NAT", "(в интернет)", SRC_PUB, DST_SRV)
      + '<svg class="n6np-wire"><path class="fl" d="M930 346H1010M1346 346H1410"/><path d="M1004 334l18 12-18 12z" style="fill:#5cd2ff"/>'
        '<path class="fl or" d="M1584 440Q1584 492 1520 492H1100Q1020 492 950 395"/><path d="M936 394l22 0-8 20z" style="fill:#ffb347"/></svg></div>')

S4 = ('<div class="step"><div class="n6np-p" style="left:20px;top:602px;width:965px;height:226px"></div>'
      + badge(34, 613, 4, GRN, "Обратный перевод")
      + '<div class="n6np-t" style="left:40px;top:680px;line-height:1.24"><span class="n6np-ii">!</span>Ответ приходит на публичный адрес<br>'
        '<span style="padding-left:34px">маршрутизатора</span></div>'
      '<div class="n6np-t" style="left:40px;top:730px;line-height:1.24"><span class="n6np-ii">A</span>Маршрутизатор находит запись<br>'
      '<span style="padding-left:34px">в таблице NAT</span></div>'
      '<div class="n6np-t" style="left:40px;top:780px"><span class="n6np-ii">A</span>Адрес назначения меняется на локальный</div>'
      + pkt(378, 652, 334, "Ответный пакет", "(от интернет-ресурса)", SRC_SRV, DST_PUB)
      + img("n6_napt_rt2.png", "left:733px;top:648px;width:179px")
      + '<svg class="n6np-wire"><path class="fl or" d="M824 645V606"/><path d="M812 612l12-18 12 18z" style="fill:#ffb347"/>'
        '<path class="fl or" d="M745 750H722"/><path d="M728 738l-18 12 18 12z" style="fill:#ffb347"/></svg></div>')

S5 = ('<div class="step"><div class="n6np-p" style="left:995px;top:602px;width:658px;height:226px"></div>'
      + badge(995, 614, 5, "#7fd0ff", "Доставка в локальную сеть")
      + '<div class="n6np-t" style="left:1078px;top:668px">Ответ получает устройство,<br>отправившее запрос</div>'
      '<div class="n6np-s" style="left:1490px;top:620px;width:160px;font-size:15px">Локальная сеть<br>(частные IP-адреса)</div>'
      '<div class="n6np-p" style="left:1466px;top:684px;width:172px;height:130px;border-radius:12px"></div>'
      + img("n6_napt_ld.png", "left:1402px;top:705px;width:230px")
      + '<div class="n6np-s" style="left:1400px;top:787px;width:110px">Устройство 1</div>'
        '<div class="n6np-s" style="left:1525px;top:787px;width:110px">Устройство 2</div>'
      + pkt(1018, 712, 338, "Пакет после обратного перевода", "", SRC_SRV, DST_LOC)
      + '<svg class="n6np-wire"><path class="fl" d="M910 752Q950 775 990 775M1358 766H1392"/>'
        '<path d="M984 763l18 12-18 12zM1388 754l18 12-18 12z" style="fill:#5cd2ff"/></svg></div>')

FOOT = ('<div class="step"><div class="n6np-p" style="left:20px;top:838px;width:1633px;height:92px"></div>'
        + img("n6_napt_devs.png", "left:28px;top:838px;width:264px") + img("n6_napt_rt3.png", "left:362px;top:838px;width:120px")
        + img("n6_napt_cl2.png", "left:1358px;top:843px;width:137px") + img("n6_napt_srv2.png", "left:1522px;top:838px;width:106px")
        + '<svg class="n6np-wire"><path class="fl th" d="M480 888H512M1350 883H1288M1488 888H1524"/></svg>'
        '<div style="position:absolute;left:538px;top:848px;font:700 21px/1 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
        'Много устройств используют ограниченный пул публичных IP-адресов</div>'
        '<div style="position:absolute;left:538px;top:878px;font:400 15.5px/1.3 \'Golos Text\',sans-serif;color:#b9d2f5;white-space:nowrap">'
        'NAT/NAPT позволяет многим устройствам из локальной сети одновременно выходить в интернет,<br>'
        'используя один или несколько публичных IP-адресов.</div></div>')

HTML = CSS + bg("bgk_net") + INTRO + S1 + S2 + S3 + S4 + S5 + FOOT
