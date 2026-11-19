import pytest
import requests
from httpie.models import infer_requests_message_kind
from httpie.models import RequestsMessageKind

def test_infer_requests_message_kind_with_prepared_request():
    # Create a simple PreparedRequest
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_with_response():
    # Use requests to get a Response object
    resp = requests.get('https://httpbin.org/status/200')
    kind = infer_requests_message_kind(resp)
    assert kind is RequestsMessageKind.RESPONSE
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_with_invalid_type_raises():
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value)
    assert "Dummy" in str(excinfo.value)
