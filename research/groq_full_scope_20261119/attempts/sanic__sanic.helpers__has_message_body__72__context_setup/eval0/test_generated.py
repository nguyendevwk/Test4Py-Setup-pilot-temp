import pytest
from sanic.helpers import has_message_body

def test_has_message_body_normal_cases():
    # 200 OK should have a message body
    assert has_message_body(200) is True
    # 201 Created should have a message body
    assert has_message_body(201) is True
    # 204 No Content should NOT have a message body
    assert has_message_body(204) is False
    # 304 Not Modified should NOT have a message body
    assert has_message_body(304) is False
    # 100 Continue should NOT have a message body
    assert has_message_body(100) is False
    # 199 should NOT have a message body
    assert has_message_body(199) is False
    # 300 Multiple Choices should have a message body
    assert has_message_body(300) is True

def test_has_message_body_boundary_values():
    # Edge of 1xx range: 199 should be False
    assert has_message_body(199) is False
    # Edge of 2xx range: 200 should be True
    assert has_message_body(200) is True
    # Edge of 3xx range: 300 should be True
    assert has_message_body(300) is True
    # Edge of 4xx range: 400 should be True
    assert has_message_body(400) is True
    # Edge of 5xx range: 500 should be True
    assert has_message_body(500) is True

def test_has_message_body_invalid_input():
    # Passing a string should raise a TypeError due to comparison with int
    with pytest.raises(TypeError):
        has_message_body("200")
    # Passing a float should raise a TypeError
    with pytest.raises(TypeError):
        has_message_body(200.0)
    # Passing None should raise a TypeError
    with pytest.raises(TypeError):
        has_message_body(None)
