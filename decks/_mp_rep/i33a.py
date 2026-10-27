# -*- coding: utf-8 -*-
"""pptx: IntServ/RSVP — PATH и RESV, Sender TSpec / FlowSpec / FilterSpec. Фон bgk_30 (Хаул и Софи справа внизу)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 94

CSS = """<style>
.i33-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i33-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:100px}
.i33-t{position:absolute;white-space:nowrap;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i33-t b{display:block;font:800 26px/1.3 "Golos Text",sans-serif;color:#13306e}
.i33-num{position:absolute;width:48px;height:48px;border-radius:50%;background:#f2694a;color:#fff;font:900 28px/48px "Rubik",sans-serif;text-align:center}
.i33-cloud{position:absolute;background:#c6ece4;border-radius:50%}
.i33-y{position:absolute;background:#fbd35b;border:3px solid #1f63c6;border-radius:14px;font:800 22px/56px "Golos Text",sans-serif;color:#13306e}
</style>"""

R, G = "#f2694a", "#1f8a5e"


def arr(x1, y1, x2, y2, c):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4" marker-end="url(#i33%s)"/>' % (
        x1, y1, x2, y2, c, "r" if c == R else "g")


def pair(x1, y1, x2, y2, dy=14):
    return arr(x1, y1 - dy // 2, x2, y2 - dy // 2, R) + arr(x2, y2 + dy // 2, x1, y1 + dy // 2, G)


NET = ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941"><defs>'
       '<marker id="i33r" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="%s"/></marker>'
       '<marker id="i33g" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="%s"/></marker></defs>'
       % (R, G) + pair(218, 356, 306, 356) + pair(404, 356, 500, 356) + pair(596, 336, 742, 284, 26) + pair(596, 380, 742, 424, 26)
       + pair(836, 284, 928, 284) + pair(836, 424, 928, 424)
       + arr(160, 496, 246, 496, R) + arr(246, 532, 160, 532, G)
       + '<rect x="138" y="470" width="452" height="86" rx="10" fill="none" stroke="#3a8f84" stroke-width="2" stroke-dasharray="7 5"/></svg>')

STEPS = [(260, "1", "PATH — описание трафика", "Источник C1 сообщает Sender TSpec.<br>PATH следует к C2 и C3 по маршрутам сети."),
         (368, "2", "Состояние пути", "Маршрутизаторы запоминают предыдущий<br>RSVP-узел (PHOP), чтобы направить RESV обратно."),
         (478, "3", "RESV — запрос ресурсов", "Получатели C2 и C3 отправляют запрос QoS.<br>При достаточных ресурсах и разрешении политики<br>"
          "узлы устанавливают резервирование.")]


def card(x, w, ico, head, txt):
    return '<div class="i33-p" style="left:%dpx;top:588px;width:%dpx;height:184px"></div>' % (x, w) + \
        img(ico, "left:%dpx;top:600px;width:94px" % (x + 14)) + \
        '<div class="i33-t" style="left:%dpx;top:604px;width:%dpx;font-size:15.5px"><b style="font-size:29px;margin-bottom:6px">%s</b>%s</div>' % (
            x + 116, w - 126, head, txt)


HTML = CSS + bg("bgk_30") + "".join([
    '<div class="step">',
    '<div class="i33-p" style="left:118px;top:102px;width:1434px;height:96px"></div>',
    '<div class="i33-t" style="left:118px;top:112px;width:1434px;text-align:center;font-size:25px;line-height:1.3">'
    '<span style="font:800 29px Golos Text,sans-serif;color:#13306e">IntServ резервирует ресурсы для отдельных потоков с помощью RSVP.</span><br>'
    'RSVP передаёт сигнальные сообщения, а IP-пакеты следуют маршрутам, определяемым маршрутизацией.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i33-p" style="left:112px;top:212px;width:1448px;height:360px"></div>',
    '<div class="i33-cloud" style="left:232px;top:250px;width:560px;height:300px;border-radius:46% 54% 50% 50%"></div>',
    '<div class="i33-cloud" style="left:420px;top:224px;width:380px;height:140px"></div>',
    '<div class="i33-cloud" style="left:620px;top:300px;width:300px;height:260px"></div>',
    '<div class="i33-t" style="left:492px;top:238px;font-weight:700;color:#13306e">Сеть с поддержкой RSVP</div>',
    NET,
    img("i33a_lt.png", "left:142px;top:330px;width:76px"), '<div class="i33-n" style="left:126px;top:400px">C1</div>',
    img("i33a_rt.png", "left:310px;top:326px;width:92px"), '<div class="i33-n" style="left:304px;top:400px">R1</div>',
    img("i33a_rt.png", "left:504px;top:326px;width:92px"), '<div class="i33-n" style="left:498px;top:400px">R2</div>',
    img("i33a_rt.png", "left:744px;top:262px;width:92px"), '<div class="i33-n" style="left:738px;top:334px">R3</div>',
    img("i33a_rt.png", "left:744px;top:394px;width:92px"), '<div class="i33-n" style="left:738px;top:468px">R4</div>',
    img("i33a_lt.png", "left:934px;top:256px;width:72px"), '<div class="i33-n" style="left:916px;top:324px">C2</div>',
    img("i33a_lt.png", "left:934px;top:396px;width:72px"), '<div class="i33-n" style="left:916px;top:464px">C3</div>',
    '<div class="i33-t" style="left:266px;top:484px;font-size:18px"><span style="font-weight:800;color:#13306e">PATH:</span> от источника к получателям</div>',
    '<div class="i33-t" style="left:266px;top:520px;font-size:18px"><span style="font-weight:800;color:#13306e">RESV:</span> от получателей к источнику</div>',
    '<div style="position:absolute;left:1044px;top:232px;width:2px;height:322px;background:#1f63c6;opacity:.5"></div>',
    '</div>',
    '<div class="step">',
    "".join('<div class="i33-num" style="left:1072px;top:%dpx">%s</div>' % (y - 24, n) +
            '<div class="i33-t" style="left:1140px;top:%dpx;width:420px;font-size:16px"><b>%s</b>%s</div>' % (y - 28, h, t)
            for y, n, h, t in STEPS),
    '</div>',
    '<div class="step">',
    card(242, 422, "i33a_ic1.png", "Sender TSpec", "<span style='font-weight:700'>Описание потока:</span> скорость r,<br>глубина ведра b, пиковая "
         "скорость p,<br>минимальная учитываемая единица m<br>и максимальный размер пакета M."),
    card(676, 388, "i33a_ic2.png", "FlowSpec", "Включает TSpec и спецификацию<br>требуемого обслуживания RSpec,<br>если она предусмотрена<br>"
         "выбранным сервисом."),
    card(1076, 372, "i33a_ic3.png", "FilterSpec", "<span style='font-size:14.5px'>Определяет пакеты, к которым<br>относится резервирование:<br>"
         "например, по адресу отправителя<br>и порту. FlowSpec и FilterSpec<br>образуют дескриптор потока.</span>"),
    '</div>',
    '<div class="step">',
    '<div class="i33-y" style="left:276px;top:786px;width:1114px;height:70px"></div>',
    img("i33a_ex.png", "left:294px;top:796px;width:54px"),
    '<div class="i33-t" style="left:366px;top:808px;font-weight:800;font-size:18.5px;color:#13306e">'
    'PATH сам по себе не резервирует ресурсы. Резервирование инициирует получатель сообщением RESV.</div>',
    '<div class="i33-t" style="top:872px;left:440px;width:auto;padding:2px 18px;border-radius:10px;background:rgba(19,48,110,.6);color:#fff;font-size:17px">'
    'Фильтр выбирает потоки; он не задаёт произвольную долю пакетов одного потока.</div>',
    '</div>',
])
