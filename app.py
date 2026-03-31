
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Monte Carlo Review Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

SKH_CSS = """
<style>
:root {
    --sk-orange: #ea5b0c;
    --sk-red: #d83a34;
    --sk-light-orange: #fff2e8;
    --sk-light-red: #fff0f0;
    --sk-border: #f2c3a5;
    --sk-text: #1f2937;
    --sk-muted: #6b7280;
    --card-bg: #ffffff;
}
html, body, [class*="css"]  {
    font-family: "Segoe UI", Arial, sans-serif;
    color: var(--sk-text);
}
.stApp {
    background: linear-gradient(180deg, #fffaf7 0%, #fffdfb 100%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
.app-hero {
    background: linear-gradient(90deg, rgba(234,91,12,0.12) 0%, rgba(216,58,52,0.08) 100%);
    border: 1px solid var(--sk-border);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.hero-top {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 8px;
}
.logo-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 12px;
    border-radius: 999px;
    background: white;
    border: 1px solid var(--sk-border);
    box-shadow: 0 2px 8px rgba(216,58,52,0.08);
    font-weight: 700;
    color: var(--sk-red);
}
.logo-dot {
    width: 12px;
    height: 12px;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--sk-orange), var(--sk-red));
    display: inline-block;
}
.hero-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--sk-text);
    margin: 0;
}
.hero-sub {
    color: var(--sk-muted);
    font-size: 0.95rem;
    margin: 0;
}
.section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--sk-text);
    margin-top: 0.2rem;
    margin-bottom: 0.8rem;
}
.metric-card {
    background: var(--card-bg);
    border: 1px solid #f2e3d9;
    border-left: 5px solid var(--sk-orange);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 4px 12px rgba(17,24,39,0.04);
    margin-bottom: 10px;
    min-height: 112px;
}
.metric-label {
    font-size: 0.85rem;
    color: var(--sk-muted);
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--sk-text);
    line-height: 1.1;
}
.metric-note {
    font-size: 0.84rem;
    color: var(--sk-muted);
    margin-top: 8px;
}
.panel-card {
    background: var(--card-bg);
    border: 1px solid #f2e3d9;
    border-radius: 16px;
    padding: 14px 16px 10px 16px;
    box-shadow: 0 4px 12px rgba(17,24,39,0.04);
    margin-bottom: 14px;
}
.small-tag {
    display: inline-block;
    padding: 4px 10px;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--sk-red);
    background: var(--sk-light-red);
    border-radius: 999px;
    border: 1px solid #f1c5c3;
    margin-bottom: 8px;
}
.note-box {
    border-left: 4px solid var(--sk-orange);
    background: var(--sk-light-orange);
    padding: 10px 12px;
    border-radius: 10px;
    color: var(--sk-text);
    font-size: 0.9rem;
    margin-bottom: 12px;
}
.summary-box {
    background: #fff8f3;
    border: 1px solid #f2d7c3;
    border-left: 5px solid var(--sk-red);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 12px;
}
.summary-title {
    font-weight: 800;
    color: var(--sk-red);
    margin-bottom: 8px;
}
.summary-list {
    margin: 0;
    padding-left: 18px;
    color: var(--sk-text);
}
div[data-testid="stDataFrame"] {
    border: 1px solid #f2e3d9;
    border-radius: 12px;
    overflow: hidden;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    margin-bottom: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 12px;
    background: #fff6f2;
    color: #7c4a35;
    border: 1px solid #f2d3c2;
    padding-left: 16px;
    padding-right: 16px;
    font-weight: 700;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(234,91,12,0.10), rgba(216,58,52,0.10));
    color: #7f231f;
    border: 1px solid #efb28d;
}
section[data-testid="stSidebar"] {
    background: #fff9f5;
    border-right: 1px solid #f1ddd1;
}
.sidebar-title {
    font-weight: 800;
    color: var(--sk-red);
    margin-bottom: 0.4rem;
}
hr.soft {
    border: none;
    border-top: 1px solid #f1ddd1;
    margin: 0.8rem 0 1rem 0;
}
</style>
"""

st.markdown(SKH_CSS, unsafe_allow_html=True)


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


def build_default_specs(v1: pd.DataFrame, v2: pd.DataFrame) -> pd.DataFrame:
    common_cols = [c for c in v1.columns if c in v2.columns]
    meta_cols = {"run", "corner", "temp_C", "vdd_V", "seed", "trial", "iteration"}
    metric_cols = []
    for c in common_cols:
        if c in meta_cols:
            continue
        if pd.api.types.is_numeric_dtype(v1[c]) and pd.api.types.is_numeric_dtype(v2[c]):
            metric_cols.append(c)

    rows = []
    for c in metric_cols:
        rows.append({
            "metric": c,
            "display_name": c,
            "rule_type": "min",
            "spec_value": float(pd.concat([v1[c], v2[c]], ignore_index=True).median()),
            "unit": "",
            "enabled": "Y",
        })
    return pd.DataFrame(rows)


def normalize_specs(specs: pd.DataFrame, v1: pd.DataFrame, v2: pd.DataFrame) -> pd.DataFrame:
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
        raise ValueError("No valid metrics found. Add numeric metric columns to both MC_v1 and MC_v2.")
    return specs


def evaluate_metric(series: pd.Series, rule_type: str, spec_value: float) -> pd.Series:
    if rule_type == "min":
        return series >= spec_value
    if rule_type == "max":
        return series <= spec_value
    if rule_type == "absmax":
        return series.abs() <= spec_value
    raise ValueError(f"Unsupported rule_type: {rule_type}")


def compute_margin(series: pd.Series, rule_type: str, spec_value: float) -> pd.Series:
    if rule_type == "min":
        return series - spec_value
    if rule_type == "max":
        return spec_value - series
    if rule_type == "absmax":
        return spec_value - series.abs()
    raise ValueError(f"Unsupported rule_type: {rule_type}")


def summarize_version(df: pd.DataFrame, specs: pd.DataFrame, version_name: str):
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
            "version": version_name,
            "metric": metric,
            "display_name": display_name,
            "unit": unit,
            "rule_type": rule_type,
            "spec_value": spec_value,
            "mean": detail[metric].mean(),
            "sigma": detail[metric].std(ddof=1),
            "min": detail[metric].min(),
            "max": detail[metric].max(),
            "pass_count": int(detail[pass_col].sum()),
            "fail_count": int((~detail[pass_col]).sum()),
            "yield_pct": 100.0 * detail[pass_col].mean(),
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

    failed_metric_list = []
    fail_count_list = []
    for _, row in detail.iterrows():
        failed = [metric for metric in active_specs["metric"] if not bool(row[f"{metric}_pass"])]
        failed_metric_list.append(", ".join(failed) if failed else "PASS")
        fail_count_list.append(len(failed))
    detail["failed_metrics"] = failed_metric_list
    detail["num_failed_metrics"] = fail_count_list

    overall = pd.DataFrame([{
        "version": version_name,
        "fixed_corner": detail["corner"].iloc[0] if "corner" in detail.columns else "",
        "fixed_temp_C": detail["temp_C"].iloc[0] if "temp_C" in detail.columns else "",
        "fixed_vdd_V": detail["vdd_V"].iloc[0] if "vdd_V" in detail.columns else "",
        "total_runs": len(detail),
        "overall_pass_count": int(detail["overall_pass"].sum()),
        "overall_fail_count": int((~detail["overall_pass"]).sum()),
        "overall_yield_pct": 100.0 * detail["overall_pass"].mean(),
    }])

    summary = pd.DataFrame(summary_rows).sort_values("metric").reset_index(drop=True)
    return active_specs, summary, overall, detail


def compare_versions(summary_v1: pd.DataFrame, summary_v2: pd.DataFrame) -> pd.DataFrame:
    merged = summary_v1.merge(
        summary_v2,
        on=["metric", "display_name", "unit", "rule_type", "spec_value"],
        suffixes=("_v1", "_v2"),
    )
    compare_cols = ["mean", "sigma", "min", "max", "pass_count", "fail_count", "yield_pct", "mean_minus_spec"]
    for col in compare_cols:
        merged[f"{col}_delta_v2_minus_v1"] = merged[f"{col}_v2"] - merged[f"{col}_v1"]
    return merged.sort_values("metric").reset_index(drop=True)


def build_fail_ranking(detail: pd.DataFrame, specs: pd.DataFrame, version_name: str) -> pd.DataFrame:
    rows = []
    for metric in specs["metric"]:
        fail_count = int((~detail[f"{metric}_pass"]).sum())
        rows.append({"version": version_name, "metric": metric, "fail_count": fail_count})
    return pd.DataFrame(rows).sort_values(["fail_count", "metric"], ascending=[False, True]).reset_index(drop=True)


def build_fail_decomposition(detail: pd.DataFrame, version_name: str) -> pd.DataFrame:
    fail_df = detail.loc[~detail["overall_pass"], ["failed_metrics", "num_failed_metrics"]].copy()
    if fail_df.empty:
        return pd.DataFrame([{
            "version": version_name,
            "failed_metrics": "NO_FAIL",
            "num_failed_metrics": 0,
            "fail_count": 0,
            "fail_pct_of_total_runs": 0.0,
            "fail_type": "none",
        }])

    grouped = fail_df.groupby(["failed_metrics", "num_failed_metrics"]).size().reset_index(name="fail_count")
    grouped["version"] = version_name
    grouped["fail_pct_of_total_runs"] = 100.0 * grouped["fail_count"] / len(detail)
    grouped["fail_type"] = grouped["num_failed_metrics"].apply(lambda x: "single" if x == 1 else "multi")
    cols = ["version", "failed_metrics", "num_failed_metrics", "fail_count", "fail_pct_of_total_runs", "fail_type"]
    return grouped[cols].sort_values(["fail_count", "num_failed_metrics"], ascending=[False, True]).reset_index(drop=True)


def build_near_fail_samples(detail: pd.DataFrame, specs: pd.DataFrame, version_name: str, n: int = 10) -> pd.DataFrame:
    metric_cols = specs["metric"].tolist()
    meta_cols = [c for c in ["run", "overall_pass", "worst_margin", "critical_metric"] if c in detail.columns]
    use_cols = meta_cols + metric_cols
    sort_cols = ["worst_margin"] + (["run"] if "run" in detail.columns else [])
    near_fail = detail.loc[detail["overall_pass"]].sort_values(sort_cols, ascending=True)[use_cols].head(n).copy()
    near_fail.insert(0, "version", version_name)
    return near_fail.reset_index(drop=True)


def build_worst_samples(detail: pd.DataFrame, specs: pd.DataFrame, version_name: str, n: int = 10) -> pd.DataFrame:
    metric_cols = specs["metric"].tolist()
    meta_cols = [c for c in ["run", "overall_pass", "worst_margin", "critical_metric", "failed_metrics", "num_failed_metrics"] if c in detail.columns]
    use_cols = meta_cols + metric_cols
    out = detail.sort_values(["overall_pass", "worst_margin"], ascending=[True, True])[use_cols].head(n).copy()
    out.insert(0, "version", version_name)
    return out.reset_index(drop=True)


def empirical_cdf(values):
    s = pd.Series(values).dropna().sort_values().to_list()
    if not s:
        return [], []
    y = [(i + 1) / len(s) for i in range(len(s))]
    return s, y


def plot_histogram(v1: pd.DataFrame, v2: pd.DataFrame, metric: str, rule_type: str, spec_value: float):
    plot_v1 = v1[metric].abs() if rule_type == "absmax" else v1[metric]
    plot_v2 = v2[metric].abs() if rule_type == "absmax" else v2[metric]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(plot_v1.dropna(), bins=24, alpha=0.6, label="v1")
    ax.hist(plot_v2.dropna(), bins=24, alpha=0.6, label="v2")
    ax.axvline(spec_value, linestyle="--", label="current spec")
    ax.set_title(f"Histogram - {metric}")
    ax.set_xlabel(metric)
    ax.set_ylabel("Count")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_cdf(v1: pd.DataFrame, v2: pd.DataFrame, metric: str, rule_type: str, spec_value: float):
    plot_v1 = v1[metric].abs() if rule_type == "absmax" else v1[metric]
    plot_v2 = v2[metric].abs() if rule_type == "absmax" else v2[metric]
    x1, y1 = empirical_cdf(plot_v1)
    x2, y2 = empirical_cdf(plot_v2)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x1, y1, label="v1")
    ax.plot(x2, y2, label="v2")
    ax.axvline(spec_value, linestyle="--", label="current spec")
    ax.set_title(f"CDF - {metric}")
    ax.set_xlabel(metric)
    ax.set_ylabel("Cumulative Probability")
    ax.legend()
    fig.tight_layout()
    return fig


def overall_compare_long(overall_v1: pd.DataFrame, overall_v2: pd.DataFrame) -> pd.DataFrame:
    row1 = overall_v1.iloc[0].to_dict()
    row2 = overall_v2.iloc[0].to_dict()
    fields = ["total_runs", "overall_pass_count", "overall_fail_count", "overall_yield_pct"]
    rows = []
    for field in fields:
        v1_val = row1.get(field, "")
        v2_val = row2.get(field, "")
        delta = ""
        if isinstance(v1_val, (int, float)) and isinstance(v2_val, (int, float)):
            delta = v2_val - v1_val
        rows.append({"field": field, "version_1": v1_val, "version_2": v2_val, "delta": delta})
    return pd.DataFrame(rows)


def metric_compare_long(metric_compare: pd.DataFrame) -> pd.DataFrame:
    stats = ["mean", "sigma", "min", "max", "pass_count", "fail_count", "yield_pct", "mean_minus_spec"]
    rows = []
    for _, row in metric_compare.iterrows():
        for stat in stats:
            rows.append({
                "metric": row["metric"],
                "display_name": row["display_name"],
                "statistic": stat,
                "version_1": row[f"{stat}_v1"],
                "version_2": row[f"{stat}_v2"],
                "delta": row[f"{stat}_delta_v2_minus_v1"],
            })
    return pd.DataFrame(rows)


def get_numeric_metric_df(detail: pd.DataFrame, active_specs: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [m for m in active_specs["metric"].tolist() if m in detail.columns]
    if not metric_cols:
        return pd.DataFrame()
    return detail[metric_cols].copy()


def plot_tradeoff_scatter(detail: pd.DataFrame, x_metric: str, y_metric: str):
    fig, ax = plt.subplots(figsize=(7, 5))
    pass_mask = detail["overall_pass"] if "overall_pass" in detail.columns else pd.Series([True] * len(detail), index=detail.index)
    fail_mask = ~pass_mask
    if pass_mask.any():
        ax.scatter(detail.loc[pass_mask, x_metric], detail.loc[pass_mask, y_metric], alpha=0.55, label="pass")
    if fail_mask.any():
        ax.scatter(detail.loc[fail_mask, x_metric], detail.loc[fail_mask, y_metric], alpha=0.85, label="fail")
    ax.set_xlabel(x_metric)
    ax.set_ylabel(y_metric)
    ax.set_title(f"Tradeoff Scatter: {y_metric} vs {x_metric}")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(corr_df: pd.DataFrame, title: str):
    fig, ax = plt.subplots(figsize=(7, 6))
    if corr_df.empty:
        ax.text(0.5, 0.5, "No numeric metrics available", ha="center", va="center")
        ax.set_axis_off()
        return fig
    im = ax.imshow(corr_df.values, aspect="auto")
    ax.set_xticks(range(len(corr_df.columns)))
    ax.set_xticklabels(corr_df.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr_df.index)))
    ax.set_yticklabels(corr_df.index)
    ax.set_title(title)
    for i in range(len(corr_df.index)):
        for j in range(len(corr_df.columns)):
            val = corr_df.iloc[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig


def fmt_value(val, decimals=2):
    if pd.isna(val):
        return "-"
    if isinstance(val, (int, float)):
        return f"{val:.{decimals}f}"
    return str(val)


def render_metric_card(label, value, note="", decimals=2):
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{fmt_value(value, decimals)}</div>
        <div class="metric-note">{note}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def build_summary_insights(overall_v1, overall_v2, fail_rank_v1, fail_rank_v2, near_fail_v1, near_fail_v2, metric_compare):
    lines = []
    y1 = float(overall_v1.iloc[0]["overall_yield_pct"])
    y2 = float(overall_v2.iloc[0]["overall_yield_pct"])
    delta = y2 - y1
    if delta > 0:
        lines.append(f"v2 overall yield is higher than v1 by {delta:.1f}%p.")
    elif delta < 0:
        lines.append(f"v2 overall yield is lower than v1 by {abs(delta):.1f}%p.")
    else:
        lines.append("v1 and v2 have the same overall yield.")

    if not fail_rank_v1.empty:
        lines.append(f"Top fail metric in v1 is {fail_rank_v1.iloc[0]['metric']}.")
    if not fail_rank_v2.empty:
        lines.append(f"Top fail metric in v2 is {fail_rank_v2.iloc[0]['metric']}.")

    if not near_fail_v1.empty and "critical_metric" in near_fail_v1.columns:
        nf1 = near_fail_v1["critical_metric"].value_counts().idxmax()
        lines.append(f"Near-fail samples in v1 are dominated by {nf1}.")
    if not near_fail_v2.empty and "critical_metric" in near_fail_v2.columns:
        nf2 = near_fail_v2["critical_metric"].value_counts().idxmax()
        lines.append(f"Near-fail samples in v2 are dominated by {nf2}.")

    if not metric_compare.empty:
        best = metric_compare.sort_values("yield_pct_delta_v2_minus_v1", ascending=False).iloc[0]
        worst = metric_compare.sort_values("yield_pct_delta_v2_minus_v1", ascending=True).iloc[0]
        lines.append(f"Biggest yield improvement in v2 comes from {best['metric']} ({best['yield_pct_delta_v2_minus_v1']:.1f}%p).")
        lines.append(f"Largest yield degradation in v2 comes from {worst['metric']} ({worst['yield_pct_delta_v2_minus_v1']:.1f}%p).")
    return lines


def build_spec_sensitivity(detail: pd.DataFrame, specs: pd.DataFrame, version_name: str, step_pct: float = 2.0) -> pd.DataFrame:
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

        spec_up = spec_value * (1.0 + step_pct / 100.0)
        spec_down = spec_value * (1.0 - step_pct / 100.0)

        temp = detail.copy()

        def overall_yield_for_changed_spec(changed_spec):
            pass_df = pd.DataFrame(index=temp.index)
            for _, s in active_specs.iterrows():
                m = s["metric"]
                rt = s["rule_type"]
                sv = float(s["spec_value"])
                if m == metric:
                    sv = changed_spec
                pass_df[m] = evaluate_metric(temp[m], rt, sv)
            return 100.0 * pass_df.all(axis=1).mean()

        yield_up = overall_yield_for_changed_spec(spec_up)
        yield_down = overall_yield_for_changed_spec(spec_down)

        rows.append({
            "version": version_name,
            "metric": metric,
            "display_name": spec["display_name"],
            "rule_type": rule_type,
            "current_spec": spec_value,
            "base_overall_yield_pct": base_yield,
            f"yield_if_spec_plus_{step_pct:.0f}pct": yield_up,
            f"yield_if_spec_minus_{step_pct:.0f}pct": yield_down,
            "max_abs_yield_shift_pctp": max(abs(yield_up - base_yield), abs(yield_down - base_yield)),
        })
    return pd.DataFrame(rows).sort_values("max_abs_yield_shift_pctp", ascending=False).reset_index(drop=True)


def plot_metric_margin_bar(summary: pd.DataFrame, title: str):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(summary["metric"], summary["mean_minus_spec"])
    ax.set_title(title)
    ax.set_ylabel("Mean margin vs spec")
    ax.set_xlabel("Metric")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def plot_near_fail_critical_bar(near_fail: pd.DataFrame, title: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    if near_fail.empty or "critical_metric" not in near_fail.columns:
        ax.text(0.5, 0.5, "No near-fail data", ha="center", va="center")
        ax.set_axis_off()
        return fig
    counts = near_fail["critical_metric"].value_counts()
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel("Critical metric")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


st.markdown(
    """
    <div class="app-hero">
        <div class="hero-top">
            <div class="logo-badge"><span class="logo-dot"></span>SK hynix-style review UI</div>
            <div>
                <h1 class="hero-title">Monte Carlo Review Dashboard</h1>
                <p class="hero-sub">Readable review layout for version comparison, failure analysis, near-fail tracking, tradeoff inspection, and sensitivity review.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="sidebar-title">Dashboard Controls</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    st.markdown('<hr class="soft" />', unsafe_allow_html=True)
    st.markdown("**Display options**")
    top_n = st.slider("Rows for near-fail / worst", min_value=5, max_value=30, value=10, step=1)
    sensitivity_step = st.slider("Spec sensitivity step (%)", min_value=1.0, max_value=10.0, value=2.0, step=1.0)
    show_raw = st.checkbox("Show raw data tables", value=False)
    st.markdown(
        """
        <div class="note-box">
        Use an Excel file with <b>MC_v1</b> and <b>MC_v2</b>. 
        <b>Specs</b> is optional and can be edited below in the main view.
        </div>
        """,
        unsafe_allow_html=True,
    )

if uploaded_file is None:
    st.info("Upload an Excel workbook from the left sidebar to begin.")
    st.stop()

try:
    specs_from_file, v1, v2 = load_workbook(uploaded_file)
    specs_base = normalize_specs(specs_from_file, v1, v2)
except Exception as e:
    st.error(f"Failed to read workbook: {e}")
    st.stop()

st.markdown('<div class="section-title">Fixed Review Condition</div>', unsafe_allow_html=True)
pvt_col1, pvt_col2, pvt_col3 = st.columns(3)
fixed_corner = v1["corner"].iloc[0] if "corner" in v1.columns and len(v1) else "-"
fixed_temp = v1["temp_C"].iloc[0] if "temp_C" in v1.columns and len(v1) else "-"
fixed_vdd = v1["vdd_V"].iloc[0] if "vdd_V" in v1.columns and len(v1) else "-"
with pvt_col1:
    render_metric_card("Corner", fixed_corner, "Fixed Monte Carlo review condition.", decimals=0)
with pvt_col2:
    render_metric_card("Temperature (°C)", fixed_temp, "Applied to all runs in this file.", decimals=0)
with pvt_col3:
    render_metric_card("VDD (V)", fixed_vdd, "Applied to all runs in this file.", decimals=2)

st.markdown('<div class="section-title">Spec Settings</div>', unsafe_allow_html=True)
spec_panel_col1, spec_panel_col2 = st.columns([3, 1])

with spec_panel_col1:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    spec_editor = specs_base.copy()
    spec_editor["enabled"] = spec_editor["enabled"].astype(str).str.upper().map(lambda x: True if x == "Y" else False)
    edited_specs = st.data_editor(
        spec_editor,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "metric": st.column_config.TextColumn("metric"),
            "display_name": st.column_config.TextColumn("display_name"),
            "rule_type": st.column_config.SelectboxColumn("rule_type", options=["min", "max", "absmax"]),
            "spec_value": st.column_config.NumberColumn("spec_value", format="%.4f"),
            "unit": st.column_config.TextColumn("unit"),
            "enabled": st.column_config.CheckboxColumn("enabled"),
        },
        key="spec_editor",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with spec_panel_col2:
    enabled_count = int(specs_base["enabled"].astype(str).str.upper().eq("Y").sum()) if "enabled" in specs_base.columns else len(specs_base)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="small-tag">SPEC STATUS</div>', unsafe_allow_html=True)
    render_metric_card("Metrics in sheet", len(specs_base), "Loaded from workbook or auto-generated.", decimals=0)
    render_metric_card("Enabled metrics", enabled_count, "Only enabled specs are used in overall pass.", decimals=0)
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
overall_compare = overall_compare_long(overall_v1, overall_v2)
fail_rank_v1 = build_fail_ranking(detail_v1, active_specs_v1, "v1")
fail_rank_v2 = build_fail_ranking(detail_v2, active_specs_v2, "v2")
fail_decomp_v1 = build_fail_decomposition(detail_v1, "v1")
fail_decomp_v2 = build_fail_decomposition(detail_v2, "v2")
near_fail_v1 = build_near_fail_samples(detail_v1, active_specs_v1, "v1", n=top_n)
near_fail_v2 = build_near_fail_samples(detail_v2, active_specs_v2, "v2", n=top_n)
worst_v1 = build_worst_samples(detail_v1, active_specs_v1, "v1", n=top_n)
worst_v2 = build_worst_samples(detail_v2, active_specs_v2, "v2", n=top_n)

sensitivity_v1 = build_spec_sensitivity(detail_v1, edited_specs, "v1", step_pct=sensitivity_step)
sensitivity_v2 = build_spec_sensitivity(detail_v2, edited_specs, "v2", step_pct=sensitivity_step)

summary_lines = build_summary_insights(overall_v1, overall_v2, fail_rank_v1, fail_rank_v2, near_fail_v1, near_fail_v2, metric_compare)

tab_exec, tab_summary, tab_compare, tab_sensitivity, tab_nearviz, tab_fail, tab_near, tab_tradeoff, tab_charts, tab_raw = st.tabs(
    ["Executive Summary", "Summary", "Compare", "Spec Sensitivity", "Near-Fail Visualization", "Fail Analysis", "Near-Fail / Worst", "Correlation / Tradeoff", "Charts", "Raw Data"]
)

with tab_exec:
    st.markdown('<div class="section-title">Executive Review Summary</div>', unsafe_allow_html=True)
    items = "".join([f"<li>{line}</li>" for line in summary_lines])
    st.markdown(f'<div class="summary-box"><div class="summary-title">Key findings</div><ul class="summary-list">{items}</ul></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("v1 overall yield (%)", overall_v1.iloc[0]["overall_yield_pct"], "Current enabled-spec result.", decimals=1)
    with c2:
        render_metric_card("v2 overall yield (%)", overall_v2.iloc[0]["overall_yield_pct"], "Current enabled-spec result.", decimals=1)
    with c3:
        render_metric_card("Yield delta (v2-v1)", overall_v2.iloc[0]["overall_yield_pct"] - overall_v1.iloc[0]["overall_yield_pct"], "Positive means v2 improved.", decimals=1)

    c4, c5 = st.columns(2)
    with c4:
        st.markdown('<div class="panel-card"><div class="small-tag">Top sensitivity - v1</div>', unsafe_allow_html=True)
        st.dataframe(sensitivity_v1.head(5), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c5:
        st.markdown('<div class="panel-card"><div class="small-tag">Top sensitivity - v2</div>', unsafe_allow_html=True)
        st.dataframe(sensitivity_v2.head(5), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_summary:
    st.markdown('<div class="section-title">Overall Summary</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(overall_v1.drop(columns=[c for c in ["fixed_corner", "fixed_temp_C", "fixed_vdd_V"] if c in overall_v1.columns]), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(overall_v2.drop(columns=[c for c in ["fixed_corner", "fixed_temp_C", "fixed_vdd_V"] if c in overall_v2.columns]), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Metric Summary</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(summary_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(summary_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_compare:
    st.markdown('<div class="section-title">Overall Compare</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.dataframe(overall_compare, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Metric Compare</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.dataframe(metric_compare_long(metric_compare), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_sensitivity:
    st.markdown('<div class="section-title">Spec Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="note-box">Each enabled spec is perturbed by ±{sensitivity_step:.0f}% while others are fixed. '
        'The table shows how much overall yield shifts. Larger shift means that spec is more yield-sensitive.</div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(sensitivity_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(sensitivity_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_nearviz:
    st.markdown('<div class="section-title">Near-Fail Visualization</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card"><div class="small-tag">Near-fail critical metric mix - v1</div>', unsafe_allow_html=True)
        fig_nf1 = plot_near_fail_critical_bar(near_fail_v1, "Near-fail critical metric mix - v1")
        st.pyplot(fig_nf1)
        plt.close(fig_nf1)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card"><div class="small-tag">Near-fail critical metric mix - v2</div>', unsafe_allow_html=True)
        fig_nf2 = plot_near_fail_critical_bar(near_fail_v2, "Near-fail critical metric mix - v2")
        st.pyplot(fig_nf2)
        plt.close(fig_nf2)
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel-card"><div class="small-tag">Mean margin by metric - v1</div>', unsafe_allow_html=True)
        fig_m1 = plot_metric_margin_bar(summary_v1, "Mean margin by metric - v1")
        st.pyplot(fig_m1)
        plt.close(fig_m1)
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="panel-card"><div class="small-tag">Mean margin by metric - v2</div>', unsafe_allow_html=True)
        fig_m2 = plot_metric_margin_bar(summary_v2, "Mean margin by metric - v2")
        st.pyplot(fig_m2)
        plt.close(fig_m2)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_fail:
    st.markdown('<div class="section-title">Fail Ranking</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(fail_rank_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(fail_rank_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Fail Decomposition</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(fail_decomp_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(fail_decomp_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_near:
    st.markdown('<div class="section-title">Near-Fail Samples</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(near_fail_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(near_fail_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Worst Samples</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 1</div>', unsafe_allow_html=True)
        st.dataframe(worst_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="panel-card"><div class="small-tag">VERSION 2</div>', unsafe_allow_html=True)
        st.dataframe(worst_v2, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_tradeoff:
    st.markdown('<div class="section-title">Correlation / Tradeoff Analysis</div>', unsafe_allow_html=True)
    control_left, control_right = st.columns([1, 2])
    with control_left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        selected_version = st.radio("Select version", ["v1", "v2"], horizontal=True)
        selected_detail = detail_v1 if selected_version == "v1" else detail_v2
        selected_specs = active_specs_v1 if selected_version == "v1" else active_specs_v2
        metric_df = get_numeric_metric_df(selected_detail, selected_specs)
        corr_df = metric_df.corr() if not metric_df.empty else pd.DataFrame()
        metric_options = metric_df.columns.tolist()
        if metric_options:
            x_metric = st.selectbox("X metric", metric_options, index=0)
            y_metric = st.selectbox("Y metric", metric_options, index=1 if len(metric_options) > 1 else 0)
        else:
            x_metric = None
            y_metric = None
            st.warning("No numeric metrics available.")
        st.markdown("</div>", unsafe_allow_html=True)
    with control_right:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.dataframe(corr_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if metric_options and x_metric is not None and y_metric is not None:
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            fig_scatter = plot_tradeoff_scatter(selected_detail, x_metric, y_metric)
            st.pyplot(fig_scatter)
            plt.close(fig_scatter)
            st.markdown("</div>", unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            fig_heatmap = plot_correlation_heatmap(corr_df, f"Correlation Heatmap - {selected_version}")
            st.pyplot(fig_heatmap)
            plt.close(fig_heatmap)
            st.markdown("</div>", unsafe_allow_html=True)

with tab_charts:
    st.markdown('<div class="section-title">Distribution Charts</div>', unsafe_allow_html=True)
    active_metric_options = active_specs_v1["metric"].tolist()
    selected_metric = st.selectbox("Select metric", active_metric_options)
    spec_row = active_specs_v1.loc[active_specs_v1["metric"] == selected_metric].iloc[0]
    rule_type = spec_row["rule_type"]
    spec_value = float(spec_row["spec_value"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        fig1 = plot_histogram(v1, v2, selected_metric, rule_type, spec_value)
        st.pyplot(fig1)
        plt.close(fig1)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        fig2 = plot_cdf(v1, v2, selected_metric, rule_type, spec_value)
        st.pyplot(fig2)
        plt.close(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_raw:
    if not show_raw:
        st.info("Enable 'Show raw data tables' from the sidebar to view raw tables here.")
    else:
        st.markdown('<div class="section-title">Active Specs</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.dataframe(active_specs_v1, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Raw Data - MC_v1</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.dataframe(v1.drop(columns=[c for c in ["corner", "temp_C", "vdd_V"] if c in v1.columns]), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Raw Data - MC_v2</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.dataframe(v2.drop(columns=[c for c in ["corner", "temp_C", "vdd_V"] if c in v2.columns]), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
