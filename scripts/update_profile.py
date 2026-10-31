"""Script principal de mise à jour du profil GitHub (elm-as).

Génère la bannière vectorielle d'en-tête (header.svg).
Tous les autres éléments (projets, compétences, liens) sont gérés
directement en Markdown natif pour une performance et lisibilité maximales.
"""

from pathlib import Path

from profile_config import PALETTE
from svg_identity import render_header_svg


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    assets_dir = repo_root / "assets"
    assets_dir.mkdir(exist_ok=True)

    print("=== Génération du profil GitHub épuré (elm-as) ===")
    header_svg = render_header_svg(palette=PALETTE)
    header_path = assets_dir / "header.svg"
    header_path.write_text(header_svg, encoding="utf-8")
    print(f"[OK] {header_path.name:<18} ({len(header_svg) / 1024:.1f} Ko)")
    print("\n[SUCCÈS] Bannière d'en-tête à jour.")


if __name__ == "__main__":
    main()
