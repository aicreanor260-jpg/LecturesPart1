# -*- coding: utf-8 -*-
"""Рендер деки в PDF: каждый слайд — отдельная страница по размеру содержимого."""
import io, pathlib, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
OUTDIR = HERE.parent / "pdf"
OUTDIR.mkdir(exist_ok=True)

HIDE = """
#nav,#prog,#deco,#ov,#lb,#zl,#tm-btn,#tm-ov,#cnt,.navb{display:none!important}
*{animation-duration:.001s!important;animation-delay:0s!important;transition:none!important}
"""

G6_FLOW = """
html,body{height:auto!important;overflow:visible!important}
#stage{position:static!important;display:block!important}
#deck{width:1920px!important;height:auto!important;min-height:1080px!important;transform:none!important}
.slide{position:static!important}
.slide:not(.on){display:none!important}
.slide.on{display:flex!important;height:auto!important;min-height:1080px!important}
.fill,.sv,.sv2,.sv2 .top,.sv2 .bot{min-height:0!important;flex:none!important}
.sv2 .top{height:auto!important}
.sv-steps{overflow:visible!important;max-height:none!important}
.bgl{position:absolute!important;inset:0!important}
"""

G7_FLOW = """
html,body{height:auto!important;overflow:visible!important}
.slide{position:static!important;inset:auto!important}
.slide:not(.on){display:none!important}
.slide.on{display:block!important;background:var(--bg)!important}
.sc{height:auto!important;min-height:1030px;overflow:visible!important;padding-bottom:40px!important}
"""

def shoot_g6(page, outdir):
    page.add_style_tag(content=HIDE + G6_FLOW)
    n = page.evaluate("document.querySelectorAll('.slide').length")
    page.keyboard.press("Home")
    page.wait_for_timeout(300)
    files = []
    for k in range(n):
        if k:
            page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
        for _ in range(16):
            did = page.evaluate("""()=>{const s=document.querySelector('.slide.on');if(!s)return false;
                const b=[...s.querySelectorAll('button')].find(x=>/Показать решение|Показать всё|Показать все/i.test(x.textContent));
                if(b){b.click();return true}return false}""")
            if not did:
                break
            page.wait_for_timeout(130)
        page.wait_for_timeout(220)
        p = outdir / f"{k+1:03d}.png"
        page.locator("#deck").screenshot(path=str(p))
        files.append(p)
        print("  слайд", k + 1, "/", n, flush=True)
    return files

def shoot_g7(page, outdir):
    page.add_style_tag(content=HIDE + G7_FLOW)
    page.evaluate("()=>document.querySelectorAll('.slide').forEach(s=>s.classList.add('man'))")
    n = page.evaluate("document.querySelectorAll('.slide').length")
    files = []
    for k in range(n):
        page.evaluate("k=>document.querySelectorAll('.ovi')[k].click()", k)
        page.wait_for_timeout(150)
        mx = page.evaluate("()=>document.querySelector('.slide.on')._max||0")
        for _ in range(mx):
            page.evaluate("()=>document.querySelector('#b-next').click()")
            page.wait_for_timeout(45)
        page.evaluate("""()=>{const s=document.querySelector('.slide.on');
            if(!s||!s.querySelector('.dhdr')||s.querySelector('.tiplist'))return;
            const ul=document.createElement('div');ul.className='tiplist';
            ul.style.cssText='margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:6px 28px;font-size:.86rem;line-height:1.4';
            s.querySelectorAll('.dfld').forEach(f=>{const n=f.querySelector('b').textContent,d=f.querySelector('.tip').textContent;
              const row=document.createElement('div');row.innerHTML='<b style="color:#fff">'+n+'</b> — '+d;ul.appendChild(row)});
            s.querySelector('.dhdrcard').after(ul)}""")
        page.wait_for_timeout(450)
        p = outdir / f"{k+1:03d}.png"
        page.locator(".slide.on").screenshot(path=str(p))
        files.append(p)
        print("  слайд", k+1, "/", n, flush=True)
    return files

def to_pdf(files, dest, dpi=96):
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        ims.append(im)
    ims[0].save(dest, "PDF", save_all=True, append_images=ims[1:], resolution=dpi)
    print("PDF:", dest, dest.stat().st_size // 1024, "КБ")

def run(deck, kind, title):
    shots = OUTDIR / ("_" + kind)
    shots.mkdir(exist_ok=True)
    for old in shots.glob("*.png"): old.unlink()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto((HERE / deck).as_uri(), wait_until="load")
        page.wait_for_timeout(1500)
        files = (shoot_g6 if kind == "g6" else shoot_g7)(page, shots)
        b.close()
    to_pdf(files, OUTDIR / title)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("g6", "both"):
        print("Глава 6…"); run("glava6-podseti-ip.html", "g6", "Глава 6 — разбиение IP-сетей на подсети.pdf")
    if which in ("g7", "both"):
        print("Глава 7…"); run("glava7-application.html", "g7", "Глава 7 — уровень приложений.pdf")
