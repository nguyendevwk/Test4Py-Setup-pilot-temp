import pytest
from rich.progress import Progress, Text
from tqdm.rich import RateColumn

def test_rate_column_with_unit_scale():
    """Test rendering with unit scaling enabled."""
    column = RateColumn(unit="B", unit_scale=True, unit_divisor=1024)
    progress = Progress(column)
    task_id = progress.add_task("download", total=1000)
    # Simulate a speed of 2048 bytes per second
    progress.update(task_id, speed=2048)
    rendered = column.render(progress.tasks[task_id])
    # 2048 bytes/s should be displayed as 2.0 KiB/s
    assert isinstance(rendered, Text)
    assert rendered.plain == "2.0 KiB/s"

def test_rate_column_without_unit_scale():
    """Test rendering with unit scaling disabled."""
    column = RateColumn(unit="B", unit_scale=False)
    progress = Progress(column)
    task_id = progress.add_task("upload", total=500)
    # Simulate a speed of 1234 bytes per second
    progress.update(task_id, speed=1234)
    rendered = column.render(progress.tasks[task_id])
    # Without scaling, the unit should be bytes directly
    assert isinstance(rendered, Text)
    assert rendered.plain == "1234.0 B/s"

def test_rate_column_speed_none():
    """Test rendering when speed is None."""
    column = RateColumn(unit="B", unit_scale=True)
    progress = Progress(column)
    task_id = progress.add_task("process", total=200)
    # Do not set speed; it remains None
    rendered = column.render(progress.tasks[task_id])
    assert isinstance(rendered, Text)
    assert rendered.plain == "? B/s"
