import pytest
from httpie.uploads import get_multipart_data_and_content_type
from requests_toolbelt import MultipartEncoder


def test_default_content_type_and_boundary():
    data = {"file": ("test.txt", b"hello", "text/plain")}
    encoder, content_type = get_multipart_data_and_content_type(data)
    assert isinstance(encoder, MultipartEncoder)
    # encoder should contain the original fields
    assert encoder.fields == data
    # content_type should be the default from MultipartEncoder
    assert content_type == encoder.content_type
    # boundary should be present in the content_type
    assert f"boundary={encoder.boundary_value}" in content_type


def test_provided_boundary_overrides_encoder():
    data = {"field": ("name", "value")}
    boundary = "custom-boundary-123"
    encoder, content_type = get_multipart_data_and_content_type(data, boundary=boundary)
    assert isinstance(encoder, MultipartEncoder)
    # boundary should be the one we passed
    assert encoder.boundary_value == boundary
    # content_type should reflect the custom boundary
    assert f"boundary={boundary}" in content_type
    # content_type should still start with multipart/form-data
    assert content_type.startswith("multipart/form-data")


def test_content_type_without_boundary_appends_boundary():
    data = {"foo": ("bar", "baz")}
    custom_ct = "multipart/mixed"
    encoder, content_type = get_multipart_data_and_content_type(data, content_type=custom_ct)
    assert isinstance(encoder, MultipartEncoder)
    # content_type should be the custom one with boundary appended
    assert content_type.startswith(custom_ct)
    assert f"boundary={encoder.boundary_value}" in content_type
    # boundary should not be in the original custom_ct
    assert "boundary=" not in custom_ct
