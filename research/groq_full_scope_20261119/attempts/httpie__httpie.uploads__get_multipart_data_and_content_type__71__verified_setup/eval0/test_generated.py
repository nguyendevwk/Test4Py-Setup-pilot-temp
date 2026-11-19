import pytest
from httpie.uploads import get_multipart_data_and_content_type
from requests_toolbelt import MultipartEncoder


def test_default_content_type_and_boundary(tmp_path):
    # Create a simple multipart data dict with a file field
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    data = {
        "field1": "value1",
        "file": ("test.txt", open(file_path, "rb"), "text/plain"),
    }

    encoder, content_type = get_multipart_data_and_content_type(data)

    # The returned encoder should be a MultipartEncoder instance
    assert isinstance(encoder, MultipartEncoder)

    # The content type should match the encoder's content type
    assert content_type == encoder.content_type

    # The encoder's fields should match the original data
    # Note: MultipartEncoder stores fields as a list of tuples
    assert dict(encoder.fields) == {
        "field1": "value1",
        "file": ("test.txt", open(file_path, "rb"), "text/plain"),
    }

    # The boundary should be present in the content type
    assert "boundary=" in content_type
    assert encoder.boundary_value in content_type


def test_custom_boundary_and_content_type(tmp_path):
    # Prepare data with a file field
    file_path = tmp_path / "image.png"
    file_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    data = {
        "image": ("image.png", open(file_path, "rb"), "image/png"),
    }

    # Provide a custom boundary
    custom_boundary = "my_boundary_123"

    # Provide a custom content type without boundary
    custom_content_type = "multipart/form-data"

    encoder, content_type = get_multipart_data_and_content_type(
        data, boundary=custom_boundary, content_type=custom_content_type
    )

    # The encoder should use the custom boundary
    assert encoder.boundary_value == custom_boundary

    # The content type should be updated to include the boundary
    assert content_type == f"{custom_content_type}; boundary={custom_boundary}"


def test_content_type_with_existing_boundary(tmp_path):
    # Prepare data with a simple field
    data = {"name": "Alice"}

    # Provide a content type that already contains a boundary
    existing_boundary = "existing_boundary_456"
    content_type_with_boundary = f"multipart/form-data; boundary={existing_boundary}"

    encoder, content_type = get_multipart_data_and_content_type(
        data, content_type=content_type_with_boundary
    )

    # The encoder should still use its own boundary
    assert encoder.boundary_value != existing_boundary

    # The returned content type should remain unchanged
    assert content_type == content_type_with_boundary
