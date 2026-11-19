import mimetypes
import pytest
from httpie.utils import get_content_type


def test_known_extension_returns_correct_mime(tmp_path):
    # Create a temporary file with a .txt extension
    txt_file = tmp_path / "example.txt"
    txt_file.write_text("sample")
    # The function should return the MIME type for .txt files
    assert get_content_type(str(txt_file)) == "text/plain"
    # Verify that mimetypes also recognizes the same type
    assert mimetypes.guess_type(str(txt_file), strict=False)[0] == "text/plain"


def test_unknown_extension_returns_none(tmp_path):
    # Create a temporary file with an uncommon extension
    unknown_file = tmp_path / "data.unknownext"
    unknown_file.write_text("data")
    # The function should return None for an unknown MIME type
    assert get_content_type(str(unknown_file)) is None
    # Confirm that mimetypes also returns None for this extension
    assert mimetypes.guess_type(str(unknown_file), strict=False)[0] is None


def test_invalid_input_raises_type_error():
    # Passing a non-string (None) should raise a TypeError
    with pytest.raises(TypeError):
        get_content_type(None)
