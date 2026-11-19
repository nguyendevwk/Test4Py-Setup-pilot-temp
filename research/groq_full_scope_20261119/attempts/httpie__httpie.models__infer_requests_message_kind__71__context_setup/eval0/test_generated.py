import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind, RequestsMessage

def test_infer_requests_message_kind_request():
    # Create a simple PreparedRequest and verify the kind is REQUEST
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    assert isinstance(prepared, requests.PreparedRequest)
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_response():
    # Create a Response object via a Session and verify the kind is RESPONSE
    session = requests.Session()
    # Use a dummy request to get a Response object
    response = session.get('https://httpbin.org/get')
    assert isinstance(response, requests.Response)
    kind = infer_requests_message_kind(response)
    assert kind is RequestsMessageKind.RESPONSE
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_invalid_type():
    # Pass an object that is neither PreparedRequest nor Response and expect TypeError
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value)
