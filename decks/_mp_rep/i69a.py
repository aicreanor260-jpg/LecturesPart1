# -*- coding: utf-8 -*-
"""pptx: Реализация пересылки SR — список сегментов и обработка активного SID, фон bgk_07."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i69-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i69-h{position:absolute;font:800 26px/1 "Golos Text",sans-serif;color:#13306e}
.i69-t{position:absolute;font:500 22px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i69-s{position:absolute;font:500 17px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i69-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:100px}
.i69-c{position:absolute;top:472px;height:190px;border-radius:14px}
.i69-ch{position:absolute;font:800 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i69-sl{position:absolute;left:434px;top:226px;display:flex;height:66px;border:3px solid #1d3f8a;border-left-width:16px;border-radius:6px;overflow:hidden;
 font:700 24px/60px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i69-sl div{width:136px;border-right:2px solid #1d3f8a}.i69-sl div:last-child{width:276px;border:0;background:#fdf8ea}
.i69-ls{position:absolute;display:flex;border:2px solid #1d3f8a;font:500 19px/30px "Golos Text",sans-serif;color:#13306e;background:#fff}
.i69-ls span{padding:0 4px}.i69-ls .a{background:#f68a5c}
.i69-fly{animation:i69f 2.6s ease-in-out infinite}
@keyframes i69f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""


def rt(x, y, name, sub=""):
    s = '<div class="i69-s" style="left:%dpx;top:%dpx;width:200px;text-align:center;font-weight:600;color:#13306e">%s</div>' % (
        x - 50, y + 90, sub) if sub else ""
    return img("i69a_rt.png", "left:%dpx;top:%dpx;width:96px" % (x, y)) + \
        '<div class="i69-n" style="left:%dpx;top:%dpx">%s</div>' % (x - 2, y + 70, name) + s


def ls(x, y, items):
    body = ", ".join('<span class="%s">%s</span>' % ("a" if i == 0 else "", t) for i, t in enumerate(items))
    return ('<div class="i69-fly" style="position:absolute;left:0;top:0"><div class="i69-ls" style="left:%dpx;top:%dpx">[%s]</div></div>' % (
        x, y, body)).replace(
        '[<span class="a">', '<span class="a">[').replace('</span>]', ']</span>')


M = ('<marker id="i69m" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:#1d3f8a"/></marker>')


def ar(x1, y1, x2, y2, w=3, dash=""):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:#1d3f8a;stroke-width:%d;%s" marker-end="url(#i69m)"/>' % (
        x1, y1, x2, y2, w, dash)


HTML = CSS + bg("bgk_07") + "".join([
    '<div class="step">',
    '<div class="i69-p" style="left:276px;top:166px;width:1340px;height:172px;border-radius:22px"></div>',
    '<div class="i69-h" style="left:306px;top:180px;font-size:27px">Входной узел кодирует упорядоченный список SID в пакете.</div>',
    '<div class="i69-sl" style="border-left-color:#cfe4f5"><div style="background:#f68a5c">SID 1</div><div style="background:#a6dcb2">SID 2</div>'
    '<div style="background:#9cc8f2">SID 3</div><div>Данные</div></div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>'
    '<path d="M550 324 H526 Q516 324 516 300" style="fill:none;stroke:#1d3f8a;stroke-width:3" marker-end="url(#i69m)"/></svg>',
    '<div class="i69-h" style="left:562px;top:312px;font-size:21px">Активный сегмент</div>',
    '<div style="position:absolute;left:1194px;top:236px;width:2px;height:88px;background:#1d3f8a"></div>',
    '<div class="i69-t" style="left:1232px;top:254px;font-size:20px">SR-MPLS: стек меток;<br>SRv6: IPv6 SID</div>',
    '</div>',
    '<div class="step">',
    '<div class="i69-p" style="left:56px;top:358px;width:1564px;height:574px;border-radius:22px"></div>',
    '<div class="i69-h" style="left:78px;top:372px;font:900 34px/1 Rubik,sans-serif">Как обрабатывается активный сегмент</div>',
    '<div style="position:absolute;left:540px;top:416px;width:590px;height:38px;border:2px solid #1d3f8a;border-radius:18px;background:#e3f3f1;'
    'font:700 22px/38px Golos Text,sans-serif;color:#13306e;text-align:center">Определить действие активного SID</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>'
    '<path d="M530 436 H362 V464" style="fill:none;stroke:#1d3f8a;stroke-width:2" marker-end="url(#i69m)"/>'
    '<path d="M1140 436 H1312 V464" style="fill:none;stroke:#1d3f8a;stroke-width:2" marker-end="url(#i69m)"/></svg>',
    '<div class="i69-c" style="left:78px;width:528px;background:#cdeee2"></div>',
    '<div class="i69-c" style="left:620px;width:434px;background:#fbd4c3"></div>',
    '<div class="i69-c" style="left:1068px;width:526px;background:#cde6f8"></div>',
    img("i69a_rt.png", "left:210px;top:482px;width:86px"), img("i69a_rtf.png", "left:430px;top:483px;width:84px"),
    img("i69a_rtp.png", "left:793px;top:463px;width:89px"),
    img("i69a_rt.png", "left:1188px;top:486px;width:80px"), img("i69a_rt.png", "left:1386px;top:486px;width:80px"),
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>' +
    ar(302, 510, 424, 510, 2, "stroke-dasharray:6 4") + ar(1272, 512, 1380, 512, 2) + '</svg>',
    '<div class="i69-ch" style="left:78px;top:548px;width:528px">Node-SID: цель ещё не достигнута</div>',
    '<div class="i69-t" style="left:146px;top:578px">Продвижение по кратчайшему<br>пути IGP к узлу. При равной<br>стоимости путей возможен ECMP.</div>',
    '<div class="i69-ch" style="left:620px;top:552px;width:434px">Node-SID: цель достигнута</div>',
    '<div class="i69-t" style="left:688px;top:586px">Сегмент завершён —<br>обработать следующий SID.</div>',
    '<div class="i69-ch" style="left:1068px;top:550px;width:526px">Adjacency-SID</div>',
    '<div class="i69-t" style="left:1160px;top:588px">На узле-владельце выполнить<br>переход по указанной смежности.</div>',
    '</div>',
    '<div class="step">',
    '<div style="position:absolute;left:80px;top:687px;width:1512px;height:2px;background:#1d3f8a"></div>',
    '<div class="i69-h" style="left:600px;top:676px;padding:0 16px;background:#fdf8ea;font-size:22px">Условный пример списка инструкций</div>',
    ls(146, 718, ["16003", "16035", "16005"]), ls(752, 712, ["16035", "16005"]), ls(1240, 712, ["16005"]),
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>' +
    ar(370, 766, 406, 766, 3) + ar(532, 774, 770, 774, 3) + ar(902, 774, 1234, 774, 3) + '</svg>',
    rt(416, 732, "R1"), rt(786, 740, "R3", "16003: достичь R3"), rt(1248, 740, "R5", "16005: достичь R5"),
    '<div class="i69-h" style="left:950px;top:786px;font-size:19px">16035: перейти R3 → R5</div>',
    '</div>',
    '<div class="step">',
    '<div style="position:absolute;left:134px;top:852px;width:1264px;height:72px;border:2px solid #1f63c6;border-radius:12px;background:#fdf8ea"></div>',
    img("i69a_gear.png", "left:152px;top:856px;width:66px"),
    '<div class="i69-s" style="left:238px;top:866px">ECMP применяется там, где это допускает сегмент.<br>Строгая смежность задаёт конкретный переход.</div>',
    '<div style="position:absolute;left:776px;top:860px;width:2px;height:58px;background:#1d3f8a"></div>',
    img("i69a_doc.png", "left:834px;top:856px;width:66px"),
    '<div class="i69-s" style="left:934px;top:866px">В SR-MPLS метка Node-SID может сниматься<br>на предыдущем узле при PHP.</div>',
    '</div>',
])
