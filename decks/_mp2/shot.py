# -*- coding: utf-8 -*-
"""python -X utf8 _mp2/shot.py _mp2_sN  → собрать только этот модуль во временный файл и снять все его слайды
(все шаги раскрыты, сцены на последнем шаге) в _mp2/shots/_mp2_sN/NNN.png + лист sheet.png. Ошибки JS — в выводе."""
import os, sys, subprocess, tempfile, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image
D = pathlib.Path(__file__).resolve().parent.parent
mod = sys.argv[1]
out = D / "_mp2" / "shots" / mod; out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*.png"): f.unlink()
tmp = pathlib.Path(tempfile.gettempdir()) / f"mp2_{mod}_{os.getpid()}.html"
r = subprocess.run([sys.executable, "-X", "utf8", str(D / "_mp2_build.py")], cwd=D, capture_output=True, text=True, encoding="utf-8",
                   env={**os.environ, "MP2_OUT": str(tmp), "MP2_MODULES": mod})
print(r.stdout[-400:], r.stderr[-3000:])
if r.returncode: sys.exit(1)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:/Program Files/Google/Chrome/Application/chrome.exe")
    pg = b.new_page(viewport={"width": 1600, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(1200)
    n = pg.evaluate("document.querySelectorAll('.slide').length"); files = []
    for k in range(1, n + 1):
        pg.evaluate("""k=>{const S=[...document.querySelectorAll('.slide')];S.forEach(s=>s.classList.remove('on'));
          const s=S[k-1];s.classList.add('on');s.querySelectorAll('.step').forEach(e=>e.classList.add('vis'));
          s.querySelectorAll('.scene').forEach(sc=>{const n=+sc.dataset.n;sc.querySelectorAll('[data-ph]').forEach(e=>{
            const at=+e.dataset.ph;const only=e.hasAttribute('data-ph-only');e.classList.toggle('on',only?at===n-1:true)});
            sc.querySelectorAll('[data-cap]').forEach(c=>c.style.display=(+c.dataset.cap===n-1)?'':'none')});
          document.getElementById('sname').textContent=s.dataset.label;}""", k)
        pg.wait_for_timeout(350)
        over = pg.evaluate("k=>{const m=document.querySelectorAll('.slide')[k-1].querySelector('.m2in');return m?m.scrollHeight-m.clientHeight:0}", k)
        f = out / f"{k:03d}.png"; pg.screenshot(path=str(f)); files.append(f)
        if over > 4: print("ПЕРЕПОЛНЕНИЕ слайд", k, "на", over, "px")
    b.close()
print("слайдов", n, "ошибки JS", errs)
tmp.unlink()
ims = [Image.open(f).resize((800, 450)) for f in files]
if ims:
    s = Image.new("RGB", (1600, 450 * ((len(ims) + 1) // 2)), "white")
    for i, im in enumerate(ims): s.paste(im, ((i % 2) * 800, (i // 2) * 450))
    s.save(out / "sheet.png"); print("лист:", out / "sheet.png")
