import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_requests_message_kind_with_prepared_request():
    # Create a minimal PreparedRequest
    req = requests.Request('GET', 'http://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST

def test_infer_requests_message_kind_with_response():
    # Create a minimal Response object
    resp = requests.Response()
    resp.status_code = 200
    resp.url = 'http://example.com'
    kind = infer_requests_message_kind(resp)
    assert kind is RequestsMessageKind.RESPONSE

def test_infer_requests_message_kind_with_invalid_type_raises():
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value)
