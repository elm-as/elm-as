"""Génère assets/contributions.svg à partir du calendrier public de contributions GitHub.

Sans token, sans GitHub Actions : un simple `python scripts/update_grid.py`,
puis commit du fichier assets/contributions.svg.
"""
import re
import sys
import urllib.request
from pathlib import Path

USER = "elm-as"
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path(__file__).resolve().parent.parent / "assets" / "contributions.svg"

PALETTE = ["#18233d", "#1e3a6e", "#2563b8", "#4b91f1", "#9ecbff"]
CELL, GAP = 12, 3
PITCH = CELL + GAP


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(html: str):
    cells = re.findall(
        r'data-date="(\d{4}-\d\d-\d\d)"\s+id="contribution-day-component-(\d+)-(\d+)"\s+data-level="(\d)"',
        html,
    )
    if not cells:
        sys.exit("Calendrier introuvable : GitHub a peut-être changé son HTML.")
    total = re.search(r"([\d,\s\u202f\u00a0]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
    total_txt = re.sub(r"\D", "", total.group(1)) if total else ""
    return [(d, int(r), int(c), int(l)) for d, r, c, l in cells], total_txt


def render(cells, total_txt: str) -> str:
    weeks = max(c for _, _, c, _ in cells) + 1
    grid_w = weeks * PITCH - GAP
    left, top = 30, 62
    width = grid_w + 2 * left
    height = top + 7 * PITCH + 52
    title = "Contributions des 12 derniers mois"
    subtitle = f"{int(total_txt):,}".replace(",", " ") + " contributions" if total_txt else ""

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f"font-family=\"'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif\" role=\"img\" "
        f'aria-label="{title}">',
        "<style>@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}"
        ".d{animation:pop .5s ease-out backwards;transform-box:fill-box;transform-origin:center}</style>",
        f'<rect width="{width}" height="{height}" rx="16" fill="#111a2e" stroke="#1f2a44"/>',
        f'<text x="{left}" y="36" font-size="15" font-weight="700" fill="#ffffff">{title}</text>',
    ]
    if subtitle:
        out.append(f'<text x="{width - left}" y="36" font-size="13" text-anchor="end" fill="#8b98b0">{subtitle}</text>')
    for date, r, c, lvl in cells:
        x, y = left + c * PITCH, top + r * PITCH
        out.append(
            f'<rect class="d" style="animation-delay:{c * 0.025:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="3" fill="{PALETTE[lvl]}"><title>{date}</title></rect>'
        )
    ly = top + 7 * PITCH + 26
    out.append(f'<text x="{left}" y="{ly + 10}" font-size="12" fill="#8b98b0">Moins</text>')
    for i, col in enumerate(PALETTE):
        out.append(f'<rect x="{left + 46 + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{col}"/>')
    out.append(f'<text x="{left + 46 + 5 * PITCH + 4}" y="{ly + 10}" font-size="12" fill="#8b98b0">Plus</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    cells, total = parse(fetch(URL))
    OUT.write_text(render(cells, total), encoding="utf-8")
    print(f"{len(cells)} jours écrits dans {OUT}")
