# -*- coding: utf-8 -*-
"""python _mp_rep/_cmp.py <имя> ... -> _mp_rep/_cmp/<имя>.jpg (сверху оригинал, снизу вёрстка, все шаги видны)."""
import sys, os, pathlib, subprocess, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent.parent
OUT = D / "_mp_rep" / "_cmp"; OUT.mkdir(exist_ok=True)
names = sys.argv[1:]
tmp = pathlib.Path(tempfile.gettempdir()) / f"mp_cmp_{os.getpid()}.html"
r = subprocess.run([sys.executable, "-X", "utf8", str(D / "_mp_build.py")], cwd=D, capture_output=True, text=True,
                   encoding="utf-8", env={**os.environ, "MP_OUT": str(tmp)})
if r.returncode:
    print(r.stdout[-500:], r.stderr[-2000:]); sys.exit(1)
for ln in r.stdout.splitlines():
    if "ОШИБКА" in ln:
        print(ln)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=r"C:/Program Files/Google/Chrome/Application/chrome.exe")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(1200)
    for name in names:
        k = pg.evaluate("n=>[...document.querySelectorAll('section.slide')].findIndex(s=>s.querySelector('[data-rep=\"'+n+'\"]'))", name)
        if k < 0:
            print("нет вёрстки/слайда", name); continue
        pg.evaluate("""k=>{const S=[...document.querySelectorAll('section.slide')];S.forEach(s=>s.classList.remove('on'));S[k].classList.add('on');
            window.dispatchEvent(new Event('resize'))}""", k)
        pg.add_style_tag(content='.step{opacity:1!important;transform:none!important}')
        pg.wait_for_timeout(900)
        shot = OUT / f"_{name}.png"
        pg.locator(f'.slide.on [data-rep="{name}"] .mprepc').screenshot(path=str(shot))
        a = Image.open(D / "_mp_src" / f"{name}.png").convert("RGB")
        c2 = Image.open(shot).convert("RGB"); c2 = c2.resize((1672, round(c2.height * 1672 / c2.width)))
        c = Image.new("RGB", (1672, a.height + 16 + c2.height), "red"); c.paste(a, (0, 0)); c.paste(c2, (0, a.height + 16))
        c.thumbnail((1500, 1800)); c.save(OUT / f"{name}.jpg", quality=85); shot.unlink()
        print("ok", name, "слайд", k + 1)
    b.close()
tmp.unlink()
