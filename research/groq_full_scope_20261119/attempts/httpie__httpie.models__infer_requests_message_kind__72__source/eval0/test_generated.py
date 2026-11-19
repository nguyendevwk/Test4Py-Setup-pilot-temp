import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_prepared_request_returns_request_kind():
    # Create a simple PreparedRequest
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST, "PreparedRequest should infer to REQUEST kind"

def test_infer_response_returns_response_kind():
    # Create a Response object by making a real request to a known URL
    # Use a lightweight request to avoid network dependency issues
    response = requests.get('https://httpbin.org/get')
    kind = infer_requests_message_kind(response)
    assert kind is RequestsMessageKind.RESPONSE, "Response should infer to RESPONSE kind"

def test_infer_invalid_type_raises_type_error():
    # Pass an object that is neither PreparedRequest nor Response
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value), "TypeError message should indicate unexpected type"
