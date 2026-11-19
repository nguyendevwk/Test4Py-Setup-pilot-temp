#!/usr/bin/env python3
"""Comprehensive Benchmark & Ablation Study for Test4Py Paper.

Evaluates 4 configurations on the curated Test4Py paper benchmark targets:
1. Full Method (Council Enhanced): State Grounding + Auto-Import + Critic Repair
2. w/o Critic: Single-pass Coder with State Grounding & Auto-Import (First Pass)
3. w/o State Grounding: Baseline API-only prompting (no setup hint or dependency context)
4. w/o Auto-Import: Generated test executed raw without deterministic AST import resolver
"""
import ast
import csv
import json
import os
import shutil
import time
from pathlib import Path

from council.groq_engine import GroqCouncilEngine
from pilot.multitarget import clean_code_block, execute_pytest_and_coverage, inspect_api
from pilot.grounding import dependency_context
from council.generator import auto_resolve_imports
from council.critic import audit_test_quality
from council.runner import repair_audit
from council_multitarget import extract_target_source, OUTPUT_RULES

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "local_benchmark_repos"
OUT_DIR = BASE_DIR / "paper_ablation_results"

PAPER_TARGETS = [
    {
        "id": "genty_repeat",
        "project": "genty",
        "category": "Decorator / Param",
        "module": "genty.genty_repeat",
        "file": "genty/genty_repeat.py",
        "symbol": "genty_repeat",
        "setup_hint": "from genty.genty_repeat import genty_repeat\ncount = 3\ndec = genty_repeat(count)"
    },
    {
        "id": "codetiming_timer",
        "project": "codetiming",
        "category": "Context Manager",
        "module": "codetiming._timer",
        "file": "codetiming/_timer.py",
        "symbol": "Timer",
        "setup_hint": "from codetiming import Timer\nt = Timer(name='perf', text='Elapsed: {:0.4f}s')\nt.start()"
    },
    {
        "id": "docstring_parser_parse",
        "project": "docstring_parser",
        "category": "Type-rich AST",
        "module": "docstring_parser.parser",
        "file": "docstring_parser/parser.py",
        "symbol": "parse",
        "setup_hint": 'sample_doc = """Summary line.\n\n:param name: param desc\n:type name: str\n:returns: return desc\n"""'
    },
    {
        "id": "woa_whale_opt",
        "project": "woa",
        "category": "Numerical Optimization",
        "module": "src.whale_optimization",
        "file": "src/whale_optimization.py",
        "symbol": "WhaleOptimization",
        "setup_hint": "from src.whale_optimization import WhaleOptimization\nopt_func = lambda x, y: x**2 + y**2\nconstraints = [(-5, 5), (-5, 5)]\nwoa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)"
    },
    {
        "id": "superstring",
        "project": "superstring.py",
        "category": "Data Structure",
        "module": "superstring.superstring",
        "file": "superstring/superstring.py",
        "symbol": "SuperString",
        "setup_hint": "from superstring.superstring import SuperString\ns = SuperString('Test String For Python Testing')\n# Methods return SuperString instances or standard types"
    },
    {
        "id": "typesystem_schema",
        "project": "typesystem",
        "category": "Schema Validation",
        "module": "typesystem.schemas",
        "file": "typesystem/schemas.py",
        "symbol": "Schema",
        "setup_hint": "from typesystem.schemas import Schema\nfrom typesystem.fields import String, Integer\nschema = Schema(fields={'username': String(max_length=50), 'age': Integer()})\n# Usage: valid_data = schema.validate({'username': 'alice', 'age': 30})"
    }
]

def evaluate_configuration(target, config_name, engine, target_dir):
    repo_root = REPOS_DIR / target["project"]
    sample_dir = target_dir / config_name
    if sample_dir.exists():
        shutil.rmtree(sample_dir)
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    root = sample_dir / "product"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(repo_root, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    
    info = extract_target_source(root / target["file"], target["symbol"])
    api = inspect_api(root, target["module"], target["symbol"])
    
    # 1. State Grounding ablation control
    use_grounding = (config_name != "no_grounding")
    setup = target.get("setup_hint", "") if use_grounding else ""
    dependencies = dependency_context(root, target["file"], target["symbol"]) if use_grounding else None
    
    prompt_api = dict(api, file=target["file"])
    context = (f"Target source:\n{info['source']}\nModule: {target['module']}\nSymbol: {target['symbol']}\n"
               + "Runtime API inventory:\n" + json.dumps(prompt_api, indent=2)
               + ("\nProduction dependency source:\n" + json.dumps(dependencies["snippets"], indent=2) if dependencies else "")
               + ("\nCurated setup example:\n" + setup if setup else ""))
    
    sys_prompt = "Generate rigorous Python unit tests.\n" + OUTPUT_RULES
    raw = engine.call_coder(sys_prompt, context)
    
    initial_clean = None
    try:
        initial_clean = clean_code_block(raw)
    except Exception:
        pass
        
    if initial_clean is None:
        return {
            "target": target["id"],
            "config": config_name,
            "pass": False,
            "line_cov": 0.0,
            "branch_cov": 0.0,
            "status": "extraction_error",
            "first_pass": False
        }
        
    # 2. Auto-import resolver ablation control
    use_auto_import = (config_name != "no_auto_import")
    test_code = auto_resolve_imports(initial_clean, target["module"], info["source"]) if use_auto_import else initial_clean
    
    first_eval = execute_pytest_and_coverage(test_code, root, target["module"], sample_dir / "first_run")
    first_pass = bool(first_eval.get("suite_pass"))
    
    final_pass = first_pass
    final_eval = first_eval
    
    # 3. Critic Repair ablation control
    use_critic = (config_name in ("full_method", "no_grounding", "no_auto_import"))
    if not first_pass and use_critic:
        rep_report = sample_dir / "first_run" / "pytest_report.json"
        diagnostics = rep_report.read_text()[:4000] if rep_report.exists() else "Test failed."
        rep_prompt = (context + "\nCandidate:\n" + test_code + "\nDiagnostics:\n" + diagnostics)
        repair_raw = engine.call_critic(
            "Repair imports, setup or syntax while preserving every test and assertion expression.\n" + OUTPUT_RULES,
            rep_prompt
        )
        try:
            repaired = clean_code_block(repair_raw)
            if use_auto_import:
                repaired = auto_resolve_imports(repaired, target["module"], info["source"])
            audit = repair_audit(test_code, repaired)
            if audit["accepted"] and not audit["review_required"]:
                rep_eval = execute_pytest_and_coverage(repaired, root, target["module"], sample_dir / "repair_run")
                if rep_eval.get("suite_pass"):
                    final_pass = True
                    final_eval = rep_eval
        except Exception:
            pass

    line_cov = final_eval.get("line_pct") if final_pass else 0.0
    branch_cov = final_eval.get("branch_pct") if final_pass else 0.0
    
    return {
        "target": target["id"],
        "category": target["category"],
        "config": config_name,
        "first_pass": first_pass,
        "final_pass": final_pass,
        "line_cov": round(line_cov, 2) if line_cov is not None else 0.0,
        "branch_cov": round(branch_cov, 2) if branch_cov is not None else 0.0,
        "status": "passed" if final_pass else "failed"
    }

def run_study():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    engine = GroqCouncilEngine(
        model="openai/gpt-oss-20b",
        max_new_tokens=2500,
        max_total_tokens=1_000_000,
        max_budget_usd=5.0
    )
    
    configs = [
        ("full_method", "Council Full (Grounded + AutoImport + Critic)"),
        ("no_critic", "w/o Critic Repair (Single-pass Coder)"),
        ("no_grounding", "w/o State Grounding (Baseline API)"),
        ("no_auto_import", "w/o Auto-Import (Raw AST)")
    ]
    
    all_results = []
    
    print("=" * 80)
    print("STARTING TEST4PY BENCHMARK & ABLATION STUDY")
    print("Configs: Full Method | w/o Critic | w/o State Grounding | w/o Auto-Import")
    print("=" * 80)
    
    for target in PAPER_TARGETS:
        print(f"\nTarget: [{target['id']}] ({target['category']})")
        t_dir = OUT_DIR / target["id"]
        t_dir.mkdir(exist_ok=True)
        
        for cfg_key, cfg_label in configs:
            t0 = time.perf_counter()
            res = evaluate_configuration(target, cfg_key, engine, t_dir)
            elapsed = time.perf_counter() - t0
            res["config_label"] = cfg_label
            res["latency_sec"] = round(elapsed, 2)
            all_results.append(res)
            
            p_sym = "✅ PASS" if res["final_pass"] else "❌ FAIL"
            print(f"  [{cfg_key:15}] -> {p_sym} | Line: {res['line_cov']:6.2f}% | Branch: {res['branch_cov']:6.2f}% | Time: {elapsed:.2f}s")
            
    # Save CSV
    csv_path = OUT_DIR / "ablation_summary.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        w.writeheader()
        w.writerows(all_results)
        
    # Generate LaTeX Table & Markdown Report
    generate_ablation_artifacts(all_results, engine)
    
    print("\n" + "=" * 80)
    print("ABLATION STUDY COMPLETED!")
    print(f"Report: {OUT_DIR / 'ABLATION_STUDY_REPORT.md'}")
    print(f"CSV:    {csv_path}")
    print(engine.get_summary_report())
    print("=" * 80)

def generate_ablation_artifacts(results, engine):
    # Aggregate by config
    configs = ["full_method", "no_critic", "no_grounding", "no_auto_import"]
    config_labels = {
        "full_method": "Council Full (Grounded + AutoImport + Critic)",
        "no_critic": "w/o Critic (First Pass Only)",
        "no_grounding": "w/o State Grounding (API Only)",
        "no_auto_import": "w/o Auto-Import Resolver"
    }
    
    stats = {}
    for c in configs:
        sub = [r for r in results if r["config"] == c]
        tot = len(sub)
        p = sum(1 for r in sub if r["final_pass"])
        avg_line = sum(r["line_cov"] for r in sub) / tot if tot else 0.0
        avg_branch = sum(r["branch_cov"] for r in sub) / tot if tot else 0.0
        stats[c] = {
            "pass_rate": (p / tot * 100) if tot else 0.0,
            "pass_count": f"{p}/{tot}",
            "avg_line": avg_line,
            "avg_branch": avg_branch
        }
        
    # 1. LaTeX Table
    tex = r"""\begin{table}[t]
\centering
\caption{Ablation study evaluating the contribution of State Grounding, Auto-Import, and Critic Repair on Test4Py benchmark targets.}
\label{tab:ablation_study}
\small
\begin{tabular}{lcccc}
\toprule
\textbf{Configuration} & \textbf{Pass Rate (\%)} & \textbf{Passed Nodes} & \textbf{Avg Line Cov (\%)} & \textbf{Avg Branch Cov (\%)} \\
\midrule
"""
    for c in configs:
        lbl = config_labels[c]
        s = stats[c]
        tex += f"{lbl} & {s['pass_rate']:.1f}\\% & {s['pass_count']} & {s['avg_line']:.2f}\\% & {s['avg_branch']:.2f}\\% \\\\\n"
    tex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    (OUT_DIR / "table_ablation.tex").write_text(tex, encoding="utf-8")
    
    # 2. Markdown Report
    t = engine.telemetry
    md = f"""# Báo Cáo Nghiên Cứu Đánh Giá Thành Phần (Ablation Study) - Test4Py Benchmark
*Mô hình:* `openai/gpt-oss-20b` (Groq Engine)
*Số lượng đối tượng đánh giá:* 6 Module chuẩn từ Bảng 1 Test4Py

---

## 1. Bảng Tổng Hợp Kết Quả Ablation Study

| Cấu hình Thực nghiệm (Configuration) | Tỷ lệ Pass (%) | Số Test Pass | Line Coverage TB (%) | Branch Coverage TB (%) | Vai trò & Đóng góp Khoa học |
|---|:---:|:---:|:---:|:---:|---|
| **Council Full (Đầy đủ cải tiến)** | **{stats['full_method']['pass_rate']:.1f}%** | **{stats['full_method']['pass_count']}** | **{stats['full_method']['avg_line']:.2f}%** | **{stats['full_method']['avg_branch']:.2f}%** | Phương pháp hoàn chỉnh đạt hiệu năng tối đa |
| **w/o Critic (Không có Critic Repair)** | {stats['no_critic']['pass_rate']:.1f}% | {stats['no_critic']['pass_count']} | {stats['no_critic']['avg_line']:.2f}% | {stats['no_critic']['avg_branch']:.2f}% | Đo lường độ chính xác tức thì (First Pass) |
| **w/o State Grounding (Không có Setup)**| {stats['no_grounding']['pass_rate']:.1f}% | {stats['no_grounding']['pass_count']} | {stats['no_grounding']['avg_line']:.2f}% | {stats['no_grounding']['avg_branch']:.2f}% | Chứng minh tầm quan trọng của ngữ cảnh đối tượng |
| **w/o Auto-Import (Không có Auto-import)**| {stats['no_auto_import']['pass_rate']:.1f}% | {stats['no_auto_import']['pass_count']} | {stats['no_auto_import']['avg_line']:.2f}% | {stats['no_auto_import']['avg_branch']:.2f}% | Khắc phục điểm yếu `NameError` của SLM |

---

## 2. Chi Tiết Thực Nghiệm Trên Từng Đối Tượng

| Đối tượng (Target ID) | Phân Loại | Council Full | w/o Critic | w/o Grounding | w/o Auto-Import |
|---|---|:---:|:---:|:---:|:---:|
"""
    targets = sorted(list({r["target"] for r in results}))
    for tgt in targets:
        sub = {r["config"]: r for r in results if r["target"] == tgt}
        cat = sub["full_method"]["category"]
        c_full = "✅ Pass" if sub["full_method"]["final_pass"] else "❌ Fail"
        c_nocritic = "✅ Pass" if sub["no_critic"]["final_pass"] else "❌ Fail"
        c_noground = "✅ Pass" if sub["no_grounding"]["final_pass"] else "❌ Fail"
        c_noimport = "✅ Pass" if sub["no_auto_import"]["final_pass"] else "❌ Fail"
        md += f"| `{tgt}` | {cat} | {c_full} | {c_nocritic} | {c_noground} | {c_noimport} |\n"

    md += f"""
---

## 3. Kiểm Toán Ngân Sách Thực Tế (Budget Telemetry)
- **Tổng số lượt gọi LLM:** {t['coder_calls'] + t['critic_calls']} calls
- **Tổng Tokens tiêu thụ:** **{t['total_tokens']:,}** / 1,000,000 (Chỉ chiếm **{t['total_tokens']/engine.max_total_tokens*100:.2f}%** hạn mức)
- **Chi phí ước tính:** **${t['estimated_cost_usd']:.4f} USD** / $5.00
- **Thời gian suy luận toàn bộ:** {t['seconds']:.2f}s
"""
    (OUT_DIR / "ABLATION_STUDY_REPORT.md").write_text(md, encoding="utf-8")

if __name__ == "__main__":
    run_study()
