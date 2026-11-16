# -*- coding: utf-8 -*-
"""STP: слайды pptx без инфографик (BPDU в Wireshark, show-выводы, задачи, этапы RSTP, настройка MES) — в пиксельном стиле.
Скриншоты консоли и Wireshark перепечатаны дословно."""
from _stp_pix import S, net, L
from _pix import panel, items, nums, note, grid, stack, sc, scp, psw, badge, ln, lbl, chip, xx, square, path, env, show, tab, TE, YE, RE, GN, BL
import _pt_kit as K


def T(lines, title=""):
    return stack(K.term(lines, title))


def C(lines, title=""):
    return stack(K.conf(lines, title))


def s14():
    return S("Выборы корневого моста", "BPDU — Bridge Protocol Data Unit · multicast 01:80:C2:00:00:00", grid("1fr 1.2fr",
        panel("Что передаёт BPDU", '<ul class="li"><li>Идентификатор версии протокола STP (Protocol Version Identifier)</li><li>Тип BPDU (BPDU Type)</li>'
              '<li>Идентификатор моста (Bridge Identifier)</li><li>Идентификатор порта, с которого был выслан BPDU (Port Identifier)</li>'
              '<li>Идентификатор корневого моста (Root Identifier)</li><li>Стоимость пути до корневого моста (Root Path Cost)</li>'
              '<li>Таймеры: Message Age, Max Age, Hello Time, Forward Delay</li></ul>'),
        stack(T(["IEEE 802.3 Ethernet", "  Destination: Spanning-tree-(for-bridges)_00 (01:80:c2:00:00:00)", "  Source: EltexEnt_2c:1c:c2 (e0:d9:e3:2c:1c:c2)",
                 "  Length: 38", "  Padding: 0000000000000000", "Logical-Link Control", "Spanning Tree Protocol"], "Wireshark · кадр BPDU"),
              T(["Spanning Tree Protocol", "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Spanning Tree (0)",
                 "  BPDU Type: Configuration (0x00)", "  BPDU flags: 0x00", "  Root Identifier: 32768 / 0 / e0:d9:e3:2c:1c:c0", "  Root Path Cost: 0",
                 "  Bridge Identifier: 32768 / 0 / e0:d9:e3:2c:1c:c0", "  Port identifier: 0x8032", "  Message Age: 0", "  Max Age: 20", "  Hello Time: 2",
                 "  Forward Delay: 15"], "Поля BPDU"))))


def s19():
    return S("Роли портов в протоколе STP", "Проверка ролей командой show spanning-tree active", grid("1fr 1.5fr",
        stack(panel("Корневые порты", "<p>«Смотрят» в сторону корневого моста: Gi0/1 коммутатора SW-3 и Te0/2 коммутатора SW-1.</p>"),
              panel("Назначенные порты", "<p>Все порты корневого SW-2, а также Te0/1 коммутатора SW-1 и Gi0/2 SW-3.</p>")),
        stack(T(["MES (config)#show spanning-tree active", "", "Spanning tree enabled mode STP", "-------------------------часть вывода пропущена------------",
                 "Interfaces", " Name     State    Prio.Nbr  Cost   Sts   Role PortFast       Type", " -------- -------- -------- ------ ------ ---- -------- -----------",
                 " gi1/0/1  enabled  128.49    20000  Frw   [[Desg]] Yes            P2P (STP)", " gi1/0/5  enabled  128.53    20000  Frw   [[Desg]] Yes            P2P (STP)"],
                "Корневой коммутатор"),
              T(["MES (config)#show spanning-tree active", "-------------------------часть вывода пропущена------------", "Interfaces",
                 " Name     State    Prio.Nbr  Cost   Sts   Role PortFast       Type", " -------- -------- -------- ------ ------ ---- -------- -----------",
                 " gi1/0/3  enabled  128.51    20000  Frw   [[Root]] No             P2P (STP)", " gi1/0/5  enabled  128.53    20000  Frw   [[Desg]] Yes            P2P (STP)"],
                "Некорневой коммутатор"))))


def s25():
    return S("Состояния портов в STP", "", panel("", tab(["Состояние порта", "Описание"], [
        [("Disabled", "y"), "Порт не может отправлять или принимать BPDU или пользовательские кадры данных. То есть порт находится в состоянии Down."],
        [("Blocking", "r"), "Порт заблокирован STP. Заблокированный порт не может отправлять BPDU, но прослушивает BPDU. Заблокированный порт также не может отправлять или получать пользовательские кадры данных или изучать MAC-адреса."],
        [("Listening", "y"), "В STP состояние Listening может быть у корневого или назначенного порта, в тот момент, когда порт ещё находится в процессе расчёта STP. В этом случае порт может отправлять и принимать BPDU, но не может отправлять или принимать кадры данных услуг или изучать MAC-адреса."],
        [("Learning", "y"), "Порт в состоянии Learning прослушивает пользовательские данные, но пересылать их не может. После получения пользовательских кадров данных, порт изучает MAC-адреса."],
        [("Forwarding", "g"), "Порт в состоянии Forwarding может отправлять и получать пользовательские данные и обрабатывать BPDU. Только корневой порт или назначенный порт могут переключиться в состояние Forwarding."]])))


def s30():
    Y, N = ("Да", "g"), ("Нет", "r")
    return S("Состояния портов в STP", "Состояние Disabled и сравнение состояний", stack(grid("1fr 1.3fr",
        panel("Disabled (Отключён)", '<ul class="li"><li>на порту отключён протокол STP;</li><li>порт отключён администратором (Down Adm);</li>'
                                     '<li>порт на другом конце канала отключён администратором, или отсутствует кабельное соединение (Down nc).</li></ul>'),
        T(["MES#show spanning-tree", "-------------------------часть вывода пропущена------------", "Interfaces",
           " Name     State    Prio.Nbr  Cost     Sts   Role PortFast  Type", " -------- -------- -------- -------- ------ ---- -------- --------------",
           " gi1/0/1  enabled  128.49    2000000  Dsbl  [[Dsbl]] No        -", " gi1/0/3  enabled  128.51    20000    Frw   [[Root]] No        P2P (STP)", "",
           "MES#show interfaces status", "                                             Flow    Link", "Port     Type         Duplex  Speed  Neg      ctrl    State",
           "-------- ------------ ------  -----  -------- ----    -----------", "[[gi1/0/1]]  1G-Copper      --      --     --       --      [[Down (nc)]]",
           "gi1/0/2  1G-Copper      --      --     --       --      Down (nc)", "gi1/0/3  1G-Copper    Full    1000   Enabled  Off     Up",
           "------------------часть текста пропущена-------------------"])),
        panel("Состояния портов в протоколе STP", tab(["", "Принимает BPDU", "Отправляет BPDU", "Изучает MAC-адреса", "Принимает данные", "Отправляет данные"], [
            ["Blocking", Y, N, N, N, N], ["Listening", Y, Y, N, N, N], ["Learning", Y, Y, Y, N, N], ["Forwarding", Y, Y, Y, Y, Y]]))))


def _tcn_sq(T_=5, ack=False):
    r = {(300, 115): "D", (560, 115): "R", (230, 285): "R", (230, 150): "D", (300, 340): "D", (575, 340): "R", (640, 155): "D", (640, 285): "ND",
         (690, 145): "D", (850, 300): "?", (705, 340): "Ds", (805, 340): "Ds"}
    fl = [(path("SW-5", "SW-5.t", "SW-3.br", "SW-3"), .2, 1.6)]
    if ack:
        fl.append((path("SW-3", "SW-3.br", "SW-5.t", "SW-5"), 2.2, 1.6))
    return square(sw5=True, root="SW-2", roles=r, links={"45": (RE, True), "35": YE}, flows=fl, T=T_, extra=xx(755, 337, 12) + chip(780, 210, "TCN", "#fff3c4", YE))


def s33():
    return S("Изменение топологии STP", "TCN BPDU и что делает вышестоящий коммутатор", grid("1fr 1.3fr",
        stack(nums([("Старение MAC-таблицы", "уравнивает таймер «старения» таблицы коммутации с таймером Forward Delay (обычно 15 секунд)"),
                    ("TCN Acknowledgement", "отправляет подтверждение с Designated-порта в сторону коммутатора, отправившего TCN"),
                    ("TCN дальше к корню", "отправляет TCN со своего корневого порта в сторону корневого коммутатора")], 1),
              T(["IEEE 802.3 Ethernet", "  Destination: Spanning-tree-(for-bridges)_00 (01:80:c2:00:00:00)", "  Source: EltexEnt_8c:cd:d3 (e4:5a:d4:8c:cd:d3)", "  Length: 7",
                 "Logical-Link Control", "Spanning Tree Protocol", "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Spanning Tree (0)",
                 "  BPDU Type: [[Topology Change Notification (0x80)]]"], "Wireshark · TCN")),
        scp(_tcn_sq(ack=True), "SW-5 → SW-3: TCN; SW-3 → SW-5: TCAck · BPDU: Root SW-2, Bridge SW-3, Cost 20 000, TCAck 1, TCN 1, Age 1")))


def s34():
    return S("Изменение топологии STP", "Topology Change Acknowledgement (TCA)", grid("1fr 1.2fr",
        panel("Подтверждение изменения топологии", "<p>Отправляется с SW-3 на SW-5. Это конфигурационное BPDU, отличающееся от обычного только наличием двух «флагов» в поле BPDU Flags. "
                                                   "Оно подтверждает, что сообщение получено: незачем засорять сеть лишними TCN — можно дожидаться перехода Gi0/2 в Forwarding.</p>"),
        T(["Spanning Tree Protocol", "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Spanning Tree (0)", "  BPDU Type: Configuration (0x00)",
           "  [[BPDU flags: 0x81, Topology Change Acknowledgment, Topology Change]]", "    1... .... = Topology Change Acknowledgment: Yes", "    .... ...1 = Topology Change: Yes",
           "  Root Identifier: 32768 / 0 / a8:f9:4b:30:fc:c0", "  Root Path Cost: 20000", "  Bridge Identifier: 32768 / 0 / e0:d9:e3:2c:1c:c0", "  Port identifier: 0x8031",
           "  Message Age: 1", "  Max Age: 20", "  Hello Time: 2", "  Forward Delay: 15"], "Wireshark · TCA")))


def s35():
    return S("Изменение топологии STP", "Корень рассылает TC + Root Config BPDU", grid("1fr 1.2fr",
        stack(panel("Флаг Topology Change (TC)", "<p>Получив TCN, корень отправляет TC Acknowledgement, а затем BPDU с флагом Topology Change.</p>"),
              note("Не разово, а каждые 2 секунды в течение 60–70 секунд — чтобы BPDU с правильной топологией дошли до самых дальних ветвей сети.", "clock", "g"),
              panel("В Wireshark", "<p>Такие BPDU называются <b>TC + Root Config. BPDU</b>.</p>")),
        T(["Spanning Tree Protocol", "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Spanning Tree (0)", "  BPDU Type: Configuration (0x00)",
           "  [[BPDU flags: 0x01, Topology Change]]", "    0... .... = Topology Change Acknowledgment: No", "    .... ...1 = Topology Change: Yes",
           "  Root Identifier: 32768 / 0 / a8:f9:4b:30:fc:c0", "  Root Path Cost: 20000", "  Bridge Identifier: 32768 / 0 / e0:d9:e3:2c:1c:c0", "  Port identifier: 0x8031",
           "  Message Age: 1", "  Max Age: 20", "  Hello Time: 2", "  Forward Delay: 15"], "Wireshark · TC BPDU")))


def s37():
    return S("Настройка протокола STP на коммутаторах MES", "", grid("1fr 1fr",
        panel("По умолчанию", '<ul class="li"><li>STP глобально включён на всех коммутаторах Eltex MES.</li><li>MES 23xx/33xx/35xx/5324 — версия RSTP.</li>'
                              '<li>MES 14xx/24xx — версия MSTP.</li></ul>'),
        stack(C(["MES(config)#no spanning-tree"], "Отключить STP глобально"), C(["MES(config)#spanning-tree"], "Включить STP глобально"),
              C(["MES2308(config)#spanning-tree mode stp"], "Режим «классического» STP"),
              C(["MES(config-if)#spanning-tree disable", "MES(config-if)#no spanning-tree disable"], "Отключить / включить на интерфейсе"))))


def s38():
    return S("Настройка протокола STP на коммутаторах MES", "Приоритет, стоимость, таймеры", grid("1fr 1fr",
        stack(C(["MES(config)# spanning-tree priority <prior_val>"], "Приоритет коммутатора (Bridge Priority)"),
              panel("", "<p><b>prior_val</b> — от 0 до 61440 с шагом 4096. По умолчанию 32768.</p>"),
              C(["MES(config)#spanning-tree pathcost method <long|short>"], "Метод вычисления стоимости пути"),
              panel("", '<ul class="li"><li><b>short</b> — значение стоимости в диапазоне [1..65535];</li><li><b>long</b> — значение стоимости в диапазоне [1..200000000].</li></ul>'),
              C(["MES(config-if)#spanning-tree cost <Portcost>"], "Стоимость для порта"), panel("", "<p><b>Portcost</b> — от 0 до 200 000 000.</p>")),
        stack(C(["MES(config)# spanning-tree hello-time <1-10 sec>"], "Таймер отправки BPDU (hello-timer) · по умолчанию 2 с"),
              C(["MES(config)# spanning-tree max-age <sec>"], "Max Age · по умолчанию 20 с"),
              C(["MES(config)# spanning-tree forward-time <4-30 sec>"], "Forward Delay · по умолчанию 15 с"),
              C(["MES (config-if)spanning-tree bpdu filtering"], "При отключённом STP: блокировать приём и отправку BPDU на порту"))))


def _test_tri():
    nodes = {"SW1": (450, 70), "SW2": (180, 300), "SW3": (720, 300)}
    g = net(nodes, [("SW1", "SW2", "#5d6f80", False), ("SW1", "SW3", "#5d6f80", False), ("SW2", "SW3", "#5d6f80", False)], w=110)
    g += lbl(450, 20, "4096.4c1f-aabc-0001", 14, RE) + lbl(180, 380, "4096.4c1f-aabc-0002", 14, RE) + lbl(720, 380, "4096.4c1f-aabc-0003", 14, RE)
    g += lbl(370, 120, "GE0/0/0", 13) + lbl(540, 120, "GE0/0/1", 13) + lbl(190, 240, "GE0/0/1", 13) + lbl(710, 240, "GE0/0/1", 13)
    g += lbl(270, 330, "GE0/0/2", 13) + lbl(630, 330, "GE0/0/2", 13) + lbl(300, 190, "1000M", 13) + lbl(600, 190, "1000M", 13) + lbl(450, 320, "1000M", 13)
    return g


def s39():
    return S("Тест 1: определите корневой мост и роли портов", "", grid("1.2fr 1fr", scp(_test_tri(), "", 900, 400),
        stack(panel("Задание", "<p>Определите корневой мост, роли портов и их состояния после сходимости.</p>"),
              panel("1. Выбор корневого коммутатора — Root Bridge", "<p>Корневым становится коммутатор с наименьшим Bridge ID. Сначала сравнивается приоритет, при равных — MAC-адрес.</p>"
                    "<p>Приоритет у всех одинаковый — <b>4096</b>: <b>4c1f-aabc-0001 &lt; 4c1f-aabc-0002 &lt; 4c1f-aabc-0003</b>.</p>"
                    "<p>Следовательно, <b>SW1 становится корневым мостом</b>. Его стоимость пути до самого себя равна <b>0</b>.</p>"))))


def s40():
    g = _test_tri() + badge(395, 100, "D") + badge(505, 100, "D") + badge(215, 255, "R") + badge(685, 255, "R") + badge(245, 300, "D") + badge(655, 300, "ND") + xx(600, 300, 10)
    return S("Тест 1: ответ", "", grid("1fr 1.2fr", scp(g, "", 900, 400), panel("", tab(["Коммутатор", "Порт", "Куда подключён", "Роль", "Состояние после сходимости"], [
        ["SW1 — корневой", "GE0/0/0", "SW2", "Designated", "Forwarding"], ["SW1 — корневой", "GE0/0/1", "SW3", "Designated", "Forwarding"],
        ["SW2", "GE0/0/1", "SW1", "Root", "Forwarding"], ["SW2", "GE0/0/2", "SW3", "Designated", "Forwarding"], ["SW3", "GE0/0/1", "SW1", "Root", "Forwarding"],
        ["SW3", "GE0/0/2", "SW2", ("Заблокированный / Alternate в RSTP", "r"), ("Blocking / Discarding", "r")]]))))


def _diamond():
    nodes = {"SW1": (450, 60), "SW2": (180, 210), "SW3": (720, 210), "SW4": (450, 360)}
    g = net(nodes, [("SW1", "SW2", "#5d6f80", False), ("SW1", "SW3", "#5d6f80", False), ("SW2", "SW4", "#5d6f80", False), ("SW3", "SW4", "#5d6f80", False)], w=110)
    g += lbl(450, 15, "4096.4c1f-aabc-0001", 14, RE) + lbl(180, 160, "4096.4c1f-aabc-0002", 14, RE) + lbl(720, 160, "4096.4c1f-aabc-0003", 14, RE) + lbl(450, 430, "4096.4c1f-aabc-0004", 14, RE)
    g += lbl(360, 100, "GE0/0/0", 12) + lbl(540, 100, "GE0/0/1", 12) + lbl(230, 165 + 80, "GE0/0/2", 12) + lbl(250, 140, "GE0/0/1", 12)
    g += lbl(650, 140, "GE0/0/2", 12) + lbl(670, 250, "GE0/0/1", 12) + lbl(360, 330, "GE0/0/1", 12) + lbl(540, 330, "GE0/0/2", 12)
    return g


def s41():
    return S("Тест 2: определите корневой мост и роли портов", "в следующей топологии", grid("1.2fr 1fr", scp(_diamond(), "", 900, 450),
        stack(panel("Задание", "<p>Определите корневой мост и роли всех портов.</p>"),
              panel("Выбираем корневой мост", "<p>Приоритеты всех коммутаторов равны <b>4096</b>, поэтому сравниваем MAC-адреса.</p>"
                    "<p>У <b>SW1</b> наименьший MAC, следовательно, он становится корневым. Оба его порта — <b>Designated Port (DP)</b>.</p>"))))


def s42():
    g = _diamond() + badge(395, 85, "D") + badge(505, 85, "D") + badge(225, 180, "R") + badge(675, 180, "R") + badge(225, 245, "D") + badge(675, 245, "D")
    g += badge(400, 335, "R") + badge(500, 335, "ND") + xx(560, 300, 10)
    return S("Тест 2: итог", "", grid("1fr 1.2fr", scp(g, "", 900, 450), panel("", tab(["Коммутатор", "Порт", "Сосед", "Роль", "Передача пользовательских кадров"], [
        ["SW1 — корень", "GE0/0/0", "SW2", "Designated", "Да"], ["SW1 — корень", "GE0/0/1", "SW3", "Designated", "Да"], ["SW2", "GE0/0/1", "SW1", "Root", "Да"],
        ["SW2", "GE0/0/2", "SW4", "Designated", "Да"], ["SW3", "GE0/0/2", "SW1", "Root", "Да"], ["SW3", "GE0/0/1", "SW4", "Designated", "Да"],
        ["SW4", "GE0/0/1", "SW2", "Root", "Да"], ["SW4", "GE0/0/2", "SW3", ("Заблокированный / Alternate", "r"), ("Нет", "r")]]))))


def s43():
    g = (psw(200, 120, "SW1", w=130) + psw(700, 120, "SW2", w=130) + ln("M265,105 L635,105", "#5d6f80", 6) + ln("M265,140 L635,140", "#5d6f80", 6)
         + lbl(330, 92, "GE0/0/1", 13) + lbl(570, 92, "GE0/0/1", 13) + lbl(330, 165, "GE0/0/2", 13) + lbl(570, 165, "GE0/0/2", 13)
         + lbl(200, 40, "4096.4c1f-aabc-0001", 14, RE) + lbl(700, 40, "4096.4c1f-aabc-0002", 14, RE))
    return S("Тест 3: определите корневой мост и роли портов", "", stack(scp(g, "", 900, 200),
        panel("1. Выбираем корневой мост", "<p>Приоритеты одинаковые, а MAC у SW1 меньше. Поэтому <b>SW1 — корневой мост</b>, оба его порта становятся <b>Designated Port</b>.</p>")))


def s45():
    return S("Принцип работы RSTP", "IEEE 802.1w (2001)", stack(grid("1fr 1fr",
        panel("RSTP — усовершенствование STP", '<ul class="li"><li>Быстрая конвергенция топологии сети.</li><li>Тот же механизм работы, что и у STP.</li>'
              '<li>При изменении топологии может использовать Proposal/Agreement для быстрого восстановления подключения.</li>'
              '<li>Нет трёх состояний порта, определены две новые роли порта; атрибуты порта различаются по состояниям и ролям.</li></ul>'),
        panel("Улучшения в RSTP", '<ul class="li"><li>Иначе обрабатывает конфигурационные BPDU; в стабильной топологии отправка оптимизирована.</li>'
              '<li>Более короткий интервал ожидания для BPDU.</li><li>Оптимизирована обработка Inferior BPDU.</li>'
              '<li>Изменён формат BPDU: поле Flags описывает роли портов.</li><li>Ускорена реакция на изменения топологии.</li></ul>', "e")),
        note("Не рекомендуется совместное использование RSTP с STP из-за медленной сходимости STP.", "warn", "r")))


def _rstp_stage(stage, T_=5):
    """Этапы 1–4 RSTP после отказа SW-1 — SW-3."""
    nodes = {"SW-1": (450, 70), "SW-2": (200, 260), "SW-3": (700, 260), "HUB": (700, 410)}
    g = net(nodes, [("SW-1", "SW-2", "#5d6f80", False), ("SW-1", "SW-3", RE, True), ("SW-2", "SW-3", "#5d6f80", False), ("SW-3", "HUB", "#5d6f80", False)], "SW-1")
    g += xx(575, 165, 12) + badge(395, 105, "D") + badge(505, 105, "Ds") + badge(650, 225, "Ds") + badge(250, 225, "R")
    p23, p32 = L((270, 262), (630, 262)), L((630, 262), (270, 262))
    if stage == 1:
        g += badge(255, 270, "D") + badge(640, 270, "D") + env(p32, .2, 2, T_) + chip(450, 300, "3A — BPDU от SW-3: «корень — я»", "#fff3c4", YE, size=12)
    elif stage == 2:
        g += badge(255, 270, "D") + badge(640, 270, "D") + env(p23, .2, 2, T_) + chip(450, 300, "1P — BPDU от SW-1 с флагом Proposal", "#fff3c4", YE, size=12)
    elif stage == 3:
        g += badge(255, 270, "D") + badge(640, 270, "R") + env(p32, .2, 2, T_) + chip(450, 300, "1A — ответ Agreement", "#fff3c4", YE, size=12)
    else:
        g += badge(255, 270, "D") + badge(640, 270, "R") + env(p23, .2, 2, T_) + env(L((200, 230), (420, 80)), .2, 2, T_) + chip(450, 300, "1TC — Topology Change", "#fff3c4", YE, size=12)
    return g + badge(660, 330, "D") + badge(740, 330, "Bck")


def s50():
    return S("Принцип работы RSTP", "Этап №1: SW-3 объявляет себя корнем", grid("1fr 1.2fr",
        stack(scp(_rstp_stage(1), "", 900, 450), panel("", "<p>Не получив подряд 3 BPDU от SW-1 на Gi0/1, SW-3 считает себя корневым и оповещает соседей (BPDU 3A). "
                                                         "Поле BPDU flags расширилось: в STP — два флага, теперь все восемь. Bridge ID = Root ID — отправитель считает себя корнем.</p>")),
        T(["Source: EltexEnt_1f:f4:82 (e4:5a:d4:1f:f4:82)", "Length: 39", "Padding: 00000000000000", "Logical-Link Control", "Spanning Tree Protocol",
           "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Rapid Spanning Tree (2)", "  BPDU Type: Rapid/Multiple Spanning Tree (0x02)",
           "  [[BPDU flags: 0x7c, Agreement, Forwarding, Learning, Port Role: Designated]]", "    0... .... = Topology Change Acknowledgment: No", "    .1.. .... = Agreement: Yes",
           "    ..1. .... = Forwarding: Yes", "    ...1 .... = Learning: Yes", "    .... 11.. = Port Role: Designated (3)", "    .... ..0. = Proposal: No",
           "    .... ...0 = Topology Change: No", "  Root Identifier: 32768 / 0 / e4:5a:d4:1f:f4:80", "  Root Path Cost: 0", "  Bridge Identifier: 32768 / 0 / e4:5a:d4:1f:f4:80"],
          "Wireshark · BPDU 3A")))


def s51():
    return S("Принцип работы RSTP", "Этап №2: Proposal от SW-2", grid("1fr 1.2fr",
        stack(scp(_rstp_stage(2), "", 900, 450), panel("", "<p>SW-2 знает настоящий корень SW-1 (за Gi0/1), его приоритет лучше. SW-2 переводит Gi0/2 из Discarding в Learning, "
                                                         "из Alternate в Designated и пересылает SW-3 BPDU от SW-1 с флагом <b>Proposal</b>.</p>")),
        T(["Source: EltexEnt_3d:7f:42 (e4:5a:d4:3d:7f:42)", "Length: 39", "Padding: 00000000000000", "Logical-Link Control", "Spanning Tree Protocol",
           "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Rapid Spanning Tree (2)", "  BPDU Type: Rapid/Multiple Spanning Tree (0x02)",
           "  [[BPDU flags: 0x0e, Port Role: Designated, Proposal]]", "    0... .... = Topology Change Acknowledgment: No", "    .0.. .... = Agreement: No",
           "    ..0. .... = Forwarding: No", "    ...0 .... = Learning: No", "    .... 11.. = Port Role: Designated (3)", "    .... ..1. = Proposal: Yes",
           "    .... ...0 = Topology Change: No", "  Root Identifier: 32768 / 0 / a8:f9:4b:30:fc:c0", "  Root Path Cost: 20000", "  Bridge Identifier: 32768 / 0 / e4:5a:d4:3d:7f:40"],
          "Wireshark · BPDU 1P")))


def s52():
    return S("Принцип работы RSTP", "Этап №3: Agreement от SW-3", grid("1fr 1.2fr",
        stack(scp(_rstp_stage(3), "", 900, 450), panel("", "<p>SW-3 понимает, что за Gi0/2 есть мост с меньшим BID: Gi0/2 и Gi0/3 — Discarding → Learning, роли Root и Designated. "
                                                         "SW-3 отвечает BPDU с флагом <b>Agreement</b>; Gi0/2 в нём уже Root — SW-2 может не ждать и сразу переводить порт в Forwarding.</p>")),
        T(["Source: EltexEnt_1f:f4:82 (e4:5a:d4:1f:f4:82)", "Length: 39", "Padding: 00000000000000", "Logical-Link Control", "Spanning Tree Protocol",
           "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Rapid Spanning Tree (2)", "  BPDU Type: Rapid/Multiple Spanning Tree (0x02)",
           "  [[BPDU flags: 0x78, Agreement, Forwarding, Learning, Port Role: Root]]", "    0... .... = Topology Change Acknowledgment: No", "    .1.. .... = Agreement: Yes",
           "    ..1. .... = Forwarding: Yes", "    ...1 .... = Learning: Yes", "    .... 10.. = Port Role: Root (2)", "    .... ..0. = Proposal: No",
           "    .... ...0 = Topology Change: No", "  Root Identifier: 32768 / 0 / a8:f9:4b:30:fc:c0", "  Root Path Cost: 40000", "  Bridge Identifier: 32768 / 0 / e4:5a:d4:1f:f4:80",
           "  Port identifier: 0x8002"], "Wireshark · BPDU 1A")))


def s53():
    return S("Принцип работы RSTP", "Этап №4: Topology Change", grid("1fr 1.2fr",
        stack(scp(_rstp_stage(4), "", 900, 450),
              panel("", "<p>SW-2 переводит Gi0/2 в Forwarding и отправляет BPDU с флагом <b>Topology Change</b> из Designated- и Root-порта. Каждый коммутатор ставит таймер "
                        "<b>tcWhile = Hello Time + 1 с</b> (2 + 1 = 3 с), рассылает TC, сбрасывает изученные MAC-адреса на всех портах, кроме порта получения, и пересылает TC дальше.</p>")),
        T(["Source: EltexEnt_3d:7f:42 (e4:5a:d4:3d:7f:42)", "Length: 39", "Padding: 00000000000000", "Logical-Link Control", "Spanning Tree Protocol",
           "  Protocol Identifier: Spanning Tree Protocol (0x0000)", "  Protocol Version Identifier: Rapid Spanning Tree (2)", "  BPDU Type: Rapid/Multiple Spanning Tree (0x02)",
           "  [[BPDU flags: 0x3d, Forwarding, Learning, Port Role: Designated, Topology Change]]", "    0... .... = Topology Change Acknowledgment: No", "    .0.. .... = Agreement: No",
           "    ..1. .... = Forwarding: Yes", "    ...1 .... = Learning: Yes", "    .... 11.. = Port Role: Designated (3)", "    .... ..0. = Proposal: No",
           "    .... ...1 = Topology Change: Yes", "  Root Identifier: 32768 / 0 / a8:f9:4b:30:fc:c0", "  Root Path Cost: 20000", "  Bridge Identifier: 32768 / 0 / e4:5a:d4:3d:7f:40",
           "  Port identifier: 0x8002"], "Wireshark · BPDU 1TC")))


def s55():
    return S("Граничные (edge) и неграничные (non-edge) порты", "", grid("1fr 1.2fr",
        stack(panel("Неграничные порты", '<ul class="li"><li><b>P2P</b> (point-to-point) — порты в режиме полного дуплекса (full duplex).</li>'
                                         '<li><b>Shared</b> — порты в режиме полудуплекса (half-duplex).</li></ul><p>Встретить Shared в рабочей сети почти невозможно; '
                                         'если он есть в диагностике, скорее всего, STP на коммутаторе отключён.</p>'),
              panel("portfast", "<p>Команда <b>portfast</b> приводит к немедленному переключению порта доступа в состояние пересылки (forwarding).</p>"
                    + C(["MES (config-if)#spanning-tree portfast"]))),
        stack(T(["Warning: portfast should only be enabled on ports connected to a single host.", "Connecting hubs, concentrators, switches, bridges, etc... to this interface",
                 "when portfast is enabled, can cause temporary bridging loops.", "Use with CAUTION"], "Предупреждение MES"),
              T(["Spanning tree Protocol has been disabled", "Bridge Id      Priority  32768", "               Address   00:00:00:00:00:00",
                 "               Max age is 20 sec 0 cs, forward delay is 15 sec 0 cs", "               Hello Time is 2 sec 0 cs", "               Dynamic Path Cost is Disabled",
                 "               Dynamic Path Cost Lag-Speed Change is Disabled", "Name      Role      State    Cost    Prio  Type", "----      ----      -----    ----    ----  ------",
                 "fa 0/1    Disabled  Unknown  200000  128   [[SharedLan]]", "fa 0/2    Disabled  Unknown  200000  128   [[SharedLan]]"], "STP отключён — порты Shared"))))


def s56():
    return S("Настройка протокола RSTP на коммутаторах MES", "", grid("1fr 1fr",
        stack(C(["MES(config)#no spanning-tree"], "Отключить STP глобально"), C(["MES(config)#spanning-tree"], "Включить STP глобально"),
              C(["MES (config)#spanning-tree mode rstp"], "Режим RSTP")),
        stack(C(["MES(config-if)#spanning-tree disable"], "Отключить на интерфейсе"), C(["MES(config-if)#no spanning-tree disable"], "Включить на интерфейсе"),
              C(["MES(config)# spanning-tree priority <prior_val>"], "Приоритет коммутатора (Bridge Priority)"),
              panel("", "<p><b>Prior_val</b> — от 0 до 61440 с шагом 4096. По умолчанию 32768.</p>"))))


def s57():
    return S("Настройка протокола RSTP на коммутаторах MES", "Стоимость, таймеры, BPDU filtering, edge-порты", grid("1fr 1fr",
        stack(C(["MES(config)#spanning-tree pathcost method <long|short>"], "Метод вычисления стоимости пути"),
              panel("", '<ul class="li"><li><b>long</b> — [1..200000000];</li><li><b>short</b> — [1..65535].</li></ul>'),
              C(["MES(config-if)spanning-tree cost Portcost"], "Стоимость порта · Portcost от 0 до 200 000 000"),
              C(["MES(config)# spanning-tree hello-time <1-10 sec>"], "Hello-timer · по умолчанию 2 с")),
        stack(C(["MES(config)# spanning-tree max-age <sec>"], "Max Age · по умолчанию 20 с"), C(["MES(config)# spanning-tree forward-time <4-30 sec>"], "Forward Delay · по умолчанию 15 с"),
              C(["MES (config-if)#spanning-tree bpdu filtering"], "При отключённом STP: блокировать приём и отправку BPDU"),
              C(["MES(config-if)#spanning-tree portfast", "MES(config-if)#no spanning-tree portfast"], "Включить / отключить граничный порт"))))


def s64():
    return S("Настройка PVST+", "", grid("1fr 1fr",
        stack(C(["MES2308P(config)# spanning-tree mode pvst"], "Включение PVST"), C(["MES2308P(config)# vlan database", "MES2308P(config-vlan)# vlan vlan_list"], "VLAN-участники PVST"),
              C(["MES2308P(config)# interface gigabitethernet0/1", "MES2308P(config-if)# switchport mode trunk", "MES2308P(config-if)# switchport trunk allowed vlan add vlan_list"],
                "Добавить VLAN на интерфейсы"),
              C(["MES2308P(config)# no spanning-tree vlan vlan_list"], "Отключить PVSTP+ в указанных VLAN")),
        C(["MES2308P(config)# spanning-tree mode pvst", "MES2308P(config)# vlan database", "MES2308P(config-vlan)# vlan 2-63", "MES2308P(config)# interface gigabitethernet1/0/14",
           "MES2308P(config-if)# switchport mode trunk", "MES2308P(config-if)# switchport trunk allowed vlan add 2-63"], "Пример: PVST для VLAN 2-63")))


def s70():
    return S("Настройка протокола MSTP на коммутаторах MES", "", grid("1fr 1fr",
        stack(C(["MES(config)#spanning-tree mode mst"], "Включение MSTP"),
              C(["MES(config)#spanning-tree mst configuration", "MES(config-mst)#name RegionName", "MES(config-mst)#instance InstNumber vlan vlan-range",
                 "MES(config-mst)#revision RevNumber", "MES(config)#[exit | abort]"], "Регион, экземпляры и версия конфигурации"),
              panel("", '<ul class="li"><li><b>RegionName</b> — имя региона; <b>InstNum</b> — номер экземпляра; <b>vlan-range</b> — VLAN экземпляра.</li>'
                        '<li><b>exit</b> — выход с сохранением; <b>abort</b> — выход <b>без</b> сохранения настроенных параметров.</li></ul>'),
              C(["MES(config)#spanning-tree mst InstNum priority 0"], "Сделать коммутатор корнем экземпляра")),
        stack(C(["MES(config)#spanning-tree mode mst", "MES(config)#spanning-tree mst configuration", "MES(config-mst)#name testRegion", "MES(config-mst)#instance 1 vlan 10-20",
                 "MES(config-mst)#instance 2 vlan 21-30", "MES(config-mst)#instance 3 vlan 31-40", "MES(config-mst)#revision 1", "MES(config)#exit",
                 "MES(config)#spanning-tree mst 1 priority 0"], "Пример конфигурации"),
              T(["MES#show spanning-tree mst-configuration", "Current MST configuration", "Name: e4:5a:d4:39:bc:e0", "Revision: 0", "Instance   State      Vlans Mapped",
                 "--------   -------    ------------------------------------------------", "0          enabled    1,72-73,253-254,337,420,560,700-712"],
                "Проверка: команды show могут незначительно отличаться по синтаксису на разных моделях"))))


PX2 = {14: s14, 19: s19, 25: s25, 30: s30, 33: s33, 34: s34, 35: s35, 37: s37, 38: s38, 39: s39, 40: s40, 41: s41, 42: s42, 43: s43, 45: s45,
       50: s50, 51: s51, 52: s52, 53: s53, 55: s55, 56: s56, 57: s57, 64: s64, 70: s70}
