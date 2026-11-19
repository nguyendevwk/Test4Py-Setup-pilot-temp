import pytest
from sanic.exceptions import WebsocketClosed
from sanic.exceptions import SanicException

def test_websocket_closed_attributes():
    """Verify that WebsocketClosed has the expected attributes."""
    exc = WebsocketClosed()
    # The exception should be quiet and have the correct message
    assert exc.quiet is True
    assert exc.message == "Client has closed the websocket connection"
    # It should be an instance of SanicException
    assert isinstance(exc, SanicException)
    # The string representation should include the message
    assert str(exc) == exc.message

def test_websocket_closed_raises_and_catches():
    """Ensure that raising WebsocketClosed propagates correctly."""
    with pytest.raises(WebsocketClosed) as excinfo:
        raise WebsocketClosed("Client closed")
    # The exception message should be the one passed to the constructor
    assert str(excinfo.value) == "Client closed"

def test_websocket_closed_in_context_manager(tmp_path):
    """Test that WebsocketClosed can be used in a context manager and cleaned up."""
    # Create a temporary file to simulate a resource that might raise WebsocketClosed
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("data")
    # Define a context manager that raises WebsocketClosed when exiting
    class DummyContext:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            raise WebsocketClosed("Context closed")
    with pytest.raises(WebsocketClosed) as excinfo:
        with DummyContext():
            pass
    assert str(excinfo.value) == "Context closed"
