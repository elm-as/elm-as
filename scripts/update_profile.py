"""Script de mise à jour globale du profil GitHub elm-as.

Met à jour l'ensemble des métriques et des graphiques SVG du profil en local :
- assets/contributions.svg (calendrier animé 12 mois via l'API publique)
- assets/monthly.svg (commits par mois pour 2026, incluant octobre)
- assets/stats.svg (cartes clés : commits, jours actifs, volume de code, série)
- assets/tierlist.svg (projets majeurs et volume de commits)

Sans token, sans carte bancaire, sans GitHub Actions :
    python scripts/update_profile.py
"""

from __future__ import annotations

from pathlib import Path
from update_grid import update_contributions_grid

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
STATS_SVG_PATH = ASSETS_DIR / "stats.svg"
MONTHLY_SVG_PATH = ASSETS_DIR / "monthly.svg"
TIERLIST_SVG_PATH = ASSETS_DIR / "tierlist.svg"


def render_monthly_chart_svg(
    monthly_data: list[tuple[str, int]],
    peak_month_name: str,
    peak_count: int,
    total_count: int,
) -> str:
    """Génère le graphique SVG des commits mensuels pour l'année en cours."""
    width, height = 1000, 330
    baseline_y = 270.0
    max_bar_height = 190.0
    bar_width = 58.0
    pitch = 92.0

    total_span = (len(monthly_data) - 1) * pitch + bar_width
    start_x = (width - total_span) / 2.0
    scale = max_bar_height / peak_count if peak_count > 0 else 1.0

    percentage = round((peak_count / total_count * 100)) if total_count > 0 else 0
    subtitle = (
        f"{peak_month_name} : {peak_count} commits, soit {percentage} % "
        f"de l'année ({total_count} commits au total)"
    )

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="\'Segoe UI\', -apple-system, \'Helvetica Neue\', Arial, sans-serif">',
        '<defs>',
        '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#58a6ff"/>'
        '<stop offset="1" stop-color="#3178c6"/>'
        '</linearGradient>',
        '<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#3b5b8f"/>'
        '<stop offset="1" stop-color="#23385c"/>'
        '</linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" rx="16" fill="#111a2e" stroke="#1f2a44"/>',
        '<text x="32" y="44" font-size="19" font-weight="700" fill="#fff">Commits par mois</text>',
        f'<text x="32" y="68" font-size="14" fill="#8b98b0">{subtitle}</text>',
        '<line x1="32" x2="968" y1="175.0" y2="175.0" stroke="#1f2a44" stroke-dasharray="3 5"/>',
        '<line x1="32" x2="968" y1="80" y2="80" stroke="#1f2a44" stroke-dasharray="3 5"/>',
        '<line x1="32" x2="968" y1="270" y2="270" stroke="#1f2a44"/>',
    ]

    for index, (month_name, count) in enumerate(monthly_data):
        pos_x = start_x + index * pitch
        center_x = pos_x + bar_width / 2.0
        is_peak = count == peak_count and count > 0

        gradient = "url(#b)" if is_peak else "url(#bd)"
        text_fill = "#fff" if is_peak else "#e6edf3"
        bar_height = max(3.0, round(count * scale, 1)) if count > 0 else 3.0
        bar_y = baseline_y - bar_height

        elements.append(
            f'<rect x="{pos_x:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" '
            f'height="{bar_height:.1f}" rx="8" fill="{gradient}"/>'
        )
        elements.append(
            f'<text x="{center_x:.1f}" y="{bar_y - 10:.1f}" font-size="15" '
            f'font-weight="700" fill="{text_fill}" text-anchor="middle">{count}</text>'
        )
        elements.append(
            f'<text x="{center_x:.1f}" y="296" font-size="14" '
            f'fill="#8b98b0" text-anchor="middle">{month_name}</text>'
        )

    elements.append("</svg>")
    return "".join(elements)


def render_stats_cards_svg(
    commits_total: int,
    active_days: int,
    code_balance: str,
    max_streak_days: int,
) -> str:
    """Génère les 4 cartes synthétiques annuelles en SVG."""
    width, height = 985, 132
    card_width, gap = 235, 20

    cards_data = [
        (str(commits_total), "commits en 2026", "287 rien qu'en septembre"),
        (str(active_days), "jours actifs", "42 % le week-end"),
        (code_balance, "lignes de code (solde)", "72 % de TypeScript"),
        (f"{max_streak_days} jours", "plus longue série", "plutôt le matin"),
    ]

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="\'Segoe UI\', -apple-system, \'Helvetica Neue\', Arial, sans-serif">',
        '<defs></defs>',
    ]

    for index, (value, label, detail) in enumerate(cards_data):
        pos_x = index * (card_width + gap)
        elements.append(
            f'<rect x="{pos_x}" y="0" width="{card_width}" height="{height}" '
            f'rx="14" fill="#111a2e" stroke="#1f2a44"/>'
        )
        elements.append(f'<rect x="{pos_x}" y="22" width="4" height="40" rx="2" fill="#58a6ff"/>')
        elements.append(f'<text x="{pos_x + 24}" y="58" font-size="38" font-weight="700" fill="#fff">{value}</text>')
        elements.append(f'<text x="{pos_x + 24}" y="86" font-size="15" fill="#e6edf3">{label}</text>')
        elements.append(f'<text x="{pos_x + 24}" y="110" font-size="13" fill="#8b98b0">{detail}</text>')

    elements.append("</svg>")
    return "".join(elements)


def update_tierlist_metrics() -> None:
    """Synchronise les compteurs de commits des projets phares dans tierlist.svg."""
    if not TIERLIST_SVG_PATH.exists():
        return

    content = TIERLIST_SVG_PATH.read_text(encoding="utf-8")
    replacements = [
        ("196 commits · +104 k", "217 commits · +104 k"),
        ("121 commits · +48 k", "129 commits · +48 k"),
        ("82 commits · +3,7 k", "90 commits · +3,7 k"),
        ("18 commits · +2,6 k", "19 commits · +2,6 k"),
    ]
    for old_text, new_text in replacements:
        if old_text in content:
            content = content.replace(old_text, new_text)

    TIERLIST_SVG_PATH.write_text(content, encoding="utf-8")
    print(f"[OK] Métriques de tierlist.svg synchronisées")


def update_all_profile_assets() -> None:
    """Orchestre la mise à jour complète de tous les graphiques du profil."""
    print("=== Mise à jour du profil GitHub (elm-as) ===")

    # 1. Grille de contributions annuelle
    update_contributions_grid()

    # 2. Commits par mois 2026 (Janv à Oct)
    monthly_stats_2026 = [
        ("Janv", 156),
        ("Févr", 0),
        ("Mars", 2),
        ("Avr", 6),
        ("Mai", 122),
        ("Juin", 30),
        ("Juil", 73),
        ("Août", 142),
        ("Sept", 287),
        ("Oct", 49),
    ]
    monthly_svg = render_monthly_chart_svg(
        monthly_data=monthly_stats_2026,
        peak_month_name="Septembre",
        peak_count=287,
        total_count=867,
    )
    MONTHLY_SVG_PATH.write_text(monthly_svg, encoding="utf-8")
    print(f"[OK] Graphique mensuel enregistré dans {MONTHLY_SVG_PATH.name} (867 commits)")

    # 3. Cartes de synthèse 2026
    stats_svg = render_stats_cards_svg(
        commits_total=867,
        active_days=76,
        code_balance="+385 k",
        max_streak_days=9,
    )
    STATS_SVG_PATH.write_text(stats_svg, encoding="utf-8")
    print(f"[OK] Cartes de statistiques enregistrées dans {STATS_SVG_PATH.name}")

    # 4. Tier list des projets
    update_tierlist_metrics()

    print("\n[SUCCÈS] Tous les assets sont à jour, sans GitHub Actions ni clé API.")
    print("Tu peux désormais commiter et pousser sur GitHub :")
    print("    git add assets/ README.md scripts/")
    print('    git commit -m "chore: mise à jour des statistiques et de la grille de contributions"')
    print("    git push origin main")


if __name__ == "__main__":
    update_all_profile_assets()
