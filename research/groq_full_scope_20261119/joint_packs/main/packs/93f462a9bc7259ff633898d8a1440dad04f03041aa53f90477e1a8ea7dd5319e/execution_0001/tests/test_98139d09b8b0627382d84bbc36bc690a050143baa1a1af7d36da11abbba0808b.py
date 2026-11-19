import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_prepared_request_returns_request_kind():
    # Create a simple PreparedRequest
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST, (
        f"Expected RequestsMessageKind.REQUEST, got {kind}"
    )

def test_infer_response_returns_response_kind():
    # Use requests to get a Response object
    response = requests.get('https://httpbin.org/get')
    kind = infer_requests_message_kind(response)
    assert kind is RequestsMessageKind.RESPONSE, (
        f"Expected RequestsMessageKind.RESPONSE, got {kind}"
    )

def test_infer_invalid_type_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind("not a request or response")
    assert "Unexpected message type" in str(excinfo.value)
