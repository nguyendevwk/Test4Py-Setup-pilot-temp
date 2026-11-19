import pytest
from tqdm.rich import FractionColumn
from rich.progress import Text


class DummyTask:
    def __init__(self, completed, total):
        self.completed = completed
        self.total = total


def test_fraction_column_without_scaling():
    """When unit_scale is False, the column should display raw numbers."""
    col = FractionColumn(unit_scale=False)
    task = DummyTask(completed=5, total=10)
    result = col.render(task)
    assert isinstance(result, Text)
    # With no scaling, unit is 1, precision 0, suffix empty
    assert result.plain == "5/10 "
    # Style should be set correctly
    assert result.style == "progress.download"


def test_fraction_column_with_scaling_large_numbers():
    """When unit_scale is True, large numbers should be scaled appropriately."""
    col = FractionColumn(unit_scale=True, unit_divisor=1000)
    task = DummyTask(completed=1500, total=4500)
    result = col.render(task)
    assert isinstance(result, Text)
    # 1500 bytes -> 1.5K, 4500 bytes -> 4.5K
    assert result.plain == "1.5K/4.5K "
    assert result.style == "progress.download"


def test_fraction_column_no_total():
    """When total is None, the column should display '?' for total."""
    col = FractionColumn(unit_scale=False)
    task = DummyTask(completed=3, total=None)
    result = col.render(task)
    assert isinstance(result, Text)
    # total is unknown, so '?' is shown
    assert result.plain == "3/? "
    assert result.style == "progress.download"
