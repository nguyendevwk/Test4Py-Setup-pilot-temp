import pytest
from apimd.parser import table

def test_table_basic_single_row():
    """Verify that a single row with two columns is rendered correctly."""
    result = table('Name', 'Age', items=[['Alice', '30']])
    expected = (
        "| Name | Age |\n"
        "|:---:|:---:|\n"
        "| Alice | 30 |\n\n"
    )
    assert result == expected

def test_table_multiple_rows_and_long_titles():
    """Check that multiple rows and longer titles produce correct column widths."""
    result = table('First Name', 'Last Name', 'Occupation', items=[
        ['John', 'Doe', 'Engineer'],
        ['Jane', 'Smith', 'Artist']
    ])
    expected = (
        "| First Name | Last Name | Occupation |\n"
        "|:---:|:---:|:---:|\n"
        "| John | Doe | Engineer |\n"
        "| Jane | Smith | Artist |\n\n"
    )
    assert result == expected

def test_table_empty_items_and_single_title():
    """Ensure that an empty items iterable still produces a table header."""
    result = table('Only', items=[])
    expected = (
        "| Only |\n"
        "|:---:|\n\n"
    )
    assert result == expected
