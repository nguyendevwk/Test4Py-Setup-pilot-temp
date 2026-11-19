from pilot.multitarget import execute_pytest_and_coverage
from pathlib import Path

target_dir = Path("local_benchmark_repos/superstring.py").resolve()
work_dir = Path("/tmp/test_eval_exec")
if work_dir.exists():
    import shutil
    shutil.rmtree(work_dir)

code = """
from superstring import SuperString
def test_superstring():
    s = SuperString("hello world")
    assert s.slugify() == "hello-world"
"""

rep = execute_pytest_and_coverage(code, str(target_dir), "superstring", str(work_dir))
print("Rep keys:", list(rep.keys()))
print("Passed:", rep.get("passed"))
print("Line pct:", rep.get("line_pct"))
