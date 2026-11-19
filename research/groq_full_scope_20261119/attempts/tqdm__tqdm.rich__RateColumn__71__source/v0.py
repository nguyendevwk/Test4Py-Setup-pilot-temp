import pytest
from rich.progress import Text
from tqdm.rich import RateColumn

class DummyTask:
    def __init__(self, speed):
        self.speed = speed

def test_rate_column_with_speed_and_unit_scale():
    """When unit_scale is True, the column should format the speed with appropriate unit."""
    column = RateColumn(unit="B", unit_scale=True, unit_divisor=1024)
    task = DummyTask(speed=2048)  # 2 KiB/s
    rendered = column.render(task)
    # Expect "2.0 KiB/s" (KiB because 2048/1024 = 2)
    assert isinstance(rendered, Text)
    assert rendered.plain == "2.0 KiB/s"
    assert rendered.style == "progress.data.speed"

def test_rate_column_with_speed_and_no_unit_scale():
    """When unit_scale is False, the column should not scale the unit and use the raw speed."""
    column = RateColumn(unit="B", unit_scale=False)
    task = DummyTask(speed=1234)
    rendered = column.render(task)
    # Expect "1234.0 B/s" (no scaling)
    assert isinstance(rendered, Text)
    assert rendered.plain == "1234.0 B/s"
    assert rendered.style == "progress.data.speed"

def test_rate_column_with_no_speed():
    """When the task has no speed, the column should display a placeholder."""
    column = RateColumn(unit="B")
    task = DummyTask(speed=None)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    assert rendered.plain == "? B/s"
    assert rendered.style == "progress.data.speed"
