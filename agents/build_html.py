"""
Embute a base preparada no template e gera o index.html (arquivo único, pronto para o GitHub Pages).

Uso:
    python build_html.py src/dashboard.template.html data/porsche_dashboard_base.json index.html
"""

import sys
from pathlib import Path

MARCADOR = "/*__DATA__*/[]"


def main() -> int:
    template, dados, saida = (Path(a) for a in sys.argv[1:4])
    html = template.read_text(encoding="utf-8")
    if MARCADOR not in html:
        print(f"ERRO: marcador {MARCADOR} não encontrado no template", file=sys.stderr)
        return 1
    # "</" dentro do JSON fecharia a tag <script>; escapa por segurança
    json_txt = dados.read_text(encoding="utf-8").replace("</", "<\\/")
    saida.write_text(html.replace(MARCADOR, json_txt), encoding="utf-8")
    print(f"OK -> {saida} ({saida.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
