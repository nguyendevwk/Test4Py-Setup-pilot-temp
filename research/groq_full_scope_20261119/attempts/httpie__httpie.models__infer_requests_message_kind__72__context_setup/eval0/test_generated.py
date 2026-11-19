import pytest
import requests
from httpie.models import infer_requests_message_kind, RequestsMessageKind, RequestsMessage

def test_infer_requests_message_kind_with_prepared_request():
    # Create a simple PreparedRequest instance
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    # The function should identify it as a REQUEST kind
    kind = infer_requests_message_kind(prepared)
    assert kind is RequestsMessageKind.REQUEST
    assert isinstance(kind, RequestsMessageKind)

def test_infer_requests_message_kind_with_response_and_subclass():
    # Create a Response instance
    resp = requests.Response()
    resp.status_code = 200
    # The function should identify it as a RESPONSE kind
    kind_resp = infer_requests_message_kind(resp)
    assert kind_resp is RequestsMessageKind.RESPONSE

    # Create a subclass of PreparedRequest to test subclass handling
    class CustomPreparedRequest(requests.PreparedRequest):
        pass
    custom_req = CustomPreparedRequest()
    kind_custom = infer_requests_message_kind(custom_req)
    assert kind_custom is RequestsMessageKind.REQUEST

def test_infer_requests_message_kind_with_invalid_type_raises():
    # Pass an object that is neither PreparedRequest nor Response
    class Dummy: pass
    dummy = Dummy()
    with pytest.raises(TypeError) as excinfo:
        infer_requests_message_kind(dummy)
    assert "Unexpected message type" in str(excinfo.value)
    assert excinfo.type is TypeError
