"""Générateurs SVG purs pour l'identité, l'architecture Daloa, la roadmap et la stack.

Toutes les fonctions de ce module sont déterministes, sans effet de bord ni accès I/O,
et produisent des panneaux SVG unifiés sur un canevas de 1000 px de large.
"""

from __future__ import annotations

from html import escape

from profile_config import (
    EcosystemPillar,
    ElmasPalette,
    FONT_MONO,
    FONT_SANS,
    PALETTE,
    RoadmapStage,
    StackDomainColumn,
)


def _svg_open(width: int, height: int, aria_label: str) -> str:
    """Construit la balise ouvrante SVG accessible avec styles numériques tabulaires."""
    safe_label = escape(aria_label, quote=True)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_SANS}" '
        f'role="img" aria-label="{safe_label}">'
        "<style>"
        f".mono{{font-family:{FONT_MONO};font-variant-numeric:tabular-nums}}"
        ".num{font-variant-numeric:tabular-nums}"
        "@media (prefers-reduced-motion: no-preference){"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}"
        ".cur{animation:blink 1.15s infinite}"
        ".live{animation:pulse 2.4s ease-in-out infinite}"
        "}"
        "</style>"
    )


def render_header_svg(palette: ElmasPalette = PALETTE) -> str:
    """Génère la bannière d'en-tête principale avec console de télémétrie système."""
    width, height = 1000, 248
    parts = [
        _svg_open(width, height, "Elmas (elm-as) — Data Science, Statistiques et Ingénierie Logicielle"),
        "<defs>",
        '<linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{palette.bg_deep}"/>'
        '<stop offset="0.55" stop-color="#101c34"/>'
        '<stop offset="1" stop-color="#15284c"/>'
        "</linearGradient>",
        '<radialGradient id="hr" cx="0.18" cy="0.15" r="0.65">'
        '<stop offset="0" stop-color="#3178c6" stop-opacity="0.22"/>'
        '<stop offset="1" stop-color="#3178c6" stop-opacity="0"/>'
        "</radialGradient>",
        '<pattern id="hd" width="24" height="24" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="1" fill="#ffffff" opacity="0.055"/>'
        "</pattern>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="16" fill="url(#hg)"/>',
        f'<rect width="{width}" height="{height}" rx="16" fill="url(#hd)"/>',
        f'<rect width="{width}" height="{height}" rx="16" fill="url(#hr)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="none" stroke="{palette.border}"/>',
        f'<rect x="44" y="0.5" width="180" height="2" fill="{palette.signal_active}"/>',
        # Pill de disponibilité en haut à gauche
        f'<rect x="44" y="34" width="460" height="24" rx="12" fill="#13233f" stroke="{palette.border_strong}"/>',
        f'<circle class="live" cx="58" cy="46" r="3.8" fill="{palette.signal_prod}"/>',
        f'<text x="70" y="50" font-size="11.5" fill="{palette.text_body}">'
        "Abidjan, CI · Remote · Ouvert aux opportunités Data, Web/Mobile &amp; Systèmes"
        "</text>",
        # Identité & titre
        f'<text x="44" y="112" font-size="50" font-weight="800" fill="{palette.text_primary}" letter-spacing="-1">Elmas</text>',
        f'<text class="mono" x="198" y="110" font-size="17" font-weight="600" fill="{palette.signal_active}">@elm-as</text>',
        f'<text x="44" y="146" font-size="19" font-weight="700" fill="{palette.signal_active}">'
        "Data Science, Statistiques &amp; Ingénierie Logicielle"
        "</text>",
        f'<text x="44" y="173" font-size="13.5" fill="{palette.text_muted}">'
        "From Data to Systems — rigueur mathématique, sécurité en base et produits livrés."
        "</text>",
        # Repères académiques & production
        f'<rect x="44" y="192" width="154" height="25" rx="6" fill="{palette.bg_card}" stroke="{palette.border}"/>',
        f'<text x="121" y="209" font-size="11.5" fill="{palette.text_body}" text-anchor="middle">UFHB · Licence Stats</text>',
        f'<rect x="206" y="192" width="204" height="25" rx="6" fill="{palette.bg_card}" stroke="{palette.border}"/>',
        f'<text x="308" y="209" font-size="11.5" fill="{palette.text_body}" text-anchor="middle">Rennes 2 · Master Data &amp; IA</text>',
        f'<rect x="418" y="192" width="152" height="25" rx="6" fill="#112928" stroke="#1f5145"/>',
        f'<text x="494" y="209" font-size="11.5" font-weight="600" fill="{palette.signal_prod}" text-anchor="middle">Google Play · En ligne</text>',
        # Console système à droite
        f'<rect x="608" y="28" width="356" height="192" rx="12" fill="{palette.bg_deep}" stroke="{palette.border_strong}"/>',
        '<circle cx="628" cy="46" r="4.2" fill="#ff5f56"/>',
        '<circle cx="642" cy="46" r="4.2" fill="#ffbd2e"/>',
        '<circle cx="656" cy="46" r="4.2" fill="#27c93f"/>',
        f'<text class="mono" x="674" y="50" font-size="11" fill="{palette.text_muted}">elmas@core:~ — telemetry</text>',
        f'<line x1="608" x2="964" y1="62" y2="62" stroke="{palette.border}"/>',
        f'<text class="mono" x="626" y="84" font-size="11.5" fill="{palette.text_muted}">'
        f'$ elmas status --systems <tspan class="cur" fill="{palette.signal_active}">&#9610;</tspan></text>',
        f'<circle cx="631" cy="105" r="3.2" fill="{palette.signal_prod}"/>',
        f'<text class="mono" x="643" y="109" font-size="11.5" fill="{palette.text_primary}">daloa-market</text>',
        f'<text class="mono" x="766" y="109" font-size="11.5" fill="{palette.signal_prod}">LIVE · Google Play</text>',
        f'<circle cx="631" cy="128" r="3.2" fill="{palette.signal_active}"/>',
        f'<text class="mono" x="643" y="132" font-size="11.5" fill="{palette.text_primary}">daloa-suite</text>',
        f'<text class="mono" x="766" y="132" font-size="11.5" fill="{palette.text_body}">Delivery · Pay · API</text>',
        f'<circle cx="631" cy="151" r="3.2" fill="{palette.signal_data}"/>',
        f'<text class="mono" x="643" y="155" font-size="11.5" fill="{palette.text_primary}">openstats</text>',
        f'<text class="mono" x="766" y="155" font-size="11.5" fill="{palette.text_body}">+133k LoC · Data/TS</text>',
        f'<circle cx="631" cy="174" r="3.2" fill="{palette.signal_systems}"/>',
        f'<text class="mono" x="643" y="178" font-size="11.5" fill="{palette.text_primary}">systems-r&amp;d</text>',
        f'<text class="mono" x="766" y="178" font-size="11.5" fill="{palette.text_muted}">Go · Rust · TCP/IP</text>',
        f'<line x1="624" x2="948" y1="192" y2="192" stroke="{palette.border}"/>',
        f'<text class="mono" x="626" y="209" font-size="11" fill="{palette.text_muted}">postgres: rls=enforced</text>',
        f'<text class="mono" x="946" y="209" font-size="11" font-weight="700" fill="{palette.signal_active}" text-anchor="end">2026: 867 commits</text>',
        "</svg>",
    ]
    return "".join(parts)


def _render_ecosystem_card(pillar: EcosystemPillar, pos_x: int, palette: ElmasPalette) -> str:
    """Rend une carte pilier de l'écosystème Daloa reliée au socle partagé."""
    card_w, card_y, card_h = 276, 54, 126
    center_x = pos_x + card_w // 2
    return (
        f'<rect x="{pos_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="12" '
        f'fill="{palette.bg_card}" stroke="{palette.border}"/>'
        f'<rect x="{pos_x + 12}" y="{card_y}" width="{card_w - 24}" height="3.5" rx="1.75" fill="{pillar.accent}"/>'
        f'<circle cx="{pos_x + 22}" cy="{card_y + 24}" r="3.5" fill="{pillar.accent}"/>'
        f'<text x="{pos_x + 33}" y="{card_y + 28}" font-size="11.5" font-weight="700" fill="{pillar.accent}">'
        f"{escape(pillar.status_label)}</text>"
        f'<text x="{pos_x + 18}" y="{card_y + 60}" font-size="20.5" font-weight="700" fill="{palette.text_primary}">'
        f"{escape(pillar.title)}</text>"
        f'<text x="{pos_x + 18}" y="{card_y + 84}" font-size="12.5" fill="{palette.text_body}">'
        f"{escape(pillar.summary)}</text>"
        f'<text class="mono" x="{pos_x + 18}" y="{card_y + 110}" font-size="11.5" fill="{palette.text_muted}">'
        f"{escape(pillar.metrics)}</text>"
        f'<line x1="{center_x}" x2="{center_x}" y1="{card_y + card_h}" y2="200" '
        f'stroke="{palette.border_strong}" stroke-dasharray="3 3"/>'
        f'<circle cx="{center_x}" cy="200" r="3" fill="{pillar.accent}"/>'
    )


def render_daloa_ecosystem_svg(
    pillars: tuple[EcosystemPillar, ...],
    infra_modules: tuple[tuple[str, str], ...],
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère le schéma d'architecture de bout en bout de la suite Daloa."""
    width, height = 1000, 268
    card_w, gap = 276, 54
    start_x = 32
    flow_labels = ("flux", "escrow")

    parts = [
        _svg_open(width, height, "Architecture de l'écosystème Daloa : Market, Delivery, Pay et socle PostgreSQL RLS"),
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
        f'<text x="32" y="34" font-size="17" font-weight="700" fill="{palette.text_primary}">Architecture unifiée Daloa</text>',
        f'<text x="262" y="34" font-size="13" fill="{palette.text_muted}">· Commerce local, logistique dernier kilomètre et séquestre transactionnel</text>',
    ]

    for index, pillar in enumerate(pillars):
        pos_x = start_x + index * (card_w + gap)
        parts.append(_render_ecosystem_card(pillar, pos_x, palette))
        if index < len(pillars) - 1:
            line_x1 = pos_x + card_w + 4
            line_x2 = pos_x + card_w + gap - 6
            mid_x = (line_x1 + line_x2) // 2
            label = flow_labels[index] if index < len(flow_labels) else ""
            parts.append(
                f'<line x1="{line_x1}" x2="{line_x2}" y1="117" y2="117" stroke="{palette.signal_active}" stroke-width="1.8" stroke-dasharray="4 4"/>'
                f'<polygon points="{line_x2 + 4},117 {line_x2 - 3},113 {line_x2 - 3},121" fill="{palette.signal_active}"/>'
                f'<text class="mono" x="{mid_x}" y="108" font-size="10" fill="{palette.text_muted}" text-anchor="middle">{escape(label)}</text>'
            )

    parts.append(f'<rect x="32" y="200" width="936" height="48" rx="10" fill="{palette.bg_deep}" stroke="{palette.border_strong}"/>')
    module_width = 936 // max(1, len(infra_modules))
    for idx, (mod_name, mod_desc) in enumerate(infra_modules):
        mod_x = 32 + idx * module_width
        if idx > 0:
            parts.append(f'<line x1="{mod_x}" x2="{mod_x}" y1="208" y2="240" stroke="{palette.border}"/>')
        parts.append(
            f'<text class="mono" x="{mod_x + 16}" y="220" font-size="11.5" font-weight="700" fill="{palette.text_primary}">{escape(mod_name)}</text>'
            f'<text x="{mod_x + 16}" y="237" font-size="11.5" fill="{palette.text_muted}">{escape(mod_desc)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def render_roadmap_svg(stages: tuple[RoadmapStage, ...], palette: ElmasPalette = PALETTE) -> str:
    """Génère la frise séquentielle de progression technique en 4 étapes."""
    width, height = 1000, 214
    card_w, gap, start_x = 222, 16, 32
    parts = [
        _svg_open(width, height, "Feuille de route : Daloa Market en prod, Delivery et Pay, RAG évalué, NetSentinel et GateShield"),
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
        f'<text x="32" y="34" font-size="17" font-weight="700" fill="{palette.text_primary}">Trajectoire d\'ingénierie</text>',
        f'<text x="236" y="34" font-size="13" fill="{palette.text_muted}">· Du produit grand public déployé vers les systèmes réseau bas niveau</text>',
    ]

    for index, stage in enumerate(stages):
        pos_x = start_x + index * (card_w + gap)
        parts.append(
            f'<rect x="{pos_x}" y="54" width="{card_w}" height="134" rx="12" fill="{palette.bg_card}" stroke="{palette.border}"/>'
            f'<rect x="{pos_x + 12}" y="54" width="{card_w - 24}" height="3.5" rx="1.75" fill="{stage.accent}"/>'
            f'<text class="mono" x="{pos_x + 16}" y="80" font-size="11" font-weight="700" fill="{stage.accent}">'
            f"{escape(stage.step_code)} · {escape(stage.status_label)}</text>"
            f'<text x="{pos_x + 16}" y="109" font-size="16" font-weight="700" fill="{palette.text_primary}">'
            f"{escape(stage.title)}</text>"
            f'<text class="mono" x="{pos_x + 16}" y="137" font-size="11" fill="{palette.text_body}">'
            f"{escape(stage.stack_line)}</text>"
            f'<text x="{pos_x + 16}" y="163" font-size="12" fill="{palette.text_muted}">'
            f"{escape(stage.scope_line)}</text>"
        )
        if index < len(stages) - 1:
            ax1 = pos_x + card_w + 2
            ax2 = pos_x + card_w + gap - 5
            parts.append(
                f'<line x1="{ax1}" x2="{ax2}" y1="121" y2="121" stroke="{palette.border_strong}" stroke-width="1.8"/>'
                f'<polygon points="{ax2 + 4},121 {ax2 - 2},117 {ax2 - 2},125" fill="{palette.signal_active}"/>'
            )

    parts.append("</svg>")
    return "".join(parts)


def _render_chip_row(labels: tuple[str, ...], start_x: int, row_y: int) -> str:
    """Dispose une rangée horizontale de badges techniques calibrés sur leur texte."""
    cursor_x = start_x
    chips: list[str] = []
    for label in labels:
        chip_w = max(50, round(len(label) * 6.7 + 20))
        center_x = cursor_x + chip_w / 2.0
        chips.append(
            f'<rect x="{cursor_x}" y="{row_y}" width="{chip_w}" height="24" rx="6" fill="#0d1628" stroke="#223456"/>'
            f'<text class="mono" x="{center_x:.1f}" y="{row_y + 16}" font-size="11.5" fill="#e2e8f0" text-anchor="middle">'
            f"{escape(label)}</text>"
        )
        cursor_x += chip_w + 6
    return "".join(chips)


def render_stack_svg(columns: tuple[StackDomainColumn, ...], palette: ElmasPalette = PALETTE) -> str:
    """Génère la matrice de compétences à 3 colonnes classée par niveau de maturité."""
    width, height = 1000, 240
    col_w, gap, start_x = 296, 24, 32
    parts = [
        _svg_open(width, height, "Boîte à outils technique : Production Full-Stack, Statistiques et Data Science, Systèmes et Cyber"),
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
    ]

    for index, column in enumerate(columns):
        pos_x = start_x + index * (col_w + gap)
        parts.append(
            f'<rect x="{pos_x}" y="22" width="{col_w}" height="196" rx="12" fill="{palette.bg_card}" stroke="{palette.border}"/>'
            f'<rect x="{pos_x + 12}" y="22" width="{col_w - 24}" height="3.5" rx="1.75" fill="{column.accent}"/>'
            f'<text x="{pos_x + 18}" y="52" font-size="15.5" font-weight="700" fill="{palette.text_primary}">{escape(column.title)}</text>'
            f'<text x="{pos_x + 18}" y="71" font-size="12" fill="{palette.text_muted}">{escape(column.subtitle)}</text>'
            f'<line x1="{pos_x + 18}" x2="{pos_x + col_w - 18}" y1="84" y2="84" stroke="{palette.border}"/>'
        )
        for row_idx, row_labels in enumerate(column.rows):
            row_y = 96 + row_idx * 30
            parts.append(_render_chip_row(row_labels, pos_x + 18, row_y))

    parts.append("</svg>")
    return "".join(parts)


def render_footer_svg(palette: ElmasPalette = PALETTE) -> str:
    """Génère le bandeau de signature final ElmasCore sobre et sans dépendance externe."""
    width, height = 1000, 86
    return (
        _svg_open(width, height, "ElmasCore — From Data to Systems, Abidjan, Côte d'Ivoire")
        + "<defs>"
        + '<linearGradient id="fg" x1="0" y1="0" x2="1" y2="0">'
        + f'<stop offset="0" stop-color="{palette.bg_deep}"/>'
        + f'<stop offset="1" stop-color="{palette.bg_panel}"/>'
        + "</linearGradient>"
        + "</defs>"
        + f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14" fill="url(#fg)" stroke="{palette.border}"/>'
        + f'<rect x="28" y="23" width="3.5" height="40" rx="1.75" fill="{palette.signal_active}"/>'
        + f'<text x="44" y="39" font-size="15.5" font-weight="700" fill="{palette.text_primary}">ElmasCore · From Data to Systems</text>'
        + f'<text x="44" y="59" font-size="12.5" fill="{palette.text_muted}">'
        + "Donnée propre en entrée · Sécurité verrouillée en base (RLS) · Code modulaire et maintenable"
        + "</text>"
        + f'<text class="mono" x="968" y="39" font-size="12" font-weight="600" fill="{palette.text_body}" text-anchor="end">Abidjan, CI · Remote</text>'
        + f'<text class="mono" x="968" y="59" font-size="11.5" fill="{palette.signal_active}" text-anchor="end">github.com/elm-as</text>'
        + "</svg>"
    )
