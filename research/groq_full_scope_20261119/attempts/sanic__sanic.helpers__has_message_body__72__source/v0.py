import pytest
from sanic.helpers import has_message_body

def test_has_message_body_normal_cases(tmp_path):
    # Status codes that should include a message body
    assert has_message_body(200) is True
    assert has_message_body(301) is True
    assert has_message_body(500) is True

def test_has_message_body_boundary_cases(tmp_path):
    # Status codes that should NOT include a message body
    assert has_message_body(204) is False
    assert has_message_body(304) is False
    assert has_message_body(100) is False
    assert has_message_body(199) is False
    assert has_message_body(101) is False

def test_has_message_body_invalid_input(tmp_path):
    # Passing a non-integer should raise a TypeError
    with pytest.raises(TypeError):
        has_message_body("200")
