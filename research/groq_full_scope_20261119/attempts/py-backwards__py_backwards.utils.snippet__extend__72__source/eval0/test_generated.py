import ast
import pytest
from py_backwards.utils.snippet import extend

def test_extend_with_assignments(tmp_path):
    # Create a temporary file with two assignments
    code = "x = 1\nx = 2\nprint(x)\n"
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    # Parse the file into an AST
    tree = ast.parse(code, filename=str(file_path))
    # Find all assignment nodes
    assigns = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)]
    # Capture the original number of assignments
    original_count = len(assigns)

    # Call extend on the list of assignments
    extend(assigns)

    # After extend, the list should contain the original assignments plus any new ones
    assert len(assigns) >= original_count
    # Ensure that the original assignments are still present
    for node in assigns[:original_count]:
        assert isinstance(node, ast.Assign)

def test_extend_with_empty_list():
    # Extending an empty list should simply leave it empty
    assigns = []
    extend(assigns)
    assert assigns == []

def test_extend_with_invalid_input():
    # Passing a non-list should raise a TypeError
    with pytest.raises(TypeError):
        extend("not a list")
