import pytest
from rich.progress import Progress, TaskID
from tqdm.rich import FractionColumn


def _create_progress_and_task(total: float | None = None) -> tuple[Progress, TaskID]:
    """Helper to create a Progress instance and add a task."""
    progress = Progress()
    task_id = progress.add_task("test", total=total)
    return progress, task_id


def test_fraction_column_basic():
    """Test rendering with default settings (no unit scaling)."""
    progress, task_id = _create_progress_and_task(total=5)
    progress.update(task_id, completed=2)

    column = FractionColumn()
    rendered = column.render(progress.tasks[task_id])
    # Without scaling, unit is 1 and precision 0
    assert rendered.plain == "2/5 "
    assert rendered.style == "progress.download"


def test_fraction_column_unit_scale():
    """Test rendering with unit scaling enabled."""
    progress, task_id = _create_progress_and_task(total=1500)
    progress.update(task_id, completed=750)

    column = FractionColumn(unit_scale=True, unit_divisor=1000)
    rendered = column.render(progress.tasks[task_id])
    # 1500 bytes -> 1.5K, 750 bytes -> 0.8K (rounded to 1 decimal)
    assert rendered.plain == "0.8/1.5 K"
    assert rendered.style == "progress.download"


def test_fraction_column_no_total():
    """Test rendering when total is unknown (generator-like task)."""
    progress, task_id = _create_progress_and_task(total=None)
    progress.update(task_id, completed=123)

    column = FractionColumn()
    rendered = column.render(progress.tasks[task_id])
    # Total is unknown, should display '?' for total
    assert rendered.plain == "123/? "
    assert rendered.style == "progress.download"
