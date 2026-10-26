import sys, os
sys.path.insert(0, 'decks')
import _m4_replib as R
n = sys.argv[1]
S = 'C:/Users/anank/AppData/Local/Temp/claude/D----------------claude-worktrees-nifty-morse-f453a5/f66896ac-7ff7-4cfc-b481-1a12e6aff646/scratchpad/rep/'
open(S + 'prev_' + n + '.html', 'w', encoding='utf8').write('<html><head><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono&display=swap" rel=stylesheet><style>.ab{position:absolute}</style></head><body style=margin:0;background:#000>' + R.rep_html(n).replace('class="step"', '') + '</body></html>')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    try:
        b = p.chromium.launch()
    except Exception:
        b = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
    pg = b.new_page(viewport={'width': 1672, 'height': 941})
    pg.goto('file:///' + S + 'prev_' + n + '.html')
    pg.wait_for_timeout(1500)
    pg.screenshot(path=S + n + '.png')
    b.close()
