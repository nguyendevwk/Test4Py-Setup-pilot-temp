import io
import os
import pytest
from httpie.uploads import get_multipart_data_and_content_type

def test_basic_string_field(tmp_path):
    # Prepare a simple multipart data dict with a string field
    data = {"field1": "value1"}
    encoder, content_type = get_multipart_data_and_content_type(data)

    # The encoder should be a MultipartEncoder instance
    assert hasattr(encoder, "fields")
    assert encoder.fields == data

    # Content type should start with multipart/form-data and contain the boundary
    assert content_type.startswith("multipart/form-data; boundary=")
    boundary = content_type.split("boundary=")[1]
    assert boundary == encoder.boundary_value

def test_custom_boundary(tmp_path):
    # Prepare a multipart data dict with a file field
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    with open(file_path, "rb") as f:
        data = {"file": ("test.txt", f, "text/plain")}

    custom_boundary = "my-custom-boundary-12345"
    encoder, content_type = get_multipart_data_and_content_type(
        data, boundary=custom_boundary
    )

    # The encoder should use the custom boundary
    assert encoder.boundary_value == custom_boundary
    assert content_type.endswith(custom_boundary)

def test_content_type_handling(tmp_path):
    # Prepare a multipart data dict with a string field
    data = {"field2": "value2"}

    # Case 1: content_type without boundary
    ct_no_boundary = "multipart/form-data"
    encoder1, content_type1 = get_multipart_data_and_content_type(
        data, content_type=ct_no_boundary
    )
    assert content_type1.startswith(ct_no_boundary)
    assert "boundary=" in content_type1
    assert content_type1.endswith(encoder1.boundary_value)

    # Case 2: content_type with boundary already present
    ct_with_boundary = f"multipart/form-data; boundary={encoder1.boundary_value}"
    encoder2, content_type2 = get_multipart_data_and_content_type(
        data, content_type=ct_with_boundary
    )
    assert content_type2 == ct_with_boundary
    assert encoder2.boundary_value == encoder1.boundary_value
