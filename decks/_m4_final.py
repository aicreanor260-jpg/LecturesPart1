# -*- coding: utf-8 -*-
"""Финал деки 2.4: шпаргалка → итоговые задачи → тренажёры → тренажёр CLI ESR → тест → что запомнить → финал.
Все команды и факты — только из pptx 2.4."""
from _sw_lib import slide, head, sc, grow, col, card, p, li, step, tags, tag, task, quiz
from _m4_kit import conf, tbl
import _m4_cli


def _qslide(title, qs):
    slide(title, sc(head(title.replace("Тест", "<em>Тест</em>")), grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат: <span class="score">0 / 0</span></span></div>'))


def build():
    # ---------------------------------------------------------------- шпаргалка
    slide("Шпаргалка команд", sc(head("Шпаргалка <em>команд</em>", "Команды ESR из лекции — в том же синтаксисе."), grow("g2",
        col(step(conf(["R1#configure", "R1(config)# interface gigabitethernet 1/0/1", "R1(config-if-gi)# ip address 192.168.10.1/24",
                       "R1(config-if-gi)#exit"], "Адрес на интерфейсе → маршрут C")),
            step(conf(["R1(config)# ip route 192.168.20.0/24 203.0.113.2", "R1(config)# ip route 192.168.20.0/24 interface gigabitethernet 1/0/1",
                       "R1(config)# ip route 203.0.113.0/24 198.51.100.2 10"], "Статический и плавающий маршрут"))),
        col(step(conf(["esr# show ip route", "esr# show ip route all", "esr# show ip route static", "R1# show ip route connected",
                       "R1# show ip interfaces"], "Проверка: FIB, RIB, источники")),
            step(conf(["R1(config)# interface gi1/0/1.10", "R1(config-subif)# ip add 10.10.1.1/24", "R1(config-subif)# ip firewall disable",
                       "R1(config)# do commit", "R1(config)# do confirm"], "Router-on-a-Stick")),
            step(conf(["L3SW (config-if)#interface vlan 10", "L3SW (config-if)#ip add 10.10.1.1 /24",
                       "L3SW (config-if)#interface range Gi1/0/1-2", "L3SW (config-if)#switchport mode trunk"], "Коммутатор L3: SVI"))))))
    slide("Шпаргалка: выбор маршрута", sc(head("Шпаргалка: <em>выбор маршрута</em>"), grow("g2",
        col(step(card("Как маршрут попадает в таблицу", '<ol class="li"><li>Один маршрут — он и попадает.</li>'
                      '<li>Одинаковый префикс — наименьший preference.</li><li>Равный preference — наименьший cost.</li>'
                      '<li>Равные preference и cost — оба маршрута (балансировка).</li></ol>', "cy")),
            step(card("Пересылка", p("Из FIB выбирается маршрут с самым длинным совпадением префикса. Нет совпадения и нет "
                                     "0.0.0.0/0 — пакет отбрасывается."), "mg"))),
        col(step(tbl(["Источник маршрута", "preference"], [["Directly connected", "0"], ["Static", "1"], ["DHCP", "40"],
                                                          ["Remote client (PPTP, L2TP, PPPoE)", "50"], ["RIP", "100"], ["OSPF", "150"],
                                                          ["IS-IS", "160"], ["BGP", "170"]])),
            step(tbl(["Код", "Источник"], [["C", "Прямое подключение"], ["S", "Статический маршрут"], ["R", "RIP"], ["O", "OSPF"],
                                          ["i", "IS-IS"], ["B", "BGP"]]))))))
    # ---------------------------------------------------------------- итоговые задачи
    slide("Итоговые задачи", sc(head("Итоговые <em>задачи</em>", "Введите ответ и нажмите «Проверить»."), grow("g2",
        col(task("m4t1", "В таблице RTA есть 192.168.0.0/16 → 10.1.1.2, 192.168.2.0/24 → 20.1.1.2 и 192.168.3.0/24 → 30.1.1.2. "
                         "На какой следующий узел уйдёт пакет для 192.168.2.2?", "20.1.1.2",
                 "Самое длинное совпадение — 192.168.2.0/24, следующий узел 20.1.1.2.", "IP-адрес"),
            task("m4t2", "R1 узнал 10.0.0.0/30 статически (preference 1) и по OSPF (preference 150). Какой preference у маршрута, "
                         "попавшего в таблицу?", "1", "Между источниками выбирается наименьший preference — статический маршрут.", "число"),
            task("m4t3", "OSPF: путь R1→R2→R3 — стоимость 10 + 10, напрямую R1→R3 — 50. Какова метрика лучшего маршрута?", "20",
                 "10 + 10 = 20 &lt; 50 — лучший маршрут через R2.", "число")),
        col(task("m4t4", "Какой маршрут используется, если в таблице нет совпадения с адресом назначения? Запишите сеть с префиксом.",
                 "0.0.0.0/0", "Маршрут по умолчанию (шлюз последней надежды) — 0.0.0.0/0.", "сеть/префикс"),
            task("m4t5", "Основной маршрут в 203.0.113.0/24 без метрики, плавающий — с метрикой 10. Какую метрику имеет основной?", "0",
                 "Метрика не задана — по умолчанию 0; маршрут с меньшей метрикой основной.", "число"),
            task("m4t6", "Пакет проходит R1 → R2 → R3. TTL у отправителя 3. Каким TTL пакет выйдет из R2?", "1",
                 "Каждый маршрутизатор уменьшает TTL на 1: R1 → 2, R2 → 1.", "число")))))
    # ---------------------------------------------------------------- тренажёры
    slide("Тренажёр: самое длинное совпадение", sc(head("Тренажёр: <em>самое длинное совпадение</em>",
                                                        "Выберите маршрут из FIB, по которому уйдёт пакет."),
        grow("g", col('<div class="m4lpm"><div class="m4lpm-q"></div><div class="m4lpm-opts"></div><div class="m4lpm-r"></div>'
                      '<button class="m4lpm-n">↻ Новый пакет</button></div>'))))
    slide("Тренажёр: что попадёт в таблицу", sc(head("Тренажёр: <em>что попадёт в таблицу</em>",
                                                     "Сравните preference, затем cost — выберите маршрут для FIB."),
        grow("g", col('<div class="m4pc"><div class="m4lpm-q"></div><div class="m4lpm-opts"></div><div class="m4lpm-r"></div>'
                      '<button class="m4lpm-n">↻ Новый случай</button></div>'))))
    # ---------------------------------------------------------------- тренажёр CLI
    _m4_cli.sim_slide("Тренажёр CLI ESR", "Тренажёр <em>CLI маршрутизатора ESR</em>",
                      "Случайное задание: адреса интерфейсов, статические маршруты, маршрут по умолчанию, плавающий маршрут, ROAS.",
                      [0, 1, 2, 3, 4, 5])
    # ---------------------------------------------------------------- тест
    _qslide("Тест 1 · таблица маршрутизации", [
        quiz("Что содержит FIB на ESR?", ["Все маршруты от всех источников", "Только лучшие маршруты", "Только статические маршруты"], 1,
             "RIB — все маршруты, FIB — только лучшие; по FIB пересылаются пакеты."),
        quiz("Каким кодом обозначается статический маршрут?", ["C", "S", "R", "O"], 1),
        quiz("Когда сеть с прямым подключением попадает в таблицу?", ["Сразу после включения", "Когда на интерфейсе IP и маска и он up/up",
                                                                       "Только после ip route"], 1),
        quiz("Какой preference у Directly connected?", ["0", "1", "100", "150"], 0)])
    _qslide("Тест 2 · выбор маршрута", [
        quiz("Внутри одного протокола лучший маршрут выбирается по…", ["preference", "наименьшей метрике", "времени появления"], 1),
        quiz("Между протоколами маршрут выбирается по…", ["наименьшему preference", "наибольшему cost", "числу интерфейсов"], 0),
        quiz("Метрика RIP — это…", ["стоимость по полосе пропускания", "количество переходов (hop)", "задержка"], 1,
             "Максимум 15 переходов, 16 — сеть недоступна."),
        quiz("Пакет для 172.16.0.10, маршруты /12, /18, /26. Какой выбран?", ["172.16.0.0/12", "172.16.0.0/18", "172.16.0.0/26"], 2)])
    _qslide("Тест 3 · пересылка", [
        quiz("Что меняется на каждом переходе?", ["IP-адреса источника и назначения", "Адреса канального уровня (L2)", "Ничего"], 1),
        quiz("Что происходит при TTL = 0?", ["Пакет пересылается дальше", "Пакет отбрасывается, отправителю — уведомление", "TTL сбрасывается"], 1),
        quiz("Повторный поиск next-hop в таблице называется…", ["рекурсивным поиском", "балансировкой", "сходимостью"], 0),
        quiz("Плавающий статический маршрут используется…", ["всегда вместе с основным", "только когда основной недоступен", "только для 0.0.0.0/0"], 1)])
    _qslide("Тест 4 · маршрутизация между VLAN", [
        quiz("Главный недостаток традиционного метода?", ["Нужен L3-коммутатор", "Для каждой VLAN — отдельный интерфейс L3 маршрутизатора",
                                                          "Не работает ARP"], 1),
        quiz("В ROAS порт коммутатора к маршрутизатору работает в режиме…", ["access", "trunk"], 1),
        quiz("Подинтерфейс Gi1/0/1.20 принимает кадры…", ["VLAN 10", "VLAN 20", "без тегов"], 1),
        quiz("Шлюзами по умолчанию на коммутаторе L3 выступают…", ["физические порты", "интерфейсы SVI", "подинтерфейсы"], 1)])
    # ---------------------------------------------------------------- итоги
    slide("Что запомнить", sc(head("Что <em>запомнить</em>"), grow("g2",
        col(step(card("Таблица", li(["Источники: C, S, протоколы динамической маршрутизации (R, O, i, B).",
                                     "RIB — все маршруты, FIB — лучшие; поиск — самое длинное совпадение.",
                                     "Нет маршрута и нет 0.0.0.0/0 — пакет отбрасывается."]), "cy")),
            step(card("Выбор маршрута", li(["Префикс → preference → cost → балансировка.", "Плавающий маршрут — резерв с большей метрикой."]), "mg"))),
        col(step(card("Путь пакета", li(["L2-адреса меняются на каждом переходе, IP-адреса — нет.", "TTL уменьшается на 1 на каждом маршрутизаторе."]), "lm")),
            step(card("Между VLAN", li(["Традиционный метод — интерфейс на каждую VLAN.", "ROAS — подинтерфейсы на одном порту, транк.",
                                        "L3-коммутатор — SVI как шлюзы."]), "am"))))))
    slide("Финал", sc(head("<em>Спасибо</em> за внимание"), grow("g2",
        col(step(card("Что дальше", li(["Повторите шпаргалку и пройдите тренажёр CLI ESR.", "Лабораторная: статическая маршрутизация и ROAS."]), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) + p("Вопросы по лекции и лабораторным — пишите."), "mg"))))))


JS = r"""
(function(){
  function rnd(a,b){return a+Math.floor(Math.random()*(b-a+1));}
  function pick(a){return a[rnd(0,a.length-1)];}
  function shuffle(a){for(var i=a.length-1;i>0;i--){var j=rnd(0,i),t=a[i];a[i]=a[j];a[j]=t;}return a;}
  function lpm(box){
    var sets=[{dst:function(){return '172.16.0.'+rnd(1,62);},r:[['172.16.0.0/12','gi1/0/1'],['172.16.0.0/18','gi1/0/2'],['172.16.0.0/26','gi1/0/3']],best:2},
      {dst:function(){return '192.168.2.'+rnd(1,254);},r:[['192.168.0.0/16','10.1.1.2'],['192.168.2.0/24','20.1.1.2'],['192.168.3.0/24','30.1.1.2']],best:1},
      {dst:function(){return '192.168.'+pick([5,7,9])+'.'+rnd(1,254);},r:[['192.168.0.0/16','10.1.1.2'],['192.168.2.0/24','20.1.1.2'],['192.168.3.0/24','30.1.1.2']],best:0},
      {dst:function(){return '10.10.'+pick([30,50])+'.'+rnd(1,254);},r:[['10.10.10.0/24','203.0.113.2'],['10.10.0.0/16','203.0.113.2'],['0.0.0.0/0','203.0.113.2']],best:1},
      {dst:function(){return pick(['8.8.8.8','77.88.8.8']);},r:[['10.10.10.0/24','203.0.113.2'],['10.10.0.0/16','203.0.113.2'],['0.0.0.0/0','203.0.113.2']],best:2},
      {dst:function(){return '10.1.1.'+rnd(1,254);},r:[['0.0.0.0/0','GE0/0'],['10.1.0.0/16','GE0/1'],['10.1.1.0/24','GE0/2']],best:2}];
    function nw(){var s=pick(sets),d=s.dst(),o=s.r.map(function(x,i){return {t:x[0]+' → '+x[1],ok:i===s.best};});shuffle(o);
      box.querySelector('.m4lpm-q').innerHTML='Пакет для <b>'+d+'</b>. Маршруты в FIB:';
      box.querySelector('.m4lpm-r').innerHTML='';var op=box.querySelector('.m4lpm-opts');op.innerHTML='';
      o.forEach(function(x){var b=document.createElement('button');b.textContent=x.t;b.onclick=function(){
        box.querySelector('.m4lpm-r').innerHTML=x.ok?'<span class="ok">✓ Верно: самое длинное совпадение префикса.</span>':'<span class="no">✗ Есть более длинное совпадение.</span>';
        b.className=x.ok?'ok':'no';};op.appendChild(b);});}
    box.querySelector('.m4lpm-n').onclick=nw;nw();
  }
  function pc(box){
    var src=[['Статический',1],['RIP',100],['OSPF',150],['IS-IS',160],['BGP',170],['DHCP',40]];
    function nw(){var a=pick(src),b=pick(src),c1=rnd(0,3)*10,c2=rnd(0,3)*10;if(a===b&&c1===c2)c2+=10;
      var r=[{s:a,c:c1,nh:'20.1.1.2'},{s:b,c:c2,nh:'30.1.1.2'}];
      var best=(a[1]!==b[1])?(a[1]<b[1]?0:1):(c1<c2?0:1);
      box.querySelector('.m4lpm-q').innerHTML='Два маршрута R1 в <b>10.0.0.0/30</b>:';
      box.querySelector('.m4lpm-r').innerHTML='';var op=box.querySelector('.m4lpm-opts');op.innerHTML='';
      r.forEach(function(x,i){var b=document.createElement('button');b.textContent=x.s[0]+' · preference '+x.s[1]+' · cost '+x.c+' · via '+x.nh;
        b.onclick=function(){var ok=i===best;box.querySelector('.m4lpm-r').innerHTML=ok?'<span class="ok">✓ Верно: '+(a[1]!==b[1]?'меньше preference':'preference равны — меньше cost')+'.</span>'
          :'<span class="no">✗ Сначала сравните preference, при равенстве — cost.</span>';b.className=ok?'ok':'no';};op.appendChild(b);});}
    box.querySelector('.m4lpm-n').onclick=nw;nw();
  }
  document.querySelectorAll('.m4lpm').forEach(lpm);document.querySelectorAll('.m4pc').forEach(pc);
})();
"""

CSS = r"""
.m4lpm,.m4pc{display:flex;flex-direction:column;gap:14px;padding:22px;background:var(--panel);border:1.5px solid rgba(240,199,94,.55);border-radius:12px}
.m4lpm-q{font:700 clamp(17px,1.7vw,32px)/1.4 var(--f)}
.m4lpm-opts{display:flex;flex-direction:column;gap:10px}
.m4lpm-opts button,.m4lpm-n{font:700 clamp(15px,1.4vw,26px)/1.3 var(--m);padding:12px 16px;border-radius:10px;cursor:pointer;text-align:left;
 background:rgba(4,22,16,.9);color:var(--ink);border:1.5px solid rgba(240,199,94,.55)}
.m4lpm-opts button.ok{border-color:#9be37a;background:rgba(155,227,122,.2)}.m4lpm-opts button.no{border-color:#ff7a5c;background:rgba(255,122,92,.2)}
.m4lpm-n{align-self:flex-start;background:var(--cy);color:#1a1206;font-family:var(--f)}
.m4lpm-r{font:700 clamp(15px,1.4vw,26px)/1.4 var(--f)}.m4lpm-r .ok{color:#9be37a}.m4lpm-r .no{color:#ff9f8a}
"""
