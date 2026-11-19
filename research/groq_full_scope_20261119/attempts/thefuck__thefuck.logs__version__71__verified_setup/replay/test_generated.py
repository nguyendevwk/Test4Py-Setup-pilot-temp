import sys
import io
import pytest
from thefuck.logs import version

def test_version_normal_output():
    """Verify that the function writes the expected formatted string."""
    buf = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = buf
    try:
        version("2.0.0", "3.11.4", "bash")
    finally:
        sys.stderr = original_stderr
    output = buf.getvalue()
    assert output == "The Fuck 2.0.0 using Python 3.11.4 and bash\n"

def test_version_boundary_empty_strings():
    """Check behavior when empty strings are passed."""
    buf = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = buf
    try:
        version("", "", "")
    finally:
        sys.stderr = original_stderr
    output = buf.getvalue()
    assert output == "The Fuck  using Python  and \n"

def test_version_with_none_values():
    """Ensure that passing None values does not raise an exception and formats correctly."""
    buf = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = buf
    try:
        version(None, None, None)
    finally:
        sys.stderr = original_stderr
    output = buf.getvalue()
    assert output == "The Fuck None using Python None and None\n"
