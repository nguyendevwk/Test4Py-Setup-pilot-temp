import pytest
from apimd.parser import table

def test_table_two_columns_basic():
    """Verify that a simple two‑column table is rendered correctly."""
    result = table('Name', 'Age', items=[['Alice', '30'], ['Bob', '25']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n"
        "| Bob | 25 |\n\n"
    )
    assert result == expected

def test_table_single_column_strings():
    """When items are strings, each string should become a single‑column row."""
    result = table('Item', items=['apple', 'banana', 'cherry'])
    expected = (
        "| Item |\n"
        "|:---:|\n"
        "| apple |\n"
        "| banana |\n"
        "| cherry |\n\n"
    )
    assert result == expected

def test_table_empty_items_returns_header_and_split_only():
    """An empty items iterable should produce only the header and split line."""
    result = table('Header', items=[])
    expected = (
        "| Header |\n"
        "|:---:|\n\n"
    )
    assert result == expected
