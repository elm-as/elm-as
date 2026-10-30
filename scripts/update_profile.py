"""Orchestrateur global de génération des assets SVG du profil GitHub elm-as.

Régénère de manière déterministe tous les panneaux visuels dans assets/ :
- identité & architecture : header.svg, daloa.svg, roadmap.svg, stack.svg, footer.svg
- télémétrie & projets   : stats.svg, monthly.svg, breakdown.svg, tierlist.svg
- activité GitHub live   : contributions.svg (via l'API publique sans token)

Exécution :
    python scripts/update_profile.py
"""

from __future__ import annotations

from pathlib import Path

from profile_config import (
    DALOA_INFRA_MODULES,
    DALOA_PILLARS,
    DOMAIN_SLICES_2026,
    LANGUAGE_SLICES_2026,
    MONTHLY_SPEC_2026,
    PORTFOLIO_BANDS,
    ROADMAP_STAGES,
    STACK_COLUMNS,
    STATS_CARDS_2026,
)
from svg_analytics import (
    render_breakdown_svg,
    render_monthly_chart_svg,
    render_portfolio_matrix_svg,
    render_stats_cards_svg,
)
from svg_identity import (
    render_daloa_ecosystem_svg,
    render_footer_svg,
    render_header_svg,
    render_roadmap_svg,
    render_stack_svg,
)
from update_grid import update_contributions_grid

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def build_static_svg_manifest() -> dict[str, str]:
    """Assemble la table complète des fichiers SVG statiques à écrire sur disque."""
    return {
        "header.svg": render_header_svg(),
        "daloa.svg": render_daloa_ecosystem_svg(DALOA_PILLARS, DALOA_INFRA_MODULES),
        "roadmap.svg": render_roadmap_svg(ROADMAP_STAGES),
        "stack.svg": render_stack_svg(STACK_COLUMNS),
        "stats.svg": render_stats_cards_svg(STATS_CARDS_2026),
        "monthly.svg": render_monthly_chart_svg(MONTHLY_SPEC_2026),
        "breakdown.svg": render_breakdown_svg(LANGUAGE_SLICES_2026, DOMAIN_SLICES_2026),
        "tierlist.svg": render_portfolio_matrix_svg(PORTFOLIO_BANDS),
        "footer.svg": render_footer_svg(),
    }


def write_svg_assets(manifest: dict[str, str], target_dir: Path) -> None:
    """Écrit chaque fichier SVG encodé en UTF-8 dans le dossier cible."""
    target_dir.mkdir(parents=True, exist_ok=True)
    for filename, svg_content in manifest.items():
        output_path = target_dir / filename
        output_path.write_text(svg_content + "\n", encoding="utf-8")
        size_kb = len(svg_content.encode("utf-8")) / 1024.0
        print(f"[OK] {filename:<18} ({size_kb:.1f} Ko)")


def update_all_profile_assets() -> None:
    """Exécute la régénération intégrale des graphiques et du calendrier GitHub."""
    print("=== Régénération complète du profil GitHub (elm-as) ===")
    manifest = build_static_svg_manifest()
    write_svg_assets(manifest, ASSETS_DIR)
    update_contributions_grid()
    print("\n[SUCCÈS] Tous les panneaux SVG sont synchronisés, propres et sans métadonnées tierces.")


if __name__ == "__main__":
    update_all_profile_assets()
