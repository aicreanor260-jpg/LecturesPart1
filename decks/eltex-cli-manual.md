# Сетевая лаборатория Eltex — мини-мануал

`eltex-cli.html` — лёгкий эмулятор сети для лабораторных NTF2: коммутаторы **MES** (CLI MES24xx, ПО 10.4), маршрутизатор **ESR** (CLI ESR), компьютеры **VPC** и **Debian**. Один HTML-файл, работает офлайн в любом браузере, без виртуальных машин. Это модель поведения по документации Eltex, а не прошивка.

## Запуск
- Откройте `decks/eltex-cli.html` в браузере (двойной щелчок) или по ссылке с хаба `index.html`.
- Для группы: положите файл на любой веб-сервер (nginx на Debian) или в общую папку. Сервер ничего не считает — всё работает в браузере студента.

## Интерфейс (как в pnetlab)
| Действие | Как |
|---|---|
| Поле | на весь экран; перетаскивание пустого места — сдвиг, колесо — масштаб, «Вся схема» — показать всё |
| Левая панель | наведите мышь на левый край (или щёлкните по нему); вкладки «Устройства», «Лабы», «Задания», «Файл», «?»; ⇤ — закрепить |
| Добавить устройство | ПКМ по пустому полю → поиск модели; или перетащите модель из левой панели |
| Меню устройства (ПКМ) | Консоль, Свойства (имя, порты, линки), Подключить кабель, Ping отсюда, Выключить/Включить, Перезагрузить, Удалить |
| Кабель | ПКМ по устройству → «Подключить кабель» → щёлкните второе устройство → выберите порты в окне |
| Терминал | двойной щелчок по устройству или кнопка «Терминал» внизу (для выбранного); окна двигаются за заголовок, растягиваются за угол, сворачиваются в нижнюю панель |
| Кабель/устройство удалить | ПКМ → Удалить, или выделить и Delete |
| Таблицы | ПКМ по устройству → «Таблицы»: ARP, MAC-таблица коммутатора, VLAN и порты, маршруты — живые, меняются от каждого пакета. Пока идёт трасса, окно показывает таблицы на текущем шаге: запись появляется (подсвечена) ровно на том шаге, где её записал ARP-запрос/ответ или кадр; кнопки ◀ ▶ трассы листают и таблицы |
| Путь пакета | при любом ping внизу экрана — пошаговая трасса: ⏮ ◀ ▶ ⏵ |
| Время сети | часы в шапке: ❚❚ пауза, ×1 / ×10 / ×60 — скорость, «⏩ 1 мин» / «⏩ 5 мин» — промотать. От этого времени стареют записи MAC и ARP (в окне «Таблицы» — колонка «Осталось, с»), идут `date` / `show date` |
| Сохранить/открыть | левая панель → «Файл» (схема в .json) |

### Старение записей (таймеры по руководствам Eltex)

| Устройство | MAC-таблица | ARP-таблица |
|---|---|---|
| MES 10.x | `mac-address-table aging-time 10..400`, по умолчанию 300 с | `arp timeout 30..86400`, по умолчанию 60000 с |
| MES 6.x / 4.x | `mac address-table aging-time 10..400`, по умолчанию 300 с | `arp timeout 1..40000000`, по умолчанию 60000 с |
| MES 8.x (FASTPATH) | `bridge aging-time 10..1000000`, по умолчанию 300 с | `arp timeout 15..21600`, по умолчанию 1200 с |
| ESR | — | `ip arp reachable-time 5000..100000000` (мс) на интерфейсе, по умолчанию 160000 мс |
| VPC | — | 120 с (`arp` показывает «expires in N seconds») |
| Debian | — | 30 с REACHABLE, затем STALE, удаление через 60 с (`ip neigh`) |

Просмотр: `show mac-address-table aging-time` (10.x), `show mac address-table aging-time` (6.x), `show forwardingdb agetime` (8.x).
Опыт для студента: ping → «⏩ 5 мин» → MAC-таблица коммутатора пуста → следующий ping снова начинается с ARP-запроса и широковещательной рассылки.

В консоли: `?` — подсказка, `Tab` — дописать, `↑ ↓` — история. Перезагрузка: `reload` на MES (загружается startup-config), `reload system` на ESR (неприменённые правки теряются); сброс кандидата ESR к заводскому: `copy system:default-config system:candidate-config`.

## Ветки ПО коммутаторов — свой CLI у каждой
| Ветка | Модели | Отличия синтаксиса |
|---|---|---|
| 10.x | MES14xx, MES24xx, MES3400, MES37xx | `spanning-tree mode rst\|mst\|rapid-pvst`, `channel-group N mode active\|passive\|on`, `set lldp enable`, `monitor session` |
| 6.x и 4.x | MES23xx, MES33xx, MES35xx, MES53xx, MES54xx–57xx | `spanning-tree mode stp\|rstp\|mstp`, `channel-group N mode auto\|on`, `lldp run`, `port monitor <порт>` на порту-получателе, `show interfaces channel-group` |
| 8.x (FASTPATH) | MES5448, MES7048 | приглашения `(switch) #`, `(switch) (Config)#`, `(switch) (Interface 1/0/1)#`; порты `1/0/N`, диапазон `interface 1/0/1-1/0/4`; `vlan database` из `#`, `vlan name 10 IT`; LAG: `port-channel ИМЯ`, `addport lag 1`, `port-channel static`; `vlan participation include`, `vlan tagging`, `vlan pvid`; `spanning-tree mst priority 0 4096`; `monitor session 1 … mode`; `show port-channel brief` |

Порты называются по типу, как на устройстве: `fa` 100M, `gi` 1G, `tw` 2.5G, `te` 10G, `fo` 40G, `hu` 100G — например, у MES2424 это gi1/0/1–24 и te1/0/1–4, у MES5324 te1/0/1–24 и fo1/0/1–4.

## Режимы
**MES:** `switch>` → `enable` → `switch#` → `configure` → `switch(config)#` → `interface gi1/0/1` → `switch(config-if)#`; также `(config-if-range)#`, `(config-vlan)#` (`vlan database`/`vlan N`), `(config-line)#`. `exit` — на уровень выше, `end` — в `#`.

**ESR:** `vesr#` → `configure` → `(config)#` → `(config-if-gi)#`, `(config-if-sub)#` (саб-интерфейс `1/0/1.10`), `(config-if-loopback)#`, `(config-user)#`. Правки копятся в кандидате и **вступают в силу только после `commit`**, затем `confirm`.

## Поддерживаемые команды (с примерами)
**MES**
```
hostname SW1                       username admin1 password P privilege 15
enable password eltex15            enable password level 7 eltex7
line console / password c0n / exec-timeout 5 / login authentication console
banner login @ Authorized only! @  banner exec @ Welcome! @   banner motd @ ... @
vlan database / vlan 10,20 / exit  vlan 10 / name IT          no vlan 30
interface range gigabitethernet 1/0/1-4
switchport mode access | trunk | general
switchport access vlan 10          no switchport access vlan
switchport trunk allowed vlan add 10,20     switchport trunk native vlan 99
switchport general allowed vlan add 100 tagged     switchport general pvid 10
shutdown / no shutdown
interface vlan 10 / ip address 10.0.0.1 255.255.255.0   (или /24)
ip default-gateway 10.0.0.254      ip route 10.2.0.0 255.255.0.0 10.0.0.2
ip ssh server / crypto key generate rsa
spanning-tree / spanning-tree mode rst / spanning-tree priority 16384 / (на порту) spanning-tree cost 20000
interface port-channel 1 / interface range gi1/0/1-4 / channel-group 1 mode active|passive|on
show spanning-tree | etherchannel summary
monitor session 1 destination interface gi1/0/12 / monitor session 1 source interface gi1/0/1 both / show monitor session 1
show running-config | startup-config | vlan | interfaces switchport gi1/0/1
show arp · clear arp-cache · clear mac address-table dynamic
show interfaces status | ip interface | ip route | mac address-table
do show vlan    write    copy running-config startup-config    reload    ping 10.0.0.2
```
**ESR**
```
hostname R1    clock timezone gmt +7    set date 11:25:30 11 November 2025    show date
interface gigabitethernet 1/0/1 / ip address 192.168.100.1/24 / ip firewall disable
interface gigabitethernet 1/0/1.50 / ip address 173.16.25.1/24
interface loopback 1 / ip address 8.8.8.8/32
username master / password eltex / privilege 14
ip ssh server    banner login Router-R1    banner exec "Connect Router R1"
ip route 10.0.0.0/8 192.168.1.2          ip route 10.0.0.0/8 10.1.1.2 10   (плавающий, метрика 10)
interface gigabitethernet 1/0/1-3       (диапазон интерфейсов)
router rip / network 192.168.0.0/23 / passive-interface gigabitethernet 1/0/3 / redistribute connected / enable
router ospf 250 / router-id 1.1.1.1 / area 0.0.0.0 / enable / exit / enable
interface … / ip ospf instance 250 / ip ospf area 0.0.0.0 / ip ospf / ip ospf passive-interface / ip ospf cost 10
show ip route all | ip rip | ip ospf | ip ospf neighbors
ip dhcp-server / ip dhcp-server pool DHCP-10 / network 192.168.10.0/24 / address-range 192.168.10.100-192.168.10.200 / default-router 192.168.10.1 / default-lease-time 0:1:0
ip dhcp-relay / interface … / ip helper-address 192.168.100.2
nat source / ruleset SNAT / to interface gi1/0/1 / rule 10 / match source-address address-range 192.168.1.1-192.168.1.254 / action source-nat interface / enable
nat destination / ruleset Dest_NAT / from interface gi1/0/1 / rule 10 / match protocol tcp / match destination-port port-range 80 / action destination-nat netmap 192.168.1.100/32 / enable
ntp enable / ntp server 192.168.1.10 / minpoll 1 / maxpoll 4
ip telnet server / ip access-list extended Test1 / rule 10 / action deny / match protocol tcp / match destination-port port-range 23 / enable
interface gi1/0/1 / service-acl input Test1          show ip access-list Test1
interface gi1/0/1 / vrrp id 100 / vrrp ip 192.168.10.1/24 / vrrp priority 200 / vrrp          show vrrp
lldp enable / interface gi1/0/1 / lldp receive / lldp transmit          show lldp neighbors | system
syslog host SERVER / source-address 192.168.1.1 / remote-address 192.168.1.10 / transport udp / port 514 / severity info
copy system:running-config tftp://192.168.1.10:/run.cfg
archive / type remote / path tftp://192.168.1.10:/Backup_run.cfg / by-commit
vlan 100 / interface gi1/0/3 / mode switchport / switchport mode access / switchport access vlan 100
bridge 100 / vlan 100 / ip address 192.168.220.1/24 / ip firewall disable / enable
show ip dhcp binding | ip nat translations | ntp peers
do commit    do confirm    rollback    show candidate-config
show running-config | ip interfaces | ip route | interfaces status | users    ping    traceroute
```
**VPC:** `ip 10.0.0.2/24 10.0.0.1`, `ip dhcp`, `show`, `ping`, `trace`, `arp`, `clear ip`.
**Debian** (вход `root`/`toor`): `ip a`, `ip link set ens3 up`, `ip addr add 192.168.100.2/24 dev ens3`, `ip route add default via 192.168.100.1`, `nano /etc/network/interfaces` + `ifdown ens3`/`ifup ens3`, `cat`, `ping`, `traceroute`, `ssh master@192.168.100.1`, `dhclient ens3`, `curl http://IP`, `date`, `timedatectl set-ntp false` / `set-time '2010-09-01 10:12:00'`, `systemctl status|restart chronyd|apache2|rsyslog|tftpd-hpa` (или `service tftpd-hpa status`), `ls /tftp`, `cat`, `telnet IP`, `tcpdump` (анализатор на зеркальном порту). Docker-браузер: `open http://IP`.

### Межсетевой экран ESR по зонам (справочник ESR-Series CLI 1.23)
```
security zone trusted
exit
security zone untrusted
exit
interface gigabitethernet 1/0/1
  security-zone trusted
exit
object-group network LAN
  ip prefix 192.168.1.0/24
exit
object-group service WEB
  port-range 80,443
exit
security zone-pair trusted untrusted
  rule 10
    action permit
    match protocol tcp
    match source-address object-group LAN
    match destination-port object-group WEB
    enable
  exit
exit
security zone-pair trusted self        ← трафик самому маршрутизатору (ping шлюза, SSH, DHCP)
```
Как ведёт себя модель:
- интерфейс с включённым firewall (по умолчанию) без зоны — пакет отбрасывается; `ip firewall disable` — зоны не проверяются;
- правила пары «зона входа → зона выхода» перебираются по номеру, первое подошедшее решает (permit / deny / reject); не подошло ни одно — неявный запрет;
- **stateful**: ответ на разрешённую сессию проходит без правил в обратную сторону; свой трафик маршрутизатора тоже;
- порядок как на ESR: Destination NAT → межсетевой экран → маршрутизация → Source NAT;
- в NAT можно `match source-address object-group LAN`, `match destination-port object-group WEB`.

Просмотр: `show security zone`, `show security zone-pair [ИЗ В]`, `show ip firewall sessions` (с колонками State и Expire), `show ip firewall counters`, `clear ip firewall sessions|counters`, `show object-group [network|service] [ИМЯ]`, `show configuration changes` — что изменится после commit.

**Сессии по протоколам — как conntrack на ESR.** Таймер идёт по модельному времени (часы в шапке, «⏩ 1/5 мин»):

| Протокол | Состояние | Когда | Таймаут по умолчанию | Команда |
|---|---|---|---|---|
| ICMP | ICMP | echo-запрос и ответ | 30 с | `ip firewall sessions icmp-timeout` |
| TCP | SYN_SENT | первый пакет (рукопожатие) | 60 с | `… tcp-connect-timeout` |
| TCP | ESTABLISHED | пришёл ответ, сессия открыта (SSH, Telnet) | 120 с | `… tcp-estabilished-timeout` (так в CLI ESR; `tcp-established` тоже принимается) |
| TCP | TIME_WAIT | обмен закончен, соединение закрыто (HTTP) | 30 с | `… tcp-disconnect-timeout` |
| UDP | UNREPLIED | ответа ещё не было | 30 с | `… udp-wait-timeout` |
| UDP | ASSURED | ответ был (NTP, DNS) | 180 с | `… udp-assured-timeout` |
| прочие | GENERIC | GRE, OSPF … | 60 с | `… generic-timeout` |

Живой UDP-поток (тот же адрес и порт) идёт по сессии без проверки правил — поэтому, если удалить правило, поток работает до истечения сессии: `clear ip firewall sessions` или подождать таймаут. Таймауты: `show ip firewall sessions timeouts`.

### RIP и OSPF по реальным таймерам (справочник ESR 1.23)
Время модельное: часы в шапке, ×10 / ×60, «⏩ 1 мин».

**OSPF** — `ip ospf hello-interval` 10 с, `ip ospf dead-interval` 40 с (по умолчанию 4×hello), wait timer = dead, `ip ospf priority` 128, `ip ospf network broadcast|point-to-point`.
- После включения сосед проходит init → 2way; на broadcast-сегменте, где ещё нет DR, роутеры ждут wait timer (40 с) и только потом выбирают DR/BDR и доходят до full. Маршруты O появляются в full. На point-to-point и при уже выбранном DR — за пару секунд.
- `show ip ospf neighbors` — состояние (2way/other, full/dr, full/bdr, full/ptp), DTime, подсказка «ожидание выбора DR, осталось N с».
- Hello/dead у соседей разные — соседства нет; причина видна в `show ip ospf neighbors`.
- Сосед замолчал (выключен, OSPF снят, обрыв за коммутатором) — он остаётся full до истечения dead-interval, маршруты через него ведут в никуда. Свой интерфейс упал — сосед удаляется сразу.
- `show ip ospf interface [gi1/0/1]` — тип сети, роль (dr/bdr/drother), приоритет, таймеры.

**RIP** — в `router rip`: `timers update` 30, `timers invalid` 180, `timers flush` 240 (по умолчанию invalid + 60).
- Новые маршруты приходят сразу (запрос/ответ при включении и триггерные обновления).
- Сосед замолчал — маршрут через него остаётся в таблице до invalid (в `show ip rip`: «обновлений нет N с, invalid через M с»), затем «possibly down» с метрикой 16 и не используется, удаляется по flush.
- Свой интерфейс выключен — маршруты через него удаляются сразу.

В автопроверке лаб после решения отсчитывается 60 с модельного времени — как на стенде, где после настройки ждут сходимости.

### Расширенный CLI MES (по руководствам 10.4.6 и 6.6.8.8)
Сокращения — как на железе: `en`, `conf t`, `int gi 1/0/1`, `sw mode trunk`, `sh ru`, `sh int st`, `wr`.

| Что | 10.x (MES14xx/24xx/3400/37xx) | 6.x / 4.x | Что происходит в сети |
|---|---|---|---|
| Port security | `switchport port-security enable`, `… mac-limit N`, `… mode max-addresses\|lock\|secure-permanent`, `… violation restrict\|protect\|discard-shutdown`, `show port-security` | `port security`, `port security max N`, `port security mode lock\|max-addresses`, `port security forward\|discard\|discard-shutdown`, `show ports security` | кадр с неразрешённого MAC отбрасывается (в трассе — шаг «port security»), при discard-shutdown порт выключается; разрешённые адреса — secure, не стареют |
| BPDU guard | `spanning-tree portfast`, `spanning-tree bpduguard enable` | то же | к порту подключили коммутатор с STP — порт выключается (err-disable), вернуть — `no shutdown` после отключения |
| Статический MAC | `mac-address-table static unicast MAC vlan N interface gi1/0/7 status permanent` | `mac address-table static MAC vlan N interface gi1/0/7` | запись Static в таблице, не стареет и не переучивается |
| Время | `clock set 10:20:30 5 Mar 2026`, `clock timezone MSK +3`, `show clock` | то же | |
| Сведения | `show version`, `show system`, `show users`, `show interfaces description`, `show running-config interface gi1/0/1`, `show lldp neighbors`, `traceroute A.B.C.D` | то же, `traceroute ip A.B.C.D` | LLDP: MES видит соседей-MES и ESR, ESR видит MES |

## Типовые ошибки
| Сообщение | Что делать |
|---|---|
| `% Unrecognized command` | опечатка или команды нет — нажмите `?` |
| `% Incomplete command` | команда не дописана (`show` → `show vlan`) |
| `% Команда недоступна в этом режиме` | смотрите на приглашение: нужен `#`, `(config)#` или режим интерфейса |
| `% VLAN 30 не создана` | сначала `vlan database` / `vlan 30` |
| ESR не отвечает | нет `commit` или не отключён экран: `ip firewall disable` |
| Маршрут есть в `show ip route all`, но без `*` | шлюз недоступен (интерфейс выключен) или есть маршрут с меньшей метрикой — это и есть плавающий маршрут в резерве |
| Нет маршрутов R/O | протокол не включён (`enable`), сеть не в `network`, интерфейс пассивный или не применён `commit` |
| ARP без ответа | разные VLAN, VLAN не разрешена на транке, нет саб-интерфейса, порт `shutdown` — шаги трассы показывают точку отбрасывания |

## Как добавить свою лабораторную
Лабы описаны в `decks/_elab/labs.js` и `decks/_elab/labs_routing.js` (маршрутизация), массив `LABS`. Шаблон:
```js
{ id: '5.0', title: 'Название', goal: 'Цель работы',
  gen: function () { return { v: EL.pick([10, 20, 30]) }; },          // случайный вариант
  build: function (net, p) {                                          // топология
    var s = net.add('MES2428', 'SW1', 420, 300), a = net.add('VPC', 'VPC1', 160, 300);
    net.connect(a.id, 'eth0', s.id, 'gi1/0/1'); },
  tasks: function (p) { return [                                      // проверки (true = выполнено)
    { t: 'gi1/0/1 в VLAN ' + p.v, ok: function (n) { return n.byName('SW1').st.ports['gi1/0/1'].access === p.v; } },
    { t: 'ping VPC1 → 10.0.0.1', ok: function (n) { return n.reach('VPC1', '10.0.0.1'); } }]; },
  sol: function (p) { return { SW1: ['enable', 'configure', 'vlan ' + p.v, 'exit', '...'], VPC1: ['ip 10.0.0.2/24 10.0.0.1'] }; },
  hint: function (p) { return 'Необязательная подсказка'; } }
```
Можно настроить устройства заранее (как в T.1): в `build` вызовите `EL.labs.apply(net, { SW1: [...команды...] })`.

Сборка и проверка:
```
python decks/_elab_build.py
```
Скрипт проверяет синтаксис, прогоняет `node decks/_elab/test.js` (решение каждой лабы и каждого задания на 12 случайных вариантах должно засчитываться) и пишет `decks/eltex-cli.html`.

Новые команды MES добавляются в `decks/_elab/mesx.js` через `E.cmd('режимы', 'шаблон <n> <w> <ip>', function (st, args) {...})`, команды ESR — в `decks/_elab/esr.js`. Движок MES (`decks/_dk_cli.js`) общий с тренажёрами дек «Базовая настройка» и «VLAN».

## Что дальше (по лабам NTF2)
6.x DHCP/relay/NAT/NTP, 7.1 ACL, 8.x RSTP/LACP/VRRP, 10.x LLDP/syslog/SPAN/TFTP, экзаменационный вариант.
