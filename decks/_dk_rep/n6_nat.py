# -*- coding: utf-8 -*-
"""2.6: Преобразование сетевых адресов — NAT (вёрстка на чистом фоне). build(terms) — общий с n6_terms."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 118

CSS = """<style>
.n6nt-p{position:absolute;box-sizing:border-box;border-radius:16px;border:1.5px solid rgba(92,190,255,.7);
  background:linear-gradient(160deg,rgba(16,40,90,.72),rgba(6,14,36,.88));box-shadow:0 0 22px rgba(58,160,255,.32)}
.n6nt-t{position:absolute;white-space:nowrap;font:800 25px/1.15 Montserrat,sans-serif;color:#fff}
.n6nt-s{position:absolute;white-space:nowrap;font:400 19px/1.3 "Golos Text",sans-serif;color:#b9d2f5}
.n6nt-l{position:absolute;white-space:nowrap;font:600 20px/1.2 "Golos Text",sans-serif;color:#fff;text-align:center}
.n6nt-ip{position:absolute;box-sizing:border-box;border-radius:8px;height:34px;font:600 21px/34px "JetBrains Mono",monospace;color:#10101a;text-align:center}
.n6nt-tag{position:absolute;box-sizing:border-box;border-radius:10px;font:600 19px/1.3 "Golos Text",sans-serif;color:#10101a;padding:10px 22px}
.n6nt-row{position:absolute;box-sizing:border-box;height:50px;border-radius:10px;border:1.5px solid rgba(92,190,255,.5);background:rgba(8,20,50,.8);
  font:600 26px/48px "JetBrains Mono",monospace;color:#fff;overflow:hidden}
.n6nt-row i{float:left;font:800 26px/48px Montserrat,sans-serif;font-style:normal;color:#10101a;width:142px;text-align:center;margin-right:80px}
.n6nt-dot{position:absolute;width:14px;height:14px;margin:-7px;border-radius:50%}
.n6nt-go{background:#ffd23a;box-shadow:0 0 14px #ffc94a;offset-path:path("M920 365H1240");animation:n6ntm 2.2s linear infinite}
.n6nt-bk{background:#6ee07a;box-shadow:0 0 14px #6ee07a;offset-path:path("M1290 440H975");animation:n6ntm 2.2s linear infinite 1.1s}
.n6nt-ln{background:#5cd2ff;box-shadow:0 0 12px #5cd2ff;offset-path:path("M164 372V338H686V408H722");animation:n6ntm 3s linear infinite}
@keyframes n6ntm{from{offset-distance:0%}to{offset-distance:100%}}
</style>"""

CLOUD = """<svg style="position:absolute;left:1255px;top:222px;width:395px;height:210px" viewBox="0 0 395 210">
<defs><linearGradient id="n6ntc%(k)s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fa6ff"/><stop offset="1" stop-color="#17418f"/></linearGradient>
<filter id="n6ntcg%(k)s"><feGaussianBlur stdDeviation="6"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<path filter="url(#n6ntcg%(k)s)" d="M60 200Q8 200 10 150Q12 104 62 102Q66 52 120 52Q146 10 200 10Q262 10 282 66Q332 58 352 104Q392 116 388 160Q384 200 336 200Z"
 fill="url(#n6ntc%(k)s)" stroke="#9fd8ff" stroke-width="3"/></svg>"""


def build(terms):
    pub = "Адрес от провайдера" if terms else "203.0.113.5"
    pubst = "font:700 23px/52px Montserrat,sans-serif;white-space:nowrap" if terms else "font:700 28px/52px 'JetBrains Mono',monospace"
    rows = [("A", "#ffc94a", "10.0.0.0/8"), ("B", "#b77bff", "172.16.0.0/12"), ("C", "#7ee86a", "192.168.0.0/16")]
    rhtml = "".join(
        '<div class="n6nt-row" style="left:55px;top:%dpx;width:582px%s">%s%s</div>'
        % (710 + i * 54, ";padding-left:120px" if terms else "",
           "" if terms else '<i style="background:%s">%s</i>' % (c, k), ip)
        for i, (k, c, ip) in enumerate(rows))
    return CSS + bg("bgk_globe") + "".join([
        '<div class="step"><div class="n6nt-s" style="left:56px;top:122px;font:500 29px/1.25 \'Golos Text\',sans-serif;color:#8fb4ff">'
        'Позволяет устройствам в локальной сети выходить в Интернет,<br>используя один или несколько публичных IPv4-адресов.</div></div>',
        # локальная сеть
        '<div class="step"><div class="n6nt-p" style="left:32px;top:212px;width:1280px;height:366px;background:linear-gradient(160deg,rgba(16,40,90,.55),rgba(6,14,36,.7))"></div>'
        '<div class="n6nt-p" style="left:32px;top:212px;width:708px;height:366px;box-shadow:none;border-right:none;border-radius:16px 0 0 16px;background:rgba(10,24,60,.45)"></div>'
        + img("n6_nat_ic1.png", "left:58px;top:233px;width:56px") +
        '<div class="n6nt-t" style="left:132px;top:227px">Локальная сеть — частные IPv4-адреса</div>'
        '<div class="n6nt-s" style="left:132px;top:261px">Устройства используют частные адреса<br>из диапазонов RFC 1918.</div>'
        '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px"><path d="M164 372V338H686V408H722M372 338V372M582 338V384" fill="none" '
        'stroke="#5cd2ff" stroke-width="3" style="filter:drop-shadow(0 0 4px #3aa0ff)"/></svg>'
        + img("n6_nat_lap.png", "left:48px;top:372px;width:182px") + img("n6_nat_pc.png", "left:276px;top:370px;width:190px")
        + img("n6_nat_ph.png", "left:548px;top:378px;width:69px") +
        '<div class="n6nt-l" style="left:104px;top:500px">Ноутбук</div><div class="n6nt-l" style="left:314px;top:500px">Компьютер</div>'
        '<div class="n6nt-l" style="left:536px;top:500px">Смартфон</div>'
        '<div class="n6nt-ip" style="left:66px;top:529px;width:156px;background:#ffc94a">192.168.1.10</div>'
        '<div class="n6nt-ip" style="left:293px;top:529px;width:158px;background:#b77bff">10.0.0.25</div>'
        '<div class="n6nt-ip" style="left:510px;top:529px;width:153px;background:#7ee86a">172.16.5.20</div>'
        '<div class="n6nt-dot n6nt-ln"></div></div>',
        # маршрутизатор
        '<div class="step">' + img("n6_nat_rt.png", "left:718px;top:268px;width:244px") +
        '<div class="n6nt-l" style="left:700px;top:472px;width:270px;font:700 25px/1.25 Montserrat,sans-serif">Маршрутизатор<br>'
        '<span style="color:#5cd2ff;font-size:27px">с NAT</span></div></div>',
        # Интернет
        '<div class="step">' + CLOUD % {'k': 't' if terms else 'n'} +
        '<div class="n6nt-l" style="left:1255px;top:336px;width:410px;font:800 42px/1 Montserrat,sans-serif">Интернет</div>'
        '<div class="n6nt-p" style="left:1320px;top:416px;width:288px;height:104px;overflow:hidden;border-color:#ff8a3d">'
        '<div style="background:#ff8a3d;height:46px;font:600 21px/46px \'Golos Text\',sans-serif;color:#10101a;text-align:center">Публичный IPv4-адрес</div>'
        '<div style="text-align:center;color:#fff;%s">%s</div></div></div>' % (pubst, pub),
        # потоки
        '<div class="step"><svg style="position:absolute;left:0;top:0;width:1672px;height:941px" fill="none" stroke-width="5" stroke-linecap="round">'
        '<path d="M920 365H1225" stroke="#ffc94a" style="filter:drop-shadow(0 0 5px #ffc94a)"/><path d="M1220 348l22 17-22 17z" fill="#ffc94a" stroke="none"/>'
        '<path d="M1290 440H990" stroke="#6ee07a" style="filter:drop-shadow(0 0 5px #6ee07a)"/><path d="M995 423l-22 17 22 17z" fill="#6ee07a" stroke="none"/>'
        '<path d="M962 408H1270" stroke="#5cd2ff" stroke-width="3"/></svg>'
        '<div class="n6nt-tag" style="left:979px;top:265px;width:269px;background:#ffc94a">NAT заменяет частный<br>адрес на публичный</div>'
        '<div class="n6nt-tag" style="left:988px;top:471px;width:255px;background:#7ee86a">Ответ возвращается<br>к отправителю</div>'
        '<div class="n6nt-dot n6nt-go"></div><div class="n6nt-dot n6nt-bk"></div></div>',
        # RFC 1918
        '<div class="step"><div class="n6nt-p" style="left:32px;top:598px;width:630px;height:292px"></div>'
        + img("n6_nat_ic2.png", "left:54px;top:616px;width:76px") +
        '<div class="n6nt-t" style="left:146px;top:614px">Частные диапазоны IPv4 — RFC 1918</div>'
        '<div class="n6nt-s" style="left:146px;top:648px;font-size:18px">Эти адреса используются во внутренних сетях<br>и не маршрутизируются в Интернете.</div>'
        + rhtml + '</div>',
        # зачем
        '<div class="step"><div class="n6nt-p" style="left:679px;top:598px;width:477px;height:292px;border:2px solid #ff8a3d;'
        'background:linear-gradient(160deg,rgba(60,30,20,.75),rgba(14,12,24,.9));box-shadow:0 0 22px rgba(255,138,61,.35)"></div>'
        + img("n6_nat_ic3.png", "left:702px;top:615px;width:78px") +
        '<div class="n6nt-t" style="left:800px;top:628px;color:#ff9a4a">Зачем появился NAT?</div>'
        '<div class="n6nt-s" style="left:800px;top:672px;font-size:20.5px;line-height:28px;color:#e8eefc">Число подключённых устройств<br>росло, а запас публичных<br>'
        'IPv4-адресов ограничен.<br>NAT помог многим устройствам<br>выходить в Интернет через<br>меньшее число публичных<br>адресов.</div></div>',
        # где
        '<div class="step"><div class="n6nt-p" style="left:1173px;top:598px;width:467px;height:292px;border:2px solid #b77bff;'
        'background:linear-gradient(160deg,rgba(50,24,90,.75),rgba(14,10,36,.9));box-shadow:0 0 22px rgba(183,123,255,.35)"></div>'
        + img("n6_nat_ic4.png", "left:1196px;top:615px;width:78px") +
        '<div class="n6nt-t" style="left:1292px;top:632px;font-size:21.5px">Где нужно преобразование?</div>'
        '<div class="n6nt-s" style="left:1294px;top:688px;font-size:20.5px;line-height:29px;color:#e8eefc">Трафик за пределы локальной<br>сети проходит через NAT.<br>'
        'Обмен между узлами одной<br>локальной сети обычно<br>не преобразуется.</div></div>',
    ])


HTML = build(False)
