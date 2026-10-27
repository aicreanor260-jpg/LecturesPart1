# Сетевая лаборатория Eltex — мини-мануал

`eltex-cli.html` — лёгкий эмулятор сети для лабораторных NTF2: коммутаторы **MES** (CLI MES24xx, ПО 10.4), маршрутизатор **ESR** (CLI ESR), компьютеры **VPC** и **Debian**. Один HTML-файл, работает офлайн в любом браузере, без виртуальных машин. Это модель поведения по документации Eltex, а не прошивка.

## Запуск
- Откройте `decks/eltex-cli.html` в браузере (двойной щелчок) или по ссылке с хаба `index.html`.
- Для группы: положите файл на любой веб-сервер (nginx на Debian) или в общую папку. Сервер ничего не считает — всё работает в браузере студента.

## Два режима: «Работа» и «Тест» (переключатель в шапке)
**Работа** (по умолчанию) — как на настоящем оборудовании, ничего лишнего:
- левая панель: «Устройства» и «Лабы»; лаба открывает готовую схему и окно с текстом задания — без автопроверки, подсказок и решения;
- вход в консоль как на железе: MES — `User Name:` / `Password:` (заводской admin / admin или `username` из конфигурации), ESR — `login:` / `Password:` (admin / password), Debian — root / toor; после перезагрузки — снова вход;
- только сообщения устройства: `% Unrecognized command`, `% Incomplete command`, `% Invalid input detected at '^' marker.` (MES), `Syntax error: Unknown command | Incomplete command | Illegal parameter` (ESR) — подсказок эмулятора на русском нет;
- клавиши консоли: ↑ ↓ — история, ← → / Home / End — по строке, Backspace / Delete, Tab — дописать, `?` — подсказка, **Ctrl+Z** — выход в `#`;
- таблицы смотрят только командами (`show mac address-table`, `show arp`, `show ip route` …); время идёт как на железе (MAC стареют, OSPF ждёт выбора DR), часов и пути пакета нет.

**Тест** — учебные инструменты: окно «Таблицы», путь пакета по шагам, часы с ускорением и «промотать», автопроверка лаб, «Новый вариант», «Решение», случайные задания, файл схемы, справка.

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

## Маршрутизаторы ESR — вся линейка с eltex.ru
В панели «Устройства» → «Маршрутизаторы ESR»: vESR (4 × gi, как в pnetlab) и 27 аппаратных моделей — ESR-10, 12V, 12VF, 14VF, 15, 15R, 15R-4G, 15VF, 20, 21, 30, 31, 100, 200, 1000, 1200, 1500, 1511, 1511 rev.B, 1700, 3100, 3150, 3200, 3200L, 3250, 3300, 3350. Порты — из таблицы характеристик страницы модели на eltex.ru (Combo считается gi); снятые с производства помечены. CLI у всех один — ESR (справочник 1.23), отличаются только порты.

| Порт | Полное имя в CLI | Приглашение |
|---|---|---|
| gi1/0/N — 1G | `interface gigabitethernet 1/0/N` | `esr(config-if-gi)#` |
| te1/0/N — 10G | `interface tengigabitethernet 1/0/N` | `esr(config-if-te)#` |
| twe1/0/N — 25G | `interface twentyfivegigabitethernet 1/0/N` | `esr(config-if-twe)#` |
| fo1/0/N — 40G | `interface fourtygigabitethernet 1/0/N` (так в CLI ESR) | `esr(config-if-fo)#` |
| hu1/0/N — 100G | `interface hundredgigabitethernet 1/0/N` | `esr(config-if-hu)#` |

Диапазоны и списки: `interface gi1/0/1-4`, `interface gi1/0/1-2,te1/0/1`. Пример: ESR-1000 — gi1/0/1–24 и te1/0/1–2; ESR-3300 — twe1/0/1–4 и hu1/0/1–4. Вход: admin / password, имя по умолчанию `esr` (у vESR — `vesr`).
Чего нет: голосовых портов FXS/FXO, E1, USB, LTE-модема (ESR-15R-4G) — только Ethernet.

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

### Живая консоль: фильтры, страницы, сообщения, счётчики
Работает в обоих режимах — это поведение устройства.

| Что | MES | ESR | Откуда |
|---|---|---|---|
| Фильтр вывода | `show running-config \| include vlan`, `\| exclude`, `\| begin`, `\| section 1/0/3` (до `exit`), `\| section "s" "конец"`, `\| section "s" include "s2"`, `\| no-more`; регистр не учитывается | `\| include "^gi1/0/1 "`, `\| exclude`, `\| begin`, `\| until`, `\| count`, `\| counter`; шаблон — регулярное выражение | ESR: справочник 1.23 «фильтрация»; MES: руководство 8.4.0.7 гл. 6.2. В руководствах 10.4.6 и 6.6.8.8 фильтры не описаны — ветки 10 и 6 работают как 8.4 |
| Постраничный вывод | 24 строки, строка `More: <space>,  Quit: q or CTRL+Z, One line: <return>` (10, 6), `--More-- or (q)uit` (8); `terminal datadump` / `terminal no datadump` (10, 6), `terminal length N` (8) | 24 строки, `More? Enter – next line; Space – next page; Q – quit; R – show the rest.`; `terminal datadump` / `no terminal datadump` | строки «More» — дословно из руководств; для ветки 10 команд нет в 10.4.6 — сделано как в 6.6.8.8 |
| Сообщения в консоль | 10.x: `CFA-6-Interface gi 1/0/1 link status UP`, `CFA-4-… DOWN`, `AST-6-[Instance 0] Interface gi 1/0/2 is moved to state Forwarding`, `AST-6-… This is the root bridge`, `AST-6-BPDU received on Bpdu Guard enabled edge …`; 6.x: `%LINK-I-Up:  gi1/0/1`, `%LINK-W-Down:  gi1/0/1`, `%STP-W-PORTSTATUS: …` | `%LINK-I-Up:  gi1/0/1`, `%LINK-W-Down:  …`, `%OSPF-I-NEIGHBOR: Neighbor 2.2.2.2 on gi1/0/1 changed state to Full`, `%VRRP-I-STATE: gi1/0/1 VRID 1 changed state to Master` | 10.x — «Руководство по сообщениям Syslog MES14xx/24xx/3400/37xx»; **6.x и ESR — формат условный** (в руководствах не приведён) |
| Журнал | `show logging` (буфер 200 строк, новые сверху), `logging console` / `no logging console` | `syslog console` / `no syslog console`; сообщения уходят и на удалённый syslog-сервер (`syslog host`) | |
| Счётчики | `show interfaces counters [gi1/0/1]` (таблицы In/Out Ucast/Mcast/Bcast/Octets, у одного порта — список ошибок), `show interfaces gi1/0/1`, `clear counters [gi1/0/1]` | `show interfaces counters [gi1/0/1]`, `clear interfaces counters [gi1/0/1]` | форматы таблиц — из 6.6.8.8 и ESR 1.23; сводка `show interfaces gi1/0/1` в руководствах не приведена — упрощена |

События: включили/выключили кабель, `shutdown`/`no shutdown`, выключили или перезагрузили соседа, сменилась роль порта STP, соседство OSPF дошло до Full или пропало, сменился мастер VRRP. Сообщение появляется в консоли устройства сразу (OSPF — по таймерам). Счётчики считают каждый кадр модели: ARP-запрос — broadcast на каждом сегменте, ARP-ответ и IP — unicast по пути, BPDU — multicast раз в 2 с с назначенного порта STP. Размеры кадров условные (ARP 64, ICMP 102, TCP 78, UDP 110 байт, +4 с тегом 802.1Q). Перезагрузка обнуляет счётчики, журнал и настройки сессии (`terminal datadump`).

Не сделано: `terminal monitor` (нет в руководствах MES 10.4.6/6.6.8.8 и ESR 1.23), `dir`/`boot system` (вывод в руководствах не приведён).

### Учебные инструменты режима «Тест»

| Инструмент | Как | Что видно |
|---|---|---|
| Захват трафика (как Wireshark в pnetlab) | ПКМ по кабелю → «Захват трафика» | окно со списком кадров на этом кабеле: No., время модели, Src/Dst MAC, VLAN (тег 802.1Q на этом кабеле), тип (ARP / IPv4 / STP), Src/Dst IP, протокол, длина, Info; фильтр `icmp`, `arp`, `!stp`, `192.168.1.10`, `vlan 10` (через запятую — «и»); пауза, очистить. Щелчок по кадру — разбор по уровням: Frame → Ethernet II → 802.1Q → ARP \| IPv4 → ICMP \| TCP \| UDP → DHCP/NTP/Syslog/TFTP; BPDU — 802.3 + LLC + STP (Root/Bridge ID, стоимость). Захват идёт, пока окно открыто |
| Разбор шага трассы (как Simulation в Packet Tracer) | любой ping в «Тесте» → панель трассы внизу | под текстом шага — уровни кадра этого шага (L2 Ethernet/802.1Q, L3 ARP/IPv4/ICMP, L4 TCP/UDP), на каких сегментах тег VLAN; «Разбор подробно» — все поля |
| Редактор лабы без кода | «Лабы» → «Редактор лабы» | соберите схему на поле, впишите название, цель, задания по строке; строка может заканчиваться проверкой `{ping PC1 192.168.1.1}` или `{http PC1 10.0.0.5}`. «Сохранить лабу (.json)» — файл со схемой, заметками и заданием. Студент: «Лабы» → «Открыть лабу (.json)» — схема и окно задания (в «Работе» — только текст, в «Тесте» — кнопка «Проверить») |
| Заметки на схеме | ПКМ по пустому полю → «Заметка здесь»; перетаскивание; двойной щелчок/ПКМ — изменить или удалить | подписи сетей, VLAN, адресов; сохраняются в файле схемы и видны в «Работе» |
| Отмена на поле | Ctrl+Z (фокус не в консоли) | отменяет добавление/удаление устройства (возвращает его с конфигурацией и кабелями), кабель, перемещение, заметки — до 50 шагов; настройки, сделанные командами, не откатываются |
| Конфигурации текстом | ПКМ по устройству → «Конфигурация текстом…»; «Файл» → «Экспорт всех (.txt)» / «Импорт (.txt)» | running-config MES/ESR: копировать, сохранить, отредактировать и «Применить» (как вставка в консоль: `configure` … `end`, на ESR ещё `commit` + `confirm`). Файл всех конфигураций — блоки `! ==== SW1 (MES2428) ====`; импорт применяет блок к устройству с тем же именем. Пароль ESR из `password encrypted …` переносится хешем — вход по прежнему паролю |

Модель: в каждый шаг трассы записан кадр (MAC, IP, TTL = 64 минус пройденные маршрутизаторы, порты — у клиента TCP/UDP эфемерный 49152+). Обмен TCP показан парой SYN / SYN,ACK — данные и закрытие соединения не моделируются. Время в захвате — модельное (часы в шапке).



### IPv6 (справочник ESR-Series CLI 1.23)

| Устройство | Команды |
|---|---|
| ESR | `interface gi1/0/1` → `ipv6 address 2001:db8:1::1/64` (до 8 адресов, через запятую), `ipv6 enable` (только link-local), `no ipv6 address X/len\|all`; `ipv6 route ::/0 fc00::1`, `ipv6 route 2001:b::/64 fc00::2 [метрика]`; `show ipv6 interfaces`, `show ipv6 route`, `show ipv6 neighbors`, `clear ipv6 neighbors`, `ping 2001:db8::10` |
| ESR, RIPng | `ipv6 router rip` → `(config-ripng)#` `network 2001::/16`, `redistribute connected`, `enable`; `show ipv6 rip` |
| ESR, OSPFv3 | `ipv6 router ospf 1` → `router-id 1.1.1.1`, `area 0.0.0.0` → `enable`, `exit`, `enable`; на интерфейсе `ipv6 ospf instance 1`, `ipv6 ospf area 0.0.0.0`, `ipv6 ospf`; `show ipv6 ospf neighbors` |
| VPC | `ip 2001:db8:1::10/64 2001:db8:1::1` (адрес и шлюз), `show ipv6`, `clear ipv6`, `ping 2001:db8:1::1` |
| Debian | `ip -6 addr add 2001:db8:2::20/64 dev ens3`, `ip -6 route add default via 2001:db8:2::1`, `ip -6 addr`, `ip -6 route`, `ip -6 neigh`, `ping -6 X` / `ping6 X` / `ping X::Y` |
| MES | IPv6-кадры коммутируются как обычные (L2), MAC-таблица учится |

Как работает: у каждого IPv6-интерфейса есть link-local fe80::/64 из MAC (EUI-64). Перед отправкой — Neighbor Solicitation на solicited-node адрес `ff02::1:ffXX:XXXX` (MAC `33:33:ff:XX:XX:XX`, кадр multicast), ответ — Neighbor Advertisement; запись появляется в `show ipv6 neighbors`. В трассе и захвате — шаги NS/NA/ICMPv6 Echo с Hop Limit, разбор IPv6 (Next Header 58) и ICMPv6 (типы 128/129/135/136). RIPng и OSPFv3: соседи — ESR в одном сегменте с адресами из одной IPv6-сети, next-hop — link-local соседа.

Упрощения: межсетевой экран ESR к IPv6 не применяется; нет RA/SLAAC и DHCPv6 (адреса и шлюз задаются вручную); записи ND не стареют; RIPng и OSPFv3 сходятся сразу (таймеры не моделируются), одна область, стоимость интерфейса 10; IPv6 на SVI MES не поддерживается.

### DNS

| Где | Команды |
|---|---|
| Сервер — Debian-server (BIND9) | зона в `/etc/bind/named.conf.local`: `zone "lab.local" { type master; file "/etc/bind/db.lab.local"; };`, файл зоны с записями `www IN A 10.0.0.53`, `ftp IN CNAME www` (SOA/NS/$TTL/$ORIGIN понимаются); `nano` для правки, `systemctl restart bind9` — загрузить зоны, `named-checkzone lab.local /etc/bind/db.lab.local` |
| Debian-клиент | `/etc/resolv.conf`: `nameserver 10.0.0.53`, `search lab.local`; `/etc/hosts` проверяется раньше DNS; `nslookup www.lab.local [сервер]`, `ping www.lab.local`, `curl http://www.lab.local/` |
| VPC | `ip dns 10.0.0.53`, `ping www.lab.local` («… resolved to …»), DNS в `show` |
| ESR | `domain lookup enable`, `domain name-server 10.0.0.53`, `domain name lab.local`, `domain ip host gw.lab.local 10.0.0.1`; `ping www.lab.local` |
| MES 10.x | `ip name-server ipv4 10.0.0.53` (руководство 10.4.6), `ping имя` |
| MES 6.x | `ip domain lookup`, `ip name-server 10.0.0.53`, `ip domain name lab.local`, `ip host printer 10.0.0.77` (6.6.8.8), `ping имя` |

Запрос — UDP 53 по сети к серверу (виден в трассе: ARP, запрос, ответ; в захвате — `Standard query A …` / `Standard query response …`). Ответы — `NXDOMAIN`, если имени нет в зоне, и «no servers could be reached», если сервер недоступен или bind9 остановлен. Поддерживаются записи A и CNAME; AAAA, PTR и рекурсия во внешний интернет не моделируются.

### GRE-туннели ESR (справочник ESR-Series CLI 1.23)
```
tunnel gre 1
  local address 100.0.0.2
  remote address 100.0.1.2
  ip address 10.10.10.1/30
  ip firewall disable          (или security-zone …)
  enable
exit
ip route 192.168.2.0/24 10.10.10.2
```
`show tunnels status` — Admin state, MTU 1476, Local/Remote IP. В режиме `(config-gre)#` есть `ip address`, `ip firewall disable`, `security-zone`, `description`, `local address`, `remote address`, `enable`.
Пакет, ушедший в туннель, инкапсулируется: внешний IPv4 local → remote, протокол 47 — и идёт через сеть провайдера как обычный (ARP, маршруты, межсетевой экран на пути). На удалённом ESR нужен зеркальный включённый туннель (local/remote наоборот), иначе GRE отбрасывается; межсетевой экран туннельного интерфейса проверяется как у обычного. В трассе — шаги «инкапсулирован в GRE» и «GRE снят», в захвате у провайдера — внешний заголовок 100.0.0.2 → 100.0.1.2 и внутри ICMP (разбор: IPv4 proto 47 → GRE → ↳ внутренний IPv4 → ICMP).
Упрощения: keepalive нет (туннель Up, когда включён и задан); RIP/OSPF через туннель соседство не строят — маршруты в туннель статические; MTU/фрагментация не моделируются. L2TP, BGP, VRF, PBR, BFD — пока нет.

### IPsec VPN на ESR (справочник ESR-Series CLI 1.23, «Управление VPN»)
```
security ike proposal P1            encryption algorithm aes128 · authentication algorithm sha1 · dh-group 2   (по умолчанию 3des / sha1 / 1)
security ike policy POL             pre-shared-key ascii-text Secret123 · proposal P1
security ike gateway GW             ike-policy POL · local address 100.0.0.2 · remote address 100.0.1.2
                                    mode policy-based · local network 192.168.1.0/24 · remote network 192.168.2.0/24
                                    (или mode route-based · bind-interface vti 1)
security ipsec proposal IP1         encryption algorithm aes128 · authentication algorithm sha1                 (по умолчанию 3des / sha1)
security ipsec policy IPOL          proposal IP1
security ipsec vpn VPN              ike establish-tunnel immediate · ike gateway GW · ike ipsec-policy IPOL · enable
tunnel vti 1                        local address · remote address · ip address 10.0.9.1/30 · ip firewall disable · enable   (route-based + ip route СЕТЬ 10.0.9.2)
```
`show security ipsec vpn status` — Established / Down (`show security ipsec vpn status VPN` — в «Тесте» с причиной).
SA устанавливается, когда у пары ESR зеркальные шлюзы (local ↔ remote), одинаковые ключ, IKE proposal (шифрование/аутентификация/DH), IPsec proposal, режим, зеркальные подсети политик, хотя бы одна сторона не `by-request` — и IKE (UDP 500) проходит по сети, в том числе через межсетевой экран самих ESR. Трафик политики (policy-based) или маршрута в VTI (route-based) уходит ESP (протокол 50); у провайдера в захвате видны только ESP 100.0.0.2 ↔ 100.0.1.2 и ISAKMP, внутренних адресов не видно. В трассе: «зашифрован в ESP», «ESP расшифрован» или причина, почему SA нет.
Упрощения: IKEv1/v2 не различаются, lifetime/rekey/DPD/NAT-T не моделируются, ключ в running-config показывается хешем.

В режиме «Работа» подсказка `?` показывает команды без русских описаний (раньше строки с описаниями пропадали).

### Сценарии «Найди неисправность»
| Лаба | Схема | Возможные неисправности (одна случайная) |
|---|---|---|
| T.1 | два MES + Router-on-a-Stick | порт не в той VLAN, VLAN не разрешена на trunk, номер саб-интерфейса ≠ VLAN, межсетевой экран на саб-интерфейсе, неверный шлюз ПК, выключен trunk |
| T.2 | VPC1 — SW1 — R1 — R2 — SRV, статические маршруты | next-hop не из подключённой сети, нет обратного маршрута, межсетевой экран на R2, неверный шлюз VPC1, выключен интерфейс R2, адреса R1/R2 в разных сетях |
| T.3 | VPC1 — SW1 — R1 — SRV (BIND9, зона lab.local) | VPC1 указывает не тот DNS-сервер, bind9 остановлен, в зоне неверный адрес www, опечатка в имени зоны (NXDOMAIN), межсетевой экран на R1, у SRV нет шлюза (ответ DNS не возвращается) |

В «Тесте» — кнопка «Подсказка» с направлением поиска и «Решение». На Debian добавлен `sed -i s/было/стало/ файл` (правка конфигурации одной строкой).

Варианты экзамена: в архиве NTF2 (`Labs_1.24.2.zip`) есть только топологии Final Exam 1–3 и текст «Вариант 1» — они уже в эмуляторе (E.1–E.3). Других вариантов в исходниках нет.

### Методичка лабы (PDF курса)
В окне лабы (оба режима) — кнопка «Методичка»: открывает PDF лабораторной `labs/<номер>.pdf` (например `labs/4.1.pdf`, экзамен — `labs/E.1.pdf`) во встроенном просмотре браузера, рядом со схемой эмулятора, плюс «Открыть в новой вкладке». Методички Eltex NTF2 лежат только на сайте курса (net-cat.duckdns.org, за кодом доступа) — в публичный репозиторий и в HTML не входят (`decks/labs/` в `.gitignore`). Если файла нет (офлайн-файл, GitHub Pages) — строка «Методичка доступна на сайте курса net-cat.duckdns.org». Схема эмулятора и PDF могут расходиться в адресах и устройствах — эмулятор генерирует свой вариант.

### Физика: кабели, трансиверы, скорость и дуплекс
- **Кабель** выбирается при прокладке (окно «Новый кабель» → «Кабель / модуль»): медь RJ-45, оптика SFP 1G, оптика SFP+ 10G; «Авто» — медь, между портами 10G — SFP+. Тип кабеля сохраняется в файле схемы. В «Тесте» ПКМ по кабелю показывает тип, скорость, дуплекс сторон или причину, почему линка нет.
- **Совместимость:** оптический модуль в медный порт gi — нет линка; SFP+ 10G между портами, один из которых 1G, — нет линка; медь в порт SFP+ — через медный модуль, 1G.
- **MES** (10.4.6, 6.6.8.8): `negotiation` / `no negotiation` (по умолчанию включено), `speed 10|100|1000|10000`, `duplex full|half` — действуют при выключенном автосогласовании; `show interfaces status` — формат руководства 6.6.8.8 (Type, Duplex, Speed, Neg, Link State).
- **ESR** (1.23): `speed 100M full-duplex | half-duplex`, `speed auto`, `no speed`.
- **Согласование:** обе стороны auto — максимум общей скорости, full; одна сторона принудительно, другая auto — auto-сторона берёт скорость, но **half-duplex** (как в 802.3); обе принудительно с разной скоростью — линка нет; 1000 по меди без автосогласования с auto-соседом — линка нет; на оптике скорость — только скорость модуля.
- **Несовпадение дуплекса:** линк есть, ping проходит, но каждый кадр по такому кабелю — FCS-ошибка на full-стороне и поздняя коллизия на half-стороне (`show interfaces counters gi1/0/1`: FCS Errors, Late Collisions; ESR — Receive errors / Collisions). Кадры не теряются — потери в модели не считаются.

### Защита L2 на MES (руководства 10.4.6 и 6.6.8.8)
| Функция | MES 10.x | MES 6.x | Что происходит |
|---|---|---|---|
| DHCP snooping | `ip dhcp snooping`, `ip dhcp snooping vlan 10`; доверенный порт — `port-security-state trusted` (+ `set port-role uplink`) | `ip dhcp snooping`, `… vlan 10`, на порту `ip dhcp snooping trust` | ответ DHCP-сервера с недоверенного порта отброшен (чужой сервер не раздаёт адреса); выданные адреса — в `show ip dhcp snooping binding` |
| ARP inspection | `ip arp inspection enable`, `ip arp inspection vlan 10` (доверенный — тот же `port-security-state trusted`) | `ip arp inspection`, `… vlan 10`, на порту `ip arp inspection trust` | ARP с недоверенного порта проходит, только если пара IP–MAC есть в базе DHCP snooping: ПК со статическим адресом и порт к маршрутизатору без trusted — ARP отброшен |
| Storm-control | `storm-control broadcast level N`, `storm-control broadcast action shutdown` | `storm-control broadcast level N` | широковещательный шторм (петля без STP) выключает порт с action shutdown (err-disable) — петля разорвана, следующий ping проходит; включить порт — `no shutdown` |

Показ: `show ip dhcp snooping`, `show ip dhcp snooping binding`, `show ip arp inspection`. Упрощения: опция 82, verify mac-address, IP source guard и пороги pps/kbps не моделируются (шторм либо есть, либо нет); формат `show ip dhcp snooping binding` в руководствах не приведён.

### Сдача работ на сайт курса (net-cat)
- **Студент** (режим «Работа»): в окне лабы — «Сдать работу» → ФИО и группа → «Отправить на сайт курса». Уходит схема со всеми настройками (как «Файл → Сохранить»), running-config всех MES/ESR текстом и вариант встроенной лабы. Без сети или из файла с диска — «Сохранить для сдачи (.json)»: файл сдаётся преподавателю как угодно.
- **Преподаватель:** `teacher.html` на сайте курса → пароль преподавателя → список сдач (фильтр по группе, лабе, ФИО), конфигурации текстом, «Скачать .json», «Открыть в эмуляторе (проверка)» — эмулятор открывается в новой вкладке в режиме «Тест» со схемой студента и тем же вариантом лабы: работают автопроверки, «Таблицы», трасса. Файл сдачи (.json) открывается и через «Файл → Открыть файл».
- **Сервер:** сервис на Python (только стандартная библиотека) за Caddy, только для вошедших по коду курса; пишет `~/net-cat/submissions/<группа>/<лаба>/<ФИО>-<время>.json`; лимит 2 МБ и частоты; пароль преподавателя — в файле на сервере. Код сервиса в репозиторий не входит.

### QinQ на MES 6.x (руководство 6.6.8.8)
`interface gi1/0/1` → `switchport mode customer`, `switchport customer vlan 100` — клиентский порт: любой кадр клиента (с тегом или без) попадает в S-VLAN 100, тег клиента сохраняется внутри. По trunk провайдера (`switchport trunk allowed vlan add 100`) кадр идёт с двумя тегами; на клиентском порту другой стороны S-тег снимается и клиент получает кадр со своим тегом. В захвате на trunk — VLAN `100/10` и два заголовка 802.1Q (S-VLAN и C-VLAN); в трассе — тег S-VLAN. У разных S-VLAN на концах — связи нет. В руководстве 10.4.6 есть только Selective Q-in-Q — для ветки 10 не моделируется.

### MSTP-экземпляры на MES (руководства 10.4.6 и 6.6.8.8)
`spanning-tree mode mst`, затем `spanning-tree mst configuration` → `(config-mst)#`: `instance 1 vlan 10`, `instance 2 vlan 20`, `name LAB`, `revision 1`, `exit`; `spanning-tree mst 1 priority 4096` (кратно 4096); на порту `spanning-tree mst 2 cost 200000`, `spanning-tree mst 2 port-priority 64`. Показ: `show spanning-tree mst 2`, `show spanning-tree mst configuration`.
У каждого экземпляра своё дерево — свой корень и свои заблокированные порты, поэтому VLAN разных экземпляров могут идти по разным линкам (балансировка); трасса показывает, в каком MSTI заблокирован порт. VLAN без экземпляра идут по CIST (обычные `spanning-tree priority`/`cost`). Упрощение: имя, ревизия и привязки региона на разных коммутаторах не сравниваются — все коммутаторы считаются одним регионом.

### VRF на ESR (справочник ESR-Series CLI 1.23)
`ip vrf RED` → `(config-vrf)#` (`description`), `exit`; на интерфейсе (gi, саб-интерфейс, loopback, gre, vti) `ip vrf forwarding RED`; `ip route vrf RED 172.16.0.0/16 192.168.5.2`; показ — `show ip route vrf RED`, `show ip vrf`; `ping vrf RED 10.0.3.10`.
У каждого VRF своя таблица маршрутов: пакет, пришедший на интерфейс VRF, ищет маршрут только среди сетей этого VRF, ответ маршрутизатора уходит в VRF интерфейса, получившего запрос. Одинаковые сети в разных VRF допустимы (проверка пересечения адресов — внутри VRF), ARP-записи разных VRF не путаются. `show ip route` без vrf показывает глобальную таблицу.
Упрощения: RIP/OSPF/BGP только в глобальной таблице, утечки маршрутов между VRF нет, межсетевой экран и NAT от VRF не зависят.

### Перезагрузка и таймер commit
- **MES:** `reload` (из `#`) спрашивает `… Do you want to continue (y/n) [n]?` (руководство 6.6.8.8): `y` — перезагрузка, загружается startup-config (`write` перед этим, иначе несохранённое пропадёт); любой другой ответ — отмена. Также ПКМ по устройству → «Перезагрузить».
- **ESR:** `reload system` — сразу; `reload system in 5` или `in 1:30` (через минуты / ЧЧ:ММ), `reload system at 13:02:02 10 august 2026`; `reload cancel`; `show system reload` → `System reload is scheduled for 13:02:02 10 August 2026`. Отсчёт идёт по модельному времени (часы в шапке, «⏩ 5 мин» ускоряет).
- **Таймер commit на ESR:** `commit` применяет конфигурацию и запускает таймер 600 с; без `confirm` по его истечении конфигурация возвращается к последней подтверждённой (в консоли — сообщение об откате, текст условный), а перезагрузка до `confirm` загружает последнюю подтверждённую. С `confirm` всё сохраняется.

### PBR — маршрутизация по политике на ESR (справочник 1.23)
```
ip access-list extended FROM-VPC2 → rule 10 → action permit, match source-address address-range 192.168.1.20-192.168.1.20, enable
route-map VIA-ISP2 → rule 10 → match ip access-group FROM-VPC2, action set ip next-hop 100.2.0.1, enable
interface gi1/0/3 → ip policy route-map VIA-ISP2
```
Пакет, пришедший на интерфейс с политикой и разрешённый ACL правила, уходит на next-hop правила мимо таблицы маршрутов (в трассе — «политика VIA-ISP2 (rule 10, ACL …)»). `action deny` или ни одно правило не подошло — обычная маршрутизация; next-hop не в подключённой сети — тоже обычная. Route-map в RIP/OSPF/BGP (фильтрация маршрутов) не моделируется.

## Известные ограничения модели

Эмулятор моделирует **логику** сети (кто кому ответит и почему), а не поток битов. Отсюда:

- **Обмен считается целиком.** Ping, curl, DNS-запрос, IKE — это одна пара «запрос + ответ», рассчитанная мгновенно; пять строк ping — один и тот же результат. Нет очередей, задержек на линках, джиттера, «первый ping теряется на ARP» не воспроизводится (ARP-запрос просто показывается отдельным шагом).
- **MTU и фрагментации нет.** Размер пакета в модели не участвует: `ping -s 2000`, Don't Fragment, Path MTU Discovery, MTU туннеля (`show tunnels status` пишет 1476 — для справки) на доставку не влияют. Цена честной модели — размер пакета в каждом шаге трассы, MTU на каждом интерфейсе (ESR, MES, хосты), фрагментация/сборка и ICMP «Fragmentation needed» на каждом маршрутизаторе, разбор фрагментов в захвате; лабы NTF-2 этого не требуют, поэтому сделано ограничением.
- **Потерь нет.** Перегрузка канала не моделируется; несовпадение дуплекса даёт ошибки в счётчиках, но кадры доходят.
- **Протоколы маршрутизации IPv4 (RIP, OSPF)** идут по реальным таймерам; **RIPng, OSPFv3** сходятся сразу; через туннели GRE/VTI соседства не строятся.
- **Межсетевой экран ESR** к IPv6 не применяется; NAT-T, DPD, rekey IPsec нет.
- **Не моделируются:** L2TP, BGP, BFD; на MES — 802.1X, IGMP snooping, стек, Selective Q-in-Q, MSTP-регионы; IPv6 на SVI MES; RA/SLAAC, DHCPv6.

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
