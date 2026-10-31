"""Générateur SVG pour la bannière d'identité du profil GitHub (header.svg).

Privilégie l'espace négatif, la hiérarchie typographique et la lisibilité immédiate
conformément à la charte ElmasCore (§5).
"""

from __future__ import annotations

from html import escape

from profile_config import (
    ElmasPalette,
    FONT_MONO,
    FONT_SANS,
    PALETTE,
)


def _svg_open(width: int, height: int, aria_label: str) -> str:
    """Construit la balise ouvrante SVG accessible avec chiffres tabulaires."""
    safe_label = escape(aria_label, quote=True)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_SANS}" '
        f'role="img" aria-label="{safe_label}">'
        "<style>"
        f".mono{{font-family:{FONT_MONO};font-variant-numeric:tabular-nums}}"
        "@media (prefers-reduced-motion: no-preference){"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}"
        ".live{animation:pulse 2.6s ease-in-out infinite}"
        "}"
        "</style>"
    )


def render_header_svg(palette: ElmasPalette = PALETTE) -> str:
    """Génère la bannière d'en-tête avec identité à gauche et console de statut à droite."""
    width, height = 1000, 212
    parts = [
        _svg_open(width, height, "Elmas (elm-as) — Data Science, Statistiques et Ingénierie Logicielle"),
        "<defs>",
        '<linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{palette.bg_deep}"/>'
        '<stop offset="1" stop-color="#132342"/>'
        "</linearGradient>",
        '<radialGradient id="hr" cx="0.15" cy="0.2" r="0.6">'
        '<stop offset="0" stop-color="#3178c6" stop-opacity="0.18"/>'
        '<stop offset="1" stop-color="#3178c6" stop-opacity="0"/>'
        "</radialGradient>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="16" fill="url(#hg)"/>',
        f'<rect width="{width}" height="{height}" rx="16" fill="url(#hr)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="none" stroke="{palette.border}"/>',
        # Pastille de statut académique et localisation
        f'<circle class="live" cx="52" cy="44" r="4" fill="{palette.signal_prod}"/>',
        f'<text class="mono" x="64" y="48" font-size="11.5" fill="{palette.text_muted}">'
        "Abidjan, CI · Remote · UFHB (Statistiques) &amp; Univ. Rennes 2 (Master Data &amp; IA)"
        "</text>",
        # Nom & positionnement
        f'<text x="44" y="106" font-size="48" font-weight="800" fill="{palette.text_primary}" letter-spacing="-1">Elmas</text>',
        f'<text class="mono" x="194" y="104" font-size="16" fill="{palette.signal_active}">@elm-as</text>',
        f'<text x="44" y="142" font-size="18.5" font-weight="700" fill="{palette.signal_active}">'
        "Data Science, Statistiques &amp; Ingénierie Logicielle"
        "</text>",
        f'<text x="44" y="170" font-size="13.5" fill="{palette.text_body}">'
        "From Data to Systems — donnée propre, sécurité PostgreSQL RLS et systèmes en production."
        "</text>",
        # Console de statut à droite
        f'<rect x="636" y="28" width="328" height="156" rx="12" fill="{palette.bg_deep}" stroke="{palette.border_strong}"/>',
        '<circle cx="656" cy="46" r="4" fill="#ff5f56"/>',
        '<circle cx="670" cy="46" r="4" fill="#ffbd2e"/>',
        '<circle cx="684" cy="46" r="4" fill="#27c93f"/>',
        f'<text class="mono" x="702" y="50" font-size="11" fill="{palette.text_dim}">elmas@core:~</text>',
        f'<line x1="636" x2="964" y1="62" y2="62" stroke="{palette.border}"/>',
        f'<circle cx="658" cy="86" r="3.2" fill="{palette.signal_prod}"/>',
        f'<text class="mono" x="670" y="90" font-size="11.5" fill="{palette.text_primary}">daloa-market</text>',
        f'<text class="mono" x="784" y="90" font-size="11.5" fill="{palette.signal_prod}">Google Play (Live)</text>',
        f'<circle cx="658" cy="112" r="3.2" fill="{palette.signal_active}"/>',
        f'<text class="mono" x="670" y="116" font-size="11.5" fill="{palette.text_primary}">daloa-suite</text>',
        f'<text class="mono" x="784" y="116" font-size="11.5" fill="{palette.text_body}">Delivery · Pay · API</text>',
        f'<circle cx="658" cy="138" r="3.2" fill="{palette.signal_data}"/>',
        f'<text class="mono" x="670" y="142" font-size="11.5" fill="{palette.text_primary}">data &amp; rag</text>',
        f'<text class="mono" x="784" y="142" font-size="11.5" fill="{palette.text_body}">OpenStats · StatRAG</text>',
        f'<circle cx="658" cy="164" r="3.2" fill="{palette.signal_systems}"/>',
        f'<text class="mono" x="670" y="168" font-size="11.5" fill="{palette.text_primary}">systems-go</text>',
        f'<text class="mono" x="784" y="168" font-size="11.5" fill="{palette.text_muted}">NetSentinel · GateShield</text>',
        "</svg>",
    ]
    return "".join(parts)
