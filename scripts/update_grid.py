"""Génère assets/contributions.svg à partir du calendrier public de contributions GitHub.

Sans token, sans GitHub Actions :
    python scripts/update_grid.py
Puis commit du fichier assets/contributions.svg.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

GITHUB_USER = "elm-as"
CONTRIBUTIONS_URL = f"https://github.com/users/{GITHUB_USER}/contributions"
OUTPUT_SVG_PATH = Path(__file__).resolve().parent.parent / "assets" / "contributions.svg"

COLOR_PALETTE = ["#18233d", "#1e3a6e", "#2563b8", "#4b91f1", "#9ecbff"]
CELL_SIZE = 12
CELL_GAP = 3
CELL_PITCH = CELL_SIZE + CELL_GAP


def fetch_contributions_html(profile_url: str) -> str:
    """Récupère le code HTML de la grille publique de contributions."""
    request = urllib.request.Request(profile_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as error:
        sys.exit(f"Erreur réseau lors de la récupération de la grille : {error}")


def parse_contributions_data(html_content: str) -> tuple[list[tuple[str, int, int, int]], str]:
    """Extrait les coordonnées des cellules et le nombre total de contributions."""
    pattern = (
        r'data-date="(\d{4}-\d\d-\d\d)"\s+'
        r'id="contribution-day-component-(\d+)-(\d+)"\s+'
        r'data-level="(\d)"'
    )
    raw_cells = re.findall(pattern, html_content)
    if not raw_cells:
        sys.exit("Calendrier introuvable : GitHub a modifié la structure de son HTML.")

    total_pattern = r"([\d,\s\u202f\u00a0]+)\s+contributions?\s+in\s+the\s+last\s+year"
    total_match = re.search(total_pattern, html_content)
    total_text = re.sub(r"\D", "", total_match.group(1)) if total_match else ""

    parsed_cells = [
        (date, int(row), int(col), int(level))
        for date, row, col, level in raw_cells
    ]
    return parsed_cells, total_text


def render_contributions_svg(
    cells: list[tuple[str, int, int, int]],
    total_count_text: str,
) -> str:
    """Génère le balisage SVG de la grille de contributions annuelle."""
    if not cells:
        return ""

    total_weeks = max(col for _, _, col, _ in cells) + 1
    grid_width = total_weeks * CELL_PITCH - CELL_GAP
    left_padding, top_padding = 30, 62
    canvas_width = grid_width + 2 * left_padding
    canvas_height = top_padding + 7 * CELL_PITCH + 52

    title = "Contributions des 12 derniers mois"
    subtitle = ""
    if total_count_text and total_count_text.isdigit():
        formatted_total = f"{int(total_count_text):,}".replace(",", " ")
        subtitle = f"{formatted_total} contributions"

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" '
        f'viewBox="0 0 {canvas_width} {canvas_height}" '
        f'font-family="\'Segoe UI\', -apple-system, \'Helvetica Neue\', Arial, sans-serif" role="img" '
        f'aria-label="{title}">',
        '<style>@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}'
        '.d{animation:pop .5s ease-out backwards;transform-box:fill-box;transform-origin:center}</style>',
        f'<rect width="{canvas_width}" height="{canvas_height}" rx="16" fill="#111a2e" stroke="#1f2a44"/>',
        f'<text x="{left_padding}" y="36" font-size="15" font-weight="700" fill="#ffffff">{title}</text>',
    ]

    if subtitle:
        elements.append(
            f'<text x="{canvas_width - left_padding}" y="36" font-size="13" '
            f'text-anchor="end" fill="#8b98b0">{subtitle}</text>'
        )

    for date, row, col, level in cells:
        pos_x = left_padding + col * CELL_PITCH
        pos_y = top_padding + row * CELL_PITCH
        animation_delay = col * 0.025
        elements.append(
            f'<rect class="d" style="animation-delay:{animation_delay:.3f}s" '
            f'x="{pos_x}" y="{pos_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="3" fill="{COLOR_PALETTE[level]}"><title>{date}</title></rect>'
        )

    legend_y = top_padding + 7 * CELL_PITCH + 26
    elements.append(f'<text x="{left_padding}" y="{legend_y + 10}" font-size="12" fill="#8b98b0">Moins</text>')
    for index, color in enumerate(COLOR_PALETTE):
        box_x = left_padding + 46 + index * CELL_PITCH
        elements.append(
            f'<rect x="{box_x}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="3" fill="{color}"/>'
        )

    plus_x = left_padding + 46 + 5 * CELL_PITCH + 4
    elements.append(f'<text x="{plus_x}" y="{legend_y + 10}" font-size="12" fill="#8b98b0">Plus</text>')
    elements.append("</svg>")
    return "".join(elements)


def update_contributions_grid() -> None:
    """Point d'entrée pour la mise à jour de la grille de contributions."""
    html = fetch_contributions_html(CONTRIBUTIONS_URL)
    cells, total_text = parse_contributions_data(html)
    svg_content = render_contributions_svg(cells, total_text)
    OUTPUT_SVG_PATH.write_text(svg_content, encoding="utf-8")
    print(f"[OK] {len(cells)} jours enregistrés dans {OUTPUT_SVG_PATH.name} ({total_text} contributions)")


if __name__ == "__main__":
    update_contributions_grid()

