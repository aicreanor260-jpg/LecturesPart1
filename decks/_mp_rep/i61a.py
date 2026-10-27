# -*- coding: utf-8 -*-
"""pptx: расчёт путей, резервирование и QoS — вёрстка поверх bgk_01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 132

CSS = """<style>
.i61-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i61-h{position:absolute;font:900 33px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i61-t{position:absolute;font:500 20px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i61-c{position:absolute;text-align:center;white-space:nowrap}
.i61-c b{display:block;font:800 21px/1.2 "Golos Text";color:#13306e}
.i61-c span{font:500 17px/1.2 "Golos Text";color:#1d2a44}
.i61-ar{position:absolute;height:3px;background:#1d4f6e;color:#1d4f6e}
.i61-ar::after{content:"";position:absolute;right:-3px;top:-7px;border:8px solid transparent;border-left:14px solid currentColor;border-right:0}
.i61-vs{position:absolute;width:0;border-left:2px solid #9aa8b8}
.i61-bx{position:absolute;border-radius:14px}
.i61-go{animation:i61g 2.6s ease-in-out infinite}
@keyframes i61g{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""

HTML = CSS + bg("bgk_01") + "".join([
    '<div class="step">',
    '<div class="i61-p" style="left:66px;top:142px;width:838px;height:218px"></div>',
    '<div class="i61-h" style="left:88px;top:154px">Последовательный расчёт</div>',
    img("i61a_tun.png", "left:100px;top:215px;width:445px"),
    '<div class="i61-vs" style="left:566px;top:194px;height:130px"></div>',
    '<div class="i61-t" style="left:588px;top:196px"><b style="font-weight:800;color:#13306e">LER</b> рассчитывает пути<br>по очереди с учётом уже<br>'
    'занятых ресурсов.</div>',
    '<div class="i61-t" style="left:588px;top:280px">Подход проще, но результат<br>зависит от порядка туннелей.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i61-p" style="left:914px;top:142px;width:692px;height:218px"></div>',
    '<div class="i61-h" style="left:934px;top:154px">Внешняя оптимизация</div>',
    img("i61a_mon.png", "left:950px;top:196px;width:258px"),
    '<div class="i61-vs" style="left:1236px;top:194px;height:130px"></div>',
    '<div class="i61-t" style="left:1256px;top:196px;font-size:19px">Внешняя система может<br>совместно учитывать несколько<br>'
    'потоков, их пульсации, задержки<br>и потери.</div>',
    '<div class="i61-t" style="left:1256px;top:296px;font-size:19px">Затем пути можно корректировать<br>оперативно.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i61-p" style="left:250px;top:372px;width:1170px;height:270px"></div>',
    '<div class="i61-h" style="left:278px;top:384px">Как выбранный путь закрепляется в сети</div>',
    img("i61a_db.png", "left:390px;top:422px;width:82px"),
    '<div class="i61-ar i61-go" style="left:492px;top:466px;width:126px"></div>',
    img("i61a_rt.png", "left:674px;top:426px;width:100px"),
    '<div class="i61-ar i61-go" style="left:812px;top:466px;width:90px"></div>',
    img("i61a_chain.png", "left:938px;top:428px;width:450px"),
    '<div class="i61-c" style="left:280px;top:506px;width:300px"><b>OSPF-TE / IS-IS-TE&nbsp; →&nbsp; TED</b><span>Сведения о ресурсах</span></div>',
    '<div class="i61-c" style="left:580px;top:506px;width:290px"><b>LER: расчёт пути</b><span>Маршрут и требуемая полоса</span></div>',
    '<div class="i61-c" style="left:910px;top:506px;width:504px"><b>RSVP-TE: установка LSP</b><span>Path — маршрут; Resv — резервирование и метки</span></div>',
    '<div class="i61-bx" style="left:276px;top:568px;width:1122px;height:38px;background:#c6ecdc"></div>',
    '<div class="i61-t" style="left:276px;top:575px;width:1122px;text-align:center;font:700 18px/1.2 Golos Text;color:#13306e">'
    'LSR проверяют ресурсы и обновляют состояние резервирования; остаток распространяется через OSPF-TE / IS-IS-TE.</div>',
    '<div style="position:absolute;left:352px;top:624px;width:968px;border-top:1px solid #1d3f8a"></div>',
    '<div class="i61-t" style="left:570px;top:612px;padding:0 14px;background:#fdf8ea;font-size:15px">'
    'CSPF — алгоритм расчёта пути, а не протокол рассылки объявлений.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i61-p" style="left:412px;top:656px;width:926px;height:268px"></div>',
    '<div class="i61-h" style="left:438px;top:666px">MPLS TE создаёт основу для QoS</div>',
    '<div class="i61-t" style="left:438px;top:706px;font-size:19px">Балансировка нагрузки снижает риск перегрузки. '
    'Для заданных задержек и потерь<br>также нужны классификация, очереди, планирование и контроль трафика.</div>',
    img("i61a_q1.png", "left:464px;top:766px;width:90px"),
    '<div class="i61-t" style="left:572px;top:770px;font-size:18px"><b style="font-weight:800;color:#13306e">Разные классы</b> → отдельные<br>'
    '<b style="font-weight:800;color:#13306e">политики</b>; при необходимости —<br>разные туннели.</div>',
    '<div class="i61-vs" style="left:900px;top:770px;height:72px"></div>',
    img("i61a_q2.png", "left:933px;top:766px;width:91px"),
    '<div class="i61-t" style="left:1042px;top:772px;font-size:18px"><b style="font-weight:800;color:#13306e">Требования QoS</b> → расчёт<br>'
    '<b style="font-weight:800;color:#13306e">и проверка</b> для конкретной<br>сети.</div>',
    '<div class="i61-bx" style="left:440px;top:852px;width:872px;height:60px;background:#f9c4b6"></div>',
    img("i61a_excl.png", "left:460px;top:856px;width:62px"),
    '<div class="i61-t" style="left:538px;top:862px;font-size:18px;line-height:1.2;color:#8a1e14"><b style="font-weight:800">'
    'Резервирование полосы само по себе не гарантирует QoS.</b><br>Универсального порога загрузки 20–30% для всех сетей нет.</div>',
    '</div>',
])
