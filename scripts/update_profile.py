"""Orchestrateur de génération des 4 panneaux SVG épurés du profil GitHub elm-as.

Génère uniquement les visuels essentiels à haute lisibilité :
- assets/header.svg        (identité & console 4 lignes)
- assets/daloa.svg         (architecture de la suite Daloa en production)
- assets/stack.svg         (compétences en 3 colonnes aérées)
- assets/contributions.svg (4 KPIs annuels + calendrier 12 mois unifié)

Exécution :
    python scripts/update_profile.py
"""

from __future__ import annotations

from pathlib import Path

from profile_config import DALOA_INFRA_MODULES, DALOA_PILLARS, STACK_COLUMNS
from svg_identity import (
    render_daloa_ecosystem_svg,
    render_header_svg,
    render_stack_svg,
)
from update_grid import update_contributions_grid

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def build_static_svg_manifest() -> dict[str, str]:
    """Assemble les 3 panneaux SVG statiques essentiels du profil."""
    return {
        "header.svg": render_header_svg(),
        "daloa.svg": render_daloa_ecosystem_svg(DALOA_PILLARS, DALOA_INFRA_MODULES),
        "stack.svg": render_stack_svg(STACK_COLUMNS),
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
    """Régénère les 4 visuels du profil épuré."""
    print("=== Régénération du profil GitHub épuré (elm-as) ===")
    manifest = build_static_svg_manifest()
    write_svg_assets(manifest, ASSETS_DIR)
    update_contributions_grid()
    print("\n[SUCCÈS] Les 4 panneaux SVG sont à jour.")


if __name__ == "__main__":
    update_all_profile_assets()
