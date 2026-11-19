import pytest
from apimd.parser import table

def test_table_normal():
    """Normal usage with two titles and two rows."""
    result = table('Name', 'Age', items=[['Alice', '30'], ['Bob', '25']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n"
        "| Bob | 25 |\n\n"
    )
    assert result == expected

def test_table_empty_items():
    """Boundary case: no items provided."""
    result = table('Header', items=[])
    expected = (
        "| Header |\n"
        "|:---:|\n\n"
    )
    assert result == expected

def test_table_invalid_item_type():
    """Error case: item is not a string or iterable of strings."""
    with pytest.raises(TypeError):
        # Passing an integer will cause a TypeError when _table_cell tries to iterate it
        table('X', items=[1])
