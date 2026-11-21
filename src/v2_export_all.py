"""V2.0 Mega-Atlas Unified Exporter: CSV, TSV, JSON, 13-Sheet XLSX, Legacy XLS, MD, TXT, Interactive HTML & Vector PDF Monograph."""

import os
import json
import html
import base64
import subprocess
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.chart import BarChart, Reference
import xlwt

from v2_loader import load_v2_master
from v2_schema import MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(BASE_DIR, "outputs_v2")
CHARTS_DIR = os.path.join(OUT_DIR, "charts")
os.makedirs(OUT_DIR, exist_ok=True)

PILLAR_HEX = {
    "Pure Mathematics": "#1D4ED8",
    "Logic, Statistics & Computing": "#0284C7",
    "Fundamental Physics & Cosmos": "#7C3AED",
    "Matter, Materials & Chemistry": "#9333EA",
    "Life, Mind & Medicine": "#059669",
    "AI, Quantum Tech, Hardware & Systems": "#EA580C",
    "Engineering, Design, Earth & Energy": "#0D9488",
    "Philosophy, Social & Humanities": "#BE185D",
}

CHART_ITEMS = [
    ("01_superdomain_landscape.png", "Figure 1 · 28-Superdomain Coverage, Hardness vs. 2050 Tractability Gap & Civilizational Impact"),
    ("02_strategic_impact_tractability_quadrant.png", "Figure 2 · Strategic 4-Quadrant Landscape (Civilizational Impact vs. Tractability by 2050)"),
    ("03_cross_domain_coupling_heatmap.png", "Figure 3 · 28×28 Cross-Superdomain Knowledge-Graph Coupling Matrix"),
    ("04_bottleneck_and_epistemic_matrices.png", "Figure 4 · Primary Bottlenecks × 8 Macro-Pillars & Problem Types × Epistemic Classes"),
    ("05_pillar_multimetric_profiles.png", "Figure 5 · Quantitative Distribution Profiles Across All 8 Macro-Pillars"),
    ("06_historical_timeline_and_longevity.png", "Figure 6 · Historical Accumulation (500 BCE – Nov 2026) & 14 Oldest Surviving Problems"),
    ("07_keystone_knowledge_graph.png", "Figure 7 · Complete 8-Pillar Radial Connectome of All Open Problems & Cross-Pillar Bridges"),
    ("08_scale_regime_vs_verification.png", "Figure 8 · Physical/Abstract Scale Regimes × Epistemic Class & Verification Modes"),
    ("09_industry_exposure_heatmap.png", "Figure 9 · Global Industry Exposure Matrix (28 Superdomains × 16 Economic Sectors)"),
    ("10_correlation_and_resolved_benchmarks.png", "Figure 10 · Quantitative Structural Correlations & 20 Resolved Historical Benchmarks (1995–2026)"),
    ("11_nov2026_status_and_registries.png", "Figure 11 · November 20, 2026 Verification Status & Global Open-Problem Registry Scale Comparison"),
    ("12_top25_keystone_dominoes.png", "Figure 12 · Top 25 Keystone Domino Hubs: Coupling Degree, Cross-Pillar Bridges & Leverage"),
]


def b64_img(fname: str) -> str:
    with open(os.path.join(CHARTS_DIR, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def df_to_md(df: pd.DataFrame, include_index=False) -> str:
    d = df.reset_index() if include_index else df.copy()
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in d.itertuples(index=False):
        vals = [str(v).replace("|", "\\|").replace("\n", " ") for v in row]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def df_to_ascii(df: pd.DataFrame, include_index=False, max_col_w=38) -> str:
    d = df.reset_index() if include_index else df.copy()
    cols = [str(c) for c in d.columns]
    rows = [[str(v).replace("\n", " ")[:max_col_w] for v in r] for r in d.itertuples(index=False)]
    widths = [max(len(cols[i]), max((len(r[i]) for r in rows), default=0)) for i in range(len(cols))]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    hdr = "|" + "|".join(f" {cols[i]:<{widths[i]}} " for i in range(len(cols))) + "|"
    out = [sep, hdr, sep.replace("-", "=")]
    for r in rows:
        out.append("|" + "|".join(f" {r[i]:<{widths[i]}} " for i in range(len(cols))) + "|")
    out.append(sep)
    return "\n".join(out)


def df_to_html_table(df: pd.DataFrame, include_index=False, cls="data-table") -> str:
    d = df.reset_index() if include_index else df.copy()
    parts = [f'<div class="table-wrap"><table class="{cls}"><thead><tr>']
    for c in d.columns:
        parts.append(f"<th>{html.escape(str(c))}</th>")
    parts.append("</tr></thead><tbody>")
    for row in d.itertuples(index=False):
        parts.append("<tr>")
        for v in row:
            s = "" if pd.isna(v) else str(v)
            num_cls = ' class="num"' if isinstance(v, (int, float)) else ""
            parts.append(f"<td{num_cls}>{html.escape(s)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts)


# ==================== 1. CSV / TSV / JSON ====================
def export_csv_tsv_json(data):
    df = data["df"]
    p_csv = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.csv")
    df.to_csv(p_csv, index=False, encoding="utf-8-sig")
    print(f"  Saved CSV: {p_csv} ({len(df):,} rows × {len(df.columns)} cols)")

    p_tsv = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.tsv")
    df.to_csv(p_tsv, index=False, sep="\t", encoding="utf-8")
    print(f"  Saved TSV: {p_tsv}")

    p_json = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.json")
    payload = {
        "metadata": {
            "title": "V2.0 Mega-Atlas of Humanity's Unsolved, Open & Hard Problems (November 20, 2026 Edition)",
            "summary_stats": data["summary_stats"],
        },
        "external_registries_nov2026": data["df_registries"].to_dict(orient="records"),
        "ai_verification_audit_nov2026": data["df_ai_audit"].to_dict(orient="records"),
        "macro_pillar_comparison": data["df_pillars"].to_dict(orient="records"),
        "superdomain_scorecard": data["df_superdomains"].to_dict(orient="records"),
        "keystone_network_rankings_top100": data["df_keystones"].head(100).to_dict(orient="records"),
        "pairwise_deep_contrasts": data["df_contrasts"].to_dict(orient="records"),
        "recently_resolved_benchmarks": data["df_benchmarks"].to_dict(orient="records"),
        "cross_superdomain_coupling_matrix": data["df_coupling"].to_dict(),
        "industry_exposure_matrix": data["df_industry"].to_dict(),
        "knowledge_graph_edges": [{"source": u, "target": v} for u, v in data["G"].edges()],
        "problems": df.to_dict(orient="records"),
    }
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  Saved JSON: {p_json}")


# ==================== 2. 13-SHEET XLSX & LEGACY XLS ====================
def style_ws(ws, end_row: int, end_col: int, header_hex="0F172A", freeze="B2", wrap_idxs=None):
    hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    hdr_fill = PatternFill("solid", fgColor=header_hex)
    zebra = PatternFill("solid", fgColor="F8FAFC")
    white = PatternFill("solid", fgColor="FFFFFF")
    thin = Side(style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    body_font = Font(name="Calibri", size=9.5, color="0F172A")
    wrap_idxs = set(wrap_idxs or [])

    for c in range(1, end_col + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws.row_dimensions[1].height = 28

    for r in range(2, end_row + 1):
        fill = zebra if r % 2 == 1 else white
        for c in range(1, end_col + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = body_font
            cell.fill = fill
            cell.border = border
            is_num = isinstance(cell.value, (int, float)) or (isinstance(cell.value, str) and cell.value.startswith("="))
            cell.alignment = Alignment(horizontal="right" if is_num else "left", vertical="top" if c in wrap_idxs else "center", wrap_text=(c in wrap_idxs))
    ws.freeze_panes = freeze
    ws.auto_filter.ref = f"A1:{get_column_letter(end_col)}{end_row}"


def write_sheet(wb, name: str, df_in: pd.DataFrame, include_index=False, header_hex="0F172A", wrap_names=None, freeze="B2"):
    ws = wb.create_sheet(title=name[:31])
    d = df_in.reset_index() if include_index else df_in.copy()
    cols = list(d.columns)
    ws.append([str(c) for c in cols])
    for row in d.itertuples(index=False):
        ws.append(["" if pd.isna(v) else v for v in row])
    wrap_idxs = {cols.index(w) + 1 for w in (wrap_names or []) if w in cols}
    style_ws(ws, len(d) + 1, len(cols), header_hex=header_hex, freeze=freeze, wrap_idxs=wrap_idxs)
    for c_i, col in enumerate(cols, 1):
        sample = [len(str(col))] + [len(str(v)) for v in d.iloc[:60, c_i - 1]]
        w = min(44, max(24, max(sample) * 0.5)) if c_i in wrap_idxs else min(34, max(11, max(sample) + 3))
        ws.column_dimensions[get_column_letter(c_i)].width = w
    return ws


def export_excel_files(data):
    df = data["df"]
    s = data["summary_stats"]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Locate exact dynamic Excel column letters in Master_Catalog
    cols_m = list(df.columns)
    col_ltr = lambda cname: get_column_letter(cols_m.index(cname) + 1)
    n_rows = len(df) + 1
    L_PIL = col_ltr("macro_pillar")
    L_YR = col_ltr("year_formulated")
    L_AGE = col_ltr("age_years_2026")
    L_DIFF = col_ltr("difficulty_score")
    L_TRAC = col_ltr("tractability_2050")
    L_IMP = col_ltr("civilizational_impact")
    L_INT = col_ltr("interdisciplinarity_index")
    L_TIT = col_ltr("titan_index")

    # Sheet 1: Executive_Dashboard (live formulas)
    ws_d = wb.create_sheet(title="Executive_Dashboard")
    ws_d.merge_cells("A1:I1")
    ws_d["A1"] = f"V2.0 MEGA-ATLAS OF HUMANITY'S {s['total_problems']:,} UNSOLVED, OPEN & HARD PROBLEMS (NOVEMBER 20, 2026 EDITION)"
    ws_d["A1"].font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    ws_d["A1"].fill = PatternFill("solid", fgColor="0F172A")
    ws_d["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_d.row_dimensions[1].height = 36

    ws_d.merge_cells("A2:I2")
    ws_d["A2"] = "8 Macro-Pillars × 28 Superdomains × Live Nov 20 2026 AI Proof-Claim Verification Audit × Global Registries × NetworkX Connectome"
    ws_d["A2"].font = Font(name="Calibri", size=10, italic=True, color="334155")
    ws_d["A2"].fill = PatternFill("solid", fgColor="E2E8F0")
    ws_d["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_d.row_dimensions[2].height = 22

    kpis = [
        ("Total Cataloged Open / Hard Problems", f"=COUNTA(Master_Catalog!A2:A{n_rows})", "#,##0", "Strictly deduplicated across all 28 superdomains"),
        ("Macro-Pillars × Superdomains × Subdomains", f"{s['total_macro_pillars']} × {s['total_superdomains']} × {s['total_subdomains']}", "@", "Complete hierarchy of human inquiry"),
        ("Knowledge-Graph Coupling Edges", s["total_graph_edges"], "#,##0", f"{s['cross_superdomain_edge_pct']}% cross-superdomain | {s['cross_pillar_edge_pct']}% cross-pillar"),
        ("Connected Components", s["connected_components"], "0", f"All {s['largest_component_size']:,} problems form 1 unified knowledge web"),
        ("Fall/Nov 2026 AI Proof Claims (Unverified)", s["ai_claims_nov2026_count"], "0", "Includes Sept 8 Navier-Stokes & Nov 20 Lean RH/GRH claims under audit"),
        ("Mean Intrinsic Difficulty (1–10)", f"=AVERAGE(Master_Catalog!{L_DIFF}2:{L_DIFF}{n_rows})", "0.00", "Highest in Pure Math & Fundamental Physics"),
        ("Mean Tractability by 2050 (1–10)", f"=AVERAGE(Master_Catalog!{L_TRAC}2:{L_TRAC}{n_rows})", "0.00", "Strong inverse coupling with Difficulty"),
        ("Mean Civilizational Impact (1–10)", f"=AVERAGE(Master_Catalog!{L_IMP}2:{L_IMP}{n_rows})", "0.00", "Strongly coupled with Interdisciplinarity"),
        ("Mean Interdisciplinarity (1–10)", f"=AVERAGE(Master_Catalog!{L_INT}2:{L_INT}{n_rows})", "0.00", "Cross-field linkage index"),
        ("Mean Composite Titan Index", f"=AVERAGE(Master_Catalog!{L_TIT}2:{L_TIT}{n_rows})", "0.00", "Hardness + Impact + Interdisc + log(Degree)"),
        ("Oldest Unsolved Problem Year", f"=MIN(Master_Catalog!{L_YR}2:{L_YR}{n_rows})", "0", "Negative = BCE (back to 500 BCE)"),
        ("Median Problem Age in 2026 (Years)", f"=MEDIAN(Master_Catalog!{L_AGE}2:{L_AGE}{n_rows})", "0", f"Median formulation year: {s['median_year']}"),
    ]
    ws_d["A4"], ws_d["B4"], ws_d["C4"] = "EXECUTIVE METRIC (LIVE EXCEL FORMULA)", "VALUE", "INTERPRETATION & NOV 2026 CONTEXT"
    for col_l in ["A", "B", "C"]:
        ws_d[f"{col_l}4"].font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        ws_d[f"{col_l}4"].fill = PatternFill("solid", fgColor="1D4ED8")
        ws_d[f"{col_l}4"].alignment = Alignment(horizontal="center", vertical="center")
    thin = Border(left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"),
                  top=Side(style="thin", color="CBD5E1"), bottom=Side(style="thin", color="CBD5E1"))
    for idx, (lbl, val, fmt, note) in enumerate(kpis, 5):
        ws_d.cell(idx, 1, lbl).font = Font(name="Calibri", size=9.8, bold=True)
        vc = ws_d.cell(idx, 2, val)
        vc.font = Font(name="Calibri", size=10.5, bold=True, color="1D4ED8")
        vc.number_format = fmt
        vc.alignment = Alignment(horizontal="right", vertical="center")
        ws_d.cell(idx, 3, note).font = Font(name="Calibri", size=9.3, color="475569")
        for ci in range(1, 4):
            ws_d.cell(idx, ci).border = thin

    # Live Pillar Table (Rows 19–28)
    hdrs = ["MACRO-PILLAR (LIVE FORMULAS)", "Count", "Mean Diff", "Mean Tract", "Mean Impact", "Mean Titan"]
    for ci, h in enumerate(hdrs, 1):
        c = ws_d.cell(19, ci, h)
        c.font = Font(name="Calibri", size=9.8, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="0F766E")
        c.alignment = Alignment(horizontal="center", vertical="center")
    for ro, pil in enumerate(MACRO_PILLARS, 20):
        ws_d.cell(ro, 1, pil).font = Font(name="Calibri", size=9.6, bold=True)
        ws_d.cell(ro, 2, f'=COUNTIF(Master_Catalog!${L_PIL}$2:${L_PIL}${n_rows}, A{ro})').number_format = "#,##0"
        ws_d.cell(ro, 3, f'=AVERAGEIF(Master_Catalog!${L_PIL}$2:${L_PIL}${n_rows}, A{ro}, Master_Catalog!${L_DIFF}$2:${L_DIFF}${n_rows})').number_format = "0.00"
        ws_d.cell(ro, 4, f'=AVERAGEIF(Master_Catalog!${L_PIL}$2:${L_PIL}${n_rows}, A{ro}, Master_Catalog!${L_TRAC}$2:${L_TRAC}${n_rows})').number_format = "0.00"
        ws_d.cell(ro, 5, f'=AVERAGEIF(Master_Catalog!${L_PIL}$2:${L_PIL}${n_rows}, A{ro}, Master_Catalog!${L_IMP}$2:${L_IMP}${n_rows})').number_format = "0.00"
        ws_d.cell(ro, 6, f'=AVERAGEIF(Master_Catalog!${L_PIL}$2:${L_PIL}${n_rows}, A{ro}, Master_Catalog!${L_TIT}$2:${L_TIT}${n_rows})').number_format = "0.00"
        for ci in range(1, 7):
            ws_d.cell(ro, ci).border = thin
    ws_d.cell(28, 1, "ALL 8 MACRO-PILLARS TOTAL / MEAN").font = Font(name="Calibri", size=9.8, bold=True)
    ws_d.cell(28, 2, "=SUM(B20:B27)").number_format = "#,##0"
    ws_d.cell(28, 3, f"=AVERAGE(Master_Catalog!{L_DIFF}2:{L_DIFF}{n_rows})").number_format = "0.00"
    ws_d.cell(28, 4, f"=AVERAGE(Master_Catalog!{L_TRAC}2:{L_TRAC}{n_rows})").number_format = "0.00"
    ws_d.cell(28, 5, f"=AVERAGE(Master_Catalog!{L_IMP}2:{L_IMP}{n_rows})").number_format = "0.00"
    ws_d.cell(28, 6, f"=AVERAGE(Master_Catalog!{L_TIT}2:{L_TIT}{n_rows})").number_format = "0.00"
    for ci in range(1, 7):
        ws_d.cell(28, ci).fill = PatternFill("solid", fgColor="E2E8F0")
        ws_d.cell(28, ci).border = thin

    bar = BarChart()
    bar.type = "col"
    bar.style = 10
    bar.title = "8 Macro-Pillars Comparative Profile (Difficulty vs. Tractability vs. Impact)"
    bar.y_axis.title = "Mean Score (1–10)"
    bar.add_data(Reference(ws_d, min_col=3, min_row=19, max_col=5, max_row=27), titles_from_data=True)
    bar.set_categories(Reference(ws_d, min_col=1, min_row=20, max_row=27))
    bar.width = 19
    bar.height = 11.5
    ws_d.add_chart(bar, "E4")
    ws_d.column_dimensions["A"].width = 40
    ws_d.column_dimensions["B"].width = 15
    ws_d.column_dimensions["C"].width = 50
    ws_d.column_dimensions["D"].width = 14
    ws_d.column_dimensions["E"].width = 14
    ws_d.column_dimensions["F"].width = 14

    # Sheet 2: Master_Catalog (ALL 1,600+ rows!)
    ws_m = write_sheet(wb, "Master_Catalog", df, header_hex="0F172A",
                       wrap_names=["name", "core_question", "formal_expression", "ai_verification_nov2026", "competing_approaches", "closest_progress_2026", "affected_industries", "contrast_axis"],
                       freeze="C2")
    for cl, lc, mc, hc in [(L_DIFF, "DCFCE7", "FEF08A", "FCA5A5"), (L_TRAC, "FCA5A5", "FEF08A", "86EFAC"),
                           (L_IMP, "E0F2FE", "93C5FD", "2563EB"), (L_TIT, "F1F5F9", "FDE047", "F97316")]:
        ws_m.conditional_formatting.add(f"{cl}2:{cl}{n_rows}", ColorScaleRule(start_type="min", start_color=lc, mid_type="percentile", mid_value=50, mid_color=mc, end_type="max", end_color=hc))

    # Sheets 3–13
    write_sheet(wb, "Nov2026_AI_Claims_Audit", data["df_ai_audit"], header_hex="B91C1C",
                wrap_names=["Problem", "Claimant_System", "Artifact_Type", "Machine_Check_Status", "Human_Fidelity_Audit", "Official_Status_Nov2026"])
    write_sheet(wb, "Global_Registries_2026", data["df_registries"], header_hex="1D4ED8",
                wrap_names=["Registry", "Scope", "Open_Count_Nov2026", "Verification_Standard", "Nov2026_Highlight"])
    ws_sd = write_sheet(wb, "Superdomain_Scorecard", data["df_superdomains"], header_hex="1E3A8A", wrap_names=["Superdomain", "Flagship_Titan_Name"])
    bar_sd = BarChart()
    bar_sd.type = "bar"
    bar_sd.style = 11
    bar_sd.title = "Open Problems Count Across All 28 Superdomains"
    bar_sd.add_data(Reference(ws_sd, min_col=3, min_row=1, max_row=29), titles_from_data=True)
    bar_sd.set_categories(Reference(ws_sd, min_col=1, min_row=2, max_row=29))
    bar_sd.legend = None
    bar_sd.width = 20
    bar_sd.height = 16
    ws_sd.add_chart(bar_sd, "A32")

    write_sheet(wb, "Macro_Pillar_Comparison", data["df_pillars"], header_hex="4C1D95")
    write_sheet(wb, "Type_x_Epistemic", data["ct_type_epistemic"], include_index=True, header_hex="065F46")
    write_sheet(wb, "Bottleneck_x_Scale", data["ct_bottleneck_scale"], include_index=True, header_hex="9A3412")
    ws_cp = write_sheet(wb, "Cross_Domain_Coupling", data["df_coupling"], include_index=True, header_hex="0E7490")
    ws_cp.conditional_formatting.add("B2:AC29", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", mid_type="num", mid_value=15, mid_color="BAE6FD", end_type="max", end_color="0284C7"))
    write_sheet(wb, "Keystone_Rankings", data["df_keystones"], header_hex="7E22CE", wrap_names=["name"])
    write_sheet(wb, "Pairwise_Contrasts", data["df_contrasts"], header_hex="9D174D", wrap_names=["title", "core_similarity", "core_contrast", "impact_asymmetry", "likely_winner_first"])
    write_sheet(wb, "Resolved_Benchmarks", data["df_benchmarks"], header_hex="047857", wrap_names=["name", "solver", "mechanism"])
    ws_ind = write_sheet(wb, "Industry_Exposure", data["df_industry"], include_index=True, header_hex="0369A1")
    ws_ind.conditional_formatting.add("B2:Q29", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", mid_type="num", mid_value=12, mid_color="A7F3D0", end_type="max", end_color="059669"))

    p_xlsx = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.xlsx")
    wb.save(p_xlsx)
    print(f"  Saved 13-sheet XLSX: {p_xlsx}")

    # Legacy BIFF .xls (Excel 97–2003, supports up to 65,536 rows cleanly!)
    book = xlwt.Workbook(encoding="utf-8")
    hs = xlwt.easyxf("font: bold on, color white; pattern: pattern solid, fore_colour dark_blue; align: wrap on, vert centre")
    cs = xlwt.easyxf("align: wrap on, vert top")
    ns = xlwt.easyxf("align: horiz right")

    def add_xls(sname, df_i, idx=False):
        sh = book.add_sheet(sname[:31])
        d = df_i.reset_index() if idx else df_i.copy()
        for ci, col in enumerate(d.columns):
            sh.write(0, ci, str(col), hs)
            sh.col(ci).width = min(10500, max(3000, len(str(col)) * 360))
        for ri, row in enumerate(d.itertuples(index=False), 1):
            for ci, val in enumerate(row):
                if pd.isna(val):
                    val = ""
                if isinstance(val, (int, float)):
                    sh.write(ri, ci, float(val) if isinstance(val, float) else int(val), ns)
                else:
                    sh.write(ri, ci, str(val)[:32000], cs)

    add_xls("Master_Catalog", df)
    add_xls("Nov2026_AI_Audit", data["df_ai_audit"])
    add_xls("Global_Registries", data["df_registries"])
    add_xls("Superdomain_Scorecard", data["df_superdomains"])
    add_xls("Macro_Pillar_Comp", data["df_pillars"])
    add_xls("Keystone_Top100", data["df_keystones"].head(100))
    add_xls("Pairwise_Contrasts", data["df_contrasts"])
    add_xls("Resolved_Benchmarks", data["df_benchmarks"])
    p_xls = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2_Legacy.xls")
    book.save(p_xls)
    print(f"  Saved 8-sheet Legacy BIFF XLS: {p_xls}")


# ==================== 3. MARKDOWN & PLAIN TEXT ====================
def export_md_and_txt(data):
    df = data["df"]
    s = data["summary_stats"]
    id_map = data["id_map"]

    # --- MARKDOWN ---
    md = []
    md.append(f"# V2.0 Mega-Atlas: Exhaustive Deep-Dive Comparison & Contrast of Humanity's {s['total_problems']:,} Unsolved, Open & Hard Problems (November 20, 2026 Edition)\n")
    md.append(f"> **True Comprehensive Scale:** **{s['total_problems']:,}** rigorously validated, deduplicated, authentic unsolved / open / hard problems spanning **8 Macro-Pillars**, **28 Superdomains**, and **{s['total_subdomains']:,} fine-grained subdomains**, wired into a single connected **{s['total_graph_edges']:,}-edge** cross-disciplinary knowledge graph (**{s['cross_superdomain_edge_pct']}%** cross-superdomain, **{s['cross_pillar_edge_pct']}%** cross-pillar) — complete with a live **November 20, 2026 AI Proof-Claim & Formal Verification Audit**, **13 Global Registry Benchmarks**, **15 Pairwise Deep Contrasts**, **20 Resolved Benchmarks (1995–2026)**, and **12 Publication-Grade Figures**.\n")

    md.append("## 1. November 20, 2026 Special Report: Why 'Open vs. Solved' Is Uniquely Volatile Right Now\n")
    md.append("No fixed finite count of open human problems exists—active mathematical registries alone track well over 1,100–2,000+ open questions (`ProofAtlas.ai`: 1,100+ eligible / 243 open in Top-500; `erdosproblems.com`: ~1,221 tracked / ~630+ open; `Kourovka Notebook`: >1,000 group theory problems; `Kirby List`: 360+ low-dimensional topology problems). In Fall–November 2026, rapid frontier AI proof announcements triggered an unprecedented verification bottleneck:\n")
    md.append(df_to_md(data["df_ai_audit"]) + "\n")
    md.append("### Global Open-Problem Registries & Scale Comparison (November 2026)\n")
    md.append(df_to_md(data["df_registries"]) + "\n")
    md.append("![Nov 2026 Status & Registries](charts/11_nov2026_status_and_registries.png)\n")

    md.append("## 2. Conceptual Models & Mermaid Taxonomies\n")
    md.append("```mermaid\nflowchart TD")
    md.append(f'    ROOT["V2.0 MEGA-ATLAS OF ALL UNSOLVED PROBLEMS<br/>{s["total_problems"]:,} Problems | 8 Macro-Pillars | 28 Superdomains | {s["total_graph_edges"]:,} Edges"]')
    for pi, pil in enumerate(MACRO_PILLARS, 1):
        sub_p = data["df_superdomains"][data["df_superdomains"]["Macro_Pillar"] == pil]
        md.append(f'    P{pi}["{pil} (n={int(sub_p["Problem_Count"].sum()):,})"]')
        md.append(f"    ROOT --> P{pi}")
        for si, row in enumerate(sub_p.itertuples(), 1):
            md.append(f'    P{pi}S{si}["{row.Superdomain} ({row.Problem_Count})"]')
            md.append(f"    P{pi} --> P{pi}S{si}")
    md.append("```\n")

    md.append("## 3. 8-Macro-Pillar & 28-Superdomain Scorecards\n")
    md.append(df_to_md(data["df_pillars"]) + "\n")
    md.append("![28 Superdomains](charts/01_superdomain_landscape.png)\n")
    md.append(df_to_md(data["df_superdomains"]) + "\n")

    md.append("## 4. Cross-Tabulation & Structural Contrast Matrices\n")
    md.append("### 4.1 Strategic 4-Quadrant × 8 Macro-Pillars\n" + df_to_md(data["ct_quadrant_pillar"], include_index=True) + "\n")
    md.append("![4-Quadrant](charts/02_strategic_impact_tractability_quadrant.png)\n")
    md.append("### 4.2 Problem Type × Epistemic Class\n" + df_to_md(data["ct_type_epistemic"], include_index=True) + "\n")
    md.append("### 4.3 Primary Bottleneck × 8 Macro-Pillars\n" + df_to_md(data["ct_bottleneck_pillar"], include_index=True) + "\n")
    md.append("![Bottlenecks & Epistemics](charts/04_bottleneck_and_epistemic_matrices.png)\n")
    md.append("### 4.4 Primary Bottleneck × Scale Regime\n" + df_to_md(data["ct_bottleneck_scale"], include_index=True) + "\n")
    md.append("### 4.5 Nov 2026 Status × 8 Macro-Pillars\n" + df_to_md(data["ct_status_pillar"], include_index=True) + "\n")
    md.append("### 4.6 Historical Era × 8 Macro-Pillars\n" + df_to_md(data["ct_era_pillar"], include_index=True) + "\n")
    md.append("### 4.7 Global Industry Exposure Matrix (28 Superdomains × 16 Sectors)\n" + df_to_md(data["df_industry"], include_index=True) + "\n")
    md.append("![Industry Exposure](charts/09_industry_exposure_heatmap.png)\n")

    md.append("## 5. Top 40 Keystone Domino Hubs (NetworkX Connectome)\n")
    md.append(df_to_md(data["df_keystones"].head(40)) + "\n")
    md.append("![8-Pillar Connectome](charts/07_keystone_knowledge_graph.png)\n")
    md.append("![Top 25 Keystone Dominoes](charts/12_top25_keystone_dominoes.png)\n")

    md.append("## 6. 15 Iconic Pairwise Deep-Dive Contrasts\n")
    for _, r in data["df_contrasts"].iterrows():
        md.append(f"### {r['contrast_id']}: {r['title']} (`{r['problem_a_id']}` vs. `{r['problem_b_id']}`)")
        md.append(f"- **Similarity:** {r['core_similarity']}")
        md.append(f"- **Structural Contrast:** {r['core_contrast']}")
        md.append(f"- **Impact Asymmetry:** {r['impact_asymmetry']}")
        md.append(f"- **Likely First Breakthrough:** {r['likely_winner_first']}\n")

    md.append("## 7. 20 Recently Resolved Historical Benchmarks (1995–2026)\n")
    md.append(df_to_md(data["df_benchmarks"]) + "\n")

    md.append("## 8. Complete 12-Figure Visual Analytics Gallery\n")
    for fname, cap in CHART_ITEMS:
        md.append(f"### {cap}\n![{cap}](charts/{fname})\n")

    md.append(f"## 9. Complete Exhaustive Master Catalog of All {s['total_problems']:,} Unsolved, Open & Hard Problems\n")
    for pi, pil in enumerate(MACRO_PILLARS, 1):
        p_df = df[df["macro_pillar"] == pil]
        md.append(f"### Macro-Pillar {pi}: {pil} ({len(p_df):,} Problems)\n")
        for sd in [k for k, v in SUPERDOMAIN_TO_PILLAR.items() if v == pil]:
            sub = p_df[p_df["superdomain"] == sd]
            md.append(f"#### {sd} ({len(sub)} Problems)\n")
            mini = sub[["id", "name", "year_formulated", "problem_type", "status_2026", "difficulty_score", "tractability_2050", "civilizational_impact", "titan_index", "graph_degree", "primary_bottleneck"]].copy()
            mini.columns = ["ID", "Problem Name", "Year", "Type", "Status (Nov 2026)", "Diff", "Tract", "Imp", "Titan", "Deg", "Bottleneck"]
            md.append(df_to_md(mini) + "\n")
            for _, r in sub.iterrows():
                yr_s = f"{abs(r['year_formulated'])} BCE" if r["year_formulated"] < 0 else str(r["year_formulated"])
                md.append(f"- **`{r['id']}` — {r['name']}** ({r['subdomain']} | {yr_s}, {r['age_years_2026']}y | *{r['originator']}* | {r['registry_source']} | **{r['status_2026']}**)")
                md.append(f"  - *Core Question:* {r['core_question']} | *Formal:* `{r['formal_expression']}`")
                md.append(f"  - *Approaches:* {r['competing_approaches']} | *2026 State:* {r['closest_progress_2026']} | *Nov 2026 AI Audit:* {r['ai_verification_nov2026']}")
                md.append(f"  - *Industries:* {r['affected_industries']} | *Links:* `{r['related_problem_ids']}` | *Axis:* *{r['contrast_axis']}*")
            md.append("")

    p_md = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"  Saved Markdown Mega-Atlas: {p_md} ({len(md):,} lines)")

    # --- PLAIN TEXT ---
    txt = []
    bar = "=" * 116
    txt.extend([bar, f"  V2.0 MEGA-ATLAS OF HUMANITY'S {s['total_problems']:,} UNSOLVED, OPEN & HARD PROBLEMS (NOVEMBER 20, 2026 EDITION)",
                f"  8 Macro-Pillars | 28 Superdomains | {s['total_subdomains']:,} Subdomains | {s['total_graph_edges']:,} Coupling Edges | 1 Connected Component", bar, ""])
    txt.append("[1] EXECUTIVE SUMMARY METRICS\n" + "-" * 116)
    for k, v in s.items():
        if k != "module_counts":
            txt.append(f"  {k:<36}: {v}")
    txt.append("\n[2] NOVEMBER 20, 2026 AI PROOF-CLAIM VERIFICATION AUDIT\n" + "-" * 116)
    for _, r in data["df_ai_audit"].iterrows():
        txt.append(f"  [{r['Claim_ID']}] {r['Problem']} ({r['Date']})")
        txt.append(f"    Claimant  : {r['Claimant_System']}")
        txt.append(f"    Machine   : {r['Machine_Check_Status']}")
        txt.append(f"    Human/Peer: {r['Human_Fidelity_Audit']}")
        txt.append(f"    Verdict   : {r['Official_Status_Nov2026']}\n")
    txt.append("[3] GLOBAL OPEN-PROBLEM REGISTRIES COMPARISON\n" + "-" * 116)
    txt.append(df_to_ascii(data["df_registries"][["Registry", "Total_Tracked", "Open_Count_Nov2026", "Nov2026_Highlight"]], max_col_w=38))
    txt.append("\n[4] 8 MACRO-PILLARS COMPARATIVE SCORECARD\n" + "-" * 116)
    txt.append(df_to_ascii(data["df_pillars"][["Macro_Pillar", "Problem_Count", "Share_Pct", "Mean_Difficulty", "Mean_Tractability_2050", "Mean_Impact", "Mean_Titan_Index", "Median_Year", "Dominant_Bottleneck"]], max_col_w=32))
    txt.append("\n[5] 28 SUPERDOMAINS ASCII DISTRIBUTION HISTOGRAM\n" + "-" * 116)
    max_c = int(data["df_superdomains"]["Problem_Count"].max())
    for _, r in data["df_superdomains"].iterrows():
        hb = "#" * int(round(r["Problem_Count"] / max_c * 28)) + "." * (28 - int(round(r["Problem_Count"] / max_c * 28)))
        txt.append(f"  {r['Superdomain'][:48]:<48} | {hb} {r['Problem_Count']:>3} ({r['Share_Pct']:>4.1f}%) | D:{r['Mean_Difficulty']:.1f} T:{r['Mean_Tractability_2050']:.1f} I:{r['Mean_Impact']:.1f}")
    txt.append("\n[6] PROBLEM TYPE x EPISTEMIC CLASS\n" + "-" * 116)
    txt.append(df_to_ascii(data["ct_type_epistemic"], include_index=True, max_col_w=34))
    txt.append("\n[7] TOP 40 KEYSTONE DOMINO HUBS\n" + "-" * 116)
    txt.append(df_to_ascii(data["df_keystones"].head(40)[["Rank", "id", "name", "macro_pillar", "difficulty_score", "tractability_2050", "civilizational_impact", "titan_index", "graph_degree", "cross_pillar_links"]], max_col_w=36))
    txt.append("\n[8] 15 ICONIC PAIRWISE CONTRASTS\n" + "-" * 116)
    for _, r in data["df_contrasts"].iterrows():
        txt.append(f"  >> {r['contrast_id']} | {r['title']} ({r['problem_a_id']} vs {r['problem_b_id']})")
        txt.append(f"     Contrast: {r['core_contrast']}")
        txt.append(f"     Asymmetr: {r['impact_asymmetry']}\n")
    txt.append(f"[9] COMPLETE EXHAUSTIVE CATALOG OF ALL {s['total_problems']:,} PROBLEMS\n" + bar)
    for pi, pil in enumerate(MACRO_PILLARS, 1):
        txt.append(f"\n==================== PILLAR {pi}: {pil.upper()} ====================")
        for sd in [k for k, v in SUPERDOMAIN_TO_PILLAR.items() if v == pil]:
            sub = df[df["superdomain"] == sd]
            txt.append(f"\n--- SUPERDOMAIN: {sd} ({len(sub)} Problems) ---")
            for _, r in sub.iterrows():
                yr_s = f"{abs(r['year_formulated'])} BCE" if r["year_formulated"] < 0 else str(r["year_formulated"])
                txt.append(f"[{r['id']}] {r['name']}")
                txt.append(f"  Subdomain : {r['subdomain']} | {r['problem_type']} | {r['epistemic_class']} | {yr_s} ({r['age_years_2026']}y) | {r['originator']} | Registry: {r['registry_source']}")
                txt.append(f"  Status    : {r['status_2026']} | AI Nov2026: {r['ai_verification_nov2026']}")
                txt.append(f"  Scores    : Diff={r['difficulty_score']} Tract={r['tractability_2050']} Impact={r['civilizational_impact']} Interdisc={r['interdisciplinarity_index']} Titan={r['titan_index']} Deg={r['graph_degree']} (XP={r['cross_pillar_links']})")
                txt.append(f"  Question  : {r['core_question']}")
                txt.append(f"  Formula   : {r['formal_expression']}")
                txt.append(f"  Bottleneck: {r['primary_bottleneck']} | Scale: {r['scale_regime']} | Verify: {r['verification_type']}")
                txt.append(f"  Approaches: {r['competing_approaches']}")
                txt.append(f"  2026 State: {r['closest_progress_2026']}")
                txt.append(f"  Links/Ind : {r['related_problem_ids']} | Industries: {r['affected_industries']} | Axis: {r['contrast_axis']}")
                txt.append("-" * 96)

    p_txt = os.path.join(OUT_DIR, "MegaAtlas_Unsolved_Problems_V2.txt")
    with open(p_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt))
    print(f"  Saved Plain Text Mega-Reference: {p_txt} ({len(txt):,} lines)")


# ==================== 4. INTERACTIVE HTML (PAGINATED FOR 1,700+ ROWS!) ====================
def export_interactive_html(data):
    df = data["df"]
    s = data["summary_stats"]
    probs_json = json.dumps(df.to_dict(orient="records"), ensure_ascii=False).replace("</", "<\\/")
    contrasts_json = json.dumps(data["df_contrasts"].to_dict(orient="records"), ensure_ascii=False).replace("</", "<\\/")
    bench_json = json.dumps(data["df_benchmarks"].to_dict(orient="records"), ensure_ascii=False).replace("</", "<\\/")
    audit_json = json.dumps(data["df_ai_audit"].to_dict(orient="records"), ensure_ascii=False).replace("</", "<\\/")
    regs_json = json.dumps(data["df_registries"].to_dict(orient="records"), ensure_ascii=False).replace("</", "<\\/")
    pal_json = json.dumps(PILLAR_HEX)

    gallery_html = "\n".join(
        f'<div class="chart-card" onclick="openLightbox(this)"><div class="chart-cap">{html.escape(cap)}</div>'
        f'<img src="{b64_img(fname)}" alt="{html.escape(cap)}" loading="lazy" /></div>'
        for fname, cap in CHART_ITEMS
    )

    matrices_html = f"""
    <div class="matrix-section"><h3>1. 8 Macro-Pillars Comparative Scorecard</h3>{df_to_html_table(data["df_pillars"])}</div>
    <div class="matrix-section"><h3>2. Complete 28-Superdomain Statistical Scorecard</h3>{df_to_html_table(data["df_superdomains"])}</div>
    <div class="matrix-section"><h3>3. Top 50 Keystone Domino Hub Problems (NetworkX PageRank &amp; Cross-Pillar Bridges)</h3>{df_to_html_table(data["df_keystones"].head(50))}</div>
    <div class="matrix-section"><h3>4. Strategic 4-Quadrant × 8 Macro-Pillars</h3>{df_to_html_table(data["ct_quadrant_pillar"], include_index=True)}</div>
    <div class="matrix-section"><h3>5. Problem Type × Epistemic Class</h3>{df_to_html_table(data["ct_type_epistemic"], include_index=True)}</div>
    <div class="matrix-section"><h3>6. Primary Bottleneck × 8 Macro-Pillars</h3>{df_to_html_table(data["ct_bottleneck_pillar"], include_index=True)}</div>
    <div class="matrix-section"><h3>7. Primary Bottleneck × Physical/Abstract Scale Regime</h3>{df_to_html_table(data["ct_bottleneck_scale"], include_index=True)}</div>
    <div class="matrix-section"><h3>8. Nov 2026 Research Status × 8 Macro-Pillars</h3>{df_to_html_table(data["ct_status_pillar"], include_index=True)}</div>
    <div class="matrix-section"><h3>9. Historical Era × 8 Macro-Pillars</h3>{df_to_html_table(data["ct_era_pillar"], include_index=True)}</div>
    <div class="matrix-section"><h3>10. Global Industry Exposure Matrix (28 Superdomains × 16 Sectors)</h3>{df_to_html_table(data["df_industry"], include_index=True)}</div>
    """

    doc = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>V2.0 Mega-Atlas: {s['total_problems']:,} Unsolved, Open &amp; Hard Problems Across All Human Knowledge (Nov 2026)</title>
<style>
  :root {{
    --bg: #0B1120; --surface: #111827; --surface2: #1E293B; --border: #334155;
    --text: #F1F5F9; --muted: #94A3B8; --accent: #38BDF8; --good: #34D399; --warn: #FBBF24; --bad: #F87171;
  }}
  [data-theme="light"] {{
    --bg: #F8FAFC; --surface: #FFFFFF; --surface2: #F1F5F9; --border: #CBD5E1;
    --text: #0F172A; --muted: #475569; --accent: #0284C7; --good: #059669; --warn: #D97706; --bad: #DC2626;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif; background: var(--bg); color: var(--text); line-height: 1.48; }}
  header {{ background: linear-gradient(135deg, #0B1120 0%, #1E1B4B 48%, #0C4A6E 100%); color: #FFF; padding: 24px 30px; border-bottom: 1px solid #334155; }}
  .hdr-top {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; flex-wrap: wrap; }}
  h1 {{ font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; }}
  .sub {{ color: #CBD5E1; font-size: 0.9rem; margin-top: 5px; max-width: 1020px; }}
  .theme-btn {{ background: rgba(255,255,255,0.14); color: #FFF; border: 1px solid rgba(255,255,255,0.28); padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.84rem; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(145px, 1fr)); gap: 10px; margin-top: 16px; }}
  .kpi {{ background: rgba(15,23,42,0.58); border: 1px solid rgba(148,163,184,0.25); border-radius: 10px; padding: 11px 13px; }}
  .kpi .v {{ font-size: 1.35rem; font-weight: 800; color: #38BDF8; }}
  .kpi .l {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: #CBD5E1; margin-top: 2px; }}

  nav.tabs {{ display: flex; gap: 6px; padding: 11px 28px; background: var(--surface); border-bottom: 1px solid var(--border); flex-wrap: wrap; position: sticky; top: 0; z-index: 40; }}
  .tab-btn {{ background: transparent; color: var(--muted); border: 1px solid transparent; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.86rem; }}
  .tab-btn:hover {{ background: var(--surface2); color: var(--text); }}
  .tab-btn.active {{ background: var(--accent); color: #0B1120; border-color: var(--accent); }}

  main {{ padding: 20px 28px 60px; max-width: 1740px; margin: 0 auto; }}
  .panel {{ display: none; }}
  .panel.active {{ display: block; }}

  .filters {{ display: grid; grid-template-columns: 2fr repeat(6, 1fr); gap: 8px; background: var(--surface); padding: 12px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 12px; }}
  @media (max-width: 1250px) {{ .filters {{ grid-template-columns: repeat(2, 1fr); }} }}
  .filters input, .filters select {{ width: 100%; padding: 8px 9px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); font-size: 0.83rem; }}
  .bar-meta {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 0.86rem; color: var(--muted); flex-wrap: wrap; gap: 8px; }}
  .btn-sm {{ background: var(--surface2); color: var(--text); border: 1px solid var(--border); padding: 6px 11px; border-radius: 7px; cursor: pointer; font-size: 0.81rem; font-weight: 600; }}
  .btn-sm:hover {{ border-color: var(--accent); color: var(--accent); }}
  .pager {{ display: flex; gap: 6px; align-items: center; }}

  .table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 10px; background: var(--surface); }}
  table.data-table {{ width: 100%; border-collapse: collapse; font-size: 0.81rem; }}
  table.data-table th {{ background: var(--surface2); color: var(--text); text-align: left; padding: 9px 9px; font-weight: 700; border-bottom: 1px solid var(--border); position: sticky; top: 0; white-space: nowrap; cursor: pointer; }}
  table.data-table th:hover {{ color: var(--accent); }}
  table.data-table td {{ padding: 7px 9px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  table.data-table tr:hover td {{ background: rgba(56,189,248,0.08); }}
  table.data-table tr.clickable {{ cursor: pointer; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }}
  .pill {{ display: inline-block; padding: 2px 7px; border-radius: 999px; font-size: 0.7rem; font-weight: 700; color: #FFF; white-space: nowrap; }}
  .badge {{ display: inline-block; padding: 2px 6px; border-radius: 5px; font-size: 0.71rem; font-weight: 600; background: var(--surface2); border: 1px solid var(--border); color: var(--text); }}
  .badge-ai {{ background: rgba(239,68,68,0.18); border-color: #EF4444; color: #FCA5A5; }}
  [data-theme="light"] .badge-ai {{ color: #991B1B; background: #FEE2E2; }}
  .score-hi {{ color: var(--bad); font-weight: 800; }}
  .score-good {{ color: var(--good); font-weight: 800; }}
  .score-mid {{ color: var(--warn); font-weight: 700; }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.77rem; }}

  .comp-controls {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; background: var(--surface); padding: 14px; border-radius: 12px; border: 1px solid var(--border); }}
  .comp-controls select, .comp-controls input {{ width: 100%; padding: 8px 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); font-size: 0.87rem; }}
  .preset-bar {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }}
  .comp-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  @media (max-width: 900px) {{ .comp-controls, .comp-grid {{ grid-template-columns: 1fr; }} }}
  .comp-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }}
  .bar-row {{ display: flex; align-items: center; gap: 10px; margin: 6px 0; font-size: 0.83rem; }}
  .bar-lbl {{ width: 135px; color: var(--muted); font-weight: 600; }}
  .bar-track {{ flex: 1; height: 9px; background: var(--surface2); border-radius: 99px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 99px; }}
  .field-box {{ margin-top: 9px; padding-top: 9px; border-top: 1px solid var(--border); font-size: 0.84rem; }}
  .field-box strong {{ color: var(--accent); display: block; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 2px; }}

  .chart-grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; }}
  .chart-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px; cursor: zoom-in; }}
  .chart-cap {{ font-weight: 700; font-size: 0.98rem; margin-bottom: 9px; color: var(--accent); }}
  .chart-card img {{ width: 100%; height: auto; border-radius: 8px; display: block; background: #FFF; }}

  .matrix-section {{ margin-bottom: 26px; }}
  .matrix-section h3 {{ font-size: 1.05rem; margin-bottom: 9px; color: var(--accent); }}
  .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(430px, 1fr)); gap: 14px; }}
  .contrast-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 15px; }}
  .contrast-card h4 {{ color: var(--accent); font-size: 0.98rem; margin-bottom: 7px; }}
  .contrast-card p {{ font-size: 0.83rem; margin-bottom: 5px; }}
  .alert-box {{ background: rgba(239,68,68,0.12); border: 1px solid #EF4444; border-left: 5px solid #EF4444; border-radius: 10px; padding: 14px 16px; margin-bottom: 18px; font-size: 0.88rem; }}

  .modal-bg {{ display: none; position: fixed; inset: 0; background: rgba(2,6,23,0.80); z-index: 100; align-items: center; justify-content: center; padding: 18px; }}
  .modal-bg.open {{ display: flex; }}
  .modal-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px; max-width: 880px; width: 100%; max-height: 89vh; overflow-y: auto; padding: 22px; position: relative; }}
  .modal-close {{ position: absolute; top: 13px; right: 15px; background: var(--surface2); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 5px 11px; cursor: pointer; font-weight: 800; }}
  .chip {{ display: inline-block; padding: 3px 8px; margin: 2px; border-radius: 6px; background: var(--surface2); border: 1px solid var(--accent); color: var(--accent); font-size: 0.77rem; font-weight: 700; cursor: pointer; }}
  .chip:hover {{ background: var(--accent); color: #0B1120; }}
  #lightbox img {{ max-width: 96vw; max-height: 91vh; border-radius: 10px; background: #FFF; }}
</style>
</head>
<body>
<header>
  <div class="hdr-top">
    <div>
      <h1>V2.0 Mega-Atlas: Humanity's {s['total_problems']:,} Unsolved, Open &amp; Hard Problems (November 20, 2026)</h1>
      <div class="sub">8 Macro-Pillars · 28 Superdomains · {s['total_subdomains']:,} Subdomains · {s['total_graph_edges']:,} Verified Knowledge-Graph Couplings · Live November 2026 AI Proof-Claim Verification Audit (Navier–Stokes, Oct 2026 722-Manuscript Dump &amp; Nov 20 Lean RH/GRH Claims) · Global Registries Comparison.</div>
    </div>
    <button class="theme-btn" onclick="toggleTheme()">Toggle Light / Dark</button>
  </div>
  <div class="kpi-grid">
    <div class="kpi"><div class="v">{s['total_problems']:,}</div><div class="l">Open / Hard Problems</div></div>
    <div class="kpi"><div class="v">8 × 28</div><div class="l">Pillars × Superdomains</div></div>
    <div class="kpi"><div class="v">{s['total_graph_edges']:,}</div><div class="l">Coupling Graph Edges</div></div>
    <div class="kpi"><div class="v">{s['cross_pillar_edge_pct']}%</div><div class="l">Cross-Pillar Bridges</div></div>
    <div class="kpi"><div class="v">{s['ai_claims_nov2026_count']}</div><div class="l">Nov 2026 AI Claims</div></div>
    <div class="kpi"><div class="v">{s['mean_difficulty']} / {s['mean_tractability']}</div><div class="l">Mean Diff / Tract 2050</div></div>
    <div class="kpi"><div class="v">{s['mean_impact']} / 10</div><div class="l">Mean Civiliz. Impact</div></div>
    <div class="kpi"><div class="v">500 BCE–2026</div><div class="l">Span (Med Age {s['median_age_years']}y)</div></div>
  </div>
</header>

<nav class="tabs">
  <button class="tab-btn active" onclick="showTab('explorer', this)">1. Master Catalog ({s['total_problems']:,})</button>
  <button class="tab-btn" onclick="showTab('nov2026', this)">2. Nov 2026 AI Audit &amp; Global Registries</button>
  <button class="tab-btn" onclick="showTab('comparator', this)">3. Live Side-by-Side Comparator</button>
  <button class="tab-btn" onclick="showTab('charts', this)">4. Visual Analytics Gallery (12 Charts)</button>
  <button class="tab-btn" onclick="showTab('matrices', this)">5. All Comparison &amp; Contrast Matrices</button>
  <button class="tab-btn" onclick="showTab('contrasts', this)">6. 15 Iconic Contrasts &amp; 20 Resolved Benchmarks</button>
</nav>

<main>
  <!-- TAB 1: MASTER CATALOG -->
  <section id="tab-explorer" class="panel active">
    <div class="filters">
      <input id="fSearch" type="text" placeholder="Instant search across all {s['total_problems']:,} problems (ID, name, equation, originator, approaches, industries, registry)..." oninput="goPage(1)" />
      <select id="fPillar" onchange="goPage(1)"><option value="">All 8 Macro-Pillars</option></select>
      <select id="fSuper" onchange="goPage(1)"><option value="">All 28 Superdomains</option></select>
      <select id="fStatus" onchange="goPage(1)"><option value="">All Nov 2026 Statuses</option></select>
      <select id="fType" onchange="goPage(1)"><option value="">All Problem Types</option></select>
      <select id="fBottleneck" onchange="goPage(1)"><option value="">All Bottlenecks</option></select>
      <select id="fQuadrant" onchange="goPage(1)"><option value="">All 4 Quadrants</option></select>
    </div>
    <div class="bar-meta">
      <div id="countSummary">Loading...</div>
      <div class="pager">
        <button class="btn-sm" onclick="filterAIClaims()">Filter: Nov 2026 AI Claims</button>
        <button class="btn-sm" onclick="resetFilters()">Reset Filters</button>
        <button class="btn-sm" onclick="goPage(curPage - 1)">← Prev</button>
        <span id="pageInfo" style="font-weight:700;">Page 1</span>
        <button class="btn-sm" onclick="goPage(curPage + 1)">Next →</button>
        <select id="pageSize" onchange="goPage(1)" style="padding:5px 7px;border-radius:6px;background:var(--surface2);color:var(--text);border:1px solid var(--border);font-size:0.8rem;">
          <option value="50">50 / page</option>
          <option value="100" selected>100 / page</option>
          <option value="250">250 / page</option>
          <option value="2000">All rows</option>
        </select>
      </div>
    </div>
    <div class="table-wrap" style="max-height:68vh;">
      <table class="data-table">
        <thead>
          <tr>
            <th onclick="sortBy('id')">ID</th>
            <th onclick="sortBy('name')">Problem Name &amp; Subdomain</th>
            <th onclick="sortBy('macro_pillar')">Macro-Pillar</th>
            <th onclick="sortBy('superdomain')">Superdomain</th>
            <th onclick="sortBy('year_formulated')">Year</th>
            <th onclick="sortBy('status_2026')">Nov 2026 Status</th>
            <th onclick="sortBy('difficulty_score')">Diff</th>
            <th onclick="sortBy('tractability_2050')">Tract</th>
            <th onclick="sortBy('civilizational_impact')">Imp</th>
            <th onclick="sortBy('titan_index')">Titan</th>
            <th onclick="sortBy('graph_degree')">Deg</th>
            <th onclick="sortBy('primary_bottleneck')">Primary Bottleneck</th>
            <th onclick="sortBy('registry_source')">Registry</th>
          </tr>
        </thead>
        <tbody id="masterTbody"></tbody>
      </table>
    </div>
  </section>

  <!-- TAB 2: NOV 2026 AI AUDIT & REGISTRIES -->
  <section id="tab-nov2026" class="panel">
    <div class="alert-box">
      <b>Why "Right Now" (November 20, 2026) Is Historically Unprecedented:</b> Active registries like <b>ProofAtlas.ai</b> (1,100+ eligible; 243 open in Top-500) and <b>Erdős Problems DB</b> (~1,221 tracked; ~630 open) coexist with dramatic Fall–November 2026 AI proof claims—including OpenAI's Sept 8 <b>3D Navier–Stokes</b> claim, OpenAI's Oct 6 bulk release (<b>722 manuscripts across 372 topics</b>), and today's Nov 20 <b>Levent Alpöge / Claude multi-million-line Lean Riemann Hypothesis &amp; GRH claim</b> alongside Stanford's <b>Alessandro Masullo</b> human draft. Machine kernel compilation checks logical deduction, NOT formal-statement fidelity or community consensus—so all six Clay Millennium Problems remain officially unretired pending independent verification.
    </div>
    <h2 style="margin-bottom:10px;">A. Live November 20, 2026 AI Proof-Claim Verification Audit</h2>
    <div class="table-wrap" style="margin-bottom:28px;">
      <table class="data-table"><thead><tr><th>Audit ID</th><th>Targeted Problem(s)</th><th>Date</th><th>Claimant / System</th><th>Artifact Type</th><th>Machine Check Status</th><th>Human Fidelity &amp; Peer Review</th><th>Official Nov 2026 Verdict</th></tr></thead><tbody id="auditTbody"></tbody></table>
    </div>
    <h2 style="margin-bottom:10px;">B. Global Open-Problem Registries &amp; Scale Comparison (13 Major Trackers)</h2>
    <div class="table-wrap">
      <table class="data-table"><thead><tr><th>Registry / Tracker</th><th>Scope</th><th>Total Tracked</th><th>Open Count (Nov 2026)</th><th>Verification Standard</th><th>November 2026 Context</th></tr></thead><tbody id="regsTbody"></tbody></table>
    </div>
  </section>

  <!-- TAB 3: LIVE COMPARATOR -->
  <section id="tab-comparator" class="panel">
    <h2 style="margin-bottom:6px;">Interactive Any-2-Problems Side-by-Side Comparison &amp; Contrast Engine</h2>
    <p style="color:var(--muted);font-size:0.86rem;margin-bottom:10px;">Compare ANY two of all {s['total_problems']:,} problems (filter each dropdown live or load one of the 15 iconic presets).</p>
    <div class="preset-bar" id="presetBar"></div>
    <div class="comp-controls">
      <div>
        <label style="font-size:0.76rem;color:var(--muted);font-weight:700;">PROBLEM A (SEARCH + SELECT)</label>
        <input id="qA" type="text" placeholder="Quick filter Problem A..." oninput="filterSelect('qA','selA')" style="margin-bottom:6px;" />
        <select id="selA" onchange="renderCompare()"></select>
      </div>
      <div>
        <label style="font-size:0.76rem;color:var(--muted);font-weight:700;">PROBLEM B (SEARCH + SELECT)</label>
        <input id="qB" type="text" placeholder="Quick filter Problem B..." oninput="filterSelect('qB','selB')" style="margin-bottom:6px;" />
        <select id="selB" onchange="renderCompare()"></select>
      </div>
    </div>
    <div id="compDeltaBanner" style="background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:11px 15px;margin-bottom:14px;font-size:0.85rem;"></div>
    <div class="comp-grid" id="compGrid"></div>
  </section>

  <!-- TAB 4: CHARTS GALLERY -->
  <section id="tab-charts" class="panel">
    <h2 style="margin-bottom:8px;">Visual Analytics Gallery — All 12 Publication-Grade Figures (Click to Zoom)</h2>
    <div class="chart-grid">{gallery_html}</div>
  </section>

  <!-- TAB 5: MATRICES -->
  <section id="tab-matrices" class="panel">
    <h2 style="margin-bottom:12px;">Complete Multi-Dimensional Comparison &amp; Industry Exposure Matrices</h2>
    {matrices_html}
  </section>

  <!-- TAB 6: CONTRASTS & BENCHMARKS -->
  <section id="tab-contrasts" class="panel">
    <h2 style="margin-bottom:12px;">15 Iconic Cross-Domain Pairwise Deep-Dive Contrasts</h2>
    <div class="card-grid" id="contrastsGrid" style="margin-bottom:32px;"></div>
    <h2 style="margin-bottom:12px;">20 Recently Resolved Historical Benchmarks (1995–2026) vs. Open Twins</h2>
    <div class="table-wrap"><table class="data-table"><thead><tr><th>ID</th><th>Resolved Problem</th><th>Domain</th><th>Posed</th><th>Solved</th><th>Yrs Open</th><th>Solver</th><th>Breakthrough Mechanism</th><th>Still-Open Twin</th></tr></thead><tbody id="benchTbody"></tbody></table></div>
  </section>
</main>

<div class="modal-bg" id="detailModal" onclick="if(event.target===this) closeModal()"><div class="modal-box" id="detailContent"></div></div>
<div class="modal-bg" id="lightbox" onclick="this.classList.remove('open')"><img id="lightboxImg" src="" alt="Zoom" /></div>

<script>
const PROBLEMS = {probs_json};
const CONTRASTS = {contrasts_json};
const BENCHMARKS = {bench_json};
const AI_AUDIT = {audit_json};
const REGISTRIES = {regs_json};
const PILLAR_COLORS = {pal_json};
const ID_MAP = Object.fromEntries(PROBLEMS.map(p => [p.id, p]));

let sortCol = 'titan_index';
let sortDir = -1;
let curPage = 1;
let filteredRows = PROBLEMS;

const esc = s => String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const fmtYear = y => y < 0 ? Math.abs(y) + ' BCE' : String(y);
function toggleTheme() {{ const r = document.documentElement; r.setAttribute('data-theme', r.getAttribute('data-theme')==='dark'?'light':'dark'); }}
function showTab(id, btn) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
}}
function openLightbox(card) {{ document.getElementById('lightboxImg').src = card.querySelector('img').src; document.getElementById('lightbox').classList.add('open'); }}
function closeModal() {{ document.getElementById('detailModal').classList.remove('open'); }}

function populateUI() {{
  const uniq = k => [...new Set(PROBLEMS.map(p => p[k]))].sort();
  const fill = (id, arr) => {{ const el = document.getElementById(id); arr.forEach(v => el.add(new Option(v, v))); }};
  fill('fPillar', uniq('macro_pillar'));
  fill('fSuper', uniq('superdomain'));
  fill('fStatus', uniq('status_2026'));
  fill('fType', uniq('problem_type'));
  fill('fBottleneck', uniq('primary_bottleneck'));
  fill('fQuadrant', uniq('strategic_quadrant'));

  filterSelect('qA', 'selA', 'NT-001');
  filterSelect('qB', 'selB', 'CS-001');

  const pbar = document.getElementById('presetBar');
  CONTRASTS.forEach(c => {{
    const b = document.createElement('button');
    b.className = 'btn-sm';
    b.textContent = c.title;
    b.onclick = () => {{
      document.getElementById('qA').value=''; document.getElementById('qB').value='';
      filterSelect('qA','selA',c.problem_a_id); filterSelect('qB','selB',c.problem_b_id); renderCompare();
    }};
    pbar.appendChild(b);
  }});

  document.getElementById('auditTbody').innerHTML = AI_AUDIT.map(a => `
    <tr><td class="mono"><b>${{esc(a.Claim_ID)}}</b></td><td><b>${{esc(a.Problem)}}</b></td><td class="num">${{esc(a.Date)}}</td><td>${{esc(a.Claimant_System)}}</td><td>${{esc(a.Artifact_Type)}}</td><td>${{esc(a.Machine_Check_Status)}}</td><td>${{esc(a.Human_Fidelity_Audit)}}</td><td><span class="badge badge-ai">${{esc(a.Official_Status_Nov2026)}}</span></td></tr>
  `).join('');

  document.getElementById('regsTbody').innerHTML = REGISTRIES.map(r => `
    <tr><td><b>${{esc(r.Registry)}}</b></td><td>${{esc(r.Scope)}}</td><td><b>${{esc(r.Total_Tracked)}}</b></td><td>${{esc(r.Open_Count_Nov2026)}}</td><td>${{esc(r.Verification_Standard)}}</td><td>${{esc(r.Nov2026_Highlight)}}</td></tr>
  `).join('');

  document.getElementById('contrastsGrid').innerHTML = CONTRASTS.map(c => `
    <div class="contrast-card">
      <h4>${{esc(c.contrast_id)}} · ${{esc(c.title)}}</h4>
      <div style="margin-bottom:7px;"><span class="chip" onclick="openDetail('${{c.problem_a_id}}')">${{c.problem_a_id}}</span> vs. <span class="chip" onclick="openDetail('${{c.problem_b_id}}')">${{c.problem_b_id}}</span></div>
      <p><b>Similarity:</b> ${{esc(c.core_similarity)}}</p>
      <p><b>Contrast:</b> ${{esc(c.core_contrast)}}</p>
      <p><b>Impact Asymmetry:</b> ${{esc(c.impact_asymmetry)}}</p>
      <p><b>Likely First Breakthrough:</b> ${{esc(c.likely_winner_first)}}</p>
    </div>
  `).join('');

  document.getElementById('benchTbody').innerHTML = BENCHMARKS.map(b => {{
    const tw = ID_MAP[b.open_twin_id];
    return `<tr><td class="mono"><b>${{esc(b.id)}}</b></td><td><b>${{esc(b.name)}}</b></td><td>${{esc(b.domain)}}</td><td class="num">${{b.year_posed}}</td><td class="num score-good">${{b.year_solved}}</td><td class="num">${{b.years_open}}y</td><td>${{esc(b.solver)}}</td><td>${{esc(b.mechanism)}}</td><td><span class="chip" onclick="openDetail('${{b.open_twin_id}}')">${{b.open_twin_id}}: ${{tw ? esc(tw.name.slice(0,38)) : ''}}</span></td></tr>`;
  }}).join('');
}}

function filterSelect(inputId, selId, forceVal) {{
  const q = document.getElementById(inputId).value.trim().toLowerCase();
  const sel = document.getElementById(selId);
  const prev = forceVal || sel.value;
  sel.innerHTML = '';
  PROBLEMS.filter(p => !q || (p.id + ' ' + p.name + ' ' + p.superdomain).toLowerCase().includes(q))
    .slice(0, 450).forEach(p => sel.add(new Option(`[${{p.id}}] ${{p.name}}`, p.id)));
  if ([...sel.options].some(o => o.value === prev)) sel.value = prev;
  renderCompare();
}}

function filterAIClaims() {{
  resetFilters();
  document.getElementById('fStatus').value = 'AI Proof Claim (Fall/Nov 2026) — Under Verification';
  goPage(1);
}}
function resetFilters() {{
  ['fSearch','fPillar','fSuper','fStatus','fType','fBottleneck','fQuadrant'].forEach(id => document.getElementById(id).value = '');
  goPage(1);
}}
function sortBy(col) {{
  if (sortCol === col) sortDir *= -1; else {{ sortCol = col; sortDir = (typeof PROBLEMS[0][col] === 'number') ? -1 : 1; }}
  goPage(1);
}}

function goPage(pg) {{
  const q = document.getElementById('fSearch').value.trim().toLowerCase();
  const fp = document.getElementById('fPillar').value;
  const fs = document.getElementById('fSuper').value;
  const fst = document.getElementById('fStatus').value;
  const ft = document.getElementById('fType').value;
  const fb = document.getElementById('fBottleneck').value;
  const fq = document.getElementById('fQuadrant').value;

  filteredRows = PROBLEMS.filter(p => {{
    if (fp && p.macro_pillar !== fp) return false;
    if (fs && p.superdomain !== fs) return false;
    if (fst && p.status_2026 !== fst) return false;
    if (ft && p.problem_type !== ft) return false;
    if (fb && p.primary_bottleneck !== fb) return false;
    if (fq && p.strategic_quadrant !== fq) return false;
    if (q) {{
      const hay = (p.id+' '+p.name+' '+p.subdomain+' '+p.core_question+' '+p.formal_expression+' '+p.originator+' '+p.competing_approaches+' '+p.affected_industries+' '+p.registry_source+' '+p.ai_verification_nov2026).toLowerCase();
      if (!hay.includes(q)) return false;
    }}
    return true;
  }});

  filteredRows.sort((a, b) => {{
    const va = a[sortCol], vb = b[sortCol];
    if (typeof va === 'number') return (va - vb) * sortDir;
    return String(va).localeCompare(String(vb)) * sortDir;
  }});

  const psize = parseInt(document.getElementById('pageSize').value, 10) || 100;
  const maxPg = Math.max(1, Math.ceil(filteredRows.length / psize));
  curPage = Math.max(1, Math.min(pg, maxPg));
  const slice = filteredRows.slice((curPage - 1) * psize, curPage * psize);

  document.getElementById('countSummary').textContent = `Showing ${{slice.length}} of ${{filteredRows.length.toLocaleString()}} matching (Total ${{PROBLEMS.length.toLocaleString()}}) · Sorted by ${{sortCol}}`;
  document.getElementById('pageInfo').textContent = `Page ${{curPage}} / ${{maxPg}}`;

  document.getElementById('masterTbody').innerHTML = slice.map(p => {{
    const isAI = p.status_2026.includes('AI Proof Claim');
    return `<tr class="clickable" onclick="openDetail('${{p.id}}')">
      <td class="mono"><b>${{esc(p.id)}}</b></td>
      <td><b>${{esc(p.name)}}</b><div style="font-size:0.73rem;color:var(--muted);">${{esc(p.subdomain)}}</div></td>
      <td><span class="pill" style="background:${{PILLAR_COLORS[p.macro_pillar]}}">${{esc(p.macro_pillar.split(',')[0].split('&')[0].trim())}}</span></td>
      <td>${{esc(p.superdomain)}}</td>
      <td class="num">${{fmtYear(p.year_formulated)}}</td>
      <td><span class="badge ${{isAI?'badge-ai':''}}">${{esc(p.status_2026)}}</span></td>
      <td class="num ${{p.difficulty_score>=9?'score-hi':''}}">${{p.difficulty_score}}</td>
      <td class="num ${{p.tractability_2050>=8?'score-good':p.tractability_2050<=4?'score-hi':'score-mid'}}">${{p.tractability_2050}}</td>
      <td class="num">${{p.civilizational_impact}}</td>
      <td class="num">${{p.titan_index.toFixed(2)}}</td>
      <td class="num">${{p.graph_degree}}</td>
      <td>${{esc(p.primary_bottleneck)}}</td>
      <td>${{esc(p.registry_source)}}</td>
    </tr>`;
  }}).join('');
}}

function openDetail(pid) {{
  const p = ID_MAP[pid];
  if (!p) return;
  const links = (p.related_problem_ids || '').split(',').filter(Boolean).map(rid => {{
    const rp = ID_MAP[rid];
    return `<span class="chip" onclick="openDetail('${{rid}}')">${{rid}}: ${{rp ? esc(rp.name.slice(0,30)) : ''}}</span>`;
  }}).join(' ');
  document.getElementById('detailContent').innerHTML = `
    <button class="modal-close" onclick="closeModal()">✕ Close</button>
    <div style="margin-bottom:8px;">
      <span class="pill" style="background:${{PILLAR_COLORS[p.macro_pillar]}}">${{esc(p.macro_pillar)}}</span>
      <span class="badge">${{esc(p.superdomain)}}</span>
      <span class="badge">${{esc(p.problem_type)}}</span>
      <span class="badge">${{esc(p.registry_source)}}</span>
    </div>
    <h2 style="font-size:1.25rem;margin-bottom:4px;">[${{esc(p.id)}}] ${{esc(p.name)}}</h2>
    <div style="color:var(--muted);font-size:0.83rem;margin-bottom:12px;">
      <b>${{esc(p.subdomain)}}</b> · ${{fmtYear(p.year_formulated)}} (${{p.age_years_2026}}y) by <b>${{esc(p.originator)}}</b> · Status: <b>${{esc(p.status_2026)}}</b>
    </div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:12px;">
      <div class="kpi" style="background:var(--surface2);"><div class="v">${{p.difficulty_score}}/10</div><div class="l">Difficulty</div></div>
      <div class="kpi" style="background:var(--surface2);"><div class="v">${{p.tractability_2050}}/10</div><div class="l">Tract 2050</div></div>
      <div class="kpi" style="background:var(--surface2);"><div class="v">${{p.civilizational_impact}}/10</div><div class="l">Impact</div></div>
      <div class="kpi" style="background:var(--surface2);"><div class="v">${{p.titan_index}}</div><div class="l">Titan Index</div></div>
      <div class="kpi" style="background:var(--surface2);"><div class="v">${{p.graph_degree}} (${{p.cross_pillar_links}} XP)</div><div class="l">Degree</div></div>
    </div>
    <div class="field-box"><strong>Core Question</strong>${{esc(p.core_question)}}</div>
    <div class="field-box"><strong>Formal / Governing Expression</strong><div class="mono" style="background:var(--surface2);padding:7px;border-radius:6px;margin-top:3px;">${{esc(p.formal_expression)}}</div></div>
    <div class="field-box"><strong>Nov 20, 2026 AI Claim &amp; Verification Audit</strong>${{esc(p.ai_verification_nov2026)}}</div>
    <div class="field-box"><strong>Primary Bottleneck · Scale · Verification</strong>${{esc(p.primary_bottleneck)}} · ${{esc(p.scale_regime)}} · ${{esc(p.verification_type)}}</div>
    <div class="field-box"><strong>Competing Approaches</strong>${{esc(p.competing_approaches)}}</div>
    <div class="field-box"><strong>2026 Frontier Progress</strong>${{esc(p.closest_progress_2026)}}</div>
    <div class="field-box"><strong>Core Contrast Axis</strong><i>${{esc(p.contrast_axis)}}</i></div>
    <div class="field-box"><strong>Affected Industries &amp; Initiative</strong>${{esc(p.affected_industries)}} · <i>${{esc(p.prize_or_initiative)}}</i></div>
    <div class="field-box"><strong>Coupled Knowledge-Graph Neighbors</strong><div style="margin-top:4px;">${{links}}</div></div>
  `;
  document.getElementById('detailModal').classList.add('open');
}}

function renderCompare() {{
  const a = ID_MAP[document.getElementById('selA').value];
  const b = ID_MAP[document.getElementById('selB').value];
  if (!a || !b) return;
  const setA = new Set((a.related_problem_ids||'').split(',').filter(Boolean));
  const setB = new Set((b.related_problem_ids||'').split(',').filter(Boolean));
  const shared = [...setA].filter(x => setB.has(x));
  const direct = setA.has(b.id) || setB.has(a.id);
  document.getElementById('compDeltaBanner').innerHTML = `
    <b>Comparison Delta:</b> ΔDiff: <b>${{a.difficulty_score-b.difficulty_score}}</b> · ΔTract2050: <b>${{a.tractability_2050-b.tractability_2050}}</b> ·
    ΔImpact: <b>${{a.civilizational_impact-b.civilizational_impact}}</b> · ΔAge: <b>${{Math.abs(a.age_years_2026-b.age_years_2026)}}y</b> ·
    Direct Link: <b>${{direct?'YES':'No'}}</b> · Shared Neighbors: <b>${{shared.length?shared.join(', '):'None direct'}}</b>`;
  const mk = p => `<div class="comp-card">
    <div style="margin-bottom:7px;"><span class="pill" style="background:${{PILLAR_COLORS[p.macro_pillar]}}">${{esc(p.macro_pillar)}}</span> <span class="badge">${{esc(p.superdomain)}}</span></div>
    <h3 style="font-size:1.08rem;margin-bottom:4px;">[${{esc(p.id)}}] ${{esc(p.name)}}</h3>
    <div style="font-size:0.79rem;color:var(--muted);margin-bottom:10px;">${{fmtYear(p.year_formulated)}} (${{p.age_years_2026}}y) · ${{esc(p.status_2026)}}</div>
    ${{[['Difficulty',p.difficulty_score,'#EF4444'],['Tract 2050',p.tractability_2050,'#10B981'],['Impact',p.civilizational_impact,'#3B82F6'],['Interdisc.',p.interdisciplinarity_index,'#8B5CF6'],['Titan Index',p.titan_index,'#F59E0B']]
      .map(([l,v,c]) => `<div class="bar-row"><div class="bar-lbl">${{l}}</div><div class="bar-track"><div class="bar-fill" style="width:${{Math.min(100,v*10)}}%;background:${{c}}"></div></div><div style="width:38px;text-align:right;font-weight:700;">${{v}}</div></div>`).join('')}}
    <div class="field-box"><strong>Core Question</strong>${{esc(p.core_question)}}</div>
    <div class="field-box"><strong>Formal Expression</strong><div class="mono">${{esc(p.formal_expression)}}</div></div>
    <div class="field-box"><strong>Nov 2026 Audit</strong>${{esc(p.ai_verification_nov2026)}}</div>
    <div class="field-box"><strong>Bottleneck &amp; Verification</strong>${{esc(p.primary_bottleneck)}} | ${{esc(p.verification_type)}}</div>
    <div class="field-box"><strong>Competing Approaches</strong>${{esc(p.competing_approaches)}}</div>
    <div class="field-box"><strong>2026 Progress</strong>${{esc(p.closest_progress_2026)}}</div>
    <div class="field-box"><strong>Contrast Axis</strong><i>${{esc(p.contrast_axis)}}</i></div>
  </div>`;
  document.getElementById('compGrid').innerHTML = mk(a) + mk(b);
}}

populateUI();
goPage(1);
</script>
</body>
</html>
"""
    p_html = os.path.join(OUT_DIR, "MegaAtlas_Interactive_Dashboard_V2.html")
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  Saved V2.0 Interactive HTML Dashboard: {p_html} ({os.path.getsize(p_html)/1048576:.2f} MB)")


# ==================== 5. PUBLICATION PRINT HTML & VECTOR PDF MONOGRAPH ====================
def export_pdf_monograph(data):
    df = data["df"]
    s = data["summary_stats"]
    id_map = data["id_map"]

    chart_blocks = "".join(
        f'<div class="fig-block"><div class="fig-cap">{html.escape(cap)}</div>'
        f'<img src="{b64_img(fname)}" alt="{html.escape(cap)}" /></div>'
        for fname, cap in CHART_ITEMS
    )

    contrast_blocks = "".join(
        f'<div class="contrast-box"><h4>{html.escape(r.contrast_id)} · {html.escape(r.title)} '
        f'<span class="tag">{r.problem_a_id}</span> vs. <span class="tag">{r.problem_b_id}</span></h4>'
        f'<p><b>Similarity:</b> {html.escape(r.core_similarity)}</p>'
        f'<p><b>Contrast:</b> {html.escape(r.core_contrast)}</p>'
        f'<p><b>Impact Asymmetry:</b> {html.escape(r.impact_asymmetry)} · <b>First Likely:</b> {html.escape(r.likely_winner_first)}</p></div>'
        for r in data["df_contrasts"].itertuples()
    )

    # Compact crisp reference directory of ALL 1,600–1,850+ problems!
    dir_parts = []
    for pi, pil in enumerate(MACRO_PILLARS, 1):
        p_df = df[df["macro_pillar"] == pil]
        col_hex = PILLAR_HEX[pil]
        dir_parts.append(f'<div class="pillar-banner" style="border-left: 6px solid {col_hex};">PILLAR {pi}: {html.escape(pil.upper())} ({len(p_df):,} Problems)</div>')
        for sd in [k for k, v in SUPERDOMAIN_TO_PILLAR.items() if v == pil]:
            sub = p_df[p_df["superdomain"] == sd]
            dir_parts.append(f'<h3 class="sd-heading">{html.escape(sd)} <span class="sd-cnt">({len(sub)} Problems)</span></h3>')
            dir_parts.append('<table class="dir-table"><thead><tr><th style="width:9%;">ID</th><th style="width:27%;">Problem, Origin &amp; Status</th><th style="width:42%;">Core Question, Formal Relation &amp; 2026 Frontier</th><th style="width:22%;">Scores, Bottleneck &amp; Links</th></tr></thead><tbody>')
            for r in sub.itertuples():
                yr_s = f"{abs(r.year_formulated)} BCE" if r.year_formulated < 0 else str(r.year_formulated)
                ai_flag = ' <span class="ai-tag">AI CLAIM NOV 2026</span>' if "AI Proof Claim" in r.status_2026 else ""
                dir_parts.append(
                    f'<tr>'
                    f'<td class="mono"><b>{html.escape(r.id)}</b></td>'
                    f'<td><b>{html.escape(r.name)}</b>{ai_flag}<br/><span class="muted">{html.escape(r.subdomain)} · {yr_s} ({r.age_years_2026}y) · {html.escape(r.originator[:42])} · <i>{html.escape(r.status_2026)}</i></span></td>'
                    f'<td>{html.escape(r.core_question)}<br/><code class="eq">{html.escape(r.formal_expression[:135])}</code><br/><span class="muted"><b>2026:</b> {html.escape(r.closest_progress_2026[:165])}</span></td>'
                    f'<td><b>D:{r.difficulty_score} T:{r.tractability_2050} I:{r.civilizational_impact}</b> · Tit:{r.titan_index} · Deg:{r.graph_degree}<br/><span class="muted">{html.escape(r.primary_bottleneck)}<br/>{html.escape(r.registry_source)}<br/>Links: {html.escape(r.related_problem_ids[:44])}</span></td>'
                    f'</tr>'
                )
            dir_parts.append("</tbody></table>")

    print_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>V2.0 Mega-Atlas: Humanity's {s['total_problems']:,} Unsolved, Open &amp; Hard Problems (Nov 2026)</title>
<style>
  @page {{ size: letter portrait; margin: 0.48in 0.45in 0.52in 0.45in; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Segoe UI", -apple-system, Roboto, Arial, sans-serif; color: #0F172A; font-size: 8.1pt; line-height: 1.34; margin: 0; }}
  .cover {{ page-break-after: always; background: linear-gradient(150deg, #0B1120 0%, #1E1B4B 52%, #0C4A6E 100%); color: #FFF; padding: 48px 40px; border-radius: 10px; min-height: 9.7in; display: flex; flex-direction: column; justify-content: space-between; }}
  .cover-kicker {{ font-size: 9.5pt; letter-spacing: 0.16em; text-transform: uppercase; color: #38BDF8; font-weight: 800; margin-bottom: 12px; }}
  .cover h1 {{ font-size: 25pt; line-height: 1.14; font-weight: 800; margin: 0 0 14px 0; }}
  .cover-sub {{ font-size: 10.6pt; color: #CBD5E1; line-height: 1.46; }}
  .cover-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 24px 0; }}
  .cover-kpi {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(148,163,184,0.3); border-radius: 8px; padding: 11px; }}
  .cover-kpi .v {{ font-size: 16pt; font-weight: 800; color: #38BDF8; }}
  .cover-kpi .l {{ font-size: 7.2pt; color: #E2E8F0; text-transform: uppercase; margin-top: 2px; }}
  .cover-pillars {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 7px; }}
  .cover-pil {{ background: rgba(15,23,42,0.58); border-left: 4px solid #38BDF8; padding: 7px 10px; font-size: 8.1pt; border-radius: 4px; }}
  .cover-foot {{ font-size: 8.0pt; color: #94A3B8; border-top: 1px solid rgba(148,163,184,0.25); padding-top: 12px; }}

  h2.sec {{ font-size: 13pt; color: #0F172A; border-bottom: 2.2px solid #0284C7; padding-bottom: 3px; margin: 14px 0 8px 0; page-break-after: avoid; }}
  h3.subsec {{ font-size: 9.8pt; color: #1E3A8A; margin: 10px 0 5px 0; page-break-after: avoid; }}
  .page-break {{ page-break-before: always; }}
  .callout {{ background: #FEF2F2; border-left: 4px solid #DC2626; padding: 8px 11px; margin: 7px 0 11px 0; border-radius: 4px; font-size: 8.0pt; }}

  table.data-table {{ width: 100%; border-collapse: collapse; font-size: 6.7pt; margin: 5px 0 10px 0; }}
  table.data-table th {{ background: #0F172A; color: #FFF; padding: 3.5px 4.5px; text-align: left; font-weight: 700; border: 0.5px solid #334155; }}
  table.data-table td {{ padding: 3px 4.5px; border: 0.5px solid #CBD5E1; vertical-align: top; }}
  table.data-table tr:nth-child(even) td {{ background: #F8FAFC; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}

  .fig-block {{ break-inside: avoid; page-break-inside: avoid; margin: 8px 0 13px 0; text-align: center; border: 0.7px solid #E2E8F0; border-radius: 5px; padding: 7px; }}
  .fig-cap {{ font-size: 8.4pt; font-weight: 700; color: #1E293B; margin-bottom: 5px; text-align: left; }}
  .fig-block img {{ max-width: 100%; max-height: 4.35in; width: auto; height: auto; display: block; margin: 0 auto; }}

  .contrast-box {{ break-inside: avoid; border: 0.7px solid #CBD5E1; border-left: 4px solid #BE185D; border-radius: 4px; padding: 6px 9px; margin-bottom: 7px; }}
  .contrast-box h4 {{ margin: 0 0 3px 0; font-size: 8.6pt; color: #831843; }}
  .contrast-box p {{ margin: 2px 0; font-size: 7.5pt; }}
  .tag {{ font-size: 6.7pt; background: #F1F5F9; border: 0.5px solid #94A3B8; padding: 0.5px 4px; border-radius: 3px; font-weight: 700; }}

  .pillar-banner {{ background: #0F172A; color: #FFF; font-size: 10pt; font-weight: 800; padding: 5px 9px; margin: 12px 0 6px 0; border-radius: 4px; page-break-after: avoid; }}
  .sd-heading {{ font-size: 9.2pt; color: #1E3A8A; border-bottom: 1px solid #CBD5E1; padding-bottom: 2px; margin: 8px 0 4px 0; page-break-after: avoid; }}
  .sd-cnt {{ font-weight: 400; color: #64748B; font-size: 7.8pt; }}

  table.dir-table {{ width: 100%; border-collapse: collapse; font-size: 6.4pt; margin-bottom: 8px; table-layout: fixed; }}
  table.dir-table th {{ background: #1E293B; color: #FFF; padding: 3px 4px; text-align: left; border: 0.5px solid #334155; }}
  table.dir-table td {{ padding: 2.8px 4px; border: 0.5px solid #CBD5E1; vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }}
  table.dir-table tr {{ break-inside: avoid; page-break-inside: avoid; }}
  table.dir-table tr:nth-child(even) td {{ background: #F8FAFC; }}
  .mono {{ font-family: Consolas, monospace; font-size: 6.3pt; }}
  .muted {{ color: #475569; font-size: 6.0pt; }}
  code.eq {{ background: #F1F5F9; padding: 0.5px 3px; border-radius: 2px; font-family: Consolas, monospace; font-size: 5.9pt; }}
  .ai-tag {{ background: #FEE2E2; color: #991B1B; border: 0.5px solid #EF4444; font-size: 5.6pt; font-weight: 800; padding: 0.5px 3px; border-radius: 2px; }}
</style>
</head>
<body>

<div class="cover">
  <div>
    <div class="cover-kicker">V2.0 Exhaustive Monograph · November 20, 2026 Special Edition</div>
    <h1>Humanity's {s['total_problems']:,} Unsolved, Open &amp; Hard Problems Across All Fields of Knowledge</h1>
    <div class="cover-sub">A Unified Quantitative Taxonomy, Multi-Dimensional Comparison &amp; Contrast Atlas, November 2026 AI Proof-Claim Verification Audit, Global Open-Problem Registry Synthesis, NetworkX Cross-Pillar Connectome, and Complete Master Directory Spanning All 8 Macro-Pillars &amp; 28 Superdomains.</div>
    <div class="cover-grid">
      <div class="cover-kpi"><div class="v">{s['total_problems']:,}</div><div class="l">Open / Hard Problems</div></div>
      <div class="cover-kpi"><div class="v">8 × 28</div><div class="l">Pillars × Superdomains</div></div>
      <div class="cover-kpi"><div class="v">{s['total_graph_edges']:,}</div><div class="l">Coupling Edges</div></div>
      <div class="cover-kpi"><div class="v">{s['cross_pillar_edge_pct']}%</div><div class="l">Cross-Pillar Bridges</div></div>
      <div class="cover-kpi"><div class="v">{s['ai_claims_nov2026_count']}</div><div class="l">Nov 2026 AI Claims</div></div>
      <div class="cover-kpi"><div class="v">{s['mean_difficulty']} / {s['mean_tractability']}</div><div class="l">Diff / Tract 2050</div></div>
      <div class="cover-kpi"><div class="v">{s['mean_impact']}</div><div class="l">Mean Impact</div></div>
      <div class="cover-kpi"><div class="v">500 BCE–2026</div><div class="l">Historical Span</div></div>
    </div>
    <div class="cover-pillars">
      {''.join(f'<div class="cover-pil" style="border-left-color:{PILLAR_HEX[r.Macro_Pillar]};"><b>{html.escape(r.Macro_Pillar)}</b> — {r.Problem_Count:,} ({r.Share_Pct}%) · D:{r.Mean_Difficulty} T:{r.Mean_Tractability_2050} I:{r.Mean_Impact}</div>' for r in data["df_pillars"].itertuples())}
    </div>
  </div>
  <div class="cover-foot">
    <b>Release Date:</b> November 20, 2026 · <b>Companion Formats:</b> CSV, TSV, JSON, 13-Sheet Live-Formula XLSX, Legacy XLS, Markdown, Plain Text, Offline Interactive HTML Dashboard &amp; 12 Vector SVG/PNG Charts · <b>Connectome:</b> {s['connected_components']} Unified Component ({s['largest_component_size']:,}/{s['total_problems']:,} nodes).
  </div>
</div>

<h2 class="sec">Section 1 · November 20, 2026 Special Report: AI Proof Claims, Verification Crisis &amp; Global Registries</h2>
<div class="callout">
  <b>Live November 20, 2026 Verification Advisory:</b> No single fixed count of open mathematical or scientific problems exists—active registries track thousands (<b>ProofAtlas.ai</b>: 1,100+ eligible / 243 open in Top-500; <b>Erdős Problems DB</b>: ~1,221 tracked / ~630+ open; <b>Kourovka</b>: &gt;1,000; <b>Kirby</b>: 360+). Rapid Fall–November 2026 AI claims (OpenAI Sept 8 Navier–Stokes, OpenAI Oct 6 722-manuscript dump, Nov 20 Alpöge/Claude Lean RH &amp; GRH archive + Masullo human draft) remain <b>unverified / officially open</b> pending independent formal-statement fidelity and peer refereeing.
</div>
<h3 class="subsec">1.1 November 20, 2026 AI Proof-Claim Verification Audit Ledger</h3>
{df_to_html_table(data["df_ai_audit"])}
<h3 class="subsec">1.2 Global Open-Problem Registries &amp; Trackers Comparison (13 Benchmarks)</h3>
{df_to_html_table(data["df_registries"])}

<div class="page-break"></div>
<h2 class="sec">Section 2 · 8-Macro-Pillar &amp; 28-Superdomain Quantitative Scorecards</h2>
<h3 class="subsec">2.1 Eight Macro-Pillars Comparative Profile</h3>
{df_to_html_table(data["df_pillars"][["Macro_Pillar","Problem_Count","Share_Pct","Mean_Difficulty","Mean_Tractability_2050","Mean_Impact","Mean_Interdisciplinarity","Mean_Titan_Index","Median_Year","AI_Claims_Nov2026","Dominant_Bottleneck"]])}
<h3 class="subsec">2.2 All 28 Superdomains Statistical Scorecard</h3>
{df_to_html_table(data["df_superdomains"][["Superdomain","Macro_Pillar","Problem_Count","Mean_Difficulty","Mean_Tractability_2050","Mean_Impact","Mean_Titan_Index","Median_Year","Dominant_Bottleneck","Flagship_Titan_ID"]])}

<div class="page-break"></div>
<h2 class="sec">Section 3 · Complete 12-Figure Visual Analytics Atlas</h2>
{chart_blocks}

<div class="page-break"></div>
<h2 class="sec">Section 4 · Cross-Tabulation Matrices &amp; Top 40 Keystone Domino Hubs</h2>
<h3 class="subsec">4.1 Strategic 4-Quadrant × 8 Macro-Pillars</h3>
{df_to_html_table(data["ct_quadrant_pillar"], include_index=True)}
<h3 class="subsec">4.2 Problem Type × Epistemic Class</h3>
{df_to_html_table(data["ct_type_epistemic"], include_index=True)}
<h3 class="subsec">4.3 Primary Bottleneck × 8 Macro-Pillars</h3>
{df_to_html_table(data["ct_bottleneck_pillar"], include_index=True)}
<h3 class="subsec">4.4 Nov 2026 Status × 8 Macro-Pillars &amp; Era × 8 Macro-Pillars</h3>
{df_to_html_table(data["ct_status_pillar"], include_index=True)}
{df_to_html_table(data["ct_era_pillar"], include_index=True)}
<h3 class="subsec">4.5 Top 40 Keystone Domino Hubs (NetworkX PageRank &amp; Bridges)</h3>
{df_to_html_table(data["df_keystones"].head(40)[["Rank","id","name","macro_pillar","difficulty_score","tractability_2050","civilizational_impact","titan_index","graph_degree","cross_pillar_links"]])}

<div class="page-break"></div>
<h2 class="sec">Section 5 · 15 Iconic Pairwise Contrasts &amp; 20 Resolved Benchmarks (1995–2026)</h2>
{contrast_blocks}
<h3 class="subsec">5.2 20 Recently Resolved Historical Benchmarks vs. Still-Open Twins</h3>
{df_to_html_table(data["df_benchmarks"])}

<div class="page-break"></div>
<h2 class="sec">Section 6 · Complete Exhaustive Directory of All {s['total_problems']:,} Unsolved, Open &amp; Hard Problems</h2>
{''.join(dir_parts)}

</body>
</html>
"""
    p_html = os.path.join(OUT_DIR, "MegaAtlas_Print_Report_V2.html")
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(print_html)
    print(f"  Saved Print Monograph HTML: {p_html}")

    p_pdf = os.path.join(OUT_DIR, "MegaAtlas_Comprehensive_Report_V2.pdf")
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = next((c for c in chrome_candidates if os.path.exists(c)), None)
    assert browser, "Chrome/Edge not found!"
    url = "file:///" + p_html.replace("\\", "/")
    print(f"  Compiling V2.0 PDF Monograph via {os.path.basename(browser)}...")
    res = subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-sandbox", "--print-to-pdf-no-header", f"--print-to-pdf={p_pdf}", url], capture_output=True, text=True, timeout=240)
    assert os.path.exists(p_pdf) and os.path.getsize(p_pdf) > 200_000, f"PDF build failed: {res.stderr}"
    print(f"  Saved V2.0 Vector PDF Monograph: {p_pdf} ({os.path.getsize(p_pdf)/1048576:.2f} MB)")


def main():
    print("Loading V2.0 Mega-Atlas...")
    data = load_v2_master()
    export_csv_tsv_json(data)
    export_excel_files(data)
    export_md_and_txt(data)
    export_interactive_html(data)
    export_pdf_monograph(data)
    print("\n=== ALL V2.0 MEGA-ATLAS EXPORTS COMPLETED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()
