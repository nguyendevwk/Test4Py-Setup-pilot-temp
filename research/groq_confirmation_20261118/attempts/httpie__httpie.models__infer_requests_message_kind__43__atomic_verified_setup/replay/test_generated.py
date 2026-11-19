import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_requests_message_kind_with_prepared_request():
    # Create a simple PreparedRequest instance
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    # The function should identify it as a REQUEST
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_with_response():
    # Create a Response instance by performing a real request to a known endpoint
    # Use httpbin.org which is reliable for testing
    resp = requests.get('https://httpbin.org/get')
    # The function should identify it as a RESPONSE
    kind = infer_requests_message_kind(resp)
    assert kind is RequestsMessageKind.RESPONSE
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_with_invalid_type():
    # Passing an unsupported type should raise a TypeError
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value)
    assert "Dummy" in str(excinfo.value)
