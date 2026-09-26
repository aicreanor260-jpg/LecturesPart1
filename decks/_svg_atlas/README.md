# Атлас SVG

Собирает все SVG со всех лекций из `decks/index.html` в один файл `decks/svg-atlas.html`
(вкладки «По лекциям» и «По темам», скачивание каждого SVG).

1. Снять SVG с деки (headless Chrome листает слайды):  `python capture.py glava9-network cap/glava9-network.json`
2. Собрать атлас: `python build.py`

Темы и ключевые слова — список `TOPICS` в `build.py`.
