import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind


def test_infer_requests_message_kind_prepared_request():
    """PreparedRequest should be identified as REQUEST."""
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST


def test_infer_requests_message_kind_response():
    """Response should be identified as RESPONSE."""
    resp = requests.Response()
    resp.status_code = 200
    kind = infer_requests_message_kind(resp)
    assert kind is RequestsMessageKind.RESPONSE


def test_infer_requests_message_kind_invalid_type():
    """Non-requests objects raise TypeError."""
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind("not a request")
    assert "Unexpected message type" in str(excinfo.value)
