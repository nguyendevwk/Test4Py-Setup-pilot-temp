from pathlib import Path
from council_multitarget import extract_target_source

REPOS_DIR = Path("local_benchmark_repos").resolve()

TARGETS_CHECK = [
    ("superstring", REPOS_DIR / "superstring.py" / "superstring" / "superstring.py", "SuperString"),
    ("codetiming_timer", REPOS_DIR / "codetiming" / "codetiming" / "_timer.py", "Timer"),
    ("docstring_parser_docstring", REPOS_DIR / "docstring_parser" / "docstring_parser" / "common.py", "Docstring"),
    ("docstring_parser_parse", REPOS_DIR / "docstring_parser" / "docstring_parser" / "parser.py", "parse"),
    ("docstring_parser_google", REPOS_DIR / "docstring_parser" / "docstring_parser" / "google.py", "parse"),
    ("docstring_parser_numpydoc", REPOS_DIR / "docstring_parser" / "docstring_parser" / "numpydoc.py", "parse"),
    ("genty_args", REPOS_DIR / "genty" / "genty" / "genty_args.py", "genty_args"),
    ("genty_dataset", REPOS_DIR / "genty" / "genty" / "genty_dataset.py", "genty_dataset"),
    ("genty_repeat", REPOS_DIR / "genty" / "genty" / "genty_repeat.py", "genty_repeat"),
    ("pycg_callgraph", REPOS_DIR / "PyCG" / "pycg" / "machinery" / "callgraph.py", "CallGraph"),
    ("pycg_classes", REPOS_DIR / "PyCG" / "pycg" / "machinery" / "classes.py", "ClassManager"),
    ("pycg_imports", REPOS_DIR / "PyCG" / "pycg" / "machinery" / "imports.py", "ImportManager"),
    ("pycg_scopes", REPOS_DIR / "PyCG" / "pycg" / "machinery" / "scopes.py", "ScopeManager"),
    ("string_utils_is_email", REPOS_DIR / "python-string-utils" / "string_utils" / "validation.py", "is_email"),
    ("string_utils_slugify", REPOS_DIR / "python-string-utils" / "string_utils" / "manipulation.py", "slugify"),
    ("typesystem_choice", REPOS_DIR / "typesystem" / "typesystem" / "fields.py", "Choice"),
    ("typesystem_oneof", REPOS_DIR / "typesystem" / "typesystem" / "composites.py", "OneOf"),
    ("typesystem_schema", REPOS_DIR / "typesystem" / "typesystem" / "schemas.py", "Schema"),
    ("typesystem_string", REPOS_DIR / "typesystem" / "typesystem" / "fields.py", "String"),
    ("typesystem_validation_error", REPOS_DIR / "typesystem" / "typesystem" / "base.py", "ValidationError"),
    ("woa_whale_opt", REPOS_DIR / "woa" / "src" / "whale_optimization.py", "WhaleOptimization"),
]

for tid, fpath, sym in TARGETS_CHECK:
    if not fpath.exists():
        print(f"[-] FILE MISSING: {tid} -> {fpath}")
        continue
    info = extract_target_source(fpath, sym)
    src_len = len(info.get("source", ""))
    print(f"[OK] {tid:28} | symbol={sym:18} | src_len={src_len}")
