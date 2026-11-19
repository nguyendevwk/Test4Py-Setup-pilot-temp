import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind

def test_infer_requests_message_kind_with_prepared_request():
    # Create a simple PreparedRequest
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST, "Expected REQUEST kind for PreparedRequest"

def test_infer_requests_message_kind_with_response():
    # Create a Response object by performing a real request
    # Use a minimal request to avoid network dependency by mocking the session
    # Since we cannot mock, we construct a Response manually
    response = requests.Response()
    response.status_code = 200
    response._content = b'{}'
    response.url = 'https://example.com'
    kind = infer_requests_message_kind(response)
    assert kind is RequestsMessageKind.RESPONSE, "Expected RESPONSE kind for Response"

def test_infer_requests_message_kind_with_invalid_type_raises():
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind("not a request or response")
    assert "Unexpected message type" in str(excinfo.value), "Expected TypeError for invalid message type"
