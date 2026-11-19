import pytest
from rich.progress import Text
from tqdm.rich import RateColumn

class DummyTask:
    def __init__(self, speed):
        self.speed = speed

def test_rate_column_with_unit_scale():
    """When unit_scale is True, the column should format the speed with appropriate unit."""
    column = RateColumn(unit="B", unit_scale=True, unit_divisor=1024)
    # 2048 bytes per second should be displayed as 2.0 KiB/s
    task = DummyTask(speed=2048)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    # The rendered text should contain "2.0 KiB/s"
    assert "2.0 KiB/s" in rendered.plain

def test_rate_column_without_unit_scale_and_none_speed():
    """When unit_scale is False and speed is None, the column should display a placeholder."""
    column = RateColumn(unit="B", unit_scale=False)
    task = DummyTask(speed=None)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    # The placeholder should be "? B/s"
    assert rendered.plain == "? B/s"

def test_rate_column_precision_and_suffix():
    """The precision should be 0 when unit is 1, otherwise 1."""
    column = RateColumn(unit="B", unit_scale=False)
    # speed less than divisor, unit will be 1, precision 0
    task1 = DummyTask(speed=500)
    rendered1 = column.render(task1)
    assert rendered1.plain == "500 B/s"
    # speed greater than divisor, unit will be 1000, precision 1
    task2 = DummyTask(speed=1500)
    rendered2 = column.render(task2)
    assert rendered2.plain == "1.5 B/s"
