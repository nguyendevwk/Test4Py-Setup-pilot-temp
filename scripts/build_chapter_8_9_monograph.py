import sys
import csv
from pathlib import Path

ROOT = Path(".").resolve()
DELIVERABLES = ROOT / "monograph_final_deliverables"
DATA_DIR = DELIVERABLES / "data"
REPORTS_DIR = DELIVERABLES / "reports"
GOLDEN_DIR = DELIVERABLES / "golden_suites"

# Load statistical data
with open(DATA_DIR / "statistical_summary_sota_3way.csv", encoding="utf-8") as f:
    summary_sota = list(csv.DictReader(f))

with open(DATA_DIR / "ablation_summary.csv", encoding="utf-8") as f:
    ablation_data = list(csv.DictReader(f))

with open(DATA_DIR / "mutation_scores_21targets.csv", encoding="utf-8") as f:
    mutation_data = list(csv.DictReader(f))

with open(DATA_DIR / "trials_raw_sota_21targets.csv", encoding="utf-8") as f:
    trials_sota = list(csv.DictReader(f))

with open(DATA_DIR / "trials_raw_curated_21targets.csv", encoding="utf-8") as f:
    trials_curated = list(csv.DictReader(f))

# Target specs mapping for Appendix A
TARGET_SPECS = [
    ("superstring", "superstring.py", "superstring/superstring.py", 182, "SuperString", 16, "Utility (Simple)"),
    ("codetiming_timer", "codetiming", "codetiming/_timer.py", 105, "Timer", 63, "Context Mgr (Medium)"),
    ("docstring_parser_docstring", "docstring_parser", "docstring_parser/common.py", 612, "Docstring", 171, "AST Data Model"),
    ("docstring_parser_parse", "docstring_parser", "docstring_parser/parser.py", 168, "parse", 28, "AST-Typed (Complex)"),
    ("docstring_parser_google", "docstring_parser", "docstring_parser/google.py", 1203, "parse", 11, "AST-Parser (Complex)"),
    ("docstring_parser_numpydoc", "docstring_parser", "docstring_parser/numpydoc.py", 911, "parse", 11, "AST-Parser (Complex)"),
    ("genty_args", "genty", "genty/genty_args.py", 81, "genty_args", 42, "Data Structure (Medium)"),
    ("genty_dataset", "genty", "genty/genty_dataset.py", 214, "genty_dataset", 99, "Decorator (Medium)"),
    ("genty_repeat", "genty", "genty/genty_repeat.py", 36, "genty_repeat", 31, "Decorator (Medium)"),
    ("pycg_callgraph", "PyCG", "pycg/machinery/callgraph.py", 59, "CallGraph", 35, "Machinery (Complex)"),
    ("pycg_classes", "PyCG", "pycg/machinery/classes.py", 78, "ClassManager", 16, "Machinery (Complex)"),
    ("pycg_imports", "PyCG", "pycg/machinery/imports.py", 235, "ImportManager", 177, "Machinery (Complex)"),
    ("pycg_scopes", "PyCG", "pycg/machinery/scopes.py", 154, "ScopeManager", 62, "Machinery (Scopes)"),
    ("string_utils_is_email", "python-string-utils", "string_utils/validation.py", 657, "is_email", 41, "Regex Validation"),
    ("string_utils_slugify", "python-string-utils", "string_utils/manipulation.py", 649, "slugify", 36, "String Manipulation"),
    ("typesystem_choice", "typesystem", "typesystem/fields.py", 792, "Choice", 34, "Fields (Choice)"),
    ("typesystem_oneof", "typesystem", "typesystem/composites.py", 122, "OneOf", 32, "Validation (Composite)"),
    ("typesystem_schema", "typesystem", "typesystem/schemas.py", 144, "Schema", 83, "Validation (Complex)"),
    ("typesystem_string", "typesystem", "typesystem/fields.py", 792, "String", 97, "Fields (Complex)"),
    ("typesystem_validation_error", "typesystem", "typesystem/base.py", 265, "ValidationError", 4, "Validation (Core Error)"),
    ("woa_whale_opt", "woa", "src/whale_optimization.py", 115, "WhaleOptimization", 113, "Optimization (Complex)"),
]

# Read Golden Suites for Appendix B
golden_samples = {}
sample_keys = [
    ("typesystem_oneof", "test_typesystem_oneof_golden.py"),
    ("pycg_callgraph", "test_pycg_callgraph_golden.py"),
    ("genty_args", "test_genty_args_golden.py"),
    ("docstring_parser_google", "test_docstring_parser_google_golden.py"),
    ("codetiming_timer", "test_codetiming_timer_golden.py"),
]

for tid, fname in sample_keys:
    fpath = GOLDEN_DIR / fname
    if fpath.exists():
        golden_samples[tid] = fpath.read_text(encoding="utf-8")
    else:
        golden_samples[tid] = "# Golden suite file not found."

print(f"Loaded {len(golden_samples)} golden samples.")
