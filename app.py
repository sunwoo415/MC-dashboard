import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Monte Carlo Review Dashboard", layout="wide", initial_sidebar_state="expanded")

DB_PATH = "mc_reviews.db"

SKH_CSS = """
<style>
:root {
    --sk-orange: #ea5b0c;
    --sk-red: #d83a34;
    --sk-light-orange: #fff2e8;
    --sk-light-red: #fff0f0;
    --sk-border: #f2c3a5;
    --sk-border-soft: #f1ddd1;
    --sk-text: #1f2937;
    --sk-muted: #6b7280;
    --panel-bg: #fffdfb;
    --header-bg: #fff1e8;
    --header-text: #8b3a10;
    --label-bg: #fff7f1;
    --value-bg: #ffffff;
    --good-bg: #ecfdf3;
    --good-text: #0f7a3d;
    --bad-bg: #fff1f1;
    --bad-text: #b42318;
    --neutral-bg: #f8fafc;
    --neutral-text: #475467;
}
html, body, [class*="css"] { font-family: "Segoe UI", Arial, sans-serif; color: var(--sk-text); }
.stApp { background: linear-gradient(180deg, #fffaf7 0%, #fffdfb 100%); }
.block-container { padding-top: 1.1rem; padding-bottom: 2rem; max-width: 1520px; }
.app-hero {
    background: linear-gradient(100deg, rgba(234,91,12,0.14) 0%, rgba(216,58,52,0.08) 100%);
    border: 1px solid var(--sk-border); border-radius: 22px; padding: 22px 26px; margin-bottom: 16px;
    box-shadow: 0 10px 24px rgba(31,41,55,0.05);
}
.logo-badge {
    display:inline-flex; align-items:center; gap:8px; padding:8px 13px; border-radius:999px;
    background:white; border:1px solid var(--sk-border); font-weight:700; color:var(--sk-red);
}
.logo-dot { width:12px; height:12px; border-radius:999px; background:linear-gradient(180deg,var(--sk-orange),var(--sk-red)); display:inline-block; }
.hero-title { font-size:1.65rem; font-weight:800; margin:0; letter-spacing:-0.02em; }
.hero-sub { color:var(--sk-muted); font-size:0.96rem; margin:0; line-height:1.45; }
.section-title { font-size:1.07rem; font-weight:800; margin-top:0.25rem; margin-bottom:0.8rem; letter-spacing:-0.01em; }
.metric-card {
    background: linear-gradient(180deg, #ffffff 0%, #fffdfa 100%);
    border: 1px solid #f2e3d9; border-left: 5px solid var(--sk-orange);
    border-radius: 16px; padding: 14px 16px; box-shadow: 0 8px 20px rgba(17,24,39,0.045);
    margin-bottom:10px; min-height:116px;
}
.metric-label { font-size:0.85rem; color:var(--sk-muted); margin-bottom:6px; }
.metric-value { font-size:1.55rem; font-weight:800; line-height:1.1; }
.metric-note { font-size:0.84rem; color:var(--sk-muted); margin-top:8px; line-height:1.35; }
.panel-card {
    background: linear-gradient(180deg, #ffffff 0%, var(--panel-bg) 100%);
    border: 1px solid #f2e3d9; border-radius: 18px; padding: 15px 16px 12px 16px;
    box-shadow: 0 8px 20px rgba(17,24,39,0.045); margin-bottom: 14px;
}
.small-tag {
    display:inline-block; padding:4px 10px; font-size:0.78rem; font-weight:700; color:var(--sk-red);
    background:var(--sk-light-red); border-radius:999px; border:1px solid #f1c5c3; margin-bottom:10px;
}
.note-box {
    border-left: 4px solid var(--sk-orange); background: var(--sk-light-orange);
    padding: 10px 12px; border-radius: 10px; font-size: 0.9rem; margin-bottom: 12px;
}
.summary-box {
    background:#fff8f3; border:1px solid #f2d7c3; border-left:5px solid var(--sk-red);
    border-radius:16px; padding:15px 16px; margin-bottom:12px;
}
.summary-title { font-weight:800; color:var(--sk-red); margin-bottom:8px; }
.summary-list { margin:0; padding-left:18px; line-height:1.5; }
.stTabs [data-baseweb="tab-list"] { gap:8px; margin-bottom:10px; }
.stTabs [data-baseweb="tab"] {
    height:46px; border-radius:13px; background:#fff6f2; color:#7c4a35; border:1px solid #f2d3c2;
    padding-left:16px; padding-right:16px; font-weight:700;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(234,91,12,0.10), rgba(216,58,52,0.10));
    color:#7f231f; border:1px solid #efb28d;
}
section[data-testid="stSidebar"] { background:#fff9f5; border-right:1px solid #f1ddd1; }
.sidebar-title { font-weight:800; color:var(--sk-red); margin-bottom:0.4rem; }
hr.soft { border:none; border-top:1px solid #f1ddd1; margin:0.8rem 0 1rem 0; }
.table-wrap { overflow-x:visible; border:1px solid var(--sk-border-soft); border-radius:14px; }
.review-table { width:100%; border-collapse:separate; border-spacing:0; font-size:13px; }
.review-table th {
    background:var(--header-bg); color:var(--header-text); padding:9px 10px;
    border-bottom:1px solid #efdbc9; text-align:left; font-weight:700;
}
.review-table td { padding:8px 10px; border-bottom:1px solid #f3e7de; }
.review-table td.label { background:var(--label-bg); font-weight:700; color:#7c4a35; }
.review-table td.value { background:var(--value-bg); text-align:right; }
.review-table td.good { background:var(--good-bg); color:var(--good-text); font-weight:700; text-align:right; }
.review-table td.bad { background:var(--bad-bg); color:var(--bad-text); font-weight:700; text-align:right; }
.review-table td.neutral { background:var(--neutral-bg); color:var(--neutral-text); font-weight:700; text-align:right; }
.board-card {
    background:white; border:1px solid #f2e3d9; border-left:5px solid var(--sk-orange); border-radius:16px;
    padding:14px 16px; box-shadow:0 8px 20px rgba(17,24,39,0.045); margin-bottom:12px;
}
.board-title { font-weight:800; font-size:1rem; color:var(--sk-text); margin-bottom:6px; }
.board-meta { color:var(--sk-muted); font-size:0.88rem; margin-bottom:10px; }
.board-yield { display:flex; gap:10px; flex-wrap:wrap; }
.board-pill {
    display:inline-block; padding:4px 10px; border-radius:999px; background:#fff7f1; color:#7c4a35;
    border:1px solid #f2d3c2; font-size:0.82rem; font-weight:700;
}
</style>
"""
st.markdown(SKH_CSS, unsafe_allow_html=True)

LABEL_COLS = {"version", "metric", "display_name", "unit", "rule_type", "field", "statistic", "critical_metric", "failed_metrics", "fail_type", "status", "owner", "comment", "project_name", "design_version", "reviewer", "saved_at"}
INT_COLS = {"run", "total_runs", "overall_pass_count", "overall_fail_count", "pass_count", "fail_count", "num_failed_metrics", "review_id"}

# ---------------- DB ----------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def ensure_column(cur, table_name, column_name, coltype):
    cols = [r[1] for r in cur.execute(f"PRAGMA table_info({table_name})").fetchall()]
    if column_name not in cols:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {coltype}")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            saved_at TEXT NOT NULL,
            project_name TEXT NOT NULL,
            design_version TEXT NOT NULL,
            reviewer TEXT,
            review_note TEXT,
            specs_json TEXT NOT NULL,
            comments_json TEXT NOT NULL,
            overall_v1_yield REAL,
            overall_v2_yield REAL
        )
        """
    )
    ensure_column(cur, "reviews", "v1_json", "TEXT")
    ensure_column(cur, "reviews", "v2_json", "TEXT")
    ensure_column(cur, "reviews", "source_filename", "TEXT")
    conn.commit()
    conn.close()

def save_review_to_db(project_name, design_version, reviewer, review_note, specs_df, comments_df, overall_v1_yield, overall_v2_yield, v1_df, v2_df, source_filename=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO reviews
        (saved_at, project_name, design_version, reviewer, review_note, specs_json, comments_json, overall_v1_yield, overall_v2_yield, v1_json, v2_json, source_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            project_name,
            design_version,
            reviewer,
            review_note,
            specs_df.to_json(orient="records"),
            comments_df.to_json(orient="records"),
            float(overall_v1_yield),
            float(overall_v2_yield),
            v1_df.to_json(orient="records"),
            v2_df.to_json(orient="records"),
            source_filename,
        ),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid

def list_saved_reviews():
    conn = get_conn()
    df = pd.read_sql_query(
        """
        SELECT review_id, saved_at, project_name, design_version, reviewer, review_note, overall_v1_yield, overall_v2_yield, source_filename
        FROM reviews
        ORDER BY review_id DESC
        """,
        conn,
    )
    conn.close()
    return df

def load_review_from_db(review_id):
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM reviews WHERE review_id = ?", conn, params=(review_id,))
    conn.close()
    if df.empty:
        return None
    row = df.iloc[0].to_dict()
    row["specs_df"] = pd.read_json(row["specs_json"])
    row["comments_df"] = pd.read_json(row["comments_json"])
    row["v1_df"] = pd.read_json(row["v1_json"]) if row.get("v1_json") else None
    row["v2_df"] = pd.read_json(row["v2_json"]) if row.get("v2_json") else None
    return row

# ---------------- utils ----------------
def fmt_value(col, val):
    if pd.isna(val):
        return "-"
    if col in INT_COLS:
        try:
            return f"{int(round(float(val))):,}"
        except Exception:
            return str(val)
    if isinstance(val, (int, float)):
        if "yield" in col.lower() or "pct" in col.lower():
            return f"{float(val):.1f}"
        return f"{float(val):.2f}"
    return str(val)

def render_metric_card(label, value, note="", decimals=2):
    num = f"{float(value):.{decimals}f}" if isinstance(value, (int, float)) else str(value)
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{num}</div>
        <div class="metric-note">{note}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_review_table(df, tag, delta_positive_good=True):
    if df is None or df.empty:
        st.markdown(f'<div class="panel-card"><div class="small-tag">{tag}</div><div class="note-box">No data available.</div></div>', unsafe_allow_html=True)
        return
    cols = list(df.columns)
    html = [f'<div class="panel-card"><div class="small-tag">{tag}</div><div class="table-wrap"><table class="review-table"><thead><tr>']
    for col in cols:
        html.append(f"<th>{col}</th>")
    html.append("</tr></thead><tbody>")
    for _, row in df.iterrows():
        html.append("<tr>")
        for col in cols:
            val = row[col]
            cls = "label" if col in LABEL_COLS else "value"
            if "delta" in col.lower() and isinstance(val, (int, float)):
                good = val > 0 if delta_positive_good else val < 0
                bad = val < 0 if delta_positive_good else val > 0
                if good:
                    cls = "good"
                elif bad:
                    cls = "bad"
                else:
                    cls = "neutral"
            html.append(f"<td class='{cls}'>{fmt_value(col, val)}</td>")
        html.append("</tr>")
    html.append("</tbody></table></div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)

def render_board(df):
    if df is None or df.empty:
        st.markdown('<div class="note-box">No saved reviews yet.</div>', unsafe_allow_html=True)
        return
    for _, row in df.iterrows():
        note = row["review_note"] if isinstance(row["review_note"], str) and row["review_note"].strip() else "(no note)"
        source = row["source_filename"] if isinstance(row["source_filename"], str) and row["source_filename"].strip() else "-"
        html = f"""
        <div class="board-card">
            <div class="board-title">#{int(row['review_id'])} · {row['project_name']} · {row['design_version']}</div>
            <div class="board-meta">Saved: {row['saved_at']} · Reviewer: {row['reviewer'] if row['reviewer'] else '-'} · Source: {source}</div>
            <div class="board-meta">Note: {note}</div>
            <div class="board-yield">
                <span class="board-pill">v1 yield: {fmt_value('overall_v1_yield', row['overall_v1_yield'])}</span>
                <span class="board-pill">v2 yield: {fmt_value('overall_v2_yield', row['overall_v2_yield'])}</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# ---------------- analysis helpers ----------------
def load_workbook(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    if "MC_v1" not in sheet_names or "MC_v2" not in sheet_names:
        raise ValueError("Input workbook must contain 'MC_v1' and 'MC_v2' sheets.")
    v1 = pd.read_excel(uploaded_file, sheet_name="MC_v1")
    uploaded_file.seek(0)
    v2 = pd.read_excel(uploaded_file, sheet_name="MC_v2")
    uploaded_file.seek(0)
    specs = None
    if "Specs" in sheet_names:
        specs = pd.read_excel(uploaded_file, sheet_name="Specs")
        uploaded_file.seek(0)
    return specs, v1, v2

def build_default_specs(v1, v2):
    common_cols = [c for c in v1.columns if c in v2.columns]
    meta_cols = {"run", "corner", "temp_C", "vdd_V", "seed", "trial", "iteration"}
    metric_cols = [c for c in common_cols if c not in meta_cols and pd.api.types.is_numeric_dtype(v1[c]) and pd.api.types.is_numeric_dtype(v2[c])]
    rows = []
    for c in metric_cols:
        rows.append({"metric": c, "display_name": c, "rule_type": "min", "spec_value": float(pd.concat([v1[c], v2[c]], ignore_index=True).median()), "unit": "", "enabled": "Y"})
    return pd.DataFrame(rows)

def normalize_specs(specs, v1, v2):
    if specs is None or specs.empty:
        specs = build_default_specs(v1, v2)
    specs = specs.copy()
    if "display_name" not in specs.columns:
        specs["display_name"] = specs["metric"]
    if "unit" not in specs.columns:
        specs["unit"] = ""
    if "enabled" not in specs.columns:
        specs["enabled"] = "Y"
    specs = specs[["metric", "display_name", "rule_type", "spec_value", "unit", "enabled"]]
    valid_metrics = set(v1.columns).intersection(set(v2.columns))
    specs = specs[specs["metric"].isin(valid_metrics)].reset_index(drop=True)
    if specs.empty:
        raise ValueError("No valid metrics found.")
    return specs

def evaluate_metric(series, rule_type, spec_value):
    if rule_type == "min":
        return series >= spec_value
    if rule_type == "max":
        return series <= spec_value
    if rule_type == "absmax":
        return series.abs() <= spec_value
    raise ValueError(f"Unsupported rule_type: {rule_type}")

def compute_margin(series, rule_type, spec_value):
    if rule_type == "min":
        return series - spec_value
    if rule_type == "max":
        return spec_value - series
    if rule_type == "absmax":
        return spec_value - series.abs()
    raise ValueError(f"Unsupported rule_type: {rule_type}")

def summarize_version(df, specs, version_name):
    detail = df.copy()
    summary_rows = []
    active_specs = specs[specs["enabled"].astype(str).str.upper() == "Y"].reset_index(drop=True)
    if active_specs.empty:
        raise ValueError("At least one spec must be enabled.")
    for _, spec in active_specs.iterrows():
        metric = spec["metric"]
        display_name = spec["display_name"]
        rule_type = spec["rule_type"]
        spec_value = float(spec["spec_value"])
        unit = spec["unit"]
        pass_col = f"{metric}_pass"
        margin_col = f"{metric}_margin"
        detail[pass_col] = evaluate_metric(detail[metric], rule_type, spec_value)
        detail[margin_col] = compute_margin(detail[metric], rule_type, spec_value)
        if rule_type == "min":
            mean_minus_spec = detail[metric].mean() - spec_value
        elif rule_type == "max":
            mean_minus_spec = spec_value - detail[metric].mean()
        else:
            mean_minus_spec = spec_value - detail[metric].abs().mean()
        summary_rows.append({
            "version": version_name, "metric": metric, "display_name": display_name, "unit": unit, "rule_type": rule_type,
            "spec_value": spec_value, "mean": detail[metric].mean(), "sigma": detail[metric].std(ddof=1),
            "min": detail[metric].min(), "max": detail[metric].max(), "pass_count": int(detail[pass_col].sum()),
            "fail_count": int((~detail[pass_col]).sum()), "yield_pct": 100.0 * detail[pass_col].mean(),
            "mean_minus_spec": mean_minus_spec,
        })
    pass_cols = [f"{m}_pass" for m in active_specs["metric"]]
    margin_cols = [f"{m}_margin" for m in active_specs["metric"]]
    detail["overall_pass"] = detail[pass_cols].all(axis=1)
    detail["worst_margin"] = detail[margin_cols].min(axis=1)
    critical_metric_names = []
    for _, row in detail[margin_cols].iterrows():
        metric_margin_map = {col.replace("_margin", ""): row[col] for col in margin_cols}
        critical_metric_names.append(min(metric_margin_map, key=metric_margin_map.get))
    detail["critical_metric"] = critical_metric_names
    failed_metric_list, fail_count_list = [], []
    for _, row in detail.iterrows():
        failed = [metric for metric in active_specs["metric"] if not bool(row[f"{metric}_pass"])]
        failed_metric_list.append(", ".join(failed) if failed else "PASS")
        fail_count_list.append(len(failed))
    detail["failed_metrics"] = failed_metric_list
    detail["num_failed_metrics"] = fail_count_list
    overall = pd.DataFrame([{
        "version": version_name,
        "total_runs": len(detail),
        "overall_pass_count": int(detail["overall_pass"].sum()),
        "overall_fail_count": int((~detail["overall_pass"]).sum()),
        "overall_yield_pct": 100.0 * detail["overall_pass"].mean(),
    }])
    return active_specs, pd.DataFrame(summary_rows).sort_values("metric").reset_index(drop=True), overall, detail

def compare_versions(summary_v1, summary_v2):
    merged = summary_v1.merge(summary_v2, on=["metric", "display_name", "unit", "rule_type", "spec_value"], suffixes=("_v1", "_v2"))
    compare_cols = ["mean", "sigma", "min", "max", "pass_count", "fail_count", "yield_pct", "mean_minus_spec"]
    for col in compare_cols:
        merged[f"{col}_delta_v2_minus_v1"] = merged[f"{col}_v2"] - merged[f"{col}_v1"]
    return merged.sort_values("metric").reset_index(drop=True)

def build_fail_ranking(detail, specs, version_name):
    rows = []
    for metric in specs["metric"]:
        fail_count = int((~detail[f"{metric}_pass"]).sum())
        rows.append({"version": version_name, "metric": metric, "fail_count": fail_count})
    return pd.DataFrame(rows).sort_values(["fail_count", "metric"], ascending=[False, True]).reset_index(drop=True)

def build_near_fail_samples(detail, specs, version_name, n=10):
    metric_cols = specs["metric"].tolist()
    meta_cols = [c for c in ["run", "overall_pass", "worst_margin", "critical_metric"] if c in detail.columns]
    use_cols = meta_cols + metric_cols
    near_fail = detail.loc[detail["overall_pass"]].sort_values(["worst_margin"], ascending=True)[use_cols].head(n).copy()
    near_fail.insert(0, "version", version_name)
    return near_fail.reset_index(drop=True)

def build_summary_insights(overall_v1, overall_v2, fail_rank_v1, fail_rank_v2, near_fail_v1, near_fail_v2, metric_compare):
    lines = []
    y1 = float(overall_v1.iloc[0]["overall_yield_pct"])
    y2 = float(overall_v2.iloc[0]["overall_yield_pct"])
    delta = y2 - y1
    lines.append(f"v2 overall yield is {'higher' if delta > 0 else 'lower' if delta < 0 else 'the same as'} v1" + (f" by {abs(delta):.1f}%p." if delta != 0 else "."))
    if not fail_rank_v1.empty:
        lines.append(f"Top fail metric in v1 is {fail_rank_v1.iloc[0]['metric']}.")
    if not fail_rank_v2.empty:
        lines.append(f"Top fail metric in v2 is {fail_rank_v2.iloc[0]['metric']}.")
    if not near_fail_v1.empty and "critical_metric" in near_fail_v1.columns:
        lines.append(f"Near-fail samples in v1 are dominated by {near_fail_v1['critical_metric'].value_counts().idxmax()}.")
    if not near_fail_v2.empty and "critical_metric" in near_fail_v2.columns:
        lines.append(f"Near-fail samples in v2 are dominated by {near_fail_v2['critical_metric'].value_counts().idxmax()}.")
    if not metric_compare.empty:
        best = metric_compare.sort_values("yield_pct_delta_v2_minus_v1", ascending=False).iloc[0]
        worst = metric_compare.sort_values("yield_pct_delta_v2_minus_v1", ascending=True).iloc[0]
        lines.append(f"Biggest yield improvement in v2 comes from {best['metric']} ({best['yield_pct_delta_v2_minus_v1']:.1f}%p).")
        lines.append(f"Largest yield degradation in v2 comes from {worst['metric']} ({worst['yield_pct_delta_v2_minus_v1']:.1f}%p).")
    return lines

def build_spec_sensitivity(detail, specs, step_pct=2.0):
    active_specs = specs[specs["enabled"].astype(str).str.upper() == "Y"].reset_index(drop=True)
    rows = []
    if active_specs.empty:
        return pd.DataFrame()
    base_pass_cols = [f"{m}_pass" for m in active_specs["metric"]]
    base_yield = 100.0 * detail[base_pass_cols].all(axis=1).mean()
    for _, spec in active_specs.iterrows():
        metric = spec["metric"]
        rule_type = spec["rule_type"]
        spec_value = float(spec["spec_value"])
        factor = step_pct / 100.0
        if rule_type == "min":
            relax_spec = spec_value * (1.0 - factor)
            tighten_spec = spec_value * (1.0 + factor)
        elif rule_type == "max":
            relax_spec = spec_value * (1.0 + factor)
            tighten_spec = spec_value * (1.0 - factor)
        else:
            relax_spec = spec_value * (1.0 + factor)
            tighten_spec = spec_value * (1.0 - factor)
        temp = detail.copy()

        def overall_yield_for_changed_spec(changed_spec):
            pass_df = pd.DataFrame(index=temp.index)
            for _, s in active_specs.iterrows():
                m = s["metric"]; rt = s["rule_type"]; sv = float(s["spec_value"])
                if m == metric:
                    sv = changed_spec
                pass_df[m] = evaluate_metric(temp[m], rt, sv)
            return 100.0 * pass_df.all(axis=1).mean()

        relax_yield = overall_yield_for_changed_spec(relax_spec)
        tighten_yield = overall_yield_for_changed_spec(tighten_spec)
        rows.append({
            "metric": metric,
            "display_name": spec["display_name"],
            "current_spec": spec_value,
            "base_yield_pct": base_yield,
            "yield_if_relaxed": relax_yield,
            "relaxed_delta": relax_yield - base_yield,
            "yield_if_tightened": tighten_yield,
            "tightened_delta": tighten_yield - base_yield,
            "max_shift_pctp": max(abs(relax_yield - base_yield), abs(tighten_yield - base_yield)),
        })
    return pd.DataFrame(rows).sort_values("max_shift_pctp", ascending=False).reset_index(drop=True)

def plot_histogram(v1, v2, metric, rule_type, spec_value):
    plot_v1 = v1[metric].abs() if rule_type == "absmax" else v1[metric]
    plot_v2 = v2[metric].abs() if rule_type == "absmax" else v2[metric]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(plot_v1.dropna(), bins=24, alpha=0.6, label="v1")
    ax.hist(plot_v2.dropna(), bins=24, alpha=0.6, label="v2")
    ax.axvline(spec_value, linestyle="--", label="current spec")
    ax.set_title(f"Histogram - {metric}")
    ax.legend()
    fig.tight_layout()
    return fig

def plot_cdf(v1, v2, metric, rule_type, spec_value):
    plot_v1 = v1[metric].abs() if rule_type == "absmax" else v1[metric]
    plot_v2 = v2[metric].abs() if rule_type == "absmax" else v2[metric]
    def empirical_cdf(values):
        s = pd.Series(values).dropna().sort_values().to_list()
        if not s:
            return [], []
        y = [(i + 1) / len(s) for i in range(len(s))]
        return s, y
    x1, y1 = empirical_cdf(plot_v1)
    x2, y2 = empirical_cdf(plot_v2)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x1, y1, label="v1")
    ax.plot(x2, y2, label="v2")
    ax.axvline(spec_value, linestyle="--", label="current spec")
    ax.set_title(f"CDF - {metric}")
    ax.legend()
    fig.tight_layout()
    return fig

# ---------------- state init ----------------
init_db()
DEFAULT_META = {"project_name": "MC Review Project", "design_version": "v1", "reviewer": "", "review_note": ""}
for k, v in DEFAULT_META.items():
    if k not in st.session_state:
        st.session_state[k] = v
for k, default in {
    "loaded_review_id": None,
    "loaded_specs_json": None,
    "loaded_comments_json": None,
    "loaded_v1_json": None,
    "loaded_v2_json": None,
    "editor_nonce": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = default

# ---------------- header ----------------
st.markdown("""
<div class="app-hero">
    <div class="logo-badge"><span class="logo-dot"></span>SK hynix-style review UI</div>
    <div style="margin-top:10px;">
        <h1 class="hero-title">Monte Carlo Review Dashboard</h1>
        <p class="hero-sub">Saved Reviews Board is always visible. Load now restores raw data too, so Excel is optional after save.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- sidebar controls ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Dashboard Controls</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    st.markdown('<hr class="soft" />', unsafe_allow_html=True)
    st.markdown("**Display options**")
    top_n = st.slider("Rows for near-fail / worst", min_value=5, max_value=30, value=10, step=1)
    sensitivity_step = st.slider("Spec sensitivity step (%)", min_value=1.0, max_value=10.0, value=2.0, step=1.0)
    show_raw = st.checkbox("Show raw data tables", value=False)
    st.markdown('<hr class="soft" />', unsafe_allow_html=True)
    st.markdown("**Saved reviews**")
    saved_reviews_df = list_saved_reviews()
    options = ["(none)"]
    if not saved_reviews_df.empty:
        options += [f"{int(r.review_id)} | {r.project_name} | {r.design_version} | {r.saved_at}" for _, r in saved_reviews_df.iterrows()]
    selected_saved = st.selectbox("Load saved review", options=options)
    load_clicked = st.button("Load selected review into current session")

# apply load before widgets and before any upload gating
if load_clicked and selected_saved != "(none)":
    rid = int(selected_saved.split("|")[0].strip())
    loaded_review = load_review_from_db(rid)
    if loaded_review is not None:
        st.session_state.loaded_review_id = rid
        st.session_state.project_name = loaded_review["project_name"] or DEFAULT_META["project_name"]
        st.session_state.design_version = loaded_review["design_version"] or DEFAULT_META["design_version"]
        st.session_state.reviewer = loaded_review["reviewer"] or DEFAULT_META["reviewer"]
        st.session_state.review_note = loaded_review["review_note"] or DEFAULT_META["review_note"]
        st.session_state.loaded_specs_json = loaded_review["specs_json"]
        st.session_state.loaded_comments_json = loaded_review["comments_json"]
        st.session_state.loaded_v1_json = loaded_review["v1_json"]
        st.session_state.loaded_v2_json = loaded_review["v2_json"]
        st.session_state.editor_nonce += 1
        st.rerun()

# ---------------- always-visible saved board ----------------
board_df = list_saved_reviews()
board_tab, analysis_tab = st.tabs(["Saved Reviews Board", "Current Review / Analysis"])

with board_tab:
    st.markdown('<div class="section-title">Saved Reviews Board</div>', unsafe_allow_html=True)
    render_board(board_df)
    if not board_df.empty:
        render_review_table(board_df[["review_id","saved_at","project_name","design_version","reviewer","overall_v1_yield","overall_v2_yield","source_filename"]], "SAVED REVIEWS TABLE")

with analysis_tab:
    # determine data source: uploaded file first, else loaded db raw data
    specs_from_file = None
    source_filename = ""
    if uploaded_file is not None:
        try:
            specs_from_file, v1, v2 = load_workbook(uploaded_file)
            source_filename = uploaded_file.name if hasattr(uploaded_file, "name") else ""
            # when user uploads new excel, uploaded data becomes current active analysis source
        except Exception as e:
            st.error(f"Failed to read workbook: {e}")
            st.stop()
    elif st.session_state.loaded_v1_json and st.session_state.loaded_v2_json:
        v1 = pd.read_json(st.session_state.loaded_v1_json)
        v2 = pd.read_json(st.session_state.loaded_v2_json)
        source_filename = "loaded_from_db"
    else:
        st.info("Upload an Excel workbook, or load a saved review from the left sidebar.")
        st.stop()

    # metadata
    st.markdown('<div class="section-title">Review Metadata</div>', unsafe_allow_html=True)
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        project_name = st.text_input("Project name", key="project_name")
        design_version = st.text_input("Design version", key="design_version")
    with meta_col2:
        reviewer = st.text_input("Reviewer", key="reviewer")
        review_note = st.text_area("Review note", key="review_note", height=100)

    # specs
    specs_base = normalize_specs(specs_from_file, v1, v2)
    if st.session_state.loaded_specs_json:
        specs_base = pd.read_json(st.session_state.loaded_specs_json).copy()
        if "enabled" in specs_base.columns:
            specs_base["enabled"] = specs_base["enabled"].astype(str).str.upper()

    st.markdown('<div class="section-title">Spec Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    spec_editor = specs_base.copy()
    spec_editor["enabled"] = spec_editor["enabled"].astype(str).str.upper().map(lambda x: True if x == "Y" else False)
    edited_specs = st.data_editor(
        spec_editor,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key=f"spec_editor_db_{st.session_state.editor_nonce}",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    edited_specs = edited_specs.copy()
    edited_specs["enabled"] = edited_specs["enabled"].map(lambda x: "Y" if bool(x) else "N")

    try:
        active_specs_v1, summary_v1, overall_v1, detail_v1 = summarize_version(v1, edited_specs, "v1")
        active_specs_v2, summary_v2, overall_v2, detail_v2 = summarize_version(v2, edited_specs, "v2")
    except Exception as e:
        st.error(f"Spec processing failed: {e}")
        st.stop()

    metric_compare = compare_versions(summary_v1, summary_v2)
    fail_rank_v1 = build_fail_ranking(detail_v1, active_specs_v1, "v1")
    fail_rank_v2 = build_fail_ranking(detail_v2, active_specs_v2, "v2")
    near_fail_v1 = build_near_fail_samples(detail_v1, active_specs_v1, "v1", n=top_n)
    near_fail_v2 = build_near_fail_samples(detail_v2, active_specs_v2, "v2", n=top_n)
    sensitivity_v1 = build_spec_sensitivity(detail_v1, edited_specs, sensitivity_step)
    sensitivity_v2 = build_spec_sensitivity(detail_v2, edited_specs, sensitivity_step)
    summary_lines = build_summary_insights(overall_v1, overall_v2, fail_rank_v1, fail_rank_v2, near_fail_v1, near_fail_v2, metric_compare)

    # comments
    comment_base = pd.DataFrame({
        "metric": active_specs_v1["metric"].tolist(),
        "status": ["open"] * len(active_specs_v1),
        "owner": [""] * len(active_specs_v1),
        "comment": [""] * len(active_specs_v1),
    })
    if st.session_state.loaded_comments_json:
        loaded_comments = pd.read_json(st.session_state.loaded_comments_json).copy()
        if not loaded_comments.empty:
            comment_base = comment_base.drop(columns=["status", "owner", "comment"]).merge(loaded_comments, on="metric", how="left")
            comment_base["status"] = comment_base["status"].fillna("open")
            comment_base["owner"] = comment_base["owner"].fillna("")
            comment_base["comment"] = comment_base["comment"].fillna("")

    tabs = st.tabs(["Executive Summary", "Summary", "Compare", "Spec Sensitivity", "Comments / Actions", "Charts", "Raw Data"])

    with tabs[0]:
        items = "".join([f"<li>{line}</li>" for line in summary_lines])
        st.markdown(f'<div class="summary-box"><div class="summary-title">Key findings</div><ul class="summary-list">{items}</ul></div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            render_metric_card("v1 overall yield (%)", overall_v1.iloc[0]["overall_yield_pct"], "Current enabled-spec result.", 1)
        with b:
            render_metric_card("v2 overall yield (%)", overall_v2.iloc[0]["overall_yield_pct"], "Current enabled-spec result.", 1)
        with c:
            render_metric_card("Yield delta (v2-v1)", overall_v2.iloc[0]["overall_yield_pct"] - overall_v1.iloc[0]["overall_yield_pct"], "Positive means v2 improved.", 1)

    with tabs[1]:
        render_review_table(overall_v1, "VERSION 1")
        render_review_table(overall_v2, "VERSION 2")
        core_cols = ["version", "metric", "display_name", "rule_type", "spec_value", "yield_pct", "fail_count", "mean_minus_spec"]
        render_review_table(summary_v1[core_cols], "VERSION 1 - CORE")
        render_review_table(summary_v2[core_cols], "VERSION 2 - CORE")

    with tabs[2]:
        overall_compare = pd.DataFrame([
            {"field":"total_runs","version_1":overall_v1.iloc[0]["total_runs"],"version_2":overall_v2.iloc[0]["total_runs"],"delta":overall_v2.iloc[0]["total_runs"]-overall_v1.iloc[0]["total_runs"]},
            {"field":"overall_pass_count","version_1":overall_v1.iloc[0]["overall_pass_count"],"version_2":overall_v2.iloc[0]["overall_pass_count"],"delta":overall_v2.iloc[0]["overall_pass_count"]-overall_v1.iloc[0]["overall_pass_count"]},
            {"field":"overall_fail_count","version_1":overall_v1.iloc[0]["overall_fail_count"],"version_2":overall_v2.iloc[0]["overall_fail_count"],"delta":overall_v2.iloc[0]["overall_fail_count"]-overall_v1.iloc[0]["overall_fail_count"]},
            {"field":"overall_yield_pct","version_1":overall_v1.iloc[0]["overall_yield_pct"],"version_2":overall_v2.iloc[0]["overall_yield_pct"],"delta":overall_v2.iloc[0]["overall_yield_pct"]-overall_v1.iloc[0]["overall_yield_pct"]},
        ])
        render_review_table(overall_compare, "OVERALL COMPARE", True)
        metric_compare_yield = metric_compare[["metric", "display_name", "yield_pct_v1", "yield_pct_v2", "yield_pct_delta_v2_minus_v1", "fail_count_v1", "fail_count_v2", "fail_count_delta_v2_minus_v1"]].copy()
        metric_compare_yield = metric_compare_yield.rename(columns={
            "yield_pct_v1":"v1_yield_pct","yield_pct_v2":"v2_yield_pct","yield_pct_delta_v2_minus_v1":"yield_delta",
            "fail_count_v1":"v1_fail_count","fail_count_v2":"v2_fail_count","fail_count_delta_v2_minus_v1":"fail_count_delta"
        })
        render_review_table(metric_compare_yield, "METRIC COMPARE - YIELD / FAIL", True)

    with tabs[3]:
        st.markdown(f'<div class="note-box">Current perturbation step: ±{sensitivity_step:.0f}%.</div>', unsafe_allow_html=True)
        relaxed_v1 = sensitivity_v1[["metric","display_name","current_spec","base_yield_pct","yield_if_relaxed","relaxed_delta","max_shift_pctp"]]
        relaxed_v2 = sensitivity_v2[["metric","display_name","current_spec","base_yield_pct","yield_if_relaxed","relaxed_delta","max_shift_pctp"]]
        tightened_v1 = sensitivity_v1[["metric","display_name","current_spec","base_yield_pct","yield_if_tightened","tightened_delta","max_shift_pctp"]]
        tightened_v2 = sensitivity_v2[["metric","display_name","current_spec","base_yield_pct","yield_if_tightened","tightened_delta","max_shift_pctp"]]
        render_review_table(relaxed_v1, "VERSION 1 - RELAXED", True)
        render_review_table(relaxed_v2, "VERSION 2 - RELAXED", True)
        render_review_table(tightened_v1, "VERSION 1 - TIGHTENED", True)
        render_review_table(tightened_v2, "VERSION 2 - TIGHTENED", True)

    with tabs[4]:
        comments_df = st.data_editor(
            comment_base,
            num_rows="fixed",
            use_container_width=True,
            hide_index=True,
            column_config={
                "status": st.column_config.SelectboxColumn("status", options=["open", "watch", "resolved"]),
                "owner": st.column_config.TextColumn("owner"),
                "comment": st.column_config.TextColumn("comment"),
            },
            key=f"comments_editor_db_{st.session_state.editor_nonce}",
        )
        render_review_table(comments_df, "CURRENT ACTION ITEMS")

    with tabs[5]:
        metric_options = active_specs_v1["metric"].tolist()
        selected_metric = st.selectbox("Select metric", metric_options)
        spec_row = active_specs_v1.loc[active_specs_v1["metric"] == selected_metric].iloc[0]
        rule_type = spec_row["rule_type"]
        spec_value = float(spec_row["spec_value"])
        a, b = st.columns(2)
        with a:
            st.markdown('<div class="panel-card"><div class="small-tag">Histogram</div>', unsafe_allow_html=True)
            fig = plot_histogram(v1, v2, selected_metric, rule_type, spec_value)
            st.pyplot(fig)
            plt.close(fig)
            st.markdown("</div>", unsafe_allow_html=True)
        with b:
            st.markdown('<div class="panel-card"><div class="small-tag">CDF</div>', unsafe_allow_html=True)
            fig = plot_cdf(v1, v2, selected_metric, rule_type, spec_value)
            st.pyplot(fig)
            plt.close(fig)
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[6]:
        if not show_raw:
            st.info("Enable 'Show raw data tables' from the sidebar to view raw tables here.")
        else:
            render_review_table(edited_specs, "ACTIVE SPECS")
            render_review_table(v1, "RAW DATA - MC_v1")
            render_review_table(v2, "RAW DATA - MC_v2")

    with st.sidebar:
        st.markdown('<hr class="soft" />', unsafe_allow_html=True)
        st.markdown("**Database save**")
        if st.button("Save current review to DB"):
            rid = save_review_to_db(
                project_name=project_name,
                design_version=design_version,
                reviewer=reviewer,
                review_note=review_note,
                specs_df=edited_specs,
                comments_df=comments_df,
                overall_v1_yield=overall_v1.iloc[0]["overall_yield_pct"],
                overall_v2_yield=overall_v2.iloc[0]["overall_yield_pct"],
                v1_df=v1,
                v2_df=v2,
                source_filename=source_filename,
            )
            st.session_state.loaded_review_id = rid
            st.session_state.loaded_specs_json = edited_specs.to_json(orient="records")
            st.session_state.loaded_comments_json = comments_df.to_json(orient="records")
            st.session_state.loaded_v1_json = v1.to_json(orient="records")
            st.session_state.loaded_v2_json = v2.to_json(orient="records")
            st.success(f"Saved review #{rid} to database.")
        st.caption(f"DB file: {DB_PATH}")
        st.caption(f"Saved reviews: {len(list_saved_reviews())}")
