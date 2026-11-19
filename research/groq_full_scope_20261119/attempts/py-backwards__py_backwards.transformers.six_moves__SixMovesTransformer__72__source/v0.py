import importlib
import sys
import types
import pytest

# Import the target transformer and helper
from py_backwards.transformers.six_moves import SixMovesTransformer
from py_backwards.utils.helpers import eager

# Helper to create a temporary module file for testing
def create_module(tmp_path, name, content):
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(content)
    return module_path

def test_rewrite_simple_import(tmp_path):
    """
    Verify that a simple import of a module that has moved to six.moves
    is rewritten correctly.
    """
    code = "import StringIO\nx = StringIO.StringIO('test')"
    transformed = eager(code, transformer=SixMovesTransformer)
    # The import should be rewritten to a from-import from six.moves
    assert "from six.moves import StringIO" in transformed
    # The usage should remain unchanged
    assert "StringIO.StringIO('test')" in transformed
    # Ensure no duplicate imports
    assert transformed.count("StringIO") == 1

def test_rewrite_from_import_and_alias(tmp_path):
    """
    Verify that a from-import of a moved module and an alias are rewritten.
    """
    code = "from StringIO import StringIO as SI\nobj = SI('data')"
    transformed = eager(code, transformer=SixMovesTransformer)
    # Should rewrite to from six.moves import StringIO as SI
    assert "from six.moves import StringIO as SI" in transformed
    # Usage should still refer to SI
    assert "SI('data')" in transformed
    # No other import statements should appear
    assert transformed.count("import StringIO") == 0

def test_no_rewrite_for_non_moved_module(tmp_path):
    """
    Verify that imports of modules not in six.moves are left untouched.
    """
    code = "import json\nprint(json.dumps({'a':1}))"
    transformed = eager(code, transformer=SixMovesTransformer)
    # The import should remain unchanged
    assert "import json" in transformed
    # No six.moves import should be added
    assert "six.moves" not in transformed
    # The code should still functionally be the same
    assert "json.dumps" in transformed
