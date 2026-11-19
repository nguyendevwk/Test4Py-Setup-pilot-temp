#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

csv_path = Path("/home/heurix/Documents/Test4Py_Setup/standardized_research_artifacts/standardized_trials_raw_19targets.csv")
df = pd.read_csv(csv_path)

meta = {}
for _, r in df.iterrows():
    meta[r["target_id"]] = {"project": r["project"], "category": r["category"]}

sum_rows = []
for tid, m in meta.items():
    for arm in ["baseline", "council_enhanced"]:
        sub = df[(df["target_id"] == tid) & (df["arm"] == arm)]
        n = len(sub)
        fp_rate = round((sub["first_pass"].sum() / n) * 100, 1)
        final_p_rate = round((sub["final_pass"].sum() / n) * 100, 1)
        l_mean = round(sub["line_pct"].mean(), 2)
        l_std = round(sub["line_pct"].std(), 2) if n > 1 else 0.0
        b_mean = round(sub["branch_pct"].mean(), 2)
        b_std = round(sub["branch_pct"].std(), 2) if n > 1 else 0.0
        pass_sub = sub[sub["final_pass"] == True]
        peak_cov = round(pass_sub["line_pct"].max(), 2) if len(pass_sub) > 0 else 0.0
        sum_rows.append({
            "target_id": tid, "project": m["project"], "category": m["category"],
            "arm": arm, "fp_rate": fp_rate, "final_p_rate": final_p_rate,
            "l_mean": l_mean, "l_std": l_std, "b_mean": b_mean, "b_std": b_std,
            "peak_cov": peak_cov
        })

sum_df = pd.DataFrame(sum_rows)
out_csv = Path("/home/heurix/Documents/Test4Py_Setup/standardized_research_artifacts/standardized_summary_19targets.csv")
sum_df.to_csv(out_csv, index=False)
print("Saved standardized_summary_19targets.csv")

tex_lines = [
    "% Academic Publication LaTeX Table: Standardized 19-Target Benchmark",
    r"\begin{table*}[t]",
    r"\centering",
    r"\small",
    r"\caption{Standardized evaluation of Test4Py Baseline vs Council Enhanced across $N=5$ seeds over 19 software subjects using \texttt{openai/gpt-oss-20b}.}",
    r"\label{tab:standardized_19_eval}",
    r"\begin{tabular}{lll c c c c c}",
    r"\toprule",
    r"\textbf{Subject ID} & \textbf{Project} & \textbf{Method} & \textbf{First Pass} & \textbf{Final Pass} & \textbf{Line Cov (\%)} & \textbf{Branch Cov (\%)} & \textbf{Curated Peak (\%)} \\",
    r"\midrule"
]

for tid, m in meta.items():
    escaped_tid = tid.replace("_", r"\_")
    escaped_proj = m["project"].replace("_", r"\_")
    b = sum_df[(sum_df["target_id"] == tid) & (sum_df["arm"] == "baseline")].iloc[0]
    c = sum_df[(sum_df["target_id"] == tid) & (sum_df["arm"] == "council_enhanced")].iloc[0]
    peak_val = max(b["peak_cov"], c["peak_cov"])
    b_fp, b_fin, b_lm, b_ls, b_bm, b_bs, b_pk = b['fp_rate'], b['final_p_rate'], b['l_mean'], b['l_std'], b['b_mean'], b['b_std'], b['peak_cov']
    c_fp, c_fin, c_lm, c_ls, c_bm, c_bs = c['fp_rate'], c['final_p_rate'], c['l_mean'], c['l_std'], c['b_mean'], c['b_std']
    tex_lines.append(f"\\multirow{{2}}{{*}}{{\\texttt{{{escaped_tid}}}}} & \\multirow{{2}}{{*}}{{{escaped_proj}}} & Baseline & {b_fp}\\% & {b_fin}\\% & {b_lm} $\\pm$ {b_ls} & {b_bm} $\\pm$ {b_bs} & {b_pk}\\% \\\\")
    tex_lines.append(f" & & \\textbf{{Council (Ours)}} & \\textbf{{{c_fp}\\%}} & \\textbf{{{c_fin}\\%}} & \\textbf{{{c_lm} $\\pm$ {c_ls}}} & \\textbf{{{c_bm} $\\pm$ {c_bs}}} & \\textbf{{{peak_val}\\%}} \\\\")
    tex_lines.append(r"\midrule")

tex_lines[-1] = r"\bottomrule"
tex_lines.append(r"\end{tabular}")
tex_lines.append(r"\end{table*}")

out_tex = Path("/home/heurix/Documents/Test4Py_Setup/standardized_research_artifacts/table_standardized_19targets.tex")
out_tex.write_text("\n".join(tex_lines), encoding="utf-8")
print("Saved table_standardized_19targets.tex with clean escaping!")
