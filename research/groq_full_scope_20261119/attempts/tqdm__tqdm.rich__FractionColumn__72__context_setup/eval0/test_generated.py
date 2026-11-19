import pytest
from rich.progress import Progress
from tqdm.rich import FractionColumn
from collections import namedtuple

Task = namedtuple("Task", ["completed", "total"])

def test_fraction_column_no_scale():
    """When unit_scale is False, values are rendered without scaling."""
    col = FractionColumn(unit_scale=False)
    # completed 1500, total 3000 -> should show 1500/3000
    task = Task(completed=1500, total=3000)
    rendered = col.render(task)
    assert isinstance(rendered, str) or hasattr(rendered, "plain")
    # The plain text should contain the exact numbers
    plain = rendered.plain if hasattr(rendered, "plain") else str(rendered)
    assert plain == "1500/3,000 progress.download"

def test_fraction_column_with_scale_and_precision():
    """When unit_scale is True, values are scaled and precision applied."""
    col = FractionColumn(unit_scale=True, unit_divisor=1000)
    # completed 1500, total 3000 -> base 3000 -> unit 1K, precision 1
    task = Task(completed=1500, total=3000)
    rendered = col.render(task)
    plain = rendered.plain if hasattr(rendered, "plain") else str(rendered)
    # 1500/1K = 1.5, 3000/1K = 3.0
    assert plain == "1.5/3.0 K progress.download"

def test_fraction_column_total_none():
    """When total is None, total_str should be '?' and unit derived from completed."""
    col = FractionColumn(unit_scale=True, unit_divisor=1000)
    task = Task(completed=2500, total=None)
    rendered = col.render(task)
    plain = rendered.plain if hasattr(rendered, "plain") else str(rendered)
    # base = completed = 2500 -> unit 1K, precision 1
    # completed/unit = 2.5, total_str = '?'
    assert plain == "2.5/? K progress.download"
