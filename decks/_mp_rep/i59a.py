# -*- coding: utf-8 -*-
"""pptx: OSPF-TE и IS-IS-TE — информация для выбора пути — вёрстка поверх bgk_09."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 168

CSS = """<style>
.i59-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i59-h{position:absolute;font:900 27px/1.1 "Rubik",sans-serif;color:#13306e;text-align:center;white-space:nowrap}
.i59-t{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i59-bx{position:absolute;border-radius:14px}
.i59-ar{position:absolute;height:8px;background:#5cc0a6;color:#5cc0a6}
.i59-ar::after{content:"";position:absolute;right:-6px;top:-10px;border:14px solid transparent;border-left:20px solid currentColor;border-right:0}
.i59-tn{position:absolute;height:52px;border-radius:10px;font:600 17px/52px "Golos Text",sans-serif;color:#13306e;padding:0 14px 0 52px;white-space:nowrap}
.i59-tn::before{content:"";position:absolute;left:14px;top:13px;width:22px;height:26px;border:2px solid #1d3f6e;border-radius:50%/40%;background:rgba(255,255,255,.4)}
.i59-ta{position:absolute;font:900 30px/1 "Golos Text";color:#2a9a86}
.i59-f{position:absolute;font:400 38px/1 "Times New Roman",serif;color:#1d2a44;white-space:nowrap}
.i59-f small{font-size:20px}
.i59-pulse{animation:i59p 2.4s ease-in-out infinite}
@keyframes i59p{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""

HTML = CSS + bg("bgk_09") + "".join([
    '<div class="i59-p" style="left:236px;top:178px;width:1198px;height:294px"></div>',
    '<div class="step">',
    '<div class="i59-h" style="left:300px;top:196px;width:300px">Распространение<br>TE-данных</div>',
    img("i59a_rt.png", "left:366px;top:266px;width:148px"),
    '<div class="i59-t" style="left:350px;top:366px;font-size:20px">OSPF-TE / IS-IS-TE</div>',
    '</div>',
    '<div class="step">',
    '<div class="i59-ar i59-pulse" style="left:562px;top:302px;width:62px"></div>',
    '<div class="i59-h" style="left:686px;top:196px;width:300px">TED — база<br>Traffic Engineering</div>',
    img("i59a_db.png", "left:676px;top:260px;width:104px"),
    '<div class="i59-t" style="left:808px;top:278px;font-size:17px;line-height:35px">Топология и метрики<br>Пропускная способность связей<br>Незарезервированная полоса</div>',
    '</div>',
    '<div class="step">',
    '<div class="i59-ar i59-pulse" style="left:1080px;top:302px;width:28px"></div>',
    '<div class="i59-h" style="left:1104px;top:206px;width:300px">Входной LER</div>',
    img("i59a_rt.png", "left:1180px;top:266px;width:148px"),
    '<div class="i59-t" style="left:1110px;top:362px;width:296px;text-align:center">Рассчитывает путь с учётом<br>требований потока</div>',
    '<div class="i59-bx" style="left:386px;top:418px;width:904px;height:42px;background:#bfe8d8"></div>',
    '<div class="i59-t" style="left:386px;top:427px;width:904px;text-align:center;font-weight:800;color:#13306e">'
    'Параметры каналов + требования туннеля → допустимый TE-путь</div>',
    '</div>',
    # критерий
    '<div class="step">',
    '<div class="i59-p" style="left:240px;top:486px;width:590px;height:308px"></div>',
    '<div class="i59-h" style="left:268px;top:500px;font-size:26px">Пример критерия оптимизации</div>',
    '<div class="i59-bx" style="left:292px;top:544px;width:508px;height:76px;background:#d3eee6"></div>',
    '<div class="i59-f" style="left:368px;top:562px">min <small>по <i>P</i></small> <span style="font-size:58px;vertical-align:-8px">[</span> '
    'max <small>по <i>i</i> ∈ <i>P</i></small> <i>K<sub style="font-size:22px">i</sub></i> '
    '<span style="font-size:58px;vertical-align:-8px">]</span></div>',
    '<div class="i59-t" style="left:298px;top:628px;font-size:20px">Из допустимых путей выбирают тот, у которого<br>'
    'максимальный коэффициент использования канала<br>минимален.</div>',
    '<div class="i59-t" style="left:306px;top:718px;font-size:15px"><i style="font-family:Times New Roman;font-size:18px">P</i> — путь; '
    '<i style="font-family:Times New Roman;font-size:18px">K<sub>i</sub></i> — коэффициент использования <i>i</i>-го канала.</div>',
    '<div class="i59-t" style="left:302px;top:752px;font-size:14px;color:#5b6577">Это один из возможных критериев, а не обязательный алгоритм MPLS TE.</div>',
    '</div>',
    # туннели
    '<div class="step">',
    '<div class="i59-p" style="left:844px;top:486px;width:590px;height:308px"></div>',
    '<div class="i59-h" style="left:876px;top:502px;font-size:26px">Несколько туннелей: порядок важен</div>',
    '<div class="i59-tn" style="left:872px;top:558px;background:#c6ecdc">Туннель 1</div>',
    '<div class="i59-ta" style="left:1026px;top:570px">➜</div>',
    '<div class="i59-tn" style="left:1072px;top:558px;background:#f8b8a6">Туннель 2</div>',
    '<div class="i59-ta" style="left:1226px;top:570px">➜</div>',
    '<div class="i59-tn" style="left:1272px;top:558px;background:#c6ecdc">Туннель 3</div>',
    '<div class="i59-t" style="left:876px;top:628px;font-size:20px">При последовательном расчёте каждый туннель меняет<br>'
    'доступные ресурсы для следующего.<br>Поэтому порядок влияет на результат.</div>',
    '<div class="i59-bx" style="left:872px;top:712px;width:532px;height:68px;background:#c6ecdc"></div>',
    '<div class="i59-t" style="left:908px;top:722px;font-size:19px">Совместная оптимизация потоков может обеспечить<br>более равномерную загрузку сети.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i59-p" style="left:452px;top:804px;width:766px;height:110px;background:#fbd8cc;border-color:#f2b8a4"></div>',
    img("i59a_gear.png", "left:478px;top:813px;width:89px"),
    '<div class="i59-t" style="left:590px;top:818px;font-size:20px;color:#13306e"><b style="font-weight:800">OSPF-TE / IS-IS-TE</b> распространяют сведения.<br>'
    'Расчёт пути выбирает маршрут.<br><b style="font-weight:800">RSVP-TE</b> сигнализирует LSP и резервирует ресурсы.</div>',
    '</div>',
])
