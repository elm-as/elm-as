"""Générateurs SVG purs pour les métriques statistiques et la cartographie des projets.

Garantit l'exactitude proportionnelle des graphiques (barres, moyennes, axes gradués)
et l'alignement tabulaire de tous les indicateurs chiffrés.
"""

from __future__ import annotations

from html import escape

from profile_config import (
    ElmasPalette,
    FONT_MONO,
    FONT_SANS,
    MonthlyChartSpec,
    PALETTE,
    PortfolioBand,
    ProjectTile,
    ShareSlice,
    StatCardSpec,
)


def _svg_header(width: int, height: int, aria_label: str) -> str:
    """Crée l'en-tête SVG standardisé avec support des chiffres tabulaires."""
    safe_label = escape(aria_label, quote=True)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_SANS}" '
        f'role="img" aria-label="{safe_label}">'
        f"<style>.mono{{font-family:{FONT_MONO};font-variant-numeric:tabular-nums}}"
        ".num{font-variant-numeric:tabular-nums}</style>"
    )


def _format_pct_fr(value: float) -> str:
    """Formate un pourcentage à une décimale selon la typographie française."""
    return f"{value:.1f}".replace(".", ",") + " %"


def render_stats_cards_svg(
    cards: tuple[StatCardSpec, ...],
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère les 4 cartes synthétiques sur un canevas exact de 1000 px sans rognage."""
    width, height = 1000, 140
    card_w, gap = 235, 20
    parts = [
        _svg_header(width, height, "Indicateurs clés 2026 : 867 commits, 76 jours actifs, +385k lignes"),
    ]

    for index, card in enumerate(cards):
        pos_x = index * (card_w + gap)
        parts.append(
            f'<rect x="{pos_x + 0.5}" y="0.5" width="{card_w - 1}" height="{height - 1}" '
            f'rx="14" fill="{palette.bg_panel}" stroke="{palette.border}"/>'
            f'<rect x="{pos_x + 0.5}" y="24" width="4" height="42" rx="2" fill="{card.accent}"/>'
            f'<text class="mono" x="{pos_x + 22}" y="58" font-size="34" font-weight="800" '
            f'fill="{palette.text_primary}">{escape(card.value)}</text>'
            f'<text x="{pos_x + 22}" y="88" font-size="14.5" font-weight="600" '
            f'fill="{palette.text_body}">{escape(card.label)}</text>'
            f'<text x="{pos_x + 22}" y="113" font-size="12.5" '
            f'fill="{palette.text_muted}">{escape(card.detail)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def render_monthly_chart_svg(
    spec: MonthlyChartSpec,
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère l'histogramme mensuel des commits avec axe gradué et moyenne annuelle."""
    if not spec.monthly_counts:
        return ""

    width, height = 1000, 338
    baseline_y, top_axis_y = 276.0, 92.0
    chart_span_y = baseline_y - top_axis_y
    axis_max = 300.0
    scale = chart_span_y / axis_max

    peak_count = max(count for _, count in spec.monthly_counts)
    mean_commits = spec.total_commits / len(spec.monthly_counts)
    mean_y = baseline_y - mean_commits * scale
    peak_share = round((peak_count / spec.total_commits) * 100) if spec.total_commits > 0 else 0

    subtitle = (
        f"Pic en {spec.peak_month_label.lower()} ({peak_count} commits, {peak_share} % du volume) "
        f"· Total : {spec.total_commits} commits"
    )

    parts = [
        _svg_header(width, height, f"Commits mensuels 2026 : {spec.total_commits} commits au total"),
        "<defs>",
        '<linearGradient id="mbPeak" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{palette.signal_active}"/>'
        '<stop offset="1" stop-color="#2563eb"/>'
        "</linearGradient>",
        '<linearGradient id="mbStd" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#3b5f99"/>'
        '<stop offset="1" stop-color="#1e345c"/>'
        "</linearGradient>",
        "</defs>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>',
        f'<text x="32" y="42" font-size="18" font-weight="700" fill="{palette.text_primary}">Cadence mensuelle des commits (2026)</text>',
        f'<text x="32" y="65" font-size="13.5" fill="{palette.text_muted}">{escape(subtitle)}</text>',
        f'<rect x="786" y="26" width="180" height="26" rx="7" fill="#1e1b14" stroke="#5c4216"/>',
        f'<line x1="798" x2="818" y1="39" y2="39" stroke="{palette.signal_data}" stroke-width="1.6" stroke-dasharray="4 3"/>',
        f'<text class="mono" x="826" y="43" font-size="11.5" fill="{palette.signal_data}">Moyenne : {round(mean_commits)} / mois</text>',
    ]

    for tick_val in (0, 150, 300):
        tick_y = baseline_y - tick_val * scale
        dash = "" if tick_val == 0 else ' stroke-dasharray="3 5"'
        parts.append(
            f'<line x1="68" x2="964" y1="{tick_y:.1f}" y2="{tick_y:.1f}" stroke="{palette.border}"{dash}/>'
            f'<text class="mono" x="56" y="{tick_y + 4:.1f}" font-size="11" fill="{palette.text_dim}" text-anchor="end">{tick_val}</text>'
        )

    parts.append(
        f'<line x1="68" x2="964" y1="{mean_y:.1f}" y2="{mean_y:.1f}" stroke="{palette.signal_data}" stroke-opacity="0.5" stroke-dasharray="5 4"/>'
    )

    bar_width, pitch, start_x = 54.0, 86.0, 92.0
    for index, (month_name, count) in enumerate(spec.monthly_counts):
        pos_x = start_x + index * pitch
        center_x = pos_x + bar_width / 2.0
        is_peak = count == peak_count and count > 0
        fill_ref = "url(#mbPeak)" if is_peak else ("#1d2c4a" if count == 0 else "url(#mbStd)")
        bar_h = max(3.0, count * scale) if count > 0 else 3.0
        bar_y = baseline_y - bar_h
        label_fill = palette.text_primary if is_peak else (palette.text_dim if count == 0 else palette.text_body)

        parts.append(
            f'<rect x="{pos_x:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" height="{bar_h:.1f}" rx="7" fill="{fill_ref}"/>'
            f'<text class="mono" x="{center_x:.1f}" y="{bar_y - 9:.1f}" font-size="13.5" font-weight="700" '
            f'fill="{label_fill}" text-anchor="middle">{count}</text>'
            f'<text x="{center_x:.1f}" y="304" font-size="13" fill="{palette.text_muted}" text-anchor="middle">'
            f"{escape(month_name)}</text>"
        )

    parts.append("</svg>")
    return "".join(parts)


def _render_language_panel(slices: tuple[ShareSlice, ...], palette: ElmasPalette) -> str:
    """Rend la colonne gauche (répartition exacte 0–100 % des langages)."""
    total_bar_w, gap_px = 436.0, 2.0
    usable_w = total_bar_w - gap_px * max(0, len(slices) - 1)
    cursor_x = 32.0
    parts = [
        f'<text x="32" y="42" font-size="18" font-weight="700" fill="{palette.text_primary}">Langages</text>',
        f'<text x="32" y="64" font-size="13" fill="{palette.text_muted}">Part du code produit en 2026 (base 100 %)</text>',
        '<clipPath id="lbar"><rect x="32" y="82" width="436" height="14" rx="7"/></clipPath>',
        '<g clip-path="url(#lbar)">',
    ]

    for idx, item in enumerate(slices):
        seg_w = usable_w * (item.percentage / 100.0)
        if idx == len(slices) - 1:
            seg_w = max(2.5, 468.0 - cursor_x)
        parts.append(f'<rect x="{cursor_x:.2f}" y="82" width="{max(2.0, seg_w):.2f}" height="14" fill="{item.color}"/>')
        cursor_x += seg_w + gap_px
    parts.append("</g>")

    for idx, item in enumerate(slices):
        row_y = 132 + idx * 38
        mini_w = max(2.0, 184.0 * (item.percentage / 100.0))
        parts.append(
            f'<circle cx="40" cy="{row_y - 5}" r="5.5" fill="{item.color}"/>'
            f'<text x="56" y="{row_y}" font-size="14" fill="{palette.text_body}">{escape(item.name)}</text>'
            f'<rect x="190" y="{row_y - 8}" width="184" height="6" rx="3" fill="{palette.bg_deep}"/>'
            f'<rect x="190" y="{row_y - 8}" width="{mini_w:.1f}" height="6" rx="3" fill="{item.color}"/>'
            f'<text class="mono" x="468" y="{row_y}" font-size="13.5" font-weight="700" '
            f'fill="{palette.text_primary}" text-anchor="end">{_format_pct_fr(item.percentage)}</text>'
        )
    return "".join(parts)


def _render_domain_panel(slices: tuple[ShareSlice, ...], palette: ElmasPalette) -> str:
    """Rend la colonne droite avec axe gradué honnête de 0 % à 50 % (somme = 100 %)."""
    axis_max_pct = 50.0
    plot_x, plot_w = 532.0, 436.0
    parts = [
        f'<text x="532" y="42" font-size="18" font-weight="700" fill="{palette.text_primary}">Destination du code</text>',
        f'<text x="532" y="64" font-size="13" fill="{palette.text_muted}">Lignes ajoutées par couche (axe gradué 0 – 50 %)</text>',
    ]

    for tick_pct, anchor in ((0, "start"), (25, "middle"), (50, "end")):
        gx = plot_x + (tick_pct / axis_max_pct) * plot_w
        parts.append(
            f'<line x1="{gx:.1f}" x2="{gx:.1f}" y1="82" y2="328" stroke="{palette.border}" stroke-dasharray="3 4"/>'
            f'<text class="mono" x="{gx:.1f}" y="346" font-size="11" fill="{palette.text_dim}" text-anchor="{anchor}">{tick_pct} %</text>'
        )

    for idx, item in enumerate(slices):
        row_y = 95 + idx * 30
        bar_w = min(plot_w, (item.percentage / axis_max_pct) * plot_w)
        parts.append(
            f'<text x="532" y="{row_y}" font-size="12.5" fill="{palette.text_body}">{escape(item.name)}</text>'
            f'<text class="mono" x="968" y="{row_y}" font-size="12.5" font-weight="700" '
            f'fill="{palette.text_primary}" text-anchor="end">{_format_pct_fr(item.percentage)}</text>'
            f'<rect x="532" y="{row_y + 5}" width="{bar_w:.1f}" height="6.5" rx="3.2" fill="{item.color}"/>'
        )
    return "".join(parts)


def render_breakdown_svg(
    languages: tuple[ShareSlice, ...],
    domains: tuple[ShareSlice, ...],
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère le double panneau analytique Langages vs Couches applicatives."""
    width, height = 1000, 368
    return (
        _svg_header(width, height, "Répartition 2026 par langage et par couche applicative")
        + f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="{palette.bg_panel}" stroke="{palette.border}"/>'
        + _render_language_panel(languages, palette)
        + f'<line x1="500" x2="500" y1="28" y2="346" stroke="{palette.border}"/>'
        + _render_domain_panel(domains, palette)
        + "</svg>"
    )


def _render_band_tiles(tiles: tuple[ProjectTile, ...], tile_y: int, accent: str) -> str:
    """Dispose les cartes de projets d'une bande horizontale avec espacement régulier."""
    cursor_x = 194
    out: list[str] = []
    for tile in tiles:
        out.append(
            f'<rect x="{cursor_x}" y="{tile_y}" width="{tile.width}" height="56" rx="10" fill="#16223b" stroke="#223456"/>'
            f'<rect x="{cursor_x}" y="{tile_y + 12}" width="3" height="32" rx="1.5" fill="{accent}"/>'
            f'<text x="{cursor_x + 14}" y="{tile_y + 23}" font-size="14" font-weight="700" fill="#f0f6fc">{escape(tile.name)}</text>'
            f'<text class="mono" x="{cursor_x + 14}" y="{tile_y + 42}" font-size="11" fill="#8b9bb4">{escape(tile.meta)}</text>'
        )
        cursor_x += tile.width + 10
    return "".join(out)


def render_portfolio_matrix_svg(
    bands: tuple[PortfolioBand, ...],
    palette: ElmasPalette = PALETTE,
) -> str:
    """Génère la cartographie structurée des projets par maturité et impact."""
    band_heights = [128 if band.footnote else 88 for band in bands]
    width, height = 1000, sum(band_heights)
    parts = [
        _svg_header(width, height, "Cartographie des projets par maturité et impact opérationnel"),
        f'<defs><clipPath id="pmc"><rect width="{width}" height="{height}" rx="16"/></clipPath></defs>',
        '<g clip-path="url(#pmc)">',
    ]

    cursor_y = 0
    for idx, band in enumerate(bands):
        band_h = band_heights[idx]
        parts.append(
            f'<rect x="0" y="{cursor_y}" width="{width}" height="{band_h}" fill="{palette.bg_panel}"/>'
            f'<rect x="0" y="{cursor_y}" width="176" height="{band_h}" fill="{palette.bg_deep}"/>'
            f'<rect x="0" y="{cursor_y}" width="4" height="{band_h}" fill="{band.accent}"/>'
            f'<line x1="176" x2="176" y1="{cursor_y}" y2="{cursor_y + band_h}" stroke="{palette.border}"/>'
            f'<text x="18" y="{cursor_y + 38}" font-size="14" font-weight="700" fill="{band.accent}">{escape(band.category)}</text>'
            f'<text x="18" y="{cursor_y + 58}" font-size="12" fill="{palette.text_muted}">{escape(band.subtitle)}</text>'
            + _render_band_tiles(band.projects, cursor_y + 16, band.accent)
        )
        if band.footnote:
            parts.append(
                f'<rect x="194" y="{cursor_y + 84}" width="786" height="28" rx="7" fill="{palette.bg_deep}" stroke="{palette.border}"/>'
                f'<text x="208" y="{cursor_y + 102}" font-size="11.5" fill="{palette.text_muted}">{escape(band.footnote)}</text>'
            )
        if idx < len(bands) - 1:
            parts.append(f'<line x1="0" x2="{width}" y1="{cursor_y + band_h}" y2="{cursor_y + band_h}" stroke="{palette.border}"/>')
        cursor_y += band_h

    parts.append("</g>")
    parts.append(f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="15.5" fill="none" stroke="{palette.border}"/>')
    parts.append("</svg>")
    return "".join(parts)
