#!/usr/bin/env python3
"""Generates comprehensive scientific publication deliverables for SOTA Council Study.

Inputs:
- curated_benchmark_results/trials_raw_curated_21targets.csv (Baseline & Council Standard)
- curated_benchmark_results/sota_council_results/trials_raw_sota_21targets.csv (Council SOTA)
- curated_benchmark_results/mutation_results/mutation_scores_21targets.csv (Mutation Testing)

Outputs:
- statistical_summary_sota_3way.csv
- table_sota_3way_comparison.tex (escaped LaTeX)
- table_mutation_scores.tex (escaped LaTeX)
- Publication charts (300 DPI PNG + vector SVG)
"""

import csv
import json
import math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "curated_benchmark_results" / "sota_council_results"
MUT_DIR = BASE_DIR / "curated_benchmark_results" / "mutation_results"
CURATED_CSV = BASE_DIR / "curated_benchmark_results" / "trials_raw_curated_21targets.csv"
SOTA_CSV = OUT_DIR / "trials_raw_sota_21targets.csv"
MUTATION_CSV = MUT_DIR / "mutation_scores_21targets.csv"

def escape_latex(s: str) -> str:
    return str(s).replace("_", "\\_").replace("&", "\\&").replace("%", "\\%")

def build_summary():
    # 1. Load curated baseline & council standard
    trials = []
    with open(CURATED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            trials.append(r)

    # 2. Load council sota
    with open(SOTA_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            trials.append(r)

    # Group by target_id and arm
    from collections import defaultdict
    grouped = defaultdict(lambda: defaultdict(list))
    for t in trials:
        tid = t["target_id"]
        arm = t["arm"]
        grouped[tid][arm].append(t)

    # 3. Load mutation scores
    mut_scores = {}
    if MUTATION_CSV.exists():
        with open(MUTATION_CSV, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                mut_scores[r["target_id"]] = {
                    "total": int(r["mutants_total"]),
                    "killed": int(r["mutants_killed"]),
                    "survived": int(r["mutants_survived"]),
                    "score": float(r["mutation_score_pct"])
                }

    summary_rows = []
    for tid, arms in sorted(grouped.items()):
        base_runs = arms.get("baseline", [])
        std_runs = arms.get("council_enhanced", [])
        sota_runs = arms.get("council_sota", [])

        def stats_for(runs):
            if not runs:
                return {"pass_rate": 0.0, "line_mean": 0.0, "line_std": 0.0, "branch_mean": 0.0, "repairs": 0}
            passes = sum(1 for r in runs if str(r.get("final_pass")).lower() == "true")
            pass_rate = round(passes / len(runs) * 100.0, 1)
            line_vals = [float(r.get("line_pct", 0.0) or 0.0) for r in runs]
            branch_vals = [float(r.get("branch_pct", 0.0) or 0.0) for r in runs]
            repairs = sum(1 for r in runs if str(r.get("repaired_by_critic")).lower() == "true")
            l_mean = round(float(np.mean(line_vals)), 2)
            l_std = round(float(np.std(line_vals, ddof=1)), 2) if len(runs) > 1 else 0.0
            b_mean = round(float(np.mean(branch_vals)), 2)
            return {
                "pass_rate": pass_rate,
                "line_mean": l_mean,
                "line_std": l_std,
                "branch_mean": b_mean,
                "repairs": repairs,
                "line_vals": line_vals,
                "project": runs[0].get("project", ""),
                "category": runs[0].get("category", "")
            }

        b_stat = stats_for(base_runs)
        c_stat = stats_for(std_runs)
        s_stat = stats_for(sota_runs)
        m_info = mut_scores.get(tid, {"score": 0.0, "killed": 0, "total": 0})

        summary_rows.append({
            "target_id": tid,
            "project": s_stat.get("project") or c_stat.get("project"),
            "category": s_stat.get("category") or c_stat.get("category"),
            "base_pass": b_stat["pass_rate"],
            "base_line": b_stat["line_mean"],
            "std_pass": c_stat["pass_rate"],
            "std_line": c_stat["line_mean"],
            "sota_pass": s_stat["pass_rate"],
            "sota_line": s_stat["line_mean"],
            "sota_repairs": s_stat["repairs"],
            "mut_score": m_info["score"],
            "mut_killed": m_info["killed"],
            "mut_total": m_info["total"]
        })

    # Save summary CSV
    sum_csv = OUT_DIR / "statistical_summary_sota_3way.csv"
    with open(sum_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)

    print(f"[+] Saved 3-way summary to {sum_csv}")

    # Build LaTeX Table
    tex_path = OUT_DIR / "table_sota_3way_comparison.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Auto-generated by generate_sota_publication_artifacts.py\n")
        f.write("\\begin{table*}[t]\n\\centering\n\\small\n")
        f.write("\\caption{Three-Way Empirical Comparison on 21 Curated Test4Py Targets ($N=5$ seeds per arm). Council SOTA combines Symbol-Table Grounding, Two-Round Adaptive Critic Repair, and Mutation Oracle Hardening.}\n")
        f.write("\\label{tab:sota_3way_comparison}\n")
        f.write("\\begin{tabular}{ll|rr|rr|rrr|r}\n\\hline\n")
        f.write("\\textbf{Target ID} & \\textbf{Project} & \\multicolumn{2}{c|}{\\textbf{Baseline}} & \\multicolumn{2}{c|}{\\textbf{Council Std}} & \\multicolumn{3}{c|}{\\textbf{Council SOTA}} & \\textbf{Mut. Score} \\\\\n")
        f.write(" & & Pass\\% & Cov\\% & Pass\\% & Cov\\% & Pass\\% & Cov\\% & Rep. & Kill\\% \\\\\n\\hline\n")

        for r in summary_rows:
            tid_esc = escape_latex(r["target_id"])
            proj_esc = escape_latex(r["project"])
            f.write(f"\\texttt{{{tid_esc}}} & {proj_esc} & {r['base_pass']:.1f} & {r['base_line']:.1f} & {r['std_pass']:.1f} & {r['std_line']:.1f} & \\textbf{{{r['sota_pass']:.1f}}} & \\textbf{{{r['sota_line']:.1f}}} & {r['sota_repairs']} & {r['mut_score']:.1f}\\% \\\\\n")

        # Means
        b_p_mean = np.mean([r["base_pass"] for r in summary_rows])
        b_c_mean = np.mean([r["base_line"] for r in summary_rows])
        s_p_mean = np.mean([r["std_pass"] for r in summary_rows])
        s_c_mean = np.mean([r["std_line"] for r in summary_rows])
        o_p_mean = np.mean([r["sota_pass"] for r in summary_rows])
        o_c_mean = np.mean([r["sota_line"] for r in summary_rows])
        tot_rep = sum(r["sota_repairs"] for r in summary_rows)
        m_mean = np.mean([r["mut_score"] for r in summary_rows])

        f.write("\\hline\n")
        f.write(f"\\textbf{{Overall Mean}} & \\textbf{{21 Targets}} & \\textbf{{{b_p_mean:.1f}}} & \\textbf{{{b_c_mean:.1f}}} & \\textbf{{{s_p_mean:.1f}}} & \\textbf{{{s_c_mean:.1f}}} & \\textbf{{{o_p_mean:.1f}}} & \\textbf{{{o_c_mean:.1f}}} & \\textbf{{{tot_rep}}} & \\textbf{{{m_mean:.1f}}}\\% \\\\\n")
        f.write("\\hline\n\\end{tabular}\n\\end{table*}\n")

    print(f"[+] Saved LaTeX table to {tex_path}")

    # Build Charts
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. 3-Way Pass Rate Chart
    fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
    x = np.arange(len(summary_rows))
    width = 0.25
    rects1 = ax.bar(x - width, [r["base_pass"] for r in summary_rows], width, label="Baseline (Zero-Shot)", color="#9e9e9e", alpha=0.9)
    rects2 = ax.bar(x, [r["std_pass"] for r in summary_rows], width, label="Council Standard (1-R Critic)", color="#1976d2", alpha=0.9)
    rects3 = ax.bar(x + width, [r["sota_pass"] for r in summary_rows], width, label="Council SOTA (Grounding + 2-R Critic)", color="#2e7d32", alpha=0.9)

    ax.set_ylabel("Pass Rate (%)", fontsize=11, fontweight="bold")
    ax.set_title("Pass Rate Progression Across 21 Curated Benchmark Targets (N=5 Seeds)", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([r["target_id"] for r in summary_rows], rotation=45, ha="right", fontsize=9)
    ax.legend(loc="upper right", frameon=True)
    ax.set_ylim(0, 115)
    plt.tight_layout()
    chart1_png = OUT_DIR / "chart_sota_3way_pass_rate.png"
    chart1_svg = OUT_DIR / "chart_sota_3way_pass_rate.svg"
    plt.savefig(chart1_png, dpi=300)
    plt.savefig(chart1_svg)
    plt.close()

    # 2. 3-Way Line Coverage Chart
    fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
    rects1 = ax.bar(x - width, [r["base_line"] for r in summary_rows], width, label="Baseline", color="#9e9e9e", alpha=0.9)
    rects2 = ax.bar(x, [r["std_line"] for r in summary_rows], width, label="Council Standard", color="#0288d1", alpha=0.9)
    rects3 = ax.bar(x + width, [r["sota_line"] for r in summary_rows], width, label="Council SOTA", color="#388e3c", alpha=0.9)

    ax.set_ylabel("Line Coverage (%)", fontsize=11, fontweight="bold")
    ax.set_title("Line Coverage Progression Across 21 Targets (N=5 Seeds)", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([r["target_id"] for r in summary_rows], rotation=45, ha="right", fontsize=9)
    ax.legend(loc="upper right", frameon=True)
    ax.set_ylim(0, 105)
    plt.tight_layout()
    chart2_png = OUT_DIR / "chart_sota_3way_coverage.png"
    chart2_svg = OUT_DIR / "chart_sota_3way_coverage.svg"
    plt.savefig(chart2_png, dpi=300)
    plt.savefig(chart2_svg)
    plt.close()

    # 3. Mutation Score Distribution Chart
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    mut_vals = [r["mut_score"] for r in summary_rows]
    colors = ["#2e7d32" if v >= 70 else ("#f57c00" if v >= 30 else "#d32f2f") for v in mut_vals]
    ax.bar(x, mut_vals, color=colors, alpha=0.85, edgecolor="#333", width=0.6)
    ax.axhline(y=37.97, color="#1976d2", linestyle="--", linewidth=1.5, label="Council Overall Mean (37.97%)")
    ax.axhline(y=84.3, color="#d32f2f", linestyle=":", linewidth=1.5, label="Test4Py Paper Score (84.30%)")
    ax.set_ylabel("Mutation Score / Kill Rate (%)", fontsize=11, fontweight="bold")
    ax.set_title("Mutation Testing Fault Detection Rates across 21 Curated Golden Suites", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([r["target_id"] for r in summary_rows], rotation=45, ha="right", fontsize=9)
    ax.legend(loc="upper right", frameon=True)
    ax.set_ylim(0, 115)
    plt.tight_layout()
    chart3_png = OUT_DIR / "chart_mutation_score_distribution.png"
    chart3_svg = OUT_DIR / "chart_mutation_score_distribution.svg"
    plt.savefig(chart3_png, dpi=300)
    plt.savefig(chart3_svg)
    plt.close()

    print(f"[+] Saved charts to {OUT_DIR}")

if __name__ == "__main__":
    build_summary()
