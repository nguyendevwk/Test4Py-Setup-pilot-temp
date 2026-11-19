import pytest
from rich.progress import Progress
from tqdm.rich import FractionColumn

def test_fraction_column_with_unit_scale_true(tmp_path):
    """When unit_scale is True, the column should scale units appropriately."""
    column = FractionColumn(unit_scale=True, unit_divisor=1000)
    progress = Progress(column)
    task_id = progress.add_task("test", total=3000)
    progress.update(task_id, completed=1500)
    rendered = column.render(progress.tasks[0])
    # With unit_divisor=1000, 3000 bytes -> 3.0 K, 1500 -> 1.5 K
    assert rendered.plain == "1.5/3.0 K"
    assert rendered.style == "progress.download"

def test_fraction_column_with_unit_scale_false(tmp_path):
    """When unit_scale is False, no scaling should occur and precision is zero."""
    column = FractionColumn(unit_scale=False)
    progress = Progress(column)
    task_id = progress.add_task("test", total=3000)
    progress.update(task_id, completed=1500)
    rendered = column.render(progress.tasks[0])
    # No scaling: 1500/3000 with zero decimal places
    assert rendered.plain == "1500/3000 "
    assert rendered.style == "progress.download"

def test_fraction_column_total_none(tmp_path):
    """When the task has no total, the column should display '?' for total."""
    column = FractionColumn(unit_scale=True, unit_divisor=1000)
    progress = Progress(column)
    task_id = progress.add_task("test")  # total defaults to None
    progress.update(task_id, completed=500)
    rendered = column.render(progress.tasks[0])
    # Base is 500, unit 1, precision 0, total is unknown
    assert rendered.plain == "500/? "
    assert rendered.style == "progress.download"
