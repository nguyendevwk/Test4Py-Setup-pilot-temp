import io
import os
import pytest
from httpie.uploads import get_multipart_data_and_content_type

def test_normal_multipart_with_file(tmp_path):
    # Create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    # Prepare multipart data: a text field and a file field
    data = {
        "field1": "value1",
        "file1": ("test.txt", open(file_path, "rb"), "text/plain"),
    }
    encoder, content_type = get_multipart_data_and_content_type(data)
    # The encoder should be a MultipartEncoder instance
    assert hasattr(encoder, "fields") and encoder.fields == data
    # Content type should include the boundary
    assert content_type.startswith("multipart/form-data; boundary=")
    # The boundary in content_type should match encoder.boundary_value
    assert encoder.boundary_value in content_type
    # The encoder should produce a bytes payload containing the file content
    payload = encoder.to_string()
    assert b"hello world" in payload
    # Clean up the opened file
    encoder.fields["file1"][1].close()

def test_boundary_override_and_custom_content_type():
    # Prepare simple multipart data
    data = {"foo": "bar"}
    # Provide a custom boundary and content type
    boundary = "myboundary123"
    custom_ct = "multipart/form-data; charset=utf-8"
    encoder, content_type = get_multipart_data_and_content_type(
        data, boundary=boundary, content_type=custom_ct
    )
    # The encoder should use the provided boundary
    assert encoder.boundary_value == boundary
    # The content type should include the boundary appended
    assert content_type == f"{custom_ct}; boundary={boundary}"
    # The payload should contain the field value
    payload = encoder.to_string()
    assert b"bar" in payload

def test_invalid_input_raises_type_error():
    # Passing a non-dict (e.g., a list) should raise a TypeError
    with pytest.raises(TypeError):
        get_multipart_data_and_content_type(["not", "a", "dict"])
