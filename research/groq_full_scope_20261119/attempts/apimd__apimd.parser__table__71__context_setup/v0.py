import pytest
from apimd.parser import table

def test_table_basic():
    """Normal case with two columns and two rows."""
    result = table('Name', 'Age', items=[['Alice', '30'], ['Bob', '25']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n"
        "| Bob | 25 |\n\n"
    )
    assert result == expected

def test_table_single_column_and_single_row():
    """Boundary case with one column and one row."""
    result = table('Only', items=[['Single']])
    expected = (
        "| Only |\n"
        "|:---:|\n"
        "| Single |\n\n"
    )
    assert result == expected

def test_table_empty_items():
    """Error/edge case: empty items iterable should produce only header and split."""
    result = table('Col1', 'Col2', items=[])
    expected = (
        "| Col1 | Col2 |\n"
        "|:---:|:---:|\n\n"
    )
    assert result == expected
