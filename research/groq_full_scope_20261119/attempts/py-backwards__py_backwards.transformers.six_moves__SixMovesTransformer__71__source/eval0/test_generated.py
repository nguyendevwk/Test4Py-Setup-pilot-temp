import pytest
from py_backwards.transformers.six_moves import SixMovesTransformer
from py_backwards.utils.helpers import eager

# Test 1: Normal rewrite of a moved module
def test_six_moves_rewrite_simple():
    code = "import urllib2\nprint(urllib2.urlopen('http://example.com'))"
    transformed = eager(code, SixMovesTransformer)
    assert "import six.moves.urllib2" in transformed
    assert "urllib2" not in transformed.splitlines()[0]
    assert "six.moves.urllib2" in transformed
    # Ensure the rest of the code remains unchanged
    assert "print(urllib2.urlopen('http://example.com'))" in transformed

# Test 2: Rewrite with alias preservation
def test_six_moves_rewrite_alias():
    code = "import urllib2 as u2\nprint(u2.urlopen('http://example.com'))"
    transformed = eager(code, SixMovesTransformer)
    # The alias should be preserved after rewriting
    assert "import six.moves.urllib2 as u2" in transformed
    assert "u2.urlopen" in transformed
    # Ensure no duplicate import
    assert transformed.count("import six.moves.urllib2") == 1

# Test 3: No rewrite for modules that are not moved
def test_six_moves_no_rewrite_nonexistent():
    code = "import math\nprint(math.sqrt(4))"
    transformed = eager(code, SixMovesTransformer)
    # The import should remain unchanged
    assert "import math" in transformed
    # No six.moves import should appear
    assert "six.moves" not in transformed
    # The rest of the code should be unchanged
    assert "print(math.sqrt(4))" in transformed
