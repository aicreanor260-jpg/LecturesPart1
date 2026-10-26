# -*- coding: utf-8 -*-
"""Титул (pptx 1), цели (pptx 2) и финал деки 2.6: шпаргалка → задачи → тренажёры → тренажёр CLI ESR → тест →
что запомнить → финал. Все факты, команды и ответы — только из pptx «2.6»."""

from _sw_lib import slide, head as _h, sc, grow, col, card, p, li, foot, tags, tag, step, task, quiz
import _i6_cli
from _i6_deck import conf


def head_():
    slide("Титул", sc(
        '<div class="cover"><div class="big">Глава 6.<br><em>IP-сервисы</em></div>'
        '<div class="lead">DHCP, преобразование сетевых адресов NAT и протокол сетевого времени NTP на маршрутизаторах Eltex ESR.</div>%s'
        '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · Esc — содержание · '
        'в сценах кнопки «Назад / Вперёд»</div></div>'
        % tags(tag("Раздел 2.6"), tag("DHCP", "v"), tag("NAT", "g"), tag("NTP", "y"), tag("Eltex ESR", "r"))), cover=True)
    slide("Цели", sc(_h("<em>Цели</em>", ""), grow("g3",
        col(step(card("DHCP", p("Дать понимание протокола динамической конфигурации узлов;"), "cy", "1"))),
        col(step(card("NAT", p("Ознакомить с преобразованием сетевых адресов;"), "mg", "2"))),
        col(step(card("NTP", p("Рассказать о протоколах сетевого времени."), "lm", "3"))))))


def _qslide(title, sub, qs):
    slide(title, sc(_h(title.replace("Тест", "<em>Тест</em>"), sub), grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат: <span class="score">0 / 0</span></span></div>'))


# ---------------------------------------------------------------- тренажёр «термины NAT»: случайные адреса
TERMS_HTML = """<div class="q i6terms"><div class="qt">Компьютер <b data-v="pc"></b> открывает сайт на сервере <b data-v="srv"></b>;
маршрутизатор подменяет адрес компьютера на <b data-v="pub"></b>. Какой термин NAT у адреса?</div>
<div class="i6t-q"></div><div class="opts">
<button data-t="Inside local">Inside local</button><button data-t="Inside global">Inside global</button>
<button data-t="Outside local">Outside local</button><button data-t="Outside global">Outside global</button></div>
<div class="note i6t-res"></div><div class="inrow"><button class="sec" data-act="i6tnew">↻ Новый вопрос</button>
<span class="i6t-sc">0 / 0</span></div></div>"""

LEASE_HTML = """<div class="q i6lease"><div class="qt">Время аренды адреса — <b data-v="lease"></b> мин.
Через сколько минут клиент отправит DHCPREQUEST по таймеру <b data-v="tn"></b>?</div>
<div class="inrow"><input type="text" placeholder="минут" autocomplete="off"><button data-act="i6lchk">Проверить</button>
<button class="sec" data-act="i6lnew">↻ Новое условие</button></div><div class="note i6l-res"></div></div>"""

JS = r"""
/* автоподбор масштаба: короткий слайд — крупнее (проектор), длинный — без прокрутки */
(function(){
  function fit(sl){
    if(!sl||sl.classList.contains('cover-slide')||sl.querySelector('.rep,.clisim6,.clisim'))return;
    var sc=sl.querySelector('.sc'),g=sc&&sc.querySelector(':scope>.grow'); if(!g)return;
    g.style.flex='none'; var lo=.55,hi=1.6;
    for(var i=0;i<9;i++){var z=(lo+hi)/2;g.style.zoom=z;
      var ok=sc.scrollHeight<=sc.clientHeight+1&&sc.scrollWidth<=sc.clientWidth+1;
      sl.querySelectorAll('pre').forEach(function(p){if(p.scrollWidth>p.clientWidth+1)ok=false;});
      if(ok)lo=z;else hi=z;}
    g.style.zoom=lo; g.style.flex='';
  }
  function all(){var on=document.querySelector('section.slide.on');fit(on);}
  var mo=new MutationObserver(function(ms){ms.forEach(function(m){if(m.target.classList.contains('on'))setTimeout(function(){fit(m.target)},30);});});
  function boot(){document.querySelectorAll('section.slide').forEach(function(s){mo.observe(s,{attributes:true,attributeFilter:['class']});});all();}
  window.addEventListener('resize',function(){setTimeout(all,60);});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  window.I6FIT=fit;
})();
(function(){
  function R(a,b){return a+Math.floor(Math.random()*(b-a+1));}
  function terms(box){
    var pc='192.168.'+R(0,9)+'.'+R(2,200), srv='203.0.113.'+R(1,250), pub='198.51.100.'+R(1,250);
    var qs=[['адрес отправителя '+pc+' до NAT','Inside local'],['адрес отправителя '+pub+' после NAT','Inside global'],
            ['адрес получателя '+srv+' в локальной сети','Outside local'],['адрес получателя '+srv+' после NAT','Outside global']];
    var q=qs[R(0,3)]; box.dataset.ans=q[1];
    box.querySelector('[data-v="pc"]').textContent=pc; box.querySelector('[data-v="srv"]').textContent=srv;
    box.querySelector('[data-v="pub"]').textContent=pub;
    box.querySelector('.i6t-q').textContent='Поле: '+q[0]; box.querySelector('.i6t-res').innerHTML='';
    box.querySelectorAll('[data-t]').forEach(function(b){b.className='';b.disabled=false;});
  }
  function lease(box){
    var L=[20,40,60,80,120,160,240,480][R(0,7)], t=R(0,1); box.dataset.ans=t?L*0.875:L*0.5;
    box.querySelector('[data-v="lease"]').textContent=L; box.querySelector('[data-v="tn"]').textContent=t?'Т1 (87,5%)':'Т0 (50%)';
    box.querySelector('input').value=''; box.querySelector('.i6l-res').innerHTML='';
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('.i6terms [data-t],[data-act="i6tnew"],[data-act="i6lchk"],[data-act="i6lnew"]'); if(!b) return;
    var box=b.closest('.q');
    if(b.dataset.act==='i6tnew') return terms(box);
    if(b.dataset.act==='i6lnew') return lease(box);
    if(b.dataset.act==='i6lchk'){var v=parseFloat(box.querySelector('input').value.replace(',','.')), a=+box.dataset.ans;
      box.querySelector('.i6l-res').innerHTML=(v===a?'<span style="color:#7dff9a">✓ Верно: ':'<span style="color:#ff8a8a">✗ Ответ: ')+
        String(a).replace('.',',')+' мин</span>'; return;}
    var ok=b.dataset.t===box.dataset.ans, s=box.querySelector('.i6t-sc').textContent.split(' / ').map(Number);
    if(box.querySelector('[data-t]:disabled')) return;
    box.querySelectorAll('[data-t]').forEach(function(x){x.disabled=true; if(x.dataset.t===box.dataset.ans) x.className='ok';});
    if(!ok) b.className='no';
    box.querySelector('.i6t-sc').textContent=(s[0]+(ok?1:0))+' / '+(s[1]+1);
    box.querySelector('.i6t-res').innerHTML=ok?'✓ Верно':'✗ Правильно: '+box.dataset.ans;
  });
  function boot(){document.querySelectorAll('.i6terms').forEach(terms);document.querySelectorAll('.i6lease').forEach(lease);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
"""

CSS = r"""
ol.i6ol li{font-size:clamp(14px,1.32vw,26px);line-height:1.42}
.i6terms .opts button.ok{background:#1f7a3a!important;color:#fff}.i6terms .opts button.no{background:#8a2230!important;color:#fff}
.i6t-q{font:700 clamp(14px,1.2vw,23px)/1.4 var(--f);color:#ffd36a;margin:8px 0}
.i6t-sc{font:800 clamp(14px,1.1vw,21px)/1 var(--f);color:var(--cy);align-self:center;margin-left:10px}
""" + _i6_cli.CSS


def tail():
    slide("Шпаргалка: DHCP", sc(_h("Шпаргалка <em>команд</em> · DHCP", "Команды ESR из лекции — в том же синтаксисе."), grow("g2",
        col(step(conf(["ESR(config-if-gi)#ip address dhcp", "ESR(config-if-gi)#ip dhcp server address 192.168.2.10", "ESR(config)#ip dhcp-server", "ESR(config)#ip dhcp-server pool DHCP-10", "ESR(config-dhcp-server)#network 192.168.10.0/24", "ESR(config-dhcp-server)#address-range 192.168.10.1-192.168.10.100", "ESR(config-dhcp-server)#excluded-address-range 192.168.10.10", "ESR(config-dhcp-server)#default-router 192.168.10.10"], "DHCP-клиент · DHCP-сервер"))),
        col(step(conf(["ESR(config)#ip dhcp-relay", "ESR(config-if-gi)# ip helper-address 10.0.0.2", "ESR# show ip dhcp binding", "ESR# show ip dhcp server pool lan-pool"], "DHCP relay · проверка"))))))
    slide("Шпаргалка: NAT и NTP", sc(_h("Шпаргалка <em>команд</em> · NAT и NTP", "Команды ESR из лекции — в том же синтаксисе."), grow("g2",
        col(step(conf(["ESR(config)# security zone TRUST", "ESR(config-if-gi)# security-zone TRUST",
                            "ESR(config)# object-group network LOCAL_NET",
                            "ESR(config-object-group-network)# ip address-range 192.168.1.1-192.168.1.254",
                            "ESR(config)# security zone-pair TRUST UNTRUST",
                            "ESR(config-zone-pair-rule)# match source-address LOCAL_NET",
                            "ESR(config-zone-pair-rule)# action permit", "ESR(config)# nat source",
                            "ESR(config-snat)# pool WAN_ADDRESS", "ESR(config-snat)# ruleset SNAT",
                            "ESR(config-snat-ruleset)# to zone UNTRUST",
                            "ESR(config-snat-rule)# action source-nat pool WAN_ADDRESS",
                            "ESR# show ip nat translations", "ESR# show ip nat proxy-arp"], "Source NAT · проверка"))),
        col(step(conf(["ESR(config)# object-group service FTP_PORT", "ESR(config-object-group-service)# port 21",
                            "ESR(config-dnat)# ruleset DNAT", "ESR(config-dnat-ruleset)# from zone UNTRUST",
                            "ESR(config-dnat-rule)# match protocol tcp",
                            "ESR(config-dnat-rule)# action destination-nat pool SERVER_POOL",
                            "ESR(config-zone-pair-rule)# match destination-nat",
                            "ESR(config)# ntp enable", "ESR(config)# ntp server 192.0.2.1", "ESR(config-ntp)# prefer",
                            "ESR(config-ntp)# minpoll 4", "esr# show ntp peers", "esr# show ntp configuration"], "Destination NAT · NTP"))))))
    slide("Итоговые задачи", sc(_h("Итоговые <em>задачи</em>", "Рассуждаем и вводим ответ."), grow("g2",
        col(task("i6z1", "Аренда адреса — 600 с (10 минут), как в DHCPACK из анализатора. Через сколько минут наступит таймер Т0?",
                 "5|5 минут|пять", "Т0 = 50% от времени аренды: 10 × 0,5 = <b>5 минут</b>.", "минут"),
            task("i6z2", "Какой адрес источника у DHCPDISCOVER, если у клиента ещё нет своего IPv4-адреса?",
                 "0.0.0.0", "Адрес источника — <b>0.0.0.0</b>, назначения — 255.255.255.255.", "IP-адрес")),
        col(task("i6z3", "Компьютер 192.168.1.10 → сервер 203.0.113.20, после NAT отправитель 198.51.100.7. Как называется адрес 198.51.100.7?",
                 "inside global|внутренний глобальный|inside global address",
                 "Адрес внутреннего компьютера «для внешнего мира» — <b>Inside global</b>.", "термин"),
            task("i6z4", "Источники времени 10 ± 2, 11 ± 1 и 12 ± 1. Какую точку даёт пересечение интервалов по алгоритму Марзулло?",
                 "11.5|11,5|11.5 ± 0.5|11,5 ± 0,5", "Пересечение [8,12], [10,12], [11,13] — [11,12], точка <b>11,5 ± 0,5</b>.", "значение")))))
    slide("Тренажёры", sc(_h("<em>Тренажёры</em>", "Случайные условия — нажимайте «Новый вопрос»."), grow("g2",
        col(step(TERMS_HTML)), col(step(LEASE_HTML),
                                   step(foot("Т0 = 50% времени аренды, Т1 = 87,5% времени аренды.", "note"))))))
    _i6_cli.sim_slide("Тренажёр CLI: DHCP", "Тренажёр CLI · <em>DHCP</em>",
                      "Консоль ESR: configure → интерфейсы, пул, relay. «Проверить» — по итоговой конфигурации.", [0, 1, 2])
    _i6_cli.sim_slide("Тренажёр CLI: NAT", "Тренажёр CLI · <em>Source и Destination NAT</em>",
                      "Зоны, object-group, пары зон, правила SNAT/DNAT. «Отправить пакет» — пройдёт ли трафик.", [3, 4])
    _i6_cli.sim_slide("Тренажёр CLI: NTP", "Тренажёр CLI · <em>NTP</em>",
                      "ntp enable, ntp server, prefer, minpoll. Проверьте: show ntp configuration.", [5])
    _qslide("Тест · 1", "DHCP. Выберите один вариант.", [
        quiz("Какое сообщение клиент отправляет первым?", ["DHCPOFFER", "DHCPDISCOVER", "DHCPACK", "DHCPREQUEST"], 1,
             "DHCPDISCOVER — широковещательный поиск DHCP-сервера."),
        quiz("Какой адрес назначения у DHCPDISCOVER?", ["0.0.0.0", "адрес шлюза", "255.255.255.255", "адрес DNS-сервера"], 2,
             "Клиент не знает, к какой сети подключен, поэтому адрес назначения 255.255.255.255."),
        quiz("Что отправит клиент, если на ARP-запрос пришёл ответ?", ["DHCPACK", "DHCPDECLINE", "DHCPOFFER", "DHCPNAK"], 1,
             "Адрес уже используется — клиент уведомляет сервер сообщением DHCPDECLINE."),
        quiz("Чему равен таймер Т1?", ["50% аренды", "75% аренды", "87,5% аренды", "100% аренды"], 2,
             "Т0 = 50%, Т1 = 87,5% от времени аренды."),
    ])
    _qslide("Тест · 2", "DHCP relay и NAT.", [
        quiz("Какая команда включает DHCP relay на ESR глобально?", ["ip dhcp-server", "ip dhcp-relay", "ip helper-address", "ip address dhcp"], 1,
             "ip dhcp-relay — глобально; ip helper-address — на интерфейсе со стороны клиента."),
        quiz("Какой диапазон частных адресов класса B по RFC 1918?", ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "100.64.0.0/10"], 1,
             "172.16.0.0-172.31.255.255, маска 172.16.0.0/12."),
        quiz("Адрес сервера, каким его видит внутренняя сеть, — это…", ["Inside local", "Inside global", "Outside local", "Outside global"], 2,
             "Outside local — адрес внешнего сервера «в представлении внутренней сети»."),
        quiz("Какой NAT сопоставляет адреса 1:n с помощью портов?", ["статический", "динамический", "NAPT", "Destination NAT"], 2,
             "NAPT преобразует IP-адрес и номера портов, несколько частных адресов — в один публичный."),
    ])
    _qslide("Тест · 3", "SNAT, DNAT и NTP.", [
        quiz("Какой NAT используют, чтобы сервер в TRUST был доступен из Интернета?", ["Source NAT", "Destination NAT", "NAT Proxy ARP", "PAT"], 1,
             "DNAT (Inbound NAT) переписывает адрес назначения и направляет запрос внутреннему ресурсу."),
        quiz("Что помечает адрес пула динамического NAT, занятый узлом?", ["Not Use", "In Use", "Static", "Reserved"], 1,
             "Назначенный адрес помечается как In Use, освобождённый — Not Use."),
        quiz("Какой уровень Stratum означает «устройство не синхронизировано»?", ["0", "1", "15", "16"], 3,
             "Stratum 16 — самый низкий уровень, устройство не синхронизировано."),
        quiz("Какая команда указывает предпочтительный NTP-сервер?", ["minpoll", "prefer", "ntp enable", "show ntp peers"], 1,
             "prefer — указание предпочтительности данного NTP-сервера."),
    ])
    slide("Что запомнить", sc(_h("Что <em>запомнить</em>", "Короткая выжимка лекции."), grow("g3",
        col(step(card("DHCP", li([
            "DISCOVER → OFFER → REQUEST → ACK; отказ — DHCPNAK.",
            "Проверка адреса ARP-запросом; конфликт — DHCPDECLINE.",
            "Т0 = 50%, Т1 = 87,5% времени аренды.",
            "Клиент в другой сети — <b>ip dhcp-relay</b> + <b>ip helper-address</b>."]), "cy"))),
        col(step(card("NAT", li([
            "Частные адреса — RFC 1918: 10/8, 172.16/12, 192.168/16.",
            "Inside local / Inside global / Outside local / Outside global.",
            "Статический 1:1, динамический из пула, NAPT 1:n по портам.",
            "SNAT — выход в Интернет, DNAT — доступ к серверу извне."], "mg"), "mg"))),
        col(step(card("NTP", li([
            "Клиент-серверный протокол синхронизации времени.",
            "Алгоритм Марзулло — пересечение интервалов источников.",
            "Stratum 0 — атомные часы/GPS, 16 — не синхронизировано.",
            "<b>ntp enable</b>, <b>ntp server</b>, <b>prefer</b>, <b>minpoll</b>."], "lm"), "lm"))))))
    slide("Финал", sc(_h("<em>Спасибо</em> за внимание", "Глава 6 · IP-сервисы: DHCP, NAT, NTP"), grow("g2",
        col(step(card("Что повторить", li(["Четыре этапа DHCP и продление аренды.", "Термины NAT в одном обмене.",
                                           "Настройку Source и Destination NAT на ESR.", "Иерархию Stratum и команды NTP."]), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) +
                      p("Вопросы по лекции и лабораторным — пишите."), "mg"))))))


head = head_
