import pytest
from sanic.helpers import has_message_body

def test_has_message_body_normal():
    # Status codes in the 2xx range should have a message body
    assert has_message_body(200) is True
    assert has_message_body(201) is True
    assert has_message_body(299) is True

def test_has_message_body_boundary():
    # 1xx, 204, and 304 should not have a message body
    assert has_message_body(100) is False
    assert has_message_body(199) is False
    assert has_message_body(204) is False
    assert has_message_body(304) is False
    # 2xx should still have a body
    assert has_message_body(200) is True

def test_has_message_body_invalid_type():
    # Passing a non-integer should raise a TypeError due to comparison with int
    with pytest.raises(TypeError):
        has_message_body("200")
