import mimetypes
import pytest
from httpie.utils import get_content_type


def test_get_content_type_known_extension(tmp_path):
    """When a file with a known extension is passed, the correct MIME type is returned."""
    # Create a temporary text file
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Hello, world!")
    # The MIME type for .txt should be 'text/plain'
    assert get_content_type(str(txt_file)) == "text/plain"
    # Ensure that the returned type matches what mimetypes would guess
    assert get_content_type(str(txt_file)) == mimetypes.guess_type(str(txt_file))[0]


def test_get_content_type_unknown_extension(tmp_path):
    """When a file with an unknown extension is passed, None is returned."""
    # Create a temporary file with an uncommon extension
    unknown_file = tmp_path / "data.unknownext"
    unknown_file.write_text("Some data")
    # The MIME type for an unknown extension should be None
    assert get_content_type(str(unknown_file)) is None
    # Verify that mimetypes also returns None for this extension
    assert mimetypes.guess_type(str(unknown_file))[0] is None


def test_get_content_type_invalid_input():
    """Passing an invalid input (None) raises a TypeError."""
    with pytest.raises(TypeError):
        get_content_type(None)
