import json, sys, time, pathlib
from playwright.sync_api import sync_playwright

DECKS = pathlib.Path(r"D:\Преза лекций\decks")
OUT = pathlib.Path(sys.argv[2])
name = sys.argv[1]

JS_CAPTURE = r"""
() => {
  try { document.getAnimations().forEach(a => { const t = a.effect && a.effect.getComputedTiming && a.effect.getComputedTiming();
    if (t && isFinite(t.endTime)) { try { a.finish(); } catch(e){} } }); } catch(e) {}
  const PROPS = ['fill','fill-opacity','stroke','stroke-width','stroke-opacity','stroke-dasharray',
    'stroke-linecap','stroke-linejoin','opacity','font-family','font-size','font-weight','font-style',
    'letter-spacing','text-anchor','dominant-baseline','visibility','display','marker-start','marker-end',
    'marker-mid','filter','clip-path','mask','transform','transform-origin','transform-box','paint-order'];
  const vw = innerWidth, vh = innerHeight;
  const slides = [...document.querySelectorAll('section.slide, .slide')].filter(s => !s.parentElement.closest('.slide'));
  const isVis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && r.left < vw && r.top < vh && cs.visibility !== 'hidden'; };
  let active = slides.findIndex(s => isVis(s) && parseFloat(getComputedStyle(s).opacity) > 0.5);
  if (active < 0) return null;
  const slide = slides[active];
  const head = slide.querySelector('h1,h2,h3,.title,.ttl,[class*=title]');
  const title = (slide.getAttribute('data-label') || (head && head.innerText) || '').trim().replace(/\s+/g,' ').slice(0,140);
  const svgs = [...slide.querySelectorAll('svg')].filter(s => !s.parentElement.closest('svg'));
  const res = [];
  svgs.forEach((svg, idx) => {
    const r = svg.getBoundingClientRect();
    if (r.width < 40 && r.height < 40) return;
    if (!isVis(svg)) return;
    const clone = svg.cloneNode(true);
    const src = [svg, ...svg.querySelectorAll('*')], dst = [clone, ...clone.querySelectorAll('*')];
    src.forEach((el, i) => {
      const cs = getComputedStyle(el), d = dst[i];
      if (el.tagName.toLowerCase() === 'foreignobject') return;
      let st = '';
      for (const p of PROPS) { let v = cs.getPropertyValue(p); if (!v) continue;
        if (p === 'transform' && v === 'none') continue;
        if ((p === 'transform-origin' || p === 'transform-box') && cs.getPropertyValue('transform') === 'none') continue;
        if (p === 'display' && v !== 'none') continue;
        if (['filter','clip-path','mask','marker-start','marker-end','marker-mid'].includes(p) && v === 'none') continue;
        st += p + ':' + v + ';'; }
      // colour for currentColor
      st += 'color:' + cs.color + ';';
      if (el.closest('foreignObject') && el.closest('foreignObject') !== el) {
        st = ['color','background-color','font-family','font-size','font-weight','padding','border','border-radius','line-height','text-align'].map(p=>p+':'+cs.getPropertyValue(p)).join(';');
      }
      d.setAttribute('style', st);
      d.removeAttribute('class');
    });
    // resolve external <use>
    const defs = [];
    clone.querySelectorAll('use').forEach(u => {
      const h = u.getAttribute('href') || u.getAttribute('xlink:href');
      if (h && h.startsWith('#') && !clone.querySelector(h)) {
        const t = document.querySelector(h); if (t && !defs.includes(t)) defs.push(t);
      }
    });
    if (defs.length) { const d = document.createElementNS('http://www.w3.org/2000/svg','defs');
      defs.forEach(t => d.appendChild(t.cloneNode(true))); clone.insertBefore(d, clone.firstChild); }
    // url(#x) references outside
    if (!clone.getAttribute('viewBox')) clone.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
    clone.setAttribute('width', Math.round(r.width)); clone.setAttribute('height', Math.round(r.height));
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    const bg = (() => { let e = svg; while (e) { const c = getComputedStyle(e).backgroundColor;
      const m = c.match(/rgba?\(([^)]+)\)/); if (m) { const a = m[1].split(',').map(x=>parseFloat(x));
        if (a.length < 4 || a[3] > 0.9) return c; } e = e.parentElement; }
      return getComputedStyle(document.body).backgroundColor || '#fff'; })();
    res.push({idx, w: Math.round(r.width), h: Math.round(r.height), bg,
      text: (svg.textContent || '').replace(/\s+/g,' ').trim().slice(0, 600),
      ids: [...svg.querySelectorAll('[id],[class]')].slice(0,80).map(e => (e.id||'') + ' ' + (e.getAttribute('class')||'')).join(' ').slice(0,600),
      ctx: (svg.closest('figure,div') ? (svg.closest('figure,div').innerText||'') : '').replace(/\s+/g,' ').slice(0,300),
      svg: clone.outerHTML});
  });
  return {active, total: slides.length, title, items: res};
}
"""

def main():
    got = {}  # key (slide, idx) -> item
    titles = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        pg.goto((DECKS / f"{name}.html").as_uri(), wait_until="domcontentloaded", timeout=120000)
        time.sleep(2.5)
        # try dismissing overlays
        last, stuck = -1, 0
        total = None
        for step in range(400):
            data = pg.evaluate(JS_CAPTURE)
            if data:
                total = data["total"]
                titles[data["active"]] = data["title"]
                for it in data["items"]:
                    got[(data["active"], it["idx"])] = it
                if last > 3 and data["active"] < last - 1:
                    break
                if data["active"] == last:
                    stuck += 1
                else:
                    stuck = 0
                last = data["active"]
                if total and last >= total - 1 and stuck >= 3:
                    break
                if stuck >= 8:
                    break
            pg.keyboard.press("ArrowRight")
            time.sleep(3.2 if stuck == 0 else 1.2)
        b.close()
    out = [{"slide": k[0], "title": titles.get(k[0], ""), **v} for k, v in sorted(got.items())]
    OUT.write_text(json.dumps({"deck": name, "total": total, "items": out}, ensure_ascii=False), encoding="utf-8")
    print(name, "slides", total, "reached", last, "svgs", len(out))

main()
