"""V2.0 Mega-Atlas: Generate 12 Publication-Grade Analytical Charts (PNG + Vector SVG) for 1,600+ Problems across 8 Macro-Pillars & 28 Superdomains."""

import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import seaborn as sns

from v2_loader import load_v2_master
from v2_schema import MACRO_PILLARS

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs_v2", "charts")
os.makedirs(OUT_DIR, exist_ok=True)

# 8-Colorblind-Safe Executive Jewel Palette for 8 Macro-Pillars
PILLAR_COLORS = {
    "Pure Mathematics": "#1D4ED8",                     # Cobalt Blue
    "Logic, Statistics & Computing": "#0284C7",        # Cerulean Cyan
    "Fundamental Physics & Cosmos": "#7C3AED",         # Deep Violet
    "Matter, Materials & Chemistry": "#9333EA",        # Royal Purple
    "Life, Mind & Medicine": "#059669",                # Emerald Green
    "AI, Quantum Tech, Hardware & Systems": "#EA580C", # Vivid Orange
    "Engineering, Design, Earth & Energy": "#0D9488",  # Deep Teal
    "Philosophy, Social & Humanities": "#BE185D",      # Crimson Rose
}

SHORT_PILLAR = {
    "Pure Mathematics": "Pure\nMath",
    "Logic, Statistics & Computing": "Logic, Stats\n& CS",
    "Fundamental Physics & Cosmos": "Physics &\nCosmos",
    "Matter, Materials & Chemistry": "Matter &\nChem",
    "Life, Mind & Medicine": "Life, Mind\n& Med",
    "AI, Quantum Tech, Hardware & Systems": "AI, QC, HW\n& Systems",
    "Engineering, Design, Earth & Energy": "Eng, Design,\nEarth & Enr",
    "Philosophy, Social & Humanities": "Phil, Social\n& Hum",
}

SHORT_SD = {
    "Number Theory & Arithmetic": "Number Theory & Arith.",
    "Algebra, Group & Category Theory": "Algebra, Groups & Cat.",
    "Geometry & Topology": "Geometry & Topology",
    "Analysis, Calculus, PDEs & Dynamics": "Analysis, PDEs & Dyn.",
    "Combinatorics & Graph Theory": "Combinatorics & Graphs",
    "Mathematical Logic, Set Theory & Computability": "Math Logic & Set Theory",
    "Probability, Stochastic Processes & Statistics": "Prob., Stoch. & Stats",
    "Computer Science, Complexity, Crypto & Info Theory": "CS, Complexity & Crypto",
    "Quantum Mechanics, QFT & Particle Physics": "QM, QFT & Particles",
    "Spacetime, Gravity, Time, Dimensions & Holography": "Spacetime, Gravity & Holo",
    "Astrophysics, Cosmology & Astrobiology": "Astro, Cosmo & SETI",
    "Condensed Matter, Solid-State & Quantum Materials": "Condensed Matter & Solids",
    "Fluids, Gases, Plasmas & Non-Equilibrium Matter": "Fluids, Gases & Plasmas",
    "Chemistry, Catalysis & Molecular Sciences": "Chemistry & Molecular",
    "Biology, Evolution, Origin of Life & Ecology": "Biology, Evolution & Life",
    "Neuroscience, Consciousness & Sentience": "Neuro, Mind & Sentience",
    "Medicine, Pharmacology, Longevity & Bioengineering": "Medicine & Longevity",
    "Artificial Intelligence, ML & Digital Simulations": "AI, ML & Simulations",
    "Quantum Computing & Quantum Information": "Quantum Computing & Info",
    "Electronics, Photonics & Computing Hardware": "Electronics & Hardware",
    "Systems, Control, Robotics & Cybernetics": "Systems, Control & Robot.",
    "Mechanical, Aerospace, Structural & Civil Engineering": "Mech, Aero, Struct & Civil",
    "Architecture, Urbanism, Design & Ergonomics": "Arch, Design & Ergonomics",
    "Geology, Geophysics, Earth, Ocean & Climate": "Geology, Ocean & Climate",
    "Energy, Environment, Food & Sustainability": "Energy, Food & Sustain.",
    "Philosophy, Metaphysics, Epistemology & Ethics": "Philosophy & Ethics",
    "Economics, Game Theory, Finance & Social Systems": "Economics & Social Sys",
    "Linguistics, Archaeology, History, Law & Aesthetics": "Linguistics, Law & Hum.",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 0.9,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 10.5,
    "xtick.labelsize": 8.8,
    "ytick.labelsize": 8.8,
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#F8FAFC",
    "grid.color": "#E2E8F0",
    "grid.linewidth": 0.7,
})


def save_fig(fig, stem: str, bg="#FFFFFF"):
    png = os.path.join(OUT_DIR, f"{stem}.png")
    svg = os.path.join(OUT_DIR, f"{stem}.svg")
    fig.savefig(png, dpi=220, bbox_inches="tight", facecolor=bg)
    fig.savefig(svg, bbox_inches="tight", facecolor=bg)
    plt.close(fig)
    print(f"  Saved {stem}.png & .svg")


def chart_01_superdomain_landscape(data):
    df_sd = data["df_superdomains"].copy()
    n_tot = data["summary_stats"]["total_problems"]
    df_sd["Short"] = df_sd["Superdomain"].map(SHORT_SD)
    df_sd["p_ord"] = df_sd["Macro_Pillar"].map({p: i for i, p in enumerate(MACRO_PILLARS)})
    df_sd = df_sd.sort_values(["p_ord", "Problem_Count"], ascending=[False, True]).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 12.8), gridspec_kw={"width_ratios": [1.55, 1.0]}, sharey=True)
    y = np.arange(len(df_sd))
    colors = [PILLAR_COLORS[p] for p in df_sd["Macro_Pillar"]]

    ax1.barh(y, df_sd["Problem_Count"], color=colors, height=0.72, edgecolor="white", linewidth=0.7, alpha=0.92)
    ax1.set_yticks(y)
    ax1.set_yticklabels(df_sd["Short"], fontsize=9.0, color="#0F172A", fontweight="bold")
    ax1.set_xlabel("Number of Cataloged Unsolved / Open / Hard Problems", fontweight="bold")
    ax1.set_title(f"A. Coverage Across All 28 Superdomains (N = {n_tot:,})", pad=10, loc="left")
    ax1.set_xlim(0, df_sd["Problem_Count"].max() * 1.18)
    ax1.grid(axis="x", linestyle="--", alpha=0.65)
    ax1.set_axisbelow(True)

    for i, (cnt, pct) in enumerate(zip(df_sd["Problem_Count"], df_sd["Share_Pct"])):
        ax1.text(cnt + 1.2, i, f"{cnt} ({pct:.1f}%)", va="center", ha="left", fontsize=8.2, fontweight="bold", color="#334155")

    for i, row in df_sd.iterrows():
        ax2.plot([row["Mean_Tractability_2050"], row["Mean_Difficulty"]], [i, i], color="#94A3B8", linewidth=2.0, zorder=2)
    ax2.scatter(df_sd["Mean_Difficulty"], y, color="#DC2626", s=58, zorder=4, label="Mean Difficulty (1–10)", marker="o", edgecolor="white", lw=0.6)
    ax2.scatter(df_sd["Mean_Tractability_2050"], y, color="#059669", s=58, zorder=4, label="Mean Tractability 2050 (1–10)", marker="s", edgecolor="white", lw=0.6)
    ax2.scatter(df_sd["Mean_Impact"], y, color="#F59E0B", s=55, zorder=5, label="Mean Civilizational Impact (1–10)", marker="D", edgecolor="#78350F", lw=0.5)
    ax2.set_xlim(1.5, 10.4)
    ax2.set_xlabel("Mean Quantitative Rating (1–10 Scale)", fontweight="bold")
    ax2.set_title("B. Hardness vs. 2050 Tractability Gap & Impact", pad=10, loc="left")
    ax2.grid(axis="x", linestyle="--", alpha=0.65)
    ax2.set_axisbelow(True)
    ax2.legend(loc="lower left", fontsize=8.5, frameon=True, facecolor="white", framealpha=0.95)

    handles = [mpatches.Patch(color=PILLAR_COLORS[p], label=p) for p in MACRO_PILLARS]
    fig.legend(handles=handles, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.99), frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=8.6)
    fig.suptitle(f"V2.0 Mega-Atlas Taxonomy of Humanity's {n_tot:,} Unsolved, Open & Hard Problems (28 Superdomains × 8 Macro-Pillars)", fontsize=15, fontweight="bold", color="#0F172A", y=1.03)
    plt.tight_layout(rect=[0, 0, 1, 0.935])
    save_fig(fig, "01_superdomain_landscape")


def chart_02_strategic_quadrant(data):
    df = data["df"].copy()
    n_tot = len(df)
    rng = np.random.default_rng(42)
    x = df["tractability_2050"].values + rng.uniform(-0.34, 0.34, n_tot)
    y = df["civilizational_impact"].values + rng.uniform(-0.34, 0.34, n_tot)

    fig, ax = plt.subplots(figsize=(15.5, 10.2))
    ax.axvspan(6.5, 10.6, ymin=(7.5 - 1.4) / (11.25 - 1.4), ymax=1.0, color="#ECFDF5", alpha=0.62, zorder=0)
    ax.axvspan(0.4, 6.5, ymin=(7.5 - 1.4) / (11.25 - 1.4), ymax=1.0, color="#FEF2F2", alpha=0.58, zorder=0)
    ax.axvspan(6.5, 10.6, ymin=0.0, ymax=(7.5 - 1.4) / (11.25 - 1.4), color="#EFF6FF", alpha=0.52, zorder=0)
    ax.axvspan(0.4, 6.5, ymin=0.0, ymax=(7.5 - 1.4) / (11.25 - 1.4), color="#F5F3FF", alpha=0.52, zorder=0)

    ax.axvline(6.5, color="#475569", linestyle="--", linewidth=1.4, zorder=1)
    ax.axhline(7.5, color="#475569", linestyle="--", linewidth=1.4, zorder=1)

    for pil in MACRO_PILLARS:
        mask = df["macro_pillar"] == pil
        sizes = 16 + np.minimum(df.loc[mask, "graph_degree"], 60) * 5.2
        ax.scatter(x[mask], y[mask], s=sizes, c=PILLAR_COLORS[pil], alpha=0.62, edgecolor="white", lw=0.45, label=pil, zorder=3)

    q_counts = df["strategic_quadrant"].value_counts()
    q_labels = [
        (8.55, 10.88, "Q1: NEAR-TERM CIVILIZATIONAL LEVERS", "Q1: Near-Term Civilizational Levers (High Impact, High Tractability)", "#065F46"),
        (3.45, 10.88, "Q2: GRAND CENTURIES-SCALE TITANS", "Q2: Grand Centuries-Scale Titans (High Impact, Low Tractability)", "#991B1B"),
        (8.55, 1.78, "Q3: TARGETED TECHNICAL FRONTIERS", "Q3: Targeted Technical Frontiers (Focused Impact, High Tractability)", "#1E40AF"),
        (3.45, 1.78, "Q4: DEEP FORMAL & EPISTEMIC ENIGMAS", "Q4: Deep Foundational & Formal Enigmas (Focused Impact, Low Tractability)", "#5B21B6"),
    ]
    for qx, qy, qt, qkey, qc in q_labels:
        cnt = int(q_counts.get(qkey, 0))
        ax.text(qx, qy, f"{qt}\nn = {cnt:,} ({100*cnt/n_tot:.1f}%)", ha="center", va="center", fontsize=9.4, fontweight="bold", color=qc,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=qc, alpha=0.95, lw=1.1), zorder=7)

    id_to_idx = {pid: i for i, pid in enumerate(df["id"])}
    callouts = [
        ("CS-001", "P vs. NP", (-0.15, -0.68)),
        ("NEURO-001", "Hard Problem of\nConsciousness", (-0.85, -0.82)),
        ("GR-001", "Quantum Gravity", (0.25, -0.58)),
        ("NT-001", "Riemann Hyp.\n(Nov 2026 Claim)", (-1.05, 0.28)),
        ("ANL-001", "Navier–Stokes 3D\n(Sept 2026 Claim)", (0.35, -0.52)),
        ("AI-001", "AI Alignment", (-0.85, 0.25)),
        ("BIO-001", "Abiogenesis", (-0.85, -0.58)),
        ("ASTRO-002", "Dark Energy / Λ", (-0.95, -0.55)),
        ("ENR-001", "Commercial Fusion", (-0.85, -0.42)),
        ("QC-001", "Fault-Tolerant QC", (0.55, -0.32)),
        ("GEO-002", "Climate Sensitivity", (0.52, 0.22)),
        ("MED-001", "Neurodegeneration", (-1.15, -0.45)),
        ("AI-003", "Simulation Hyp.", (0.38, -0.48)),
        ("NT-005", "Collatz (3n+1)", (0.35, 0.38)),
    ]
    for pid, lbl, (dx, dy) in callouts:
        if pid not in id_to_idx:
            continue
        i = id_to_idx[pid]
        ax.annotate(lbl, xy=(x[i], y[i]), xytext=(max(0.6, min(9.8, x[i] + dx)), max(2.2, min(10.35, y[i] + dy))),
                    fontsize=8.0, fontweight="bold", color="#0F172A",
                    bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#475569", alpha=0.92, lw=0.75),
                    arrowprops=dict(arrowstyle="->", color="#334155", lw=0.85, shrinkA=0, shrinkB=4), zorder=8)

    ax.set_xlim(0.4, 10.6)
    ax.set_ylim(1.4, 11.25)
    ax.set_xlabel("Estimated Tractability / Major Resolution Likelihood by 2050 (1 → 10)", fontweight="bold", fontsize=11)
    ax.set_ylabel("Civilizational, Scientific & Technological Impact if Solved (1 → 10)", fontweight="bold", fontsize=11)
    ax.set_title(f"Strategic 4-Quadrant Landscape of All {n_tot:,} Unsolved Problems (Bubble Size = Network Degree)", fontsize=14, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.55)
    leg = ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.155), ncol=4, frameon=True, facecolor="#F8FAFC", fontsize=8.8)
    for lh in leg.legend_handles:
        lh._sizes = [65]
    plt.tight_layout()
    save_fig(fig, "02_strategic_impact_tractability_quadrant")


def chart_03_coupling_heatmap(data):
    mat = data["df_coupling"].copy()
    sn = [SHORT_SD[s] for s in mat.index]
    mat.index = sn
    mat.columns = sn
    # Log-scaled color intensity so massive intra-domain counts don't wash out rich cross-domain bridges!
    mat_log = np.log1p(mat.values)

    fig, ax = plt.subplots(figsize=(17.5, 15.0))
    sns.heatmap(
        pd.DataFrame(mat_log, index=sn, columns=sn),
        ax=ax, cmap="YlGnBu", annot=mat.values, fmt="d",
        annot_kws={"size": 6.8}, linewidths=0.45, linecolor="#E2E8F0",
        cbar_kws={"label": "log(1 + Edge Count) — Cell Annotations Show Exact Coupling Counts", "shrink": 0.78},
        square=True,
    )
    for t in ax.texts:
        if t.get_text() == "0":
            t.set_text("·")
            t.set_color("#CBD5E1")
            t.set_fontsize(8)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8.2)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8.2)
    s = data["summary_stats"]
    ax.set_title(
        f"28×28 Cross-Superdomain Coupling Matrix ({s['total_graph_edges']:,} Total Edges | "
        f"{s['cross_superdomain_edge_pct']}% Cross-Superdomain | {s['cross_pillar_edge_pct']}% Cross-Pillar)",
        fontsize=13.8, fontweight="bold", pad=14
    )
    plt.tight_layout()
    save_fig(fig, "03_cross_domain_coupling_heatmap")


def chart_04_bottleneck_and_epistemic(data):
    ct_bp = data["ct_bottleneck_pillar"].drop(index="Total", columns="Total")[MACRO_PILLARS]
    ct_bp.columns = [SHORT_PILLAR[c] for c in ct_bp.columns]
    ct_bp = ct_bp.loc[ct_bp.sum(axis=1).sort_values(ascending=False).index]

    ct_te = data["ct_type_epistemic"].drop(index="Total", columns="Total")
    ct_te = ct_te.loc[ct_te.sum(axis=1).sort_values(ascending=False).index]
    ct_te.columns = [c.replace("-", "-\n") for c in ct_te.columns]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.5, 8.2), gridspec_kw={"width_ratios": [1.22, 1.0]})
    sns.heatmap(ct_bp, ax=ax1, cmap="OrRd", annot=True, fmt="d", linewidths=0.7, linecolor="white",
                cbar_kws={"label": "Problem Count", "shrink": 0.8}, annot_kws={"size": 9.0, "weight": "bold"})
    ax1.set_title("A. Primary Bottleneck × 8 Macro-Pillars", fontsize=12.5, fontweight="bold", pad=12)
    ax1.set_xlabel("")
    ax1.set_ylabel("Primary Bottleneck", fontweight="bold")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=18, ha="right", fontsize=8.2)

    sns.heatmap(ct_te, ax=ax2, cmap="PuBu", annot=True, fmt="d", linewidths=0.7, linecolor="white",
                cbar_kws={"label": "Problem Count", "shrink": 0.8}, annot_kws={"size": 9.0, "weight": "bold"})
    ax2.set_title("B. Problem Type × Epistemic Class", fontsize=12.5, fontweight="bold", pad=12)
    ax2.set_xlabel("")
    ax2.set_ylabel("Structural Problem Type", fontweight="bold")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, fontsize=8.3)

    fig.suptitle(f"Structural Anatomy of All {data['summary_stats']['total_problems']:,} Open Problems: Why They Resist Resolution", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "04_bottleneck_and_epistemic_matrices")


def chart_05_pillar_multimetric_profiles(data):
    df = data["df"].copy()
    df["SP"] = df["macro_pillar"].map(SHORT_PILLAR)
    order = [SHORT_PILLAR[p] for p in MACRO_PILLARS]
    pal = {SHORT_PILLAR[p]: PILLAR_COLORS[p] for p in MACRO_PILLARS}

    metrics = [
        ("difficulty_score", "A. Intrinsic Difficulty Score (1–10)"),
        ("tractability_2050", "B. Estimated Tractability by 2050 (1–10)"),
        ("civilizational_impact", "C. Civilizational & Scientific Impact (1–10)"),
        ("interdisciplinarity_index", "D. Cross-Domain Interdisciplinarity Index (1–10)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(17.5, 10.8))
    for ax, (col, title) in zip(axes.flat, metrics):
        sns.violinplot(data=df, x="SP", y=col, order=order, palette=pal, hue="SP", legend=False, ax=ax, inner="quartile", linewidth=0.9, alpha=0.65, cut=0)
        means = df.groupby("SP")[col].mean().reindex(order)
        ax.scatter(range(len(order)), means.values, color="#0F172A", marker="D", s=46, zorder=5)
        for idx, m in enumerate(means.values):
            ax.text(idx, min(10.5, m + 0.42), f"μ={m:.2f}", ha="center", va="bottom", fontsize=7.8, fontweight="bold",
                    color="#0F172A", bbox=dict(boxstyle="round,pad=0.14", facecolor="white", alpha=0.88, edgecolor="none"))
        ax.set_ylim(0.5, 11.35)
        ax.set_xlabel("")
        ax.set_ylabel("Score (1–10)", fontweight="bold")
        ax.set_title(title, fontsize=11.8, fontweight="bold", pad=9)
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.set_axisbelow(True)

    fig.suptitle(f"Comparative Quantitative Profiles Across All 8 Macro-Pillars (N = {len(df):,})", fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    save_fig(fig, "05_pillar_multimetric_profiles")


def chart_06_historical_timeline(data):
    df = data["df"].copy()
    n_tot = len(df)

    fig = plt.figure(figsize=(17.5, 11.4))
    gs = GridSpec(2, 2, height_ratios=[1.15, 1.0], width_ratios=[1.0, 1.15], hspace=0.38, wspace=0.58)

    ax_top = fig.add_subplot(gs[0, :])
    years = np.arange(1800, 2027, 2)
    bottom = np.zeros(len(years))
    for pil in MACRO_PILLARS:
        sub_y = df[df["macro_pillar"] == pil]["year_formulated"].values
        cum = np.array([(sub_y <= yr).sum() for yr in years])
        ax_top.fill_between(years, bottom, bottom + cum, color=PILLAR_COLORS[pil], alpha=0.84, label=pil, lw=0.4, edgecolor="white")
        bottom += cum

    pre1800 = int((df["year_formulated"] < 1800).sum())
    ymax = max(bottom) * 1.15
    ax_top.text(1804, ymax * 0.78, f"Pre-1800 Roots at Left Baseline: {pre1800} enduring problems\n(dating back to {abs(df['year_formulated'].min())} BCE in Philosophy, Math & Physics)",
                fontsize=8.6, color="#1E293B", bbox=dict(boxstyle="round,pad=0.38", facecolor="#FEF3C7", edgecolor="#D97706", alpha=0.95))
    ax_top.set_xlim(1800, 2026)
    ax_top.set_ylim(0, ymax)
    ax_top.set_xlabel("Year Formulated", fontweight="bold")
    ax_top.set_ylabel("Cumulative Active Open Problems", fontweight="bold")
    ax_top.set_title(f"A. Historical Accumulation of {n_tot:,} Unsolved Problems Across 8 Macro-Pillars (Pre-1800 to Nov 2026)", fontsize=12.6, fontweight="bold", pad=10)
    ax_top.legend(loc="upper left", bbox_to_anchor=(0.01, 0.72), ncol=2, fontsize=8.0, frameon=True, facecolor="white", framealpha=0.92)
    ax_top.grid(True, linestyle="--", alpha=0.5)

    ax_bl = fig.add_subplot(gs[1, 0])
    era_order = ["Antiquity (<500 CE)", "Early Modern (500-1799)", "19th Century (1800-1899)",
                 "Early-Mid 20th C. (1900-1969)", "Late 20th C. (1970-1999)", "21st Century (2000-2026)"]
    ct_ep = data["ct_era_pillar"].drop(index="Total", columns="Total").reindex(era_order).fillna(0)[MACRO_PILLARS]
    ct_ep.plot(kind="bar", stacked=True, color=[PILLAR_COLORS[p] for p in MACRO_PILLARS], ax=ax_bl, width=0.68, edgecolor="white", legend=False)
    for i, tot in enumerate(ct_ep.sum(axis=1)):
        ax_bl.text(i, tot + max(ct_ep.sum(axis=1)) * 0.018, f"{int(tot)}", ha="center", va="bottom", fontsize=8.8, fontweight="bold", color="#0F172A")
    ax_bl.set_xticklabels([e.replace(" (", "\n(") for e in era_order], rotation=20, ha="right", fontsize=8.1)
    ax_bl.set_ylabel("Number of Problems", fontweight="bold")
    ax_bl.set_xlabel("")
    ax_bl.set_title("B. Era of Formulation by 8 Macro-Pillars", fontsize=12, fontweight="bold", pad=10)
    ax_bl.grid(axis="y", linestyle="--", alpha=0.6)
    ax_bl.set_axisbelow(True)

    ax_br = fig.add_subplot(gs[1, 1])
    oldest = df.sort_values("year_formulated").head(14).iloc[::-1]
    labels = [r["name"][:32] + ("…" if len(r["name"]) > 32 else "") for _, r in oldest.iterrows()]
    y_pos = np.arange(len(oldest))
    ax_br.barh(y_pos, oldest["age_years_2026"], color=[PILLAR_COLORS[p] for p in oldest["macro_pillar"]], height=0.68, edgecolor="white")
    ax_br.set_yticks(y_pos)
    ax_br.set_yticklabels(labels, fontsize=8.1, fontweight="bold", color="#1E293B")
    ax_br.set_xlabel("Years Unsolved as of Nov 2026", fontweight="bold")
    ax_br.set_title("C. 14 Oldest Enduring Unsolved Problems", fontsize=12, fontweight="bold", pad=10)
    ax_br.set_xlim(0, oldest["age_years_2026"].max() * 1.28)
    for i, (_, r) in enumerate(oldest.iterrows()):
        yr_str = f"{abs(r['year_formulated'])} BCE" if r["year_formulated"] < 0 else str(r["year_formulated"])
        ax_br.text(r["age_years_2026"] + 35, i, f"{r['age_years_2026']:,}y ({yr_str})", va="center", fontsize=7.6, fontweight="bold", color="#334155")
    ax_br.grid(axis="x", linestyle="--", alpha=0.6)
    ax_br.set_axisbelow(True)

    fig.suptitle(f"Longevity & Historical Accumulation of Humanity's {n_tot:,} Unsolved Problems", fontsize=15, fontweight="bold", y=0.99)
    save_fig(fig, "06_historical_timeline_and_longevity")


def chart_07_radial_connectome(data):
    """8-Pillar Radial Connectome Knowledge Graph of ALL 1,600+ Problems & Cross-Pillar Bridges."""
    G = data["G"]
    df = data["df"].copy()
    df_k = data["df_keystones"]
    id_map = data["id_map"]
    s = data["summary_stats"]

    p_ord = {p: i for i, p in enumerate(MACRO_PILLARS)}
    df["p_ord"] = df["macro_pillar"].map(p_ord)
    df_ord = df.sort_values(["p_ord", "superdomain", "graph_degree"], ascending=[True, True, False]).reset_index(drop=True)

    gap_rad = 0.068
    usable_rad = 2 * np.pi - gap_rad * len(MACRO_PILLARS)
    n_tot = len(df_ord)

    angles = {}
    pillar_arcs = {}
    cur = np.pi / 2.0
    for pil in MACRO_PILLARS:
        sub = df_ord[df_ord["macro_pillar"] == pil]
        span = usable_rad * (len(sub) / n_tot)
        t_start, t_end = cur, cur - span
        pillar_arcs[pil] = (t_start, t_end, (t_start + t_end) / 2.0)
        for pid, th in zip(sub["id"], np.linspace(t_start, t_end, len(sub), endpoint=False)):
            angles[pid] = th
        cur = t_end - gap_rad

    pos = {pid: (np.cos(th), np.sin(th)) for pid, th in angles.items()}

    fig, ax = plt.subplots(figsize=(17.0, 17.0))
    ax.set_facecolor("#0B1120")
    fig.patch.set_facecolor("#0B1120")

    # Draw cross-pillar bridges & high-centrality edges cleanly (sample gently if >4,500 edges so figure stays razor sharp)
    all_edges = list(G.edges())
    cross_edges = [(u, v) for u, v in all_edges if id_map[u]["macro_pillar"] != id_map[v]["macro_pillar"]]
    intra_edges = [(u, v) for u, v in all_edges if id_map[u]["macro_pillar"] == id_map[v]["macro_pillar"]]
    rng = np.random.default_rng(7)
    if len(intra_edges) > 1600:
        idx_keep = rng.choice(len(intra_edges), 1600, replace=False)
        intra_draw = [intra_edges[i] for i in idx_keep]
    else:
        intra_draw = intra_edges
    if len(cross_edges) > 1800:
        idx_keep = rng.choice(len(cross_edges), 1800, replace=False)
        cross_draw = [cross_edges[i] for i in idx_keep]
    else:
        cross_draw = cross_edges

    for u, v in intra_draw:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        cx, cy = (x1 + x2) * 0.44, (y1 + y2) * 0.44
        ax.add_patch(patches.PathPatch(Path([(x1, y1), (cx, cy), (x2, y2)], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                                       facecolor="none", edgecolor=PILLAR_COLORS[id_map[u]["macro_pillar"]], lw=0.45, alpha=0.22, zorder=1))
    for u, v in cross_draw:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        cx, cy = (x1 + x2) * 0.14, (y1 + y2) * 0.14
        ax.add_patch(patches.PathPatch(Path([(x1, y1), (cx, cy), (x2, y2)], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                                       facecolor="none", edgecolor="#38BDF8", lw=0.58, alpha=0.16, zorder=1))

    # Outer pillar bands & cleanly separated sector banners
    for pil, (ts, te, tm) in pillar_arcs.items():
        arc_t = np.linspace(te, ts, 90)
        ax.plot(1.045 * np.cos(arc_t), 1.045 * np.sin(arc_t), color=PILLAR_COLORS[pil], lw=6.5, solid_capstyle="round", zorder=3)
        cnt = int((df["macro_pillar"] == pil).sum())
        rx, ry = 1.92 * np.cos(tm), 1.90 * np.sin(tm)
        ax.text(rx, ry, f"{pil.upper()}\n(n = {cnt:,})", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#FFFFFF",
                bbox=dict(boxstyle="round,pad=0.35", facecolor=PILLAR_COLORS[pil], edgecolor="#E2E8F0", lw=1.0, alpha=0.96), zorder=8)

    # Nodes around ring
    xs = [pos[pid][0] for pid in df_ord["id"]]
    ys = [pos[pid][1] for pid in df_ord["id"]]
    cs = [PILLAR_COLORS[id_map[pid]["macro_pillar"]] for pid in df_ord["id"]]
    sz = [6 + min(id_map[pid]["graph_degree"], 65) * 3.8 for pid in df_ord["id"]]
    ax.scatter(xs, ys, s=sz, c=cs, edgecolors="#F8FAFC", lw=0.35, alpha=0.92, zorder=4)

    # Radially label Top 28 Keystone Hubs with strict angular separation
    placed = []
    for _, row in df_k.head(90).iterrows():
        pid = row["id"]
        th = angles[pid]
        if any(min(abs(th - pa), 2 * np.pi - abs(th - pa)) < 0.155 for pa in placed):
            continue
        placed.append(th)
        px, py = pos[pid]
        ax.plot([px, 1.095 * np.cos(th)], [py, 1.095 * np.sin(th)], color="#F8FAFC", lw=0.8, alpha=0.8, zorder=5)
        lx, ly = 1.12 * np.cos(th), 1.12 * np.sin(th)
        short_nm = row["name"].split(":")[0].split("(")[0].strip()[:24]
        deg_rot = np.degrees(th)
        ha = "left"
        if np.cos(th) < 0:
            deg_rot += 180
            ha = "right"
        ax.text(lx, ly, f"{short_nm} [{row['graph_degree']}]", fontsize=8.0, fontweight="bold", color="#F8FAFC",
                rotation=deg_rot, rotation_mode="anchor", ha=ha, va="center", zorder=7)
        if len(placed) >= 28:
            break

    ax.text(0, 0,
            f"V2.0 UNIFIED CONNECTOME\n{s['total_problems']:,} Open Problems\n{s['total_graph_edges']:,} Coupling Edges\n{s['connected_components']} Connected Component\n{s['cross_pillar_edge_pct']}% Cross-Pillar Bridges",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#E2E8F0",
            bbox=dict(boxstyle="circle,pad=0.65", facecolor="#0F172A", edgecolor="#38BDF8", lw=1.8, alpha=0.94), zorder=9)

    ax.set_xlim(-2.36, 2.36)
    ax.set_ylim(-2.18, 2.18)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Complete 8-Pillar Radial Connectome of Humanity's {s['total_problems']:,} Unsolved Problems ({s['total_graph_edges']:,} Dependencies)\n"
        "Cyan Chords = Cross-Pillar Bridges | Colored Arcs = Intra-Pillar Couplings | Outer Labels = Top Keystone Hubs [Degree]",
        fontsize=13.4, fontweight="bold", color="#FFFFFF", pad=12
    )
    plt.tight_layout()
    save_fig(fig, "07_keystone_knowledge_graph", bg="#0B1120")


def chart_08_scale_and_verification(data):
    df = data["df"]
    scale_order = ["Planck / Sub-Atomic", "Atomic / Molecular", "Mesoscale / Cellular",
                   "Macroscopic / Human", "Planetary / Ecological", "Astrophysical / Cosmic",
                   "Scale-Invariant / Abstract Formal"]
    ep_order = ["Formal-Deductive", "Hybrid Formal-Empirical", "Empirical-Explanatory",
                "Constructive-Technological", "Normative-Philosophical"]
    ep_colors = ["#1D4ED8", "#7C3AED", "#059669", "#EA580C", "#BE185D"]

    ct_se = pd.crosstab(df["scale_regime"], df["epistemic_class"]).reindex(index=scale_order, columns=ep_order, fill_value=0)
    ct_vb = pd.crosstab(df["verification_type"], df["primary_bottleneck"])
    ct_vb = ct_vb.loc[ct_vb.sum(axis=1).sort_values(ascending=False).index]
    ct_vb = ct_vb[ct_vb.sum(axis=0).sort_values(ascending=False).index]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.5, 7.8), gridspec_kw={"width_ratios": [1.0, 1.22]})
    ct_se.plot(kind="barh", stacked=True, color=ep_colors, ax=ax1, width=0.68, edgecolor="white")
    ax1.invert_yaxis()
    max_s = ct_se.sum(axis=1).max()
    for i, tot in enumerate(ct_se.sum(axis=1)):
        ax1.text(tot + max_s * 0.015, i, f"{int(tot):,}", va="center", fontsize=8.8, fontweight="bold", color="#0F172A")
    ax1.set_xlim(0, max_s * 1.18)
    ax1.set_xlabel("Number of Open Problems", fontweight="bold")
    ax1.set_ylabel("Physical / Abstract Scale Regime", fontweight="bold")
    ax1.set_title("A. Physical & Abstract Scale Regimes × Epistemic Class", fontsize=12.3, fontweight="bold", pad=12)
    ax1.legend(title="Epistemic Class", fontsize=8.0, title_fontsize=8.6, loc="upper right", frameon=True, facecolor="white", framealpha=0.95)
    ax1.grid(axis="x", linestyle="--", alpha=0.6)
    ax1.set_axisbelow(True)

    short_bn = {
        "Mathematical Tools Missing": "Math Tools\nMissing",
        "Multiscale Coupling Complexity": "Multiscale\nCoupling",
        "Materials / Physical Limit": "Materials /\nPhysical",
        "Conceptual / Paradigmatic Gap": "Conceptual /\nParadigm",
        "Data / Observational Horizon Limit": "Data / Obs.\nHorizon",
        "Computational Complexity Barrier": "Compute\nComplexity",
        "Measurement / Instrumentation Limit": "Measurement\nLimit",
        "Ethical / Normative Ambiguity": "Ethical /\nNormative",
        "Energy / Experimental Scale Limit": "Energy Scale\nLimit",
    }
    ct_vb.columns = [short_bn.get(c, c) for c in ct_vb.columns]
    ct_vb.index = [textwrap.fill(r, 24) for r in ct_vb.index]
    sns.heatmap(ct_vb, ax=ax2, cmap="YlOrBr", annot=True, fmt="d", linewidths=0.7, linecolor="white",
                cbar_kws={"label": "Problem Count", "shrink": 0.8}, annot_kws={"size": 8.8, "weight": "bold"})
    ax2.set_title("B. Verification Mode × Primary Bottleneck", fontsize=12.3, fontweight="bold", pad=12)
    ax2.set_xlabel("")
    ax2.set_ylabel("How a Solution Is Verified", fontweight="bold")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=26, ha="right", fontsize=8.2)
    ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=8.5)

    fig.suptitle(f"Scale-to-Epistemology & Verification Architecture Across {len(df):,} Open Problems", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "08_scale_regime_vs_verification")


def chart_09_industry_heatmap(data):
    mat = data["df_industry"].copy()
    mat.index = [SHORT_SD[s] for s in mat.index]

    fig, ax = plt.subplots(figsize=(17.2, 13.0))
    sns.heatmap(mat, ax=ax, cmap="GnBu", annot=True, fmt="d", linewidths=0.55, linecolor="#E2E8F0",
                cbar_kws={"label": "Coupled Open Problems Exposing Industry Sector", "shrink": 0.82},
                annot_kws={"size": 8.0, "weight": "bold"})
    for t in ax.texts:
        if t.get_text() == "0":
            t.set_text("·")
            t.set_color("#CBD5E1")
            t.set_fontweight("normal")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=34, ha="right", fontsize=9.0, fontweight="bold")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8.5, fontweight="bold")
    ax.set_title("Global Industry & Economic Sector Exposure Matrix (28 Superdomains × 16 Canonical Sectors)", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Affected Global Industries & Economic Sectors", fontweight="bold", labelpad=10)
    ax.set_ylabel("28 Scientific, Engineering & Humanities Superdomains", fontweight="bold")
    plt.tight_layout()
    save_fig(fig, "09_industry_exposure_heatmap")


def chart_10_correlations_and_benchmarks(data):
    df = data["df"].copy()
    df_b = data["df_benchmarks"].copy().sort_values("years_open", ascending=True)
    num_cols = [
        ("difficulty_score", "Difficulty"),
        ("tractability_2050", "Tractability\n2050"),
        ("civilizational_impact", "Civiliz.\nImpact"),
        ("interdisciplinarity_index", "Interdisc.\nIndex"),
        ("graph_degree", "Graph\nDegree"),
        ("cross_pillar_links", "Cross-Pillar\nBridges"),
        ("age_years_2026", "Problem\nAge (Yrs)"),
        ("titan_index", "Titan\nIndex"),
    ]
    corr = df[[c for c, _ in num_cols]].corr()
    lbls = [l for _, l in num_cols]
    corr.index = lbls
    corr.columns = lbls

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.2, 8.6), gridspec_kw={"width_ratios": [1.0, 1.2]})
    sns.heatmap(corr, ax=ax1, cmap="RdBu_r", center=0, vmin=-1, vmax=1, annot=True, fmt=".2f",
                linewidths=0.7, linecolor="white", square=True,
                cbar_kws={"label": "Pearson r", "shrink": 0.78}, annot_kws={"size": 8.6, "weight": "bold"})
    ax1.set_title(f"A. Quantitative Correlations (N = {len(df):,})", fontsize=11.4, fontweight="bold", pad=12)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=32, ha="right", fontsize=8.3)
    ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=8.3)

    y = np.arange(len(df_b))
    bar_colors = ["#059669" if yr >= 2023 else "#2563EB" if yr >= 2012 else "#7C3AED" for yr in df_b["year_solved"]]
    ax2.barh(y, df_b["years_open"], color=bar_colors, height=0.68, edgecolor="white")
    short_b = [f"{r['name'][:38]}…" if len(r["name"]) > 39 else r["name"] for _, r in df_b.iterrows()]
    ax2.set_yticks(y)
    ax2.set_yticklabels(short_b, fontsize=8.2, fontweight="bold")
    ax2.set_xlabel("Years Open Before Historic Breakthrough", fontweight="bold")
    ax2.set_title("B. 20 Resolved Historical Benchmarks (1995–2026)", fontsize=11.8, fontweight="bold", pad=12)
    ax2.set_xlim(0, 440)
    for i, (_, r) in enumerate(df_b.iterrows()):
        ax2.text(r["years_open"] + 5, i, f"{r['years_open']}y ({r['year_posed']}→{r['year_solved']})", va="center", fontsize=7.6, fontweight="bold", color="#1E293B")
    b_handles = [
        mpatches.Patch(color="#059669", label="2023–2026 Wave"),
        mpatches.Patch(color="#2563EB", label="2012–2022 Breakthroughs"),
        mpatches.Patch(color="#7C3AED", label="1995–2011 Classics"),
    ]
    ax2.legend(handles=b_handles, loc="lower right", fontsize=8.3, frameon=True, facecolor="white")
    ax2.grid(axis="x", linestyle="--", alpha=0.6)
    ax2.set_axisbelow(True)

    fig.suptitle("Empirical Structure of Hardness vs. 20 Historical Breakthrough Benchmarks", fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    save_fig(fig, "10_correlation_and_resolved_benchmarks")


def chart_11_nov2026_status_and_registries(data):
    """Brand-New V2.0 Chart: Nov 20, 2026 Research Status & Global Registry Scale Comparison."""
    df = data["df"]
    n_tot = len(df)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.2, 7.6), gridspec_kw={"width_ratios": [1.1, 1.1]})

    # Left: 2026 Status breakdown across all problems (stacked by Macro-Pillar)
    ct_sp = data["ct_status_pillar"].drop(index="Total", columns="Total")[MACRO_PILLARS]
    ct_sp = ct_sp.loc[ct_sp.sum(axis=1).sort_values(ascending=True).index]
    ct_sp.plot(kind="barh", stacked=True, color=[PILLAR_COLORS[p] for p in MACRO_PILLARS], ax=ax1, width=0.68, edgecolor="white", legend=False)
    max_x = ct_sp.sum(axis=1).max()
    for i, tot in enumerate(ct_sp.sum(axis=1)):
        ax1.text(tot + max_x * 0.015, i, f"{int(tot):,} ({100*tot/n_tot:.1f}%)", va="center", fontsize=8.4, fontweight="bold", color="#0F172A")
    ax1.set_xlim(0, max_x * 1.24)
    ax1.set_xlabel("Number of Problems", fontweight="bold")
    ax1.set_ylabel("")
    ax1.set_title("A. Nov 20, 2026 Verification & Research Status Breakdown", fontsize=12.2, fontweight="bold", pad=12)
    ax1.grid(axis="x", linestyle="--", alpha=0.6)
    ax1.set_axisbelow(True)

    # Right: Global Open-Problem Trackers & Nov 2026 Scale Comparison
    regs = [
        ("This V2.0 Mega-Atlas\n(ALL 28 Superdomains)", n_tot, "#0284C7"),
        ("Erdős Problems DB\n(Total Tracked; ~630 Open)", 1221, "#1D4ED8"),
        ("Wikipedia Unsolved\nLists (20+ Fields Est.)", 1200, "#0D9488"),
        ("ProofAtlas.ai Full\n(Eligible; 243 Open Top-500)", 1100, "#7C3AED"),
        ("Kourovka Notebook\n(Group Theory Only)", 1000, "#6366F1"),
        ("OpenAI Oct 2026 Dump\n(722 Unrefereed MSS / 372 Topics)", 722, "#DC2626"),
        ("Open Problem Garden\n(Math Wiki Curated)", 650, "#059669"),
        ("Kirby Topology List\n(Low-Dim Manifolds/Knots)", 360, "#EA580C"),
        ("V1.0 Earlier Catalog\n(Superseded Baseline)", 278, "#94A3B8"),
    ]
    regs = regs[::-1]
    y2 = np.arange(len(regs))
    ax2.barh(y2, [r[1] for r in regs], color=[r[2] for r in regs], height=0.68, edgecolor="white")
    ax2.set_yticks(y2)
    ax2.set_yticklabels([r[0] for r in regs], fontsize=8.4, fontweight="bold", color="#0F172A")
    ax2.set_xlabel("Number of Cataloged Problems / Manuscripts", fontweight="bold")
    ax2.set_title("B. Global Open-Problem Registries & Oct–Nov 2026 Scale Comparison", fontsize=12.2, fontweight="bold", pad=12)
    ax2.set_xlim(0, max(r[1] for r in regs) * 1.2)
    for i, (_, val, _) in enumerate(regs):
        ax2.text(val + 22, i, f"{val:,}", va="center", fontsize=8.6, fontweight="bold", color="#0F172A")
    ax2.grid(axis="x", linestyle="--", alpha=0.6)
    ax2.set_axisbelow(True)

    handles = [mpatches.Patch(color=PILLAR_COLORS[p], label=p) for p in MACRO_PILLARS]
    fig.legend(handles=handles, loc="lower center", ncol=4, bbox_to_anchor=(0.30, -0.09), frameon=True, facecolor="#F8FAFC", fontsize=8.0)
    fig.suptitle("November 20, 2026 Verification Landscape: Traditional Open Frontiers vs. Unverified AI Proof Claims & Global Trackers", fontsize=14.2, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "11_nov2026_status_and_registries")


def chart_12_top25_keystone_dominoes(data):
    """Horizontal comparative scorecard of the Top 25 Keystone Domino Hub Problems across all human knowledge."""
    top = data["df_keystones"].head(25).iloc[::-1].copy()
    labels = [f"[{r['id']}] {r['name'][:34]}{'…' if len(r['name'])>34 else ''}" for _, r in top.iterrows()]
    y = np.arange(len(top))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17.5, 10.5), gridspec_kw={"width_ratios": [1.35, 1.0]}, sharey=True)
    intra_deg = top["graph_degree"] - top["cross_pillar_links"]
    ax1.barh(y, intra_deg, color="#64748B", height=0.70, label="Intra-Pillar Links", edgecolor="white")
    ax1.barh(y, top["cross_pillar_links"], left=intra_deg, color=[PILLAR_COLORS[p] for p in top["macro_pillar"]], height=0.70, label="Cross-Pillar Bridge Links (Colored by Pillar)", edgecolor="white")
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, fontsize=8.4, fontweight="bold", color="#0F172A")
    ax1.set_xlabel("Total Knowledge-Graph Coupling Degree (Intra-Pillar + Cross-Pillar Bridges)", fontweight="bold")
    ax1.set_title("A. Top 25 Keystone Domino Hubs by Coupling Degree", fontsize=12.2, fontweight="bold", pad=10, loc="left")
    ax1.set_xlim(0, top["graph_degree"].max() * 1.18)
    for i, (_, r) in enumerate(top.iterrows()):
        ax1.text(r["graph_degree"] + 0.8, i, f"{r['graph_degree']} ({r['cross_pillar_links']} XP)", va="center", fontsize=8.0, fontweight="bold", color="#1E293B")
    ax1.legend(loc="lower right", fontsize=8.4, frameon=True, facecolor="white")
    ax1.grid(axis="x", linestyle="--", alpha=0.6)
    ax1.set_axisbelow(True)

    # Right: Titan Index vs Near-Term Leverage
    w = 0.36
    ax2.barh(y + w / 2, top["titan_index"], height=w, color="#1D4ED8", label="Composite Titan Index (Hardness + Impact + Centrality)")
    leverage = (top["civilizational_impact"] * top["tractability_2050"]) / 10.0
    ax2.barh(y - w / 2, leverage, height=w, color="#10B981", label="Near-Term 2050 Leverage (Impact × Tractability / 10)")
    ax2.set_xlim(0, 11.2)
    ax2.set_xlabel("Composite Index Score (0–10)", fontweight="bold")
    ax2.set_title("B. Grand Titan Score vs. Near-Term 2050 Leverage", fontsize=12.2, fontweight="bold", pad=10, loc="left")
    ax2.legend(loc="lower right", fontsize=8.3, frameon=True, facecolor="white")
    ax2.grid(axis="x", linestyle="--", alpha=0.6)
    ax2.set_axisbelow(True)

    fig.suptitle("Top 25 Keystone Domino Problems: Solving These Unlocks the Largest Multi-Domain Cascades", fontsize=14.8, fontweight="bold", y=1.01)
    plt.tight_layout()
    save_fig(fig, "12_top25_keystone_dominoes")


def main():
    print("Loading V2.0 Mega-Atlas for 12 publication-grade charts...")
    data = load_v2_master()
    chart_01_superdomain_landscape(data)
    chart_02_strategic_quadrant(data)
    chart_03_coupling_heatmap(data)
    chart_04_bottleneck_and_epistemic(data)
    chart_05_pillar_multimetric_profiles(data)
    chart_06_historical_timeline(data)
    chart_07_radial_connectome(data)
    chart_08_scale_and_verification(data)
    chart_09_industry_heatmap(data)
    chart_10_correlations_and_benchmarks(data)
    chart_11_nov2026_status_and_registries(data)
    chart_12_top25_keystone_dominoes(data)
    print("All 12 V2.0 charts (24 files: PNG + SVG) generated!")


if __name__ == "__main__":
    main()
