# -*- coding: utf-8 -*-
"""Дека RIP 2.5.1, слайды pptx 22–33: настройка на ESR. Команды и выводы консоли — дословно;
скриншоты консоли перерисованы терминалом построчно."""

from _sw_lib import slide, head, sc, grow, col, p, li, step
from _rp1_canvas import card
from _dk_kit import pslide, term
from _rp1_deck import conf, txt, info
import _rp1_fig2 as G

S23 = ["ESR# config", "ESR(config)# router rip", "ESR(config-rip)#",
       "  authentication     Configure RIP router authentication",
       "  do                 Execute a privileged mode command",
       "  enable             Enable RIP routing process",
       "  end                Return to the root view",
       "  exit               Exit to the next highest mode in the CLI mode hierarchy",
       "  help               Show an overview of the CLI syntax",
       "  network            Add network for advertise",
       "  no                 Negate command",
       "  passive-interface  Disable sending routing updates on an interface",
       "  prefix-list        Configure prefix list",
       "  redistribute       Configure RIP redistributing",
       "  route-map          Configure route-map",
       "  timers             Configure RIP timers"]

S24A = ["ESR(config-if-gi)# ip rip metric", "  1-15  distance metric for RIP routes",
        "ESR(config-if-gi)# ip rip neighbor", "  A.B.C.D  RIP neighbor address", "",
        "ESR(config-if-gi)# ip rip summary-address", "  A.B.C.D/N  RIP network prefix", "",
        "ESR(config-if-gi)# ip rip mode", "  MODE  Select RIP mode:", "        multicast", "        broadcast", "        unicast"]

S24B = ["ESR# config", "ESR(config)# interface gigabitethernet 1/0/1", "ESR(config-if-gi)#",
        "  bridge-group        Add interface to bridge",
        "  channel-group       Add interface to port channel",
        "  description         Configure interface specific description",
        "  do                  Execute a privileged mode command",
        "  end                 Return to the root view",
        "  exit                Exit to the next highest mode in the CLI mode hierarchy",
        "  help                Show an overview of the CLI syntax",
        "  history             Configure history parameters",
        "  ip                  Configure IP interface parameters",
        "  ipv6                Configure IPv6 interface parameters",
        "  isis                Configure Intermediate System-to-Intermediate System (ISIS)",
        "  lacp                Configure interface IEEE 802.3 link aggregation parameters",
        "  lldp                Configure LLDP protocol",
        "  load-average        Configure the load average period",
        "  location            Configure Location on interface",
        "  mac-address         Configure interface MAC address",
        "  mode                Port mode",
        "  mtu                 Configure interface MTU",
        "  no                  Negate command",
        "  port                Perform switch port configuration",
        "  priority-queue      Configure priority-queues",
        "  qos                 Configure QoS parameters",
        "  rate-limit          Configure the rate-limit interface configuration command to",
        "  rmon                Configure Remote Monitoring",
        "  security-zone       Bind a security zone",
        "  service-acl         Configure access list",
        "  service-policy      Configure service-policy parameters",
        "  service-voip        Configure VoIP parameters",
        "  shutdown            Shutdown the selected interface",
        "  snmp                Modify SNMP interface parameters",
        "  speed               Configure the transmit and receive speeds",
        "  subscriber-control  Configure subscriber control parameters",
        "  switchport          Configure switch port parameters",
        "  threshold           Configure alarms thresholds parameters",
        "  traffic-shape       Configure shaper on an egress port",
        "  vrrp                Enable VRRP on interface",
        "  wan                 Configure WAN"]

S25 = ["ESR# config", "ESR(config)# router rip", "ESR(config-rip)# network 192.168.10.0/24",
       "ESR(config-rip)# network 192.168.20.0/24", "ESR(config-rip)# redistribute connected",
       "ESR(config-rip)# redistribute static", "ESR(config-rip)# redistribute ospf 123 intra-area",
       "ESR(config-rip)# redistribute ospf 123 external1", "ESR(config-rip)# █"]

S26 = ["ESR#", "ESR# config", "ESR(config)# router rip", "ESR(config-rip)# passive-interface gigabitethernet 1/0/1",
       "ESR(config-rip)# █"]

S28 = ["ESR# config", "ESR(config)# router rip", "ESR(config-rip)# timers",
       "  flush    Configure flush timer", "  invalid  Configure invalid timer", "  update   Configure update timer", "",
       "ESR(config-rip)# timers update", "  12-65535  Time in seconds at which updates are sent", "",
       "ESR(config-rip)# timers invalid", "  12-65535  Time in seconds after which a route is declared invalid", "",
       "ESR(config-rip)# timers flush",
       "  12-65535  Amount of time in seconds that must pass before the route is removed from the routing"]

S29A = ["ESR-3# sh ip route",
        " Codes: C - connected, S - static, R - RIP derived,",
        "        O - OSPF derived, IA - OSPF inter area route,",
        "        E1 - OSPF external type 1 route, E2 - OSPF external type 2 route",
        "        B - BGP derived, D - DHCP derived, K - kernel route, V - VRRP route",
        "        i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area",
        "        * - FIB route", "",
        "R     * 0.0.0.0/0          [100/2]           via 192.168.1.11 on gi1/0/3",
        "rip 01:57:13]",
        "R     * 205.15.1.0/24      [100/2]           multipath",
        "rip 01:55:43]",
        "                              via 172.16.1.10 on gi1/0/1 weight 1",
        "                              via 192.168.1.11 on gi1/0/3 weight 1",
        "C     * 172.16.1.0/24      [0/0]             dev gi1/0/1",
        "direct 09:14:19]",
        "C     * 192.168.1.0/24     [0/0]             dev gi1/0/3",
        "direct 09:14:19]"]
S29B = ["ESR-1# sh run routing rip", "",
        "interface gigabitethernet 1/0/2", "  ip rip metric 5", "  ip rip mode broadcast",
        "  ip rip neighbor 172.16.1.11", "  ip rip summary-address 172.16.1.0/24", "exit",
        "router rip", "  passive-interface gigabitethernet 1/0/1", "  timers update 60", "  timers invalid 90",
        "  timers flush 120", "  network 205.15.1.0/24", "  network 172.16.1.0/24", "  enable", "exit"]
S29C = ["ESR-3# sh ip rip",
        "R     * 0.0.0.0/0          [100/2]           via 192.168.1.11 on gi1/0/3",
        "rip 01:57:13]",
        "R     * 205.15.1.0/24      [100/2]           multipath",
        "rip 01:55:43]",
        "                              via 172.16.1.10 on gi1/0/1 weight 1",
        "                              via 192.168.1.11 on gi1/0/3 weight 1",
        "R       172.16.1.0/24      [100/2]           via 172.16.1.10 on gi1/0/1",
        "rip 01:55:43]",
        "R       192.168.1.0/24     [100/2]           via 192.168.1.11 on gi1/0/3",
        "rip 01:55:13]"]

CFG_RIP_A = ["esr(config)# hostname RIP", "esr(config)# do commit", "RIP(config)# do confirm"]
CFG_RIP_B = ["RIP(config)# ip route 0.0.0.0/0 203.0.113.2"]
CFG_RIP_C = ["RIP(config)# interface gigabitethernet 1/0/1", "RIP(config-if-gi)# ip firewall disable",
             "RIP(config-if-gi)# ip address 198.18.0.1/15", "RIP(config-if-gi)# exit",
             "RIP(config)# interface gigabitethernet 1/0/2", "RIP(config-if-gi)# ip firewall disable",
             "RIP(config-if-gi)# ip address 198.51.100.1/24", "RIP(config-if-gi)# exit",
             "RIP(config)# interface gigabitethernet 1/0/3", "RIP(config-if-gi)# ip firewall disable",
             "RIP(config-if-gi)# ip address 192.168.30.1/24", "RIP(config-if-gi)# exit",
             "RIP(config)# interface gigabitethernet 1/0/4", "RIP(config-if-gi)# ip firewall disable",
             "RIP(config-if-gi)# ip address 203.0.113.1/24", "RIP(config-if-gi)# exit"]
CFG_R1 = ["esr(config)# hostname R1", "esr(config)# do commit", "R1(config)# do confirm",
          "R1(config)# interface gigabitethernet 1/0/1", "R1(config-if-gi)# ip firewall disable",
          "R1(config-if-gi)# ip address 198.51.100.2/24", "R1(config-if-gi)# exit",
          "R1(config)# interface gigabitethernet 1/0/2", "R1(config-if-gi)# ip firewall disable",
          "R1(config-if-gi)# ip address 192.168.10.1/24", "R1(config-if-gi)# exit",
          "R1(config)# router rip", "R1(config-rip)# network 198.51.100. 0/24",
          "R1(config-rip)# passive-interface gigabitethernet 1/0/2", "R1(config-rip)# timers update 15",
          "R1(config-rip)# timers invalid 45", "R1(config-rip)# timers flush 105", "R1(config-rip)# enable",
          "R1# commit", "R1# confirm"]
CFG_R2 = ["esr(config)# hostname R2", "esr(config)# do commit", "R2(config)# do confirm",
          "R2(config)# interface gigabitethernet 1/0/1", "R2(config-if-gi)# ip firewall disable",
          "R2(config-if-gi)# ip address 198.18.0.2/15", "R2(config-if-gi)# exit",
          "R2(config)# interface gigabitethernet 1/0/2", "R2(config-if-gi)# ip firewall disable",
          "R2(config-if-gi)# ip address 192.168.20.1/24", "R2(config-if-gi)# exit",
          "R2(config)# router rip", "R2(config-rip)# network 198.18.0.0/15",
          "R2(config-rip)# passive-interface gigabitethernet1/0/2", "R2(config-rip)# timers update 15",
          "R2(config-rip)# timers invalid 45", "R2(config-rip)# timers flush 105", "R2(config-rip)# enable",
          "R2# commit", "R2# confirm"]


def build():
    TS = "Настройка <em>протокола RIP</em>"
    # ---------------------------------------------------------------- pptx 22
    import _rp1_cv as CV
    CV.setup()
    # ---------------------------------------------------------------- pptx 23
    TP = "Создание и настройка <em>процесса RIP</em>"
    pslide("Создание процесса RIP", TP, [
        txt("Команда <b>router rip</b> включает протокол RIP, команда не запускает работу протокола RIP, но осуществляется "
            "переход в режим конфигурирования маршрутизатора, где выполняется настройка параметров маршрутизации протокола "
            "RIP. Знаком контекстной подсказки «?» в режиме конфигурирования RIP можно посмотреть команды для настройки."),
        txt("Команда <b>no router rip</b> отключает и удаляет протокол RIP, останавливает работу и удаляет все существующие "
            "настройки RIP. Использование «no» перед другими командами, соответственно, может их отключить, отменить или "
            "удалить.", tone="rd"),
        txt("Команда <b>enable</b> в рамках конфигурирования протокола активирует процесс RIP. Есть ряд настроек "
            "аутентификации.", tone="lm")],
        [term(S23)])
    pslide("Аутентификация RIP", TP, [
        card("Определить алгоритм аутентификации протокола RIP (необязательно)",
             conf(["esr(config-rip)# authentication algorithm {cleartext | md5}"], "") + li([
                 "cleartext - пароль, передается открытым текстом;", "md5 - пароль хешируется по алгоритму md5."]), "cy"),
        card("Установить пароль для аутентификации с соседом (необязательно)",
             conf(["esr(config-rip)# authentication key ascii-text { <CLEAR-TEXT> |encrypted <ENCRIPTED-TEXT>}"], "") + li([
                 "&lt;CLEAR-TEXT&gt; - пароль, задаётся строкой от 8 до 16 символов;",
                 "&lt;ENCRIPTED-TEXT&gt; - зашифрованный пароль размером от 8 байт до 16 байт (от 16 до 32 символов) в "
                 "шестнадцатеричном формате (0xYYYY…) или (YYYY…)."], "mg"), "mg")],
        [card("Определить список паролей для аутентификации через алгоритм хеширования md5 (необязательно)",
              conf(["esr(config-rip)# authentication key-chain <KEYCHAIN>"], "") +
              p("&lt;KEYCHAIN&gt; - идентификатор списка ключей, задаётся строкой до 16 символов."), "lm")])
    pslide("Другие команды RIP", TP, [
        card("Другие команды", li([
            "<b>help</b>. Показывает подсказки горячих клавиш режима командной строки (CLI);",
            "<b>network</b> - это механизм, который позволяет анонсировать конкретный маршрут;",
            "<b>redistribute</b> - механизм, анонсирующий маршруты на основании их происхождения, протокола или процесса;",
            "<b>passive-interface</b>. Запрещается анонсирование протокола RIP на выбранном интерфейсе;",
            "<b>prefix-list</b> и <b>route-map</b> - это списки условий, с помощью которых можно конфигурировать "
            "анонсировании и фильтрацию маршрутов.",
            "<b>timers</b> - настройка различных счётчиков времени (таймеров) протокола."], "lm"), "lm")],
        [term(S23)])
    # ---------------------------------------------------------------- pptx 24
    TI = "Настройка <em>на интерфейсе</em>"
    pslide("Настройка на интерфейсе", TI, [
        txt("На интерфейсе также можно выполнить ряд настроек, рассмотрим некоторые:"),
        card("Установить величину метрики RIP-маршрутов на интерфейсе, туннеле или bridge-интерфейсе (необязательно)",
             conf(["esr(config-if-gi)# ip rip metric <VALUE>"], "") +
             p("&lt;VALUE&gt; - величина метрики, задаётся [0…32767]. Значение по умолчанию: 5."), "cy"),
        card("Установить режим анонсирования маршрутов по протоколу RIP (необязательно)",
             conf(["esr(config-if-gi)# ip rip mode <MODE>"], "") + p("&lt;MODE&gt; - режим анонсирования маршрутов:") + li([
                 "multicast - в многоадресном режиме (по умолчанию);", "broadcast - в широковещательном режиме;",
                 "unicast - в unicast-режиме соседям."], "mg"), "mg")],
        [term(S24A)])
    pslide("Сосед и суммирование", TI, [
        card("Задать IP-адрес соседа для установления отношения в unicast-режиме анонсирования маршрутов (не обязательно)",
             conf(["esr(config-if-gi)# ip rip neighbor <ADDR>"], "") +
             p("&lt;ADDR&gt; - IP-адрес, задаётся в виде AAA.BBB.CCC.DDD, где каждая часть принимает значение [0…255]."), "cy"),
        txt("На RIPv2 в ESR автоматическое суммирование по умолчанию отключено, но его можно включить.", tone="am"),
        card("Включить суммаризацию подсетей (необязательно)",
             conf(["esr(config-if-gi)# ip rip summary-address <ADDR/LEN>"], "") +
             p("&lt;ADDR/LEN&gt; - IP-адрес и маска подсети, задаётся в виде AAA.BBB.CCC.DDD/EE, где каждая часть AAA - DDD "
               "принимает значение [0…255], и EE - значение [1…32]."), "lm")],
        [term(S24B)])
    # ---------------------------------------------------------------- pptx 25
    TN = "Объявление <em>сетей</em>"
    pslide("Объявление сетей", TN, [
        txt("<b>Механизм анонсирования</b> - это процесс передачи разрешённых маршрутов соседним маршрутизаторам на основании "
            "комплекса правил. Без отдельных команд анонсирования маршрутизатор не отправляет маршрутную информацию. Чтобы "
            "RIP объявлял сети, необходимо включить анонсирование подсетей командой network или redistribute."),
        card("Анонсирование подсети", conf(["esr(config-rip)# network <ADDR/LEN>"], "") +
             p("где адрес указывается в формате: AAA.BBB.CCC.DDD/EE - IP-адрес подсети с маской в форме префикса, AAA-DDD "
               "принимают значения [0…255], и EE принимает значение [1…32]."), "cy")],
        [term(S25)])
    pslide("Redistribute", TN, [
        card("Включить анонсирование маршрутов, полученных альтернативным способом: напрямую подключенные сети, настроенные "
             "вручную или через протоколы BGP или OSPF",
             conf(["esr(config-rip)# redistribute connected [route-map <NAME>]"], "") +
             p("для анонсируемых, напрямую подключенных подсетей;") +
             conf(["esr(config-rip)# redistribute static [route-map <NAME>]"], "") +
             p("для фильтрации и модификации анонсируемых статических маршрутов;") +
             conf(["esr(config-rip)# redistribute ospf <ID> <ROUTE-TYPE> [[route-map<NAME>];"], "") +
             conf(["esr(config-rip)# redistribute bgp <AS> [route-map <NAME>]"], "") +
             p("для фильтрации и модификации анонсируемых BGP-маршрутов."), "cy")],
        [card("Параметры", li([
            "&lt;NAME&gt; - имя маршрутной карты, которая будет использоваться, задаётся строкой до 31 символа;",
            "&lt;ID&gt; - номер процесса, может принимать значение [1…65535];",
            "&lt;ROUTE-TYPE&gt; - тип маршрута:"], "mg") + li([
            "intra-area - анонсирование маршрутов OSPF-процесса в пределах зоны;",
            "inter-area - анонсирование маршрутов OSPF-процесса между зонами;",
            "external1 - анонсирование внешних маршрутов OSPF-формата 1;",
            "external2 - анонсирование внешних маршрутов OSPF-формата 2."], "lm"), "mg")])
    # ---------------------------------------------------------------- pptx 26
    pslide("Пассивный интерфейс", "Пассивный <em>интерфейс</em>", [
        txt("Как только конфигурация RIP выполняет команду network для подсети, протокол RIP сразу же начинает рассылку "
            "уведомлений со всех интерфейсов, входящих в эту сеть. Эти обновления могут быть нужны не на всех участках сети "
            "(в LAN не нужны RIP объявления сетей: во-первых, это лишний трафик, а во-вторых, небезопасно, так как "
            "обновление маршрутов может быть перехвачено любым устройством)."),
        txt("Команда <b>passive-interface</b> в режиме настройки интерфейса отключает обновления маршрутов в определенном "
            "интерфейсе.", tone="mg")],
        [card("Выключить анонсирование маршрутов на интерфейсах, где это не нужно (необязательно)",
              conf(["esr(config-rip)# passive-interface {<IF> | <TUN> }"], "") +
              li(["&lt;IF&gt; - интерфейс и идентификатор;", "&lt;TUN&gt; - имя и номер туннеля."], "lm"), "lm"),
         term(S26)])
    # ---------------------------------------------------------------- pptx 27
    TM = "Механизмы <em>против петель</em>"
    CV.loops()
    CV.loops_defs()
    # ---------------------------------------------------------------- pptx 28
    pslide("Таймеры", "Таймеры", [
        txt("<b>update</b> - промежуток времени, через который осуществляется многоадресная рассылка маршрутной информации "
            "RIPv2 на IP-адрес 224.0.0.9. По умолчанию: каждые 30 секунд."),
        txt("<b>invalid</b> - временной интервал корректности маршрутной записи без обновления, который должен быть не меньше "
            "3 интервалов update, обычно равен от 3 до 6 update. По истечении времени этого интервала маршрут помечается как "
            "holddown (возможно недоступный). Если в обновлениях маршрутизатор получает такой маршрут, то маршрут отмечается "
            "как недоступный, но этот маршрут всё ещё участвует в отправке трафика. По умолчанию 180 секунд.", tone="mg"),
        txt("<b>flush</b> - временной интервал, в течение которого маршрут не удаляется из таблицы маршрутизации, а по "
            "истечении этого интервала времени производится удаление данного маршрута и установка альтернативного. По "
            "умолчанию: 240 секунд.", tone="lm")],
        [term(S28),
         txt("Для ускорения сходимости сети время таймера удержания (invalid) можно уменьшить, но осторожно. Таймер update "
             "является базовым, и относительно него устанавливаются остальные таймеры, но если менять таймеры, то: менять все "
             "таймеры и вручную каждый, а также на каждом RIP маршрутизаторе в рамках сети. Значения всех таймеров можно "
             "настроить в диапазоне от 12 до 65 535 секунд.", tone="rd")])
    # ---------------------------------------------------------------- pptx 29
    TC = "Проверка <em>конфигурации</em>"
    pslide("Проверка конфигурации", TC, [
        card("Посмотреть настройки текущей конфигурации, в том числе настройки RIP",
             conf(["esr# show running-config routing rip"], ""), "cy"),
        card("Проверить значение preference для протоколов DHCP, PPTP, PPPoE, L2TP, а для протоколов RIP, OSPF, IS-IS, BGP, "
             "кроме preference, можно дополнительно посмотреть максимальное количество маршрутов таблицы маршрутизации",
             conf(["esr# show ip protocols"], ""), "mg"),
        card("Проконтролировать записи в таблице маршрутизации полученные от RIP", conf(["esr# show ip route rip"], ""), "lm"),
        term(S29B)],
        [term(S29A), term(S29C)])
    # pptx 30 «Возникновение ложных маршрутов» — в pptx только пометка «Взять с ссылки …», материала нет (вопрос автору)
    # ---------------------------------------------------------------- pptx 31
    TE = "Пример <em>настройки RIP</em>"
    slide("Пример настройки RIP: задача", sc(head(TE), step(G.example_topo()), grow("g2",
        col(step(card("Задача: настроить на маршрутизаторе RIP", li([
            "1) Имя устройства, IP-адресацию на интерфейсах, отключить firewall;",
            "2) Создать маршрут по умолчанию в сторону провайдера;",
            "3) Протокол RIP для обмена маршрутной информацией с RIP-соседями;",
            "4) Разрешить анонсы RIP статических маршрутов и подсетей 98.51.100.0/24,0.113.0/24, 198.18.0.0/15;",
            "5) Запретить анонсы RIP в локальные сети;",
            "6) Анонсирование маршрутов должно происходить каждые 15 секунд."]), "cy"))),
        col(step(card("Решение: 1) Зададим имя устройства", conf(CFG_RIP_A, ""), "mg")),
            step(card("2) Настроить маршрут по умолчанию к ISP", conf(CFG_RIP_B, ""), "lm"))))))
    slide("Пример: адресация и firewall", sc(head(TE), step(G.example_topo()), grow("g2",
        col(step(card("3) Настроить IP-адресацию на интерфейсах и отключить firewall", conf(CFG_RIP_C[:8], ""), "cy"))),
        col(step(card("3) (продолжение)", conf(CFG_RIP_C[8:], ""), "cy")),
            step(card("4) Включить RIP:", conf(["RIP(config)# router rip"], ""), "mg"))))))
    # ---------------------------------------------------------------- pptx 32
    slide("Пример: RIP на маршрутизаторе RIP", sc(head(TE), step(G.example_topo()), grow("g3",
        col(step(card("4) Включить RIP:", conf(["RIP(config)# router rip"], ""), "cy")),
            step(card("5) Укажем подсети, которые будут анонсироваться протоколом: 198.51.100.0/24, 198.18.0.0/15, "
                      "203.0.113.0/24:", conf(["RIP(config-rip)# network 198.51.100.0/24", "RIP(config-rip)# network 198.18.0.0/15",
                                               "RIP(config-rip)# network 203.0.113.0/24"], ""), "cy"))),
        col(step(card("6) Для анонсирования протоколом статических маршрутов выполним:",
                      conf(["RIP(config-rip)# redistribute static"], ""), "mg")),
            step(card("7) Отключить анонсы RIP в локальные сети:",
                      conf(["RIP(config-rip)# passive-interface gigabitethernet 1/0/3"], ""), "mg"))),
        col(step(card("8) Настроим таймер, отвечающий за отправку маршрутной информации. Если мы меняем базовый таймер, то "
                      "должны настроить остальные таймеры на всех маршрутизаторах:",
                      conf(["RIP(config-rip)# timers update 15", "RIP(config-rip)# timers invalid 45",
                            "RIP(config-rip)# timers flush 105"], ""), "lm")),
            step(card("9) После установки всех требуемых настроек включаем протокол:",
                      conf(["RIP(config-rip)# enable", "RIP(config-rip)#exit", "RIP(config)# exit", "RIP# commit",
                            "RIP# confirm"], ""), "lm"))))))
    # ---------------------------------------------------------------- pptx 33
    slide("Пример: настройка R1 и R2", sc(head(TE, "Настройка R1 и R2 будет выглядеть так:"), step(G.example_topo()),
        grow("g2", col(step(conf(CFG_R1, "R1"))), col(step(conf(CFG_R2, "R2"))))))
