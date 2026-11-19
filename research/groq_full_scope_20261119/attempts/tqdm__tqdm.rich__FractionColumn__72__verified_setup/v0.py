import pytest
from rich.progress import Text
from tqdm.rich import FractionColumn

class DummyTask:
    def __init__(self, completed, total):
        self.completed = completed
        self.total = total

def test_fraction_column_no_scale_with_total():
    """When unit_scale is False, the column should display raw numbers."""
    col = FractionColumn(unit_scale=False)
    task = DummyTask(completed=1500, total=3000)
    result = col.render(task)
    # unit is 1, precision 0, so numbers are integers
    assert isinstance(result, Text)
    assert result.plain == "1500/3000 "
    # style should be set correctly
    assert result.style == "progress.download"

def test_fraction_column_scale_with_total():
    """When unit_scale is True, the column should scale numbers to appropriate units."""
    col = FractionColumn(unit_scale=True, unit_divisor=1000)
    task = DummyTask(completed=1500, total=3000)
    result = col.render(task)
    # With divisor 1000, 1500 -> 1.5K, 3000 -> 3.0K
    assert isinstance(result, Text)
    assert result.plain == "1.5K/3.0K "
    assert result.style == "progress.download"

def test_fraction_column_no_total():
    """When total is None, the column should display '?' for total."""
    col = FractionColumn(unit_scale=True, unit_divisor=1000)
    task = DummyTask(completed=1500, total=None)
    result = col.render(task)
    # Base is completed (1500), so unit 1.5K
    assert isinstance(result, Text)
    assert result.plain == "1.5K/? "
    assert result.style == "progress.download"
