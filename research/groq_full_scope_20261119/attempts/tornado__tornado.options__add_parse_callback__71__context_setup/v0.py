import pytest
from tornado.options import add_parse_callback, options

def test_add_parse_callback_invoked_after_parsing(tmp_path):
    # Arrange: create a flag that will be set by the callback
    called = {"flag": False}
    def callback():
        called["flag"] = True

    # Act: register callback and parse empty args
    add_parse_callback(callback)
    options.parse_args([])

    # Assert: callback was invoked
    assert called["flag"] is True

def test_multiple_callbacks_invoked_in_order(tmp_path):
    # Arrange: two callbacks that record their order of execution
    order = []
    def first():
        order.append("first")
    def second():
        order.append("second")

    add_parse_callback(first)
    add_parse_callback(second)

    # Act: parse empty args
    options.parse_args([])

    # Assert: callbacks executed in the order they were added
    assert order == ["first", "second"]

def test_add_parse_callback_with_invalid_argument_raises():
    # Arrange: non-callable argument
    invalid = 42

    # Act & Assert: TypeError should be raised
    with pytest.raises(TypeError):
        add_parse_callback(invalid)
