"""Modèles de données immuables et configuration éditoriale du profil GitHub elm-as.

Centralise la palette graphique ElmasCore, les métriques vérifiées 2026 et la
structure des projets afin de séparer strictement les données du rendu SVG.
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


@dataclass(frozen=True)
class StatCardSpec:
    """Données d'une carte synthétique de télémétrie annuelle."""

    value: str
    label: str
    detail: str
    accent: str


@dataclass(frozen=True)
class EcosystemPillar:
    """Pilier applicatif de l'écosystème Daloa."""

    status_label: str
    title: str
    summary: str
    metrics: str
    accent: str


@dataclass(frozen=True)
class RoadmapStage:
    """Étape séquentielle de la feuille de route d'ingénierie."""

    step_code: str
    status_label: str
    title: str
    stack_line: str
    scope_line: str
    accent: str


@dataclass(frozen=True)
class StackDomainColumn:
    """Colonne de compétences regroupée par maturité opérationnelle."""

    title: str
    subtitle: str
    accent: str
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class ShareSlice:
    """Part proportionnelle d'un langage ou d'une couche applicative."""

    name: str
    percentage: float
    color: str


@dataclass(frozen=True)
class ProjectTile:
    """Carte synthétique d'un projet dans la matrice de portefeuille."""

    name: str
    meta: str
    width: int


@dataclass(frozen=True)
class PortfolioBand:
    """Bande horizontale regroupant les projets par impact et domaine."""

    category: str
    subtitle: str
    accent: str
    projects: tuple[ProjectTile, ...]
    footnote: str = ""


@dataclass(frozen=True)
class MonthlyChartSpec:
    """Paramètres complets du graphique des commits mensuels."""

    monthly_counts: tuple[tuple[str, int], ...]
    peak_month_label: str
    total_commits: int


FONT_SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, 'Cascadia Mono', 'SFMono-Regular', Menlo, Consolas, monospace"

PALETTE = ElmasPalette()

STATS_CARDS_2026: tuple[StatCardSpec, ...] = (
    StatCardSpec(
        value="867",
        label="Commits en 2026",
        detail="Pic : 287 en septembre (33 %)",
        accent=PALETTE.signal_active,
    ),
    StatCardSpec(
        value="76",
        label="Jours d'activité",
        detail="42 % produits le week-end",
        accent=PALETTE.signal_prod,
    ),
    StatCardSpec(
        value="+385 k",
        label="Lignes de code (solde)",
        detail="72,0 % en TypeScript",
        accent=PALETTE.signal_data,
    ),
    StatCardSpec(
        value="9 jours",
        label="Plus longue série",
        detail="38 dépôts publics · rythme matinal",
        accent=PALETTE.signal_systems,
    ),
)

MONTHLY_SPEC_2026 = MonthlyChartSpec(
    monthly_counts=(
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
    ),
    peak_month_label="Septembre",
    total_commits=867,
)

DALOA_PILLARS: tuple[EcosystemPillar, ...] = (
    EcosystemPillar(
        status_label="En production · Google Play",
        title="Daloa Market",
        summary="Catalogue temps réel, commandes & vendeurs locaux",
        metrics="217 commits · +104 k LoC",
        accent=PALETTE.signal_prod,
    ),
    EcosystemPillar(
        status_label="En finalisation",
        title="Daloa Delivery",
        summary="Attribution de courses, livreurs & dernier kilomètre",
        metrics="129 commits · +48 k LoC",
        accent=PALETTE.signal_active,
    ),
    EcosystemPillar(
        status_label="Développement actif",
        title="Daloa Pay",
        summary="Portefeuille local, séquestre & payouts",
        metrics="90 commits · API dédiée",
        accent=PALETTE.signal_data,
    ),
)

DALOA_INFRA_MODULES: tuple[tuple[str, str], ...] = (
    ("PostgreSQL + RLS", "Isolation stricte en base"),
    ("api.daloamarket.ci", "Escrow, Webhooks & Payouts"),
    ("docs.daloamarket.ci", "Documentation VitePress"),
    ("status.daloamarket.ci", "Monitoring de disponibilité"),
)

ROADMAP_STAGES: tuple[RoadmapStage, ...] = (
    RoadmapStage(
        step_code="01",
        status_label="En production",
        title="Daloa Market",
        stack_line="TS · React · Postgres RLS",
        scope_line="Déployé sur Google Play",
        accent=PALETTE.signal_prod,
    ),
    RoadmapStage(
        step_code="02",
        status_label="Finalisation",
        title="Delivery & Pay",
        stack_line="Dispatch · Escrow · API",
        scope_line="Logistique & paiement unifiés",
        accent=PALETTE.signal_active,
    ),
    RoadmapStage(
        step_code="03",
        status_label="Socle v0.1 actif",
        title="StatRAG (RAG Évalué)",
        stack_line="Python · pgvector · RLS",
        scope_line="Fidélité & IC 95 % bootstrap",
        accent=PALETTE.signal_data,
    ),
    RoadmapStage(
        step_code="04",
        status_label="Socle v0.1 actif",
        title="NetSentinel & GateShield",
        stack_line="Go · PCAP · Token Bucket",
        scope_line="Sonde réseau & reverse-proxy",
        accent=PALETTE.signal_systems,
    ),
)

STACK_COLUMNS: tuple[StackDomainColumn, ...] = (
    StackDomainColumn(
        title="Production & Full-Stack",
        subtitle="Éprouvé sur des applications livrées",
        accent=PALETTE.signal_active,
        rows=(
            ("TypeScript", "JavaScript", "SQL"),
            ("React", "Vite", "Tailwind CSS"),
            ("PostgreSQL (RLS)", "Supabase"),
            ("Node / Express", "Git & GitHub"),
        ),
    ),
    StackDomainColumn(
        title="Statistiques, Data & IA",
        subtitle="Socle académique UFHB & Rennes 2",
        accent=PALETTE.signal_data,
        rows=(
            ("Python", "Pandas", "NumPy"),
            ("Scikit-Learn", "Modélisation stat."),
            ("Diagnostic & nettoyage EDA",),
            ("pgvector", "Métriques de RAG"),
        ),
    ),
    StackDomainColumn(
        title="Systèmes, Cyber & R&D",
        subtitle="Montée en compétences active",
        accent=PALETTE.signal_systems,
        rows=(
            ("Go", "Rust", "Linux"),
            ("TCP/IP", "Wireshark", "Scapy"),
            ("Docker", "Redis", "Reverse-Proxy"),
            ("Godot Engine (2D/3D Mobile)",),
        ),
    ),
)

LANGUAGE_SLICES_2026: tuple[ShareSlice, ...] = (
    ShareSlice("TypeScript", 72.0, "#3178c6"),
    ShareSlice("Python", 16.8, "#f59e0b"),
    ShareSlice("JavaScript", 5.7, "#facc15"),
    ShareSlice("SQL", 2.7, "#34d399"),
    ShareSlice("CSS", 2.3, "#38bdf8"),
    ShareSlice("HTML", 0.5, "#fb7185"),
)

DOMAIN_SLICES_2026: tuple[ShareSlice, ...] = (
    ShareSlice("Front-end & interfaces", 48.2, "#58a6ff"),
    ShareSlice("Jeux de données (JSON, CSV)", 19.5, "#f59e0b"),
    ShareSlice("Back-end & microservices", 11.5, "#34d399"),
    ShareSlice("Logique métier partagée", 9.8, "#38bdf8"),
    ShareSlice("Documentation technique", 3.3, "#64748b"),
    ShareSlice("Pipelines Data & IA", 3.0, "#fbbf24"),
    ShareSlice("Outillage, scripts & config", 2.6, "#475569"),
    ShareSlice("Schémas SQL & politiques RLS", 2.1, "#2dd4bf"),
)

PORTFOLIO_BANDS: tuple[PortfolioBand, ...] = (
    PortfolioBand(
        category="Produits phares",
        subtitle="En ligne & référence",
        accent=PALETTE.signal_prod,
        projects=(
            ProjectTile("Daloa Market", "217 commits · +104 k · Google Play", 270),
            ProjectTile("OpenStats", "104 commits · +133 k · Analyse sans code", 290),
        ),
    ),
    PortfolioBand(
        category="Écosystème Daloa",
        subtitle="Logistique, API & Ops",
        accent=PALETTE.signal_active,
        projects=(
            ProjectTile("Daloa Delivery", "129 commits · +48 k", 210),
            ProjectTile("Daloa Pay & API", "90+ commits · Escrow & Webhooks", 258),
            ProjectTile("Docs & Status Daloa", "VitePress · Monitoring continu", 248),
        ),
    ),
    PortfolioBand(
        category="Data & Modélisation",
        subtitle="Scoring, quant & études",
        accent=PALETTE.signal_data,
        projects=(
            ProjectTile("ai-recruitment-score", "108 commits · +8,7 k", 198),
            ProjectTile("bot-trading-deriv", "15 commits · +12 k", 184),
            ProjectTile("plateforme-master-da", "6 commits · +9,4 k", 190),
            ProjectTile("comparateur-prix-ci", "10 commits · +7,3 k", 182),
        ),
    ),
    PortfolioBand(
        category="Systèmes & Labo",
        subtitle="R&D Go, RAG & sécurité",
        accent=PALETTE.signal_systems,
        projects=(
            ProjectTile("NetSentinel", "Go · Sonde PCAP & Welford", 190),
            ProjectTile("GateShield", "Go · Proxy & Token Bucket", 190),
            ProjectTile("StatRAG", "Python · pgvector & RLS", 184),
            ProjectTile("KlasNet & kripton", "+29,7 k · Shamir S.S.S", 196),
        ),
        footnote=(
            "+ 22 dépôts publics : pendu-royal (Android), SpaceJam, vanguard-sec, "
            "datasci-os, med-connect (offline-first), neural-recruit…"
        ),
    ),
)
