"""python decks/_vrrp_build.py → самодостаточная лекция vrrp.html."""
from pathlib import Path
import re
import json
import _sw_lib as L
import _pt_kit as K
import _vrrp_theme

HERE=Path(__file__).parent

LIVE_JS=r'''
document.querySelectorAll('[data-timer]').forEach(function(box){
 function update(){var p=+box.querySelector('[data-priority-input]').value,a=+box.querySelector('[data-advert]').value,st=(256-p)*a/256;box.querySelector('[data-priority]').textContent=p;box.querySelector('[data-mdi]').textContent='MDI = '+(3*a+st).toFixed(3).replace('.',',')+' с';box.querySelector('[data-skew]').textContent='ST = '+st.toFixed(6).replace('.',',')+' с';}
 box.addEventListener('input',update);update();
});
'''

def main():
    import _vrrp_deck, _vrrp_final
    L.SL.clear();_vrrp_deck.MAP.clear()
    _vrrp_deck.build();_vrrp_final.build()
    mapping=list(_vrrp_deck.MAP)+[{'slide':len(L.SL),'pptx':0,'title':'Финал · Вопросы'}]
    (HERE/'_vrrp_assets/slide-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf8')
    cli=(HERE/'_vrrp_cli.js').read_text(encoding='utf8') if (HERE/'_vrrp_cli.js').exists() else ''
    K.build('vrrp.html','VRRP — избыточность на уровне L3','th-vrrp','',_vrrp_theme.css(),list(L.SL),extra_js=LIVE_JS+cli)
    p=HERE/'vrrp.html';h=p.read_text(encoding='utf8')
    module=(HERE.parent/'.claude/skills/deck-builder/reference/draw-edit-module.html').read_text(encoding='utf8')
    module=module.replace('.slide.active','.slide.on').replace("querySelector('.wrap')","querySelector('.sc')")
    # Перо хранит пометки только в памяти; темы токенов согласованы с основной декой.
    module=module.replace('--terra','--cy').replace('--cyan','--mg').replace('--wheat','--cy2').replace('--void','--bg0')
    module=module.replace("addEventListener('keydown',e=>{","addEventListener('keydown',e=>{\n    if(e.target&&/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;")
    h=h.replace('</head>','<script>if(new URLSearchParams(location.search).has("review"))document.documentElement.dataset.review="1";</script><style>html[data-review] *,html[data-review] *::before,html[data-review] *::after{animation:none!important;transition:none!important}</style></head>')
    h=h.replace('</body>',module+'\n</body>')
    p.write_text(h,encoding='utf8')
    print('VRRP sources:',len(_vrrp_deck.MAP),'screens')

if __name__=='__main__':main()
