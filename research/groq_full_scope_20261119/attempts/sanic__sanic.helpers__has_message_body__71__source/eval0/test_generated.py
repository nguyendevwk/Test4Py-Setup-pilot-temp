import pytest
from sanic.helpers import has_message_body

def test_has_message_body_normal_cases():
    # Typical success status codes should allow a message body
    assert has_message_body(200) is True
    assert has_message_body(201) is True
    assert has_message_body(299) is True

def test_has_message_body_boundary_cases():
    # Status codes that must not include a message body
    assert has_message_body(204) is False   # No Content
    assert has_message_body(304) is False   # Not Modified
    # 1xx informational responses also exclude a body
    assert has_message_body(100) is False
    assert has_message_body(199) is False

def test_has_message_body_invalid_input():
    # Passing a non‑integer should raise a TypeError due to comparison with int
    with pytest.raises(TypeError):
        has_message_body("200")
