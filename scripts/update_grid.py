"""Génère assets/contributions.svg à partir du calendrier public de contributions GitHub.

Sans token, sans GitHub Actions :
    python scripts/update_grid.py
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

from profile_config import ElmasPalette, FONT_MONO, FONT_SANS, PALETTE

GITHUB_USER = "elm-as"
CONTRIBUTIONS_URL = f"https://github.com/users/{GITHUB_USER}/contributions"
OUTPUT_SVG_PATH = Path(__file__).resolve().parent.parent / "assets" / "contributions.svg"

COLOR_SCALE = ("#16223b", "#1d3b6e", "#2563eb", "#4f9cf9", "#93c5fd")
MONTH_NAMES_FR = (
    "Janv", "Févr", "Mars", "Avr", "Mai", "Juin",
    "Juil", "Août", "Sept", "Oct", "Nov", "Déc",
)
CELL_SIZE = 14
CELL_GAP = 3
CELL_PITCH = CELL_SIZE + CELL_GAP


@dataclass(frozen=True)
class ContributionCell:
    """Cellule journalière issue du calendrier public GitHub."""

    date: str
    row: int
    col: int
    level: int


@dataclass(frozen=True)
class ContributionsDataset:
    """Jeu de données consolidé des 12 derniers mois de contributions."""

    cells: tuple[ContributionCell, ...]
    total_contributions: int


def fetch_contributions_html(profile_url: str) -> str:
    """Récupère le fragment HTML public des contributions GitHub avec gestion d'erreur explicite."""
    request = urllib.request.Request(profile_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as error:
        sys.exit(f"[ERREUR] Impossible de récupérer les contributions GitHub : {error}")


def parse_contributions_data(html_content: str) -> ContributionsDataset:
    """Extrait les cellules datées et le compteur annuel depuis le HTML GitHub."""
    cell_pattern = (
        r'data-date="(\d{4}-\d\d-\d\d)"\s+'
        r'id="contribution-day-component-(\d+)-(\d+)"\s+'
        r'data-level="(\d)"'
    )
    raw_cells = re.findall(cell_pattern, html_content)
    if not raw_cells:
        sys.exit("[ERREUR] Structure HTML GitHub modifiée : aucune cellule détectée.")

    total_pattern = r"([\d,\s\u202f\u00a0]+)\s+contributions?\s+in\s+the\s+last\s+year"
    total_match = re.search(total_pattern, html_content)
    digits = re.sub(r"\D", "", total_match.group(1)) if total_match else "0"
    total_count = int(digits) if digits.isdigit() else 0

    cells = tuple(
        ContributionCell(date=date_str, row=int(row), col=int(col), level=min(4, int(level)))
        for date_str, row, col, level in raw_cells
    )
    return ContributionsDataset(cells=cells, total_contributions=total_count)


def extract_month_ticks(cells: tuple[ContributionCell, ...], grid_x: int) -> tuple[tuple[int, str], ...]:
    """Calcule la position horizontale des étiquettes de mois sans chevauchement."""
    ordered = sorted(cells, key=lambda item: item.date)
    raw_ticks: list[tuple[int, str]] = []
    seen_month = ""

    for cell in ordered:
        year_month = cell.date[:7]
        if year_month == seen_month:
            continue
        seen_month = year_month
        month_index = int(cell.date[5:7]) - 1
        pos_x = grid_x + cell.col * CELL_PITCH
        raw_ticks.append((pos_x, MONTH_NAMES_FR[month_index]))

    if len(raw_ticks) >= 2 and (raw_ticks[1][0] - raw_ticks[0][0]) < 30:
        raw_ticks = raw_ticks[1:]

    filtered: list[tuple[int, str]] = []
    for pos_x, label in raw_ticks:
        if not filtered or (pos_x - filtered[-1][0]) >= 30:
            filtered.append((pos_x, label))
    return tuple(filtered)


def render_contributions_svg(
    dataset: ContributionsDataset,
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère le calendrier annuel unifié en 1000 px avec mois, jours et accessibilité."""
    if not dataset.cells:
        return ""

    width, height = 1000, 244
    total_weeks = max(cell.col for cell in dataset.cells) + 1
    grid_w = total_weeks * CELL_PITCH - CELL_GAP
    block_start_x = (width - (38 + grid_w)) // 2
    grid_x = block_start_x + 38
    grid_y = 78

    active_days = sum(1 for cell in dataset.cells if cell.level > 0)
    formatted_total = f"{dataset.total_contributions:,}".replace(",", " ")
    summary_text = f"{formatted_total} contributions · {active_days} jours actifs"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_SANS}" role="img" '
        'aria-label="Calendrier des contributions des 12 derniers mois">',
        "<style>"
        f".mono{{font-family:{FONT_MONO};font-variant-numeric:tabular-nums}}"
        "@media (prefers-reduced-motion: no-preference){"
        "@keyframes pop{from{opacity:0;transform:scale(.45)}to{opacity:1;transform:scale(1)}}"
        ".d{animation:pop .45s ease-out backwards;transform-box:fill-box;transform-origin:center}"
        "}"
        "</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
        f'<text x="{block_start_x}" y="38" font-size="17" font-weight="700" fill="{palette.text_primary}">Activité des 12 derniers mois</text>',
        f'<text class="mono" x="{grid_x + grid_w}" y="38" font-size="13" font-weight="600" text-anchor="end" fill="{palette.signal_active}">{escape(summary_text)}</text>',
    ]

    for tick_x, month_label in extract_month_ticks(dataset.cells, grid_x):
        parts.append(f'<text x="{tick_x}" y="66" font-size="11.5" fill="{palette.text_muted}">{escape(month_label)}</text>')

    for row_idx, day_label in ((1, "Lun"), (3, "Mer"), (5, "Ven")):
        day_y = grid_y + row_idx * CELL_PITCH + 11
        parts.append(f'<text x="{block_start_x}" y="{day_y}" font-size="11" fill="{palette.text_dim}">{day_label}</text>')

    for cell in dataset.cells:
        pos_x = grid_x + cell.col * CELL_PITCH
        pos_y = grid_y + cell.row * CELL_PITCH
        delay = cell.col * 0.018
        parts.append(
            f'<rect class="d" style="animation-delay:{delay:.3f}s" '
            f'x="{pos_x}" y="{pos_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="3.2" fill="{COLOR_SCALE[cell.level]}"><title>{escape(cell.date)}</title></rect>'
        )

    legend_y = grid_y + 7 * CELL_PITCH + 14
    first_date = min(cell.date for cell in dataset.cells)
    last_date = max(cell.date for cell in dataset.cells)
    parts.append(
        f'<text class="mono" x="{block_start_x}" y="{legend_y + 11}" font-size="11.5" fill="{palette.text_dim}">'
        f"Période : {escape(first_date)} → {escape(last_date)}</text>"
    )

    legend_right = grid_x + grid_w
    swatches_w = len(COLOR_SCALE) * CELL_PITCH - CELL_GAP
    moins_x = legend_right - swatches_w - 40
    parts.append(f'<text x="{moins_x}" y="{legend_y + 11}" font-size="11.5" fill="{palette.text_muted}" text-anchor="end">Moins</text>')
    for idx, color in enumerate(COLOR_SCALE):
        box_x = moins_x + 8 + idx * CELL_PITCH
        parts.append(f'<rect x="{box_x}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="3.2" fill="{color}"/>')
    parts.append(f'<text x="{legend_right}" y="{legend_y + 11}" font-size="11.5" fill="{palette.text_muted}" text-anchor="end">Plus</text>')
    parts.append("</svg>")
    return "".join(parts)


def update_contributions_grid() -> None:
    """Met à jour localement assets/contributions.svg depuis le profil GitHub public."""
    html_content = fetch_contributions_html(CONTRIBUTIONS_URL)
    dataset = parse_contributions_data(html_content)
    svg_markup = render_contributions_svg(dataset)
    OUTPUT_SVG_PATH.write_text(svg_markup, encoding="utf-8")
    print(
        f"[OK] {OUTPUT_SVG_PATH.name} régénéré ({len(dataset.cells)} jours, "
        f"{dataset.total_contributions} contributions)"
    )


if __name__ == "__main__":
    update_contributions_grid()
