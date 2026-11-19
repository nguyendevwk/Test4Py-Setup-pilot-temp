import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_prepared_request_returns_request_kind():
    # Create a simple PreparedRequest object
    req = requests.Request(method="GET", url="https://example.com")
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST, "PreparedRequest should be inferred as REQUEST"

def test_infer_response_returns_response_kind():
    # Create a simple Response object
    resp = requests.Response()
    resp.status_code = 200
    resp.url = "https://example.com"
    kind = infer_requests_message_kind(resp)
    assert kind is RequestsMessageKind.RESPONSE, "Response should be inferred as RESPONSE"

def test_infer_invalid_type_raises_type_error():
    # Pass an unsupported type and verify TypeError is raised
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind("not a request or response")
    assert "Unexpected message type" in str(excinfo.value), "Error message should mention unexpected type"
