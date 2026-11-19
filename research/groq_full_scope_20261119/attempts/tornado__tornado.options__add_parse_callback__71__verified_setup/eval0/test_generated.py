import pytest
from tornado.options import add_parse_callback, options


def test_callback_invoked_after_parsing():
    """The callback should be called once parsing is finished."""
    called = False

    def cb():
        nonlocal called
        called = True

    add_parse_callback(cb)
    # Trigger parsing by accessing a known option (e.g., help)
    options.parse_command_line([])
    assert called, "Callback was not invoked after parsing"


def test_multiple_callbacks_called_in_order():
    """Multiple callbacks should be called in the order they were added."""
    order = []

    def first():
        order.append("first")

    def second():
        order.append("second")

    add_parse_callback(first)
    add_parse_callback(second)
    options.parse_command_line([])
    assert order == ["first", "second"], f"Callbacks called in wrong order: {order}"


def test_add_parse_callback_with_non_callable_raises():
    """Providing a non-callable to add_parse_callback should raise a TypeError."""
    with pytest.raises(TypeError):
        add_parse_callback(42)  # type: ignore[arg-type]
