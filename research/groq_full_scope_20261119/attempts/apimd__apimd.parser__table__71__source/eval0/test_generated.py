import pytest
from apimd.parser import table

def test_table_basic():
    """Normal usage with two columns and two rows."""
    result = table('Name', 'Age', items=[['Alice', '30'], ['Bob', '25']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n"
        "| Bob | 25 |\n\n"
    )
    assert result == expected

def test_table_single_column_and_empty_items():
    """Boundary case: single column and no rows."""
    result = table('Only', items=[])
    expected = (
        "| Only |\n"
        "|:---:|\n\n"
    )
    assert result == expected

def test_table_mismatched_row_length():
    """Error scenario: row with fewer columns than titles."""
    with pytest.raises(IndexError):
        table('A', 'B', items=[['only_one']])
