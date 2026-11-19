import pytest
from genty.genty_args import GentyArgs, format_arg, format_kwarg

def test_genty_args_iteration_yields_formatted_and_sorted_values():
    # Arrange: create GentyArgs with positional and keyword arguments
    positional = (42, "hello")
    keyword = {"z": 3, "a": 1, "m": 2}
    genty = GentyArgs(*positional, **keyword)

    # Act: iterate over the GentyArgs instance
    result = list(genty)

    # Assert: positional args are formatted first
    expected_positional = [format_arg(arg) for arg in positional]
    # Assert: keyword args are sorted by key and formatted
    expected_keyword = [format_kwarg(k, v) for k, v in sorted(keyword.items())]
    assert result == expected_positional + expected_keyword
