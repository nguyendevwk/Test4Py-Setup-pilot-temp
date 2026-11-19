import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_requests_message_kind_with_prepared_request():
    # Create a minimal PreparedRequest instance
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    # The function should return the REQUEST kind
    assert infer_requests_message_kind(prepared) is RequestsMessageKind.REQUEST

def test_infer_requests_message_kind_with_response():
    # Create a minimal Response instance
    resp = requests.Response()
    resp.status_code = 200
    resp.url = 'https://example.com'
    # The function should return the RESPONSE kind
    assert infer_requests_message_kind(resp) is RequestsMessageKind.RESPONSE

def test_infer_requests_message_kind_with_invalid_type():
    # Pass an unsupported type and expect a TypeError
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind("not a request or response")
    assert "Unexpected message type" in str(excinfo.value)
