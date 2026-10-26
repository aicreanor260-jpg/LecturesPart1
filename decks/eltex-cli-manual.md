# Сетевая лаборатория Eltex — мини-мануал

`eltex-cli.html` — лёгкий эмулятор сети для лабораторных NTF2: коммутаторы **MES** (CLI MES24xx, ПО 10.4), маршрутизатор **ESR** (CLI ESR), компьютеры **VPC** и **Debian**. Один HTML-файл, работает офлайн в любом браузере, без виртуальных машин. Это модель поведения по документации Eltex, а не прошивка.

## Запуск
- Откройте `decks/eltex-cli.html` в браузере (двойной щелчок) или по ссылке с хаба `index.html`.
- Для группы: положите файл на любой веб-сервер (nginx на Debian) или в общую папку. Сервер ничего не считает — всё работает в браузере студента.

## Интерфейс
| Где | Что |
|---|---|
| Палитра слева | MES2428, MES2428B, vESR, VPC, Debian — щелчок добавляет устройство |
| **Кабель** | щёлкните устройство → порт → второе устройство → порт |
| **Удалить** / Delete | удалить выбранное устройство или кабель |
| Щелчок по устройству | консоль справа; вкладки — открытые консоли |
| **ping** в панели | отправить ping и посмотреть путь пакета |
| Полоса внизу схемы | пошаговое объяснение: ARP-рассылка, ARP-ответ, IP-пакет, теги VLAN, где и почему кадр отброшен |
| **Лабораторные** | 2.1, 3.1, 4.1, 4.2 и T.1 (поиск неисправности): случайный вариант, проверка после каждой команды, решение, подсказка |
| **Задания** | случайные задачи «Базовая настройка» и «VLAN» на один коммутатор (как в тренажёрах дек) |
| **Сохранить / Открыть** | схема со всеми настройками в файл `.json` |

В консоли: `?` — варианты следующего слова, `Tab` — дописать, `↑ ↓` — история. Сокращения: `conf t`, `int gi1/0/1`, `sh vl`.

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
show running-config | startup-config | vlan | interfaces switchport gi1/0/1
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
ip route 10.0.0.0/8 192.168.1.2
do commit    do confirm    rollback    show candidate-config
show running-config | ip interfaces | ip route | interfaces status | users    ping    traceroute
```
**VPC:** `ip 10.0.0.2/24 10.0.0.1`, `show`, `ping`, `trace`, `arp`, `clear ip`.
**Debian** (вход `root`/`toor`): `ip a`, `ip link set ens3 up`, `ip addr add 192.168.100.2/24 dev ens3`, `ip route add default via 192.168.100.1`, `nano /etc/network/interfaces` + `ifdown ens3`/`ifup ens3`, `cat`, `ping`, `traceroute`, `ssh master@192.168.100.1`.

## Типовые ошибки
| Сообщение | Что делать |
|---|---|
| `% Unrecognized command` | опечатка или команды нет — нажмите `?` |
| `% Incomplete command` | команда не дописана (`show` → `show vlan`) |
| `% Команда недоступна в этом режиме` | смотрите на приглашение: нужен `#`, `(config)#` или режим интерфейса |
| `% VLAN 30 не создана` | сначала `vlan database` / `vlan 30` |
| ESR не отвечает | нет `commit` или не отключён экран: `ip firewall disable` |
| ARP без ответа | разные VLAN, VLAN не разрешена на транке, нет саб-интерфейса, порт `shutdown` — шаги трассы показывают точку отбрасывания |

## Как добавить свою лабораторную
Лабы описаны в `decks/_elab/labs.js`, массив `LABS`. Шаблон:
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
4.3 и 5.1 (статика, суммарный и плавающий маршрут), 5.2 RIP, 5.3 OSPF, 6.x DHCP/relay/NAT/NTP, 7.1 ACL, 8.x RSTP/LACP/VRRP, 10.x LLDP/syslog/SPAN/TFTP, экзаменационный вариант.
