import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _kr import css, defs, cloud_at
W, H, TOP = 1672, 941, 128
P = "m4x-rou"
CSS = css(P) + ("<style>.%s-tx{position:absolute;font:500 19px/26.6px 'Golos Text',sans-serif;color:#f4ecd2;text-shadow:0 1px 4px rgba(0,0,0,.7)}"
                ".%s-s{position:absolute;font:600 32px/1 'Playfair Display',serif;color:#f6ebc8;text-align:center;text-shadow:0 2px 5px #000}"
                ".%s-lg{position:absolute;font:500 21px/1 'Golos Text',sans-serif}"
                ".%s-fl{stroke-dashoffset:0;animation:%sdash 1.2s linear infinite}@keyframes %sdash{to{stroke-dashoffset:-24}}"
                "</style>") % ((P,) * 6)

def rt(cx, cy):
    return img("rout_router.png", "left:%dpx;top:%dpx;width:116px;height:90px" % (cx - 58, cy - 45))

def card(x, y, w, h):
    return '<div class="%s-pn" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:10px"></div>' % (P, x, y, w, h)

def tx(x, text):
    return '<div class="%s-tx" style="left:%dpx;top:608px">%s</div>' % (P, x, text)

wires = ('<svg class="%s-sv" viewBox="0 0 1672 941">%s'
         '<g fill="none" stroke="#f6d36a" stroke-width="4.5" filter="url(#%s-gl)">'
         '<path d="M300 350L482 347" marker-end="url(#%s-ah)"/><path d="M612 330L792 238" marker-end="url(#%s-ah)"/>'
         '<path d="M914 236L1048 308" marker-end="url(#%s-ah)"/><path d="M1172 330L1320 355" marker-end="url(#%s-ah)"/></g>'
         '<g fill="none" stroke="#3fd6e0" stroke-width="4.5" stroke-dasharray="14 9" filter="url(#%s-gl)" class="%s-fl">'
         '<path d="M600 388L664 450" marker-end="url(#%s-ahb)"/><path d="M790 481H950" marker-end="url(#%s-ahb)"/>'
         '<path d="M1062 432L1090 384" marker-end="url(#%s-ahb)"/></g></svg>' % ((P, defs(P)) + (P,) * 10))
legend = ('<svg class="%s-sv" viewBox="0 0 1672 941"><path d="M400 550H512" stroke="#f6d36a" stroke-width="4" marker-end="url(#%s-ah)"/>'
          '<path d="M857 550H976" stroke="#3fd6e0" stroke-width="4" stroke-dasharray="14 9" marker-end="url(#%s-ahb)"/></svg>' % ((P,) * 3))
listic = ('<svg style="position:absolute;left:546px;top:162px" width="63" height="62" viewBox="0 0 63 62"><rect x="2" y="2" width="59" height="58" rx="6" fill="rgba(240,199,94,.12)" stroke="#f0c75e" stroke-width="3"/>'
          '<g fill="#f6d36a"><circle cx="15" cy="18" r="3.5"/><circle cx="15" cy="31" r="3.5"/><circle cx="15" cy="44" r="3.5"/>'
          '<rect x="24" y="15" width="28" height="6" rx="2"/><rect x="24" y="28" width="28" height="6" rx="2"/><rect x="24" y="41" width="28" height="6" rx="2"/></g></svg>')
server = ('<svg style="position:absolute;left:1443px;top:312px" width="84" height="74" viewBox="0 0 84 74"><g stroke="#f0c75e" stroke-width="2.4" fill="#16463a">'
          '<rect x="2" y="2" width="80" height="20" rx="4"/><rect x="2" y="27" width="80" height="20" rx="4"/><rect x="2" y="52" width="80" height="20" rx="4"/></g>'
          '<g fill="#f6d36a"><rect x="9" y="9" width="24" height="6" rx="2"/><rect x="9" y="34" width="24" height="6" rx="2"/><rect x="9" y="59" width="24" height="6" rx="2"/>'
          '<circle cx="62" cy="12" r="2.5"/><circle cx="72" cy="12" r="2.5"/><circle cx="62" cy="37" r="2.5"/><circle cx="72" cy="37" r="2.5"/><circle cx="62" cy="62" r="2.5"/><circle cx="72" cy="62" r="2.5"/></g></svg>')
HTML = CSS + bg() + "".join([
    '<div class="step">' + wires + img("rout_cube.png", "left:40px;top:285px;width:270px;height:120px") +
    '<div class="%s-s" style="left:140px;width:200px;top:408px">IP-пакет</div>' % P +
    rt(548, 350) + rt(853, 229) + rt(1112, 332) + rt(727, 473) + rt(1015, 470) + '</div>',
    '<div class="step"><div class="%s-pn" style="left:386px;top:150px;width:248px;height:134px;border-radius:20px"></div>'
    '<svg class="%s-sv" viewBox="0 0 1672 941"><path d="M505 282L513 318L528 284z" fill="#0d3c30" stroke="#f0c75e" stroke-width="1.6"/></svg>'
    '<div class="%s-lb" style="left:402px;top:167px;width:101px;height:51px;font-size:15.5px;line-height:19px">Destination<br>Address</div>'
    '<div class="%s-t" style="left:514px;top:176px;font-size:32px;line-height:34px">+</div>%s'
    '<div class="%s-t" style="left:456px;top:230px;width:170px;text-align:center;font-size:19px;line-height:21px">Таблица<br>маршрутизации</div></div>' % ((P,) * 4 + (listic,) + (P,)),
    '<div class="step">' + cloud_at(P, 1471, 358, 300) + server +
    '<div class="%s-s" style="left:1381px;width:200px;top:392px;font-size:24px;line-height:24px">Сеть<br>назначения</div></div>' % P,
    '<div class="step">' + legend +
    '<div class="%s-lg" style="left:535px;top:540px;color:#f3d98a">Оптимальный маршрут</div>'
    '<div class="%s-lg" style="left:1000px;top:540px;color:#6fe8d0">Альтернативный маршрут</div></div>' % (P, P),
    '<div class="step">' + card(33, 587, 384, 196) + img("rout_ic_book.png", "left:50px;top:610px;width:90px;height:85px") +
    tx(153, "Маршрутизация —<br>процесс определения<br>лучшего маршрута<br>для пересылки IP-пакетов<br>между разными сетями.").replace("608px", "613px") + '</div>',
    '<div class="step">' + card(434, 587, 394, 196) + img("rout_ic_gear.png", "left:448px;top:605px;width:90px;height:90px") +
    tx(554, "Маршрутизатор получает<br>пакет, анализирует<br>Destination Address и<br>по таблице маршрутизации<br>выбирает выходной<br>интерфейс.") + '</div>',
    '<div class="step">' + card(845, 587, 393, 196) + img("rout_ic_tree.png", "left:860px;top:605px;width:90px;height:90px") +
    tx(963, "Статические маршруты<br>задаёт администратор сети.<br>Динамические маршруты<br>вычисляются по данным<br>протоколов о состоянии<br>и топологии сети.") + '</div>',
    '<div class="step">' + card(1257, 587, 385, 196) + img("rout_ic_chart.png", "left:1272px;top:605px;width:90px;height:90px") +
    tx(1378, "Каждый маршрутизатор<br>самостоятельно выбирает<br>оптимальный путь,<br>обеспечивая эффективную<br>доставку пакета до сети<br>назначения.") + '</div>',
    '<div class="step"><div class="%s-pn" style="left:228px;top:803px;width:1214px;height:90px;border-radius:14px"></div>' % P +
    img("rout_bulb.png", "left:296px;top:805px;width:54px;height:75px") +
    '<div class="%s-s" style="left:318px;width:1100px;white-space:nowrap;top:828px;font-size:32px;line-height:40px;color:#f3d98a">Destination Address + таблица маршрутизации &nbsp;⟶&nbsp; лучший путь</div></div>' % P,
])
