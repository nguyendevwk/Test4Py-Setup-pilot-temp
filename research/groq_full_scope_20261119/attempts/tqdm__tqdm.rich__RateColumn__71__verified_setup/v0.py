import pytest
from rich.text import Text
from tqdm.rich import RateColumn

class DummyTask:
    def __init__(self, speed):
        self.speed = speed

def test_rate_column_with_unit_scale():
    """Test rendering with unit scaling enabled."""
    task = DummyTask(speed=1500)  # 1.5 KB/s
    column = RateColumn(unit="B", unit_scale=True, unit_divisor=1000)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    # Expected: "1.5 K B/s" (precision 1 because unit != 1)
    assert rendered.plain == "1.5 K B/s"

def test_rate_column_without_unit_scale():
    """Test rendering with unit scaling disabled."""
    task = DummyTask(speed=1500)  # 1500 B/s
    column = RateColumn(unit="B", unit_scale=False)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    # Expected: "1500 B/s" (precision 0 because unit == 1)
    assert rendered.plain == "1500 B/s"

def test_rate_column_speed_none():
    """Test rendering when task speed is None."""
    task = DummyTask(speed=None)
    column = RateColumn(unit="B", unit_scale=True)
    rendered = column.render(task)
    assert isinstance(rendered, Text)
    # Expected placeholder with unit
    assert rendered.plain == "? B/s"
