import pytest
from apimd.parser import table

def test_table_basic():
    # Normal usage with two columns and two rows
    result = table('Name', 'Age', items=[['Alice', '30'], ['Bob', '25']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n"
        "| Bob | 25 |\n\n"
    )
    assert result == expected

def test_table_single_column_and_empty_items():
    # Boundary case: single column title and no items
    result = table('Only', items=[])
    expected = (
        "| Only |\n"
        "|:---:|\n\n"
    )
    assert result == expected

def test_table_invalid_item_type():
    # Error case: item is not a string or iterable of strings
    with pytest.raises(TypeError):
        table('A', 'B', items=[['valid', 'row'], 42])
