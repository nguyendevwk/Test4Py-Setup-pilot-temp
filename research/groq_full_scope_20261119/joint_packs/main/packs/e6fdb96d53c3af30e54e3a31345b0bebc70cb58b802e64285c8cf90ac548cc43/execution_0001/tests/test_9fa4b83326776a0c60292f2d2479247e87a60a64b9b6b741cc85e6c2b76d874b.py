import mimetypes
import pytest
from httpie.utils import get_content_type


def test_known_extension_returns_correct_mime(tmp_path):
    # Create a temporary file with a .txt extension
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Hello, world!")
    # The MIME type for .txt should be text/plain
    assert get_content_type(str(txt_file)) == "text/plain"
    # Verify that mimetypes.guess_type would return the same result
    assert mimetypes.guess_type(str(txt_file), strict=False)[0] == "text/plain"


def test_unknown_extension_returns_none(tmp_path):
    # Create a temporary file with an uncommon extension
    unknown_file = tmp_path / "data.unknownext"
    unknown_file.write_text("Some data")
    # The MIME type for an unknown extension should be None
    assert get_content_type(str(unknown_file)) is None
    # Ensure mimetypes also returns None for the same file
    assert mimetypes.guess_type(str(unknown_file), strict=False)[0] is None


def test_invalid_input_raises_type_error():
    # Passing None should raise a TypeError because guess_type expects a string
    with pytest.raises(TypeError):
        get_content_type(None)
