"""Configuration visuelle et palette de couleurs du profil GitHub elm-as.

Définit les jetons de couleur sémantiques et polices conformes à la charte ElmasCore.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ElmasPalette:
    """Jetons de couleur sémantiques de l'identité visuelle ElmasCore."""

    bg_deep: str = "#0b1220"
    bg_panel: str = "#111a2e"
    bg_card: str = "#16223b"
    bg_chip: str = "#1b2a4a"
    border: str = "#1f2e4d"
    border_strong: str = "#2b416d"
    text_primary: str = "#f0f6fc"
    text_body: str = "#cbd5e1"
    text_muted: str = "#8b9bb4"
    text_dim: str = "#5e718d"
    signal_prod: str = "#34d399"
    signal_active: str = "#58a6ff"
    signal_data: str = "#f59e0b"
    signal_systems: str = "#2dd4bf"


FONT_SANS: str = (
    "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
)
FONT_MONO: str = (
    "'JetBrains Mono','Fira Code','SF Mono',Consolas,'Liberation Mono',monospace"
)

PALETTE: ElmasPalette = ElmasPalette()
