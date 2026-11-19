import pytest
from sanic.helpers import has_message_body

def test_has_message_body_normal():
    # Status codes that should include a message body
    assert has_message_body(200) is True
    assert has_message_body(201) is True
    assert has_message_body(301) is True

def test_has_message_body_boundary():
    # Status codes that should NOT include a message body
    assert has_message_body(204) is False
    assert has_message_body(304) is False
    assert has_message_body(100) is False
    assert has_message_body(199) is False

def test_has_message_body_invalid_type():
    # Passing a non-integer should raise a TypeError due to comparison
    with pytest.raises(TypeError):
        has_message_body("200")
