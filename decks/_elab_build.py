# -*- coding: utf-8 -*-
"""Сборка эмулятора сети Eltex: decks/_elab/* + движок MES _dk_cli.js → один офлайн-файл decks/eltex-cli.html.
Перед записью прогоняет автотест (node decks/_elab/test.js) и node --check по итоговому скрипту."""
import os
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "_elab")
ORDER = ["../_dk_cli.js", "common.js", "esr.js", "esr_svc.js", "mesx.js", "hosts.js", "catalog.js", "net.js", "labs.js", "labs_routing.js", "labs_services.js", "ui.js"]


def read(p):
    with open(os.path.join(SRC, p), encoding="utf-8") as f:
        return f.read()


def main():
    js = "\n".join(read(p) for p in ORDER)
    page = read("page.html")
    helpsrc = '<template id="helpSrc">' + read("help.html") + "</template>\n"
    html = page.replace("/*__JS__*/", js.replace("</script", "<\\/script")).replace("<script>\n", helpsrc + "<script>\n", 1)
    tmp = os.path.join(SRC, "_bundle.js")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    try:
        subprocess.run(["node", "--check", tmp], check=True)
    finally:
        os.remove(tmp)
    subprocess.run(["node", os.path.join(SRC, "test.js"), "12"], check=True)
    out = os.path.join(D, "eltex-cli.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("OK", out, round(len(html.encode("utf-8")) / 1024), "КБ")


if __name__ == "__main__":
    sys.exit(main())
