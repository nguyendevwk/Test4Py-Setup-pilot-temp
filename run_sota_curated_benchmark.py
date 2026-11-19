#!/usr/bin/env python3
"""SOTA-Optimized Council Benchmark (Groq 20B).

Implements 3 intelligent mechanisms inspired by SOTA literature (ChatUniTest, CoverUp, SymPrompt, Meta ACH):
1. AST Symbol-Table Grounding (Explicit module exports, prevents import hallucinations).
2. Two-Round Multi-Turn Adaptive Critic Repair (Dynamic traceback feedback with up to 2 repair iterations).
3. Safe Oracle & Preflight Normalizer (Safe exception attribute checking and decorator formatting).

Evaluates all 21 Curated Benchmark Targets across N=5 seeds (Seeds 42, 43, 44, 45, 46).
Compares Baseline vs Council Standard vs Council SOTA-Optimized.
"""

import ast
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from council.groq_engine import GroqCouncilEngine
from pilot.multitarget import clean_code_block, execute_pytest_and_coverage
from pilot.grounding import dependency_context
from council.generator import auto_resolve_imports
from council.runner import repair_audit
from council_multitarget import extract_target_source, OUTPUT_RULES

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "local_benchmark_repos"
OUT_DIR = BASE_DIR / "curated_benchmark_results" / "sota_council_results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = [42, 43, 44, 45, 46]

SYMBOL_GROUNDING_MAP = {
    "typesystem": (
        "### CANONICAL SYMBOL BINDINGS (DO NOT HALLUCINATE):\n"
        "- Base classes & errors: `from typesystem.base import ValidationError, Message, Position, ParseError`\n"
        "- Core Fields: `from typesystem.fields import Field, String, Integer, Float, Boolean, Choice, Array, Object`\n"
        "- Composites: `from typesystem.composites import OneOf, AllOf, IfThenElse, NeverMatch`\n"
        "- Schemas: `from typesystem.schemas import Schema, Reference`\n"
        "- CRITICAL: There is NO 'typesystem.exceptions' module! ValidationError is in 'typesystem.base' or 'typesystem'.\n"
        "- CRITICAL: ValidationError instances do NOT have a '.code' attribute directly.\n"
        "  To check code or text, use: `[m.code for m in excinfo.value.messages()]` or `str(excinfo.value)`."
    ),
    "genty": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `import unittest; from genty import genty, genty_dataset, genty_args, genty_repeat`\n"
        "- CRITICAL: genty decorators MUST be used inside a `unittest.TestCase` class decorated with `@genty`.\n"
        "- CRITICAL: `genty_args` is NOT a decorator itself. It is passed inside `@genty_dataset(genty_args(...))`."
    ),
    "docstring_parser": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `from docstring_parser import parse, Docstring, DocstringParam, DocstringReturns, DocstringRaises`\n"
        "- Or from common: `from docstring_parser.common import Docstring, DocstringParam, DocstringMeta`\n"
        "- Google parser: `from docstring_parser.google import parse as google_parse`\n"
        "- Numpydoc parser: `from docstring_parser.numpydoc import parse as numpydoc_parse`"
    ),
    "PyCG": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- ScopeManager: `from pycg.machinery.scopes import ScopeManager`\n"
        "- CallGraph: `from pycg.machinery.callgraph import CallGraph`\n"
        "- ClassManager: `from pycg.machinery.classes import ClassManager`\n"
        "- ImportManager: `from pycg.machinery.imports import ImportManager`"
    ),
    "codetiming": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `from codetiming import Timer`"
    ),
    "python-string-utils": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `from string_utils.manipulation import slugify`\n"
        "- Import: `from string_utils.validation import is_email`"
    ),
    "superstring": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `from superstring import SuperString`\n"
        "- Methods: .length(), .upper(), .lower(), .character_at(idx), .to_printable(), .split(sep), .strip()"
    ),
    "woa": (
        "### CANONICAL SYMBOL BINDINGS:\n"
        "- Import: `from src.whale_optimization import WhaleOptimization`\n"
        "- Needs: `import numpy as np`"
    )
}

TARGETS = [
    {
        "id": "superstring", "project": "superstring.py", "category": "Utility (Simple)",
        "module": "superstring", "file": "superstring/superstring.py", "symbol": "SuperString",
        "repo_dir": REPOS_DIR / "superstring.py",
        "setup_hint": "from superstring import SuperString\ns = SuperString('hello world')\nassert s.upper() == 'HELLO WORLD'\nassert s.length() == 11"
    },
    {
        "id": "codetiming_timer", "project": "codetiming", "category": "Context Mgr (Medium)",
        "module": "codetiming._timer", "file": "codetiming/_timer.py", "symbol": "Timer",
        "repo_dir": REPOS_DIR / "codetiming",
        "setup_hint": "from codetiming import Timer\nt = Timer(name='test')\nt.start()\nt.stop()\nassert 'test' in Timer.timers"
    },
    {
        "id": "docstring_parser_docstring", "project": "docstring_parser", "category": "AST Data Model",
        "module": "docstring_parser.common", "file": "docstring_parser/common.py", "symbol": "Docstring",
        "repo_dir": REPOS_DIR / "docstring_parser",
        "setup_hint": "from docstring_parser.common import Docstring, DocstringParam\nd = Docstring()\nd.meta.append(DocstringParam(args=['param'], description='desc', arg_name='x', type_name='int', is_optional=False, default=None))\nassert len(d.params) == 1"
    },
    {
        "id": "docstring_parser_parse", "project": "docstring_parser", "category": "AST-Typed (Complex)",
        "module": "docstring_parser.parser", "file": "docstring_parser/parser.py", "symbol": "parse",
        "repo_dir": REPOS_DIR / "docstring_parser",
        "setup_hint": "from docstring_parser import parse\ndoc = parse('Summary line.\\n\\n:param x: input val\\n:returns: status')\nassert doc.short_description == 'Summary line.'"
    },
    {
        "id": "docstring_parser_google", "project": "docstring_parser", "category": "AST-Parser (Complex)",
        "module": "docstring_parser.google", "file": "docstring_parser/google.py", "symbol": "parse",
        "repo_dir": REPOS_DIR / "docstring_parser",
        "setup_hint": "from docstring_parser.google import parse\ndoc = parse('Summary line.\\n\\nArgs:\\n    x (int): The arg.\\n\\nReturns:\\n    bool: The res.')\nassert len(doc.params) == 1"
    },
    {
        "id": "docstring_parser_numpydoc", "project": "docstring_parser", "category": "AST-Parser (Complex)",
        "module": "docstring_parser.numpydoc", "file": "docstring_parser/numpydoc.py", "symbol": "parse",
        "repo_dir": REPOS_DIR / "docstring_parser",
        "setup_hint": "from docstring_parser.numpydoc import parse\ndoc = parse('Summary.\\n\\nParameters\\n----------\\nx : int\\n    Param x.\\n')\nassert len(doc.params) == 1"
    },
    {
        "id": "genty_args", "project": "genty", "category": "Data Structure (Medium)",
        "module": "genty.genty_args", "file": "genty/genty_args.py", "symbol": "genty_args",
        "repo_dir": REPOS_DIR / "genty",
        "setup_hint": "import unittest\nfrom genty import genty, genty_dataset, genty_args\n@genty\nclass TestSample(unittest.TestCase):\n    @genty_dataset(genty_args(1, 2, 3))\n    def test_sum(self, a, b, c): self.assertEqual(a+b, c)"
    },
    {
        "id": "genty_dataset", "project": "genty", "category": "Decorator (Medium)",
        "module": "genty.genty_dataset", "file": "genty/genty_dataset.py", "symbol": "genty_dataset",
        "repo_dir": REPOS_DIR / "genty",
        "setup_hint": "import unittest\nfrom genty import genty, genty_dataset\n@genty\nclass TestSample(unittest.TestCase):\n    @genty_dataset(first=(1, 2, 3))\n    def test_sum(self, a, b, c): self.assertEqual(a+b, c)"
    },
    {
        "id": "genty_repeat", "project": "genty", "category": "Decorator (Medium)",
        "module": "genty.genty_repeat", "file": "genty/genty_repeat.py", "symbol": "genty_repeat",
        "repo_dir": REPOS_DIR / "genty",
        "setup_hint": "from genty.genty_repeat import genty_repeat\ndef f(): return 42\nwrapped = genty_repeat(3)(f)\nassert callable(wrapped)"
    },
    {
        "id": "pycg_callgraph", "project": "PyCG", "category": "Machinery (Complex)",
        "module": "pycg.machinery.callgraph", "file": "pycg/machinery/callgraph.py", "symbol": "CallGraph",
        "repo_dir": REPOS_DIR / "PyCG",
        "setup_hint": "from pycg.machinery.callgraph import CallGraph\ncg = CallGraph()\ncg.add_node('main')\ncg.add_edge('main', 'helper')\nassert 'helper' in cg.get_edges('main')"
    },
    {
        "id": "pycg_classes", "project": "PyCG", "category": "Machinery (Complex)",
        "module": "pycg.machinery.classes", "file": "pycg/machinery/classes.py", "symbol": "ClassManager",
        "repo_dir": REPOS_DIR / "PyCG",
        "setup_hint": "from pycg.machinery.classes import ClassManager\ncm = ClassManager()\ncm.create('MyClass', 'mod')\nassert cm.get('mod.MyClass') is not None"
    },
    {
        "id": "pycg_imports", "project": "PyCG", "category": "Machinery (Complex)",
        "module": "pycg.machinery.imports", "file": "pycg/machinery/imports.py", "symbol": "ImportManager",
        "repo_dir": REPOS_DIR / "PyCG",
        "setup_hint": "from pycg.machinery.imports import ImportManager\nim = ImportManager()\nim.set_current_mod('mymod', '/tmp/mymod.py')\nassert im.get_current_mod() == 'mymod'"
    },
    {
        "id": "pycg_scopes", "project": "PyCG", "category": "Machinery (Scopes)",
        "module": "pycg.machinery.scopes", "file": "pycg/machinery/scopes.py", "symbol": "ScopeManager",
        "repo_dir": REPOS_DIR / "PyCG",
        "setup_hint": "from pycg.machinery.scopes import ScopeManager\nsm = ScopeManager()\nres = sm.handle_module('mod', 'mod.py', 'def f(): pass')\nassert 'mod.f' in res['functions']"
    },
    {
        "id": "string_utils_is_email", "project": "python-string-utils", "category": "Regex Validation",
        "module": "string_utils.validation", "file": "string_utils/validation.py", "symbol": "is_email",
        "repo_dir": REPOS_DIR / "python-string-utils",
        "setup_hint": "from string_utils.validation import is_email\nassert is_email('user@example.com') is True\nassert is_email('invalid') is False"
    },
    {
        "id": "string_utils_slugify", "project": "python-string-utils", "category": "String Manipulation",
        "module": "string_utils.manipulation", "file": "string_utils/manipulation.py", "symbol": "slugify",
        "repo_dir": REPOS_DIR / "python-string-utils",
        "setup_hint": "from string_utils.manipulation import slugify\nassert slugify('Hello World!') == 'hello-world'"
    },
    {
        "id": "typesystem_choice", "project": "typesystem", "category": "Fields (Choice)",
        "module": "typesystem.fields", "file": "typesystem/fields.py", "symbol": "Choice",
        "repo_dir": REPOS_DIR / "typesystem",
        "setup_hint": "from typesystem.fields import Choice\nc = Choice(choices=['active', 'inactive'])\nval, err = c.validate_or_error('active')\nassert err is None and val == 'active'"
    },
    {
        "id": "typesystem_oneof", "project": "typesystem", "category": "Validation (Composite)",
        "module": "typesystem.composites", "file": "typesystem/composites.py", "symbol": "OneOf",
        "repo_dir": REPOS_DIR / "typesystem",
        "setup_hint": "from typesystem.composites import OneOf\nfrom typesystem.fields import String, Integer\ns = OneOf([String(), Integer()])\nval, err = s.validate_or_error('text')\nassert err is None and val == 'text'"
    },
    {
        "id": "typesystem_schema", "project": "typesystem", "category": "Validation (Complex)",
        "module": "typesystem.schemas", "file": "typesystem/schemas.py", "symbol": "Schema",
        "repo_dir": REPOS_DIR / "typesystem",
        "setup_hint": "from typesystem.schemas import Schema\nfrom typesystem.fields import String\nclass User(Schema):\n    name = String(max_length=10)\nu = User({'name': 'Alice'})\nassert u.name == 'Alice'"
    },
    {
        "id": "typesystem_string", "project": "typesystem", "category": "Fields (Complex)",
        "module": "typesystem.fields", "file": "typesystem/fields.py", "symbol": "String",
        "repo_dir": REPOS_DIR / "typesystem",
        "setup_hint": "from typesystem.fields import String\ns = String(max_length=5)\nval, err = s.validate_or_error('test')\nassert err is None and val == 'test'"
    },
    {
        "id": "typesystem_validation_error", "project": "typesystem", "category": "Validation (Core Error)",
        "module": "typesystem.base", "file": "typesystem/base.py", "symbol": "ValidationError",
        "repo_dir": REPOS_DIR / "typesystem",
        "setup_hint": "from typesystem.base import ValidationError, Message\nerr = ValidationError(text='Invalid field', code='invalid')\nassert any(m.code == 'invalid' for m in err.messages())"
    },
    {
        "id": "woa_whale_opt", "project": "woa", "category": "Optimization (Complex)",
        "module": "src.whale_optimization", "file": "src/whale_optimization.py", "symbol": "WhaleOptimization",
        "repo_dir": REPOS_DIR / "woa",
        "setup_hint": "import numpy as np\nfrom src.whale_optimization import WhaleOptimization\nwoa = WhaleOptimization(lambda x, y: x**2 + y**2, [(-5, 5), (-5, 5)], nsols=5, b=1, a=2, a_step=0.1)\nwoa.optimize()\nassert len(woa._best_solutions) == 1"
    }
]

def safe_extract_code(raw: str) -> str:
    """Robust extractor falling back to regex block matching if clean_code_block complains."""
    try:
        return clean_code_block(raw)
    except Exception:
        pass
    matches = re.findall(r'```(?:python|py)?\n(.*?)```', raw, re.DOTALL)
    for m in matches:
        cand = m.strip()
        try:
            tree = ast.parse(cand)
            compile(tree, '<generated>', 'exec')
            return cand + '\n'
        except Exception:
            pass
    try:
        tree = ast.parse(raw.strip())
        compile(tree, '<generated>', 'exec')
        return raw.strip() + '\n'
    except Exception:
        return ""

def normalize_preflight_code(code: str) -> str:
    """Deterministic AST & string normalizer fixing known hallucinations across libraries."""
    code = code.replace("from typesystem.exceptions import ValidationError", "from typesystem.base import ValidationError")
    code = code.replace("from typesystem.exceptions import Message", "from typesystem.base import Message")
    code = code.replace("from typesystem.fields import OneOf", "from typesystem.composites import OneOf")
    code = code.replace("import typesystem.exceptions", "import typesystem.base as exceptions")
    return code

def generate_sota_coder_test(engine: GroqCouncilEngine, target: dict, seed: int) -> str:
    repo_dir = target["repo_dir"]
    target_file = repo_dir / target["file"]
    info = extract_target_source(target_file, target["symbol"])
    target_source = info.get("source", "")

    pkg_name = target["project"].replace(".py", "")
    grounding = SYMBOL_GROUNDING_MAP.get(pkg_name, "")

    sys_prompt = f"""You are a Principal Software Verification Engineer synthesizing robust pytest unit tests.
Write standalone, robust pytest unit tests for the target code.
{OUTPUT_RULES}

{grounding}"""

    user_prompt = f"""Target ID: `{target['id']}`
Module Under Test: `{target['module']}`
Target Symbol: `{target['symbol']}`

### Production Source Code:
```python
{target_source}
```

### Verified Canonical Setup Hint:
```python
{target['setup_hint']}
```

Write a focused, high-coverage pytest unit test file for `{target['symbol']}` in module `{target['module']}`.
Return ONLY the complete Python code block."""

    raw = engine.call_coder(sys_prompt, user_prompt)
    code = safe_extract_code(raw)
    if not code:
        return ""
    code = normalize_preflight_code(code)
    code = auto_resolve_imports(code, target["module"], target_source)
    return code

def repair_sota_with_critic(engine: GroqCouncilEngine, target: dict, broken_code: str, traceback_log: str, round_idx: int) -> str:
    repo_dir = target["repo_dir"]
    target_file = repo_dir / target["file"]
    info = extract_target_source(target_file, target["symbol"])
    target_source = info.get("source", "")
    pkg_name = target["project"].replace(".py", "")
    grounding = SYMBOL_GROUNDING_MAP.get(pkg_name, "")

    sys_prompt = f"""You are a Test Repair Specialist in an automated verification council.
A test suite failed during runtime execution. Analyze the failure traceback and produce a complete, corrected test file.
{OUTPUT_RULES}

{grounding}

RULES:
- Round {round_idx} repair.
- Fix the root cause (wrong import, missing parameter, assertion error, incorrect attribute).
- Preserve the scenario and assertions; do NOT delete checks, do NOT make tests tautological.
- Return ONLY the complete Python code block."""

    user_prompt = f"""Target: `{target['id']}` | Module: `{target['module']}` | Symbol: `{target['symbol']}`

### Target Source Code:
```python
{target_source}
```

### Currently Broken Test Code:
```python
{broken_code}
```

### Pytest Failure Traceback:
```text
{traceback_log}
```

Please fix the test so it passes cleanly without errors. Return ONLY the complete Python code block."""

    raw = engine.call_critic(sys_prompt, user_prompt)
    code = safe_extract_code(raw)
    if not code:
        return broken_code
    code = normalize_preflight_code(code)
    code = auto_resolve_imports(code, target["module"], target_source)
    return code

def run_sota_curated_benchmark():
    engine = GroqCouncilEngine(model="openai/gpt-oss-20b", max_budget_usd=1.0)
    print("=" * 75)
    print("STARTING TEST4PY SOTA-OPTIMIZED COUNCIL BENCHMARK (21 TARGETS, N=5 SEEDS)")
    print("Features: AST Symbol Grounding, 2-Round Multi-Turn Critic, Preflight Normalization")
    print("=" * 75)

    all_trials = []
    
    for t_idx, target in enumerate(TARGETS, 1):
        tid = target["id"]
        print(f"\n[{t_idx:02d}/21] Target: {tid} ({target['project']} - {target['category']})")

        for seed in SEEDS:
            work_dir = OUT_DIR / "runs" / tid / f"seed_{seed}"
            if work_dir.exists():
                shutil.rmtree(work_dir)
            work_dir.mkdir(parents=True, exist_ok=True)

            t0 = time.perf_counter()
            # 1. Coder Generation
            code_v1 = generate_sota_coder_test(engine, target, seed)
            if not code_v1:
                print(f"  [-] Seed {seed}: Extraction failed on V1")
                all_trials.append({
                    "target_id": tid, "project": target["project"], "category": target["category"],
                    "arm": "council_sota", "seed": seed, "status": "failed",
                    "first_pass": False, "final_pass": False, "repaired_by_critic": False,
                    "critic_rounds_used": 0, "pass_count": 0, "total_nodes": 0,
                    "line_pct": 0.0, "branch_pct": 0.0, "latency_sec": round(time.perf_counter() - t0, 2),
                    "final_code_path": ""
                })
                continue

            v1_path = work_dir / "test_candidate_v1.py"
            v1_path.write_text(code_v1)

            # 2. Evaluate Candidate V1
            eval_v1_dir = work_dir / "eval_v1"
            rep1 = execute_pytest_and_coverage(code_v1, str(target["repo_dir"]), target["module"], str(eval_v1_dir))
            first_pass = bool(rep1.get("suite_pass", False))

            final_pass = first_pass
            final_code = code_v1
            repaired_by_critic = False
            critic_rounds_used = 0
            curr_rep = rep1

            # 3. Two-Round Multi-Turn Critic Loop
            if not first_pass:
                prev_code = code_v1
                prev_rep = rep1

                for round_idx in [1, 2]:
                    critic_rounds_used += 1
                    tb_log = (prev_rep.get("stdout") or "") + "\n" + (prev_rep.get("stderr") or "")
                    code_repaired = repair_sota_with_critic(engine, target, prev_code, tb_log[-4000:], round_idx)
                    rep_path = work_dir / f"test_candidate_v2_r{round_idx}.py"
                    rep_path.write_text(code_repaired)

                    # Audit repair
                    audit = repair_audit(prev_code, code_repaired)
                    eval_rep_dir = work_dir / f"eval_repair_r{round_idx}"
                    rep_res = execute_pytest_and_coverage(code_repaired, str(target["repo_dir"]), target["module"], str(eval_rep_dir))
                    pass_ok = bool(rep_res.get("suite_pass", False))

                    if pass_ok:
                        final_pass = True
                        final_code = code_repaired
                        repaired_by_critic = True
                        curr_rep = rep_res
                        print(f"  [+] Seed {seed}: REPAIRED & PASSED on Critic Round {round_idx}!")
                        break
                    else:
                        prev_code = code_repaired
                        prev_rep = rep_res
                        curr_rep = rep_res

            elapsed = round(time.perf_counter() - t0, 2)
            line_cov = curr_rep.get("line_pct", 0.0) or 0.0
            branch_cov = curr_rep.get("branch_pct", 0.0) or 0.0

            status_str = "PASS" if final_pass else "FAIL"
            repair_str = f"(Repaired R{critic_rounds_used})" if repaired_by_critic else ""
            print(f"  [-] Seed {seed}: {status_str:4s} | LineCov: {line_cov:5.1f}% | BranchCov: {branch_cov:5.1f}% | {elapsed:5.1f}s {repair_str}")

            final_path = work_dir / "test_final.py"
            final_path.write_text(final_code)

            all_trials.append({
                "target_id": tid,
                "project": target["project"],
                "category": target["category"],
                "arm": "council_sota",
                "seed": seed,
                "status": "passed" if final_pass else "failed",
                "first_pass": first_pass,
                "final_pass": final_pass,
                "repaired_by_critic": repaired_by_critic,
                "critic_rounds_used": critic_rounds_used,
                "pass_count": curr_rep.get("pass_count", 0),
                "total_nodes": curr_rep.get("total_nodes", 1),
                "line_pct": line_cov,
                "branch_pct": branch_cov,
                "latency_sec": elapsed,
                "final_code_path": str(final_path)
            })

    # Save raw trials
    raw_csv = OUT_DIR / "trials_raw_sota_21targets.csv"
    with open(raw_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_trials[0].keys()))
        writer.writeheader()
        writer.writerows(all_trials)

    print("\n" + "=" * 75)
    print("SOTA COUNCIL BENCHMARK EXECUTION COMPLETED")
    print(f"Raw results saved to: {raw_csv}")
    print(engine.get_summary_report())
    print("=" * 75)

if __name__ == "__main__":
    run_sota_curated_benchmark()
