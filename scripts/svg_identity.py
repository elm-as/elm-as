"""Générateurs SVG épurés pour l'identité, l'architecture Daloa et la boîte à outils.

Privilégie l'espace négatif, la hiérarchie typographique et la lisibilité en une seconde
conformément à la charte ElmasCore (§5).
"""

from __future__ import annotations

from html import escape

from profile_config import (
    EcosystemPillar,
    ElmasPalette,
    FONT_MONO,
    FONT_SANS,
    PALETTE,
    StackDomainColumn,
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
    """Génère une bannière d'en-tête aérée avec identité à gauche et télémétrie sobre à droite."""
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
        # Pastille de statut sobre
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
        # Carte console épurée à droite (4 lignes aérées)
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


def _render_ecosystem_card(pillar: EcosystemPillar, pos_x: int, palette: ElmasPalette) -> str:
    """Rend une carte pilier Daloa épurée."""
    card_w, card_y, card_h = 276, 26, 114
    center_x = pos_x + card_w // 2
    return (
        f'<rect x="{pos_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="12" '
        f'fill="{palette.bg_card}" stroke="{palette.border}"/>'
        f'<rect x="{pos_x + 12}" y="{card_y}" width="{card_w - 24}" height="3" rx="1.5" fill="{pillar.accent}"/>'
        f'<circle cx="{pos_x + 22}" cy="{card_y + 24}" r="3.5" fill="{pillar.accent}"/>'
        f'<text x="{pos_x + 33}" y="{card_y + 28}" font-size="11.5" font-weight="700" fill="{pillar.accent}">'
        f"{escape(pillar.status_label)}</text>"
        f'<text x="{pos_x + 18}" y="{card_y + 60}" font-size="20" font-weight="700" fill="{palette.text_primary}">'
        f"{escape(pillar.title)}</text>"
        f'<text x="{pos_x + 18}" y="{card_y + 86}" font-size="12.5" fill="{palette.text_body}">'
        f"{escape(pillar.summary)}</text>"
        f'<line x1="{center_x}" x2="{center_x}" y1="{card_y + card_h}" y2="160" '
        f'stroke="{palette.border_strong}" stroke-dasharray="3 3"/>'
    )


def render_daloa_ecosystem_svg(
    pillars: tuple[EcosystemPillar, ...],
    infra_modules: tuple[tuple[str, str], ...],
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère le schéma d'architecture Daloa condensé et respirant."""
    width, height = 1000, 228
    card_w, gap, start_x = 276, 54, 32
    flow_labels = ("flux", "escrow")

    parts = [
        _svg_open(width, height, "Architecture Daloa : Market, Delivery, Pay et socle PostgreSQL RLS"),
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
    ]

    for index, pillar in enumerate(pillars):
        pos_x = start_x + index * (card_w + gap)
        parts.append(_render_ecosystem_card(pillar, pos_x, palette))
        if index < len(pillars) - 1:
            line_x1 = pos_x + card_w + 6
            line_x2 = pos_x + card_w + gap - 8
            mid_x = (line_x1 + line_x2) // 2
            label = flow_labels[index] if index < len(flow_labels) else ""
            parts.append(
                f'<line x1="{line_x1}" x2="{line_x2}" y1="83" y2="83" stroke="{palette.signal_active}" stroke-width="1.6" stroke-dasharray="4 4"/>'
                f'<polygon points="{line_x2 + 4},83 {line_x2 - 3},79 {line_x2 - 3},87" fill="{palette.signal_active}"/>'
                f'<text class="mono" x="{mid_x}" y="73" font-size="11" font-weight="600" fill="{palette.text_muted}" text-anchor="middle">{escape(label.upper())}</text>'
            )

    parts.append(f'<rect x="32" y="160" width="936" height="44" rx="10" fill="{palette.bg_deep}" stroke="{palette.border_strong}"/>')
    module_width = 936 // max(1, len(infra_modules))
    for idx, (mod_name, mod_desc) in enumerate(infra_modules):
        mod_x = 32 + idx * module_width
        if idx > 0:
            parts.append(f'<line x1="{mod_x}" x2="{mod_x}" y1="168" y2="196" stroke="{palette.border}"/>')
        parts.append(
            f'<text class="mono" x="{mod_x + 16}" y="179" font-size="11.5" font-weight="700" fill="{palette.text_primary}">{escape(mod_name)}</text>'
            f'<text x="{mod_x + 16}" y="195" font-size="11.5" fill="{palette.text_muted}">{escape(mod_desc)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def _render_chip_row(labels: tuple[str, ...], start_x: int, row_y: int) -> str:
    """Dispose une rangée aérée de badges techniques."""
    cursor_x = start_x
    chips: list[str] = []
    for label in labels:
        chip_w = max(52, round(len(label) * 6.8 + 22))
        center_x = cursor_x + chip_w / 2.0
        chips.append(
            f'<rect x="{cursor_x}" y="{row_y}" width="{chip_w}" height="25" rx="6" fill="#0d1628" stroke="#223456"/>'
            f'<text class="mono" x="{center_x:.1f}" y="{row_y + 16.5}" font-size="11.5" fill="#e2e8f0" text-anchor="middle">'
            f"{escape(label)}</text>"
        )
        cursor_x += chip_w + 7
    return "".join(chips)


def render_stack_svg(columns: tuple[StackDomainColumn, ...], palette: ElmasPalette = PALETTE) -> str:
    """Génère une matrice de compétences compacte en 3 colonnes."""
    width, height = 1000, 204
    col_w, gap, start_x = 296, 24, 32
    parts = [
        _svg_open(width, height, "Stack technique : Production Full-Stack, Statistiques et Data, Systèmes et Cyber"),
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
    ]

    for index, column in enumerate(columns):
        pos_x = start_x + index * (col_w + gap)
        parts.append(
            f'<rect x="{pos_x}" y="20" width="{col_w}" height="164" rx="12" fill="{palette.bg_card}" stroke="{palette.border}"/>'
            f'<rect x="{pos_x + 12}" y="20" width="{col_w - 24}" height="3" rx="1.5" fill="{column.accent}"/>'
            f'<text x="{pos_x + 18}" y="48" font-size="15" font-weight="700" fill="{palette.text_primary}">{escape(column.title)}</text>'
            f'<line x1="{pos_x + 18}" x2="{pos_x + col_w - 18}" y1="62" y2="62" stroke="{palette.border}"/>'
        )
        for row_idx, row_labels in enumerate(column.rows[:3]):
            row_y = 74 + row_idx * 34
            parts.append(_render_chip_row(row_labels, pos_x + 18, row_y))

    parts.append("</svg>")
    return "".join(parts)
