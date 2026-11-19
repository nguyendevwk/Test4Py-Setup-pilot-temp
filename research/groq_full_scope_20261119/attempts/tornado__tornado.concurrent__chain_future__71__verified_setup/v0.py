import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import chain_future
from tornado.ioloop import IOLoop
from tornado import gen


@pytest.mark.asyncio
async def test_chain_future_success():
    """When future `a` succeeds, `b` receives the same result."""
    loop = asyncio.get_running_loop()
    a = loop.create_future()
    b = loop.create_future()

    chain_future(a, b)

    # Resolve `a` with a value
    a.set_result(42)

    # Wait for `b` to be resolved
    result = await b
    assert result == 42, "b should have the same result as a"


@pytest.mark.asyncio
async def test_chain_future_exception():
    """When future `a` raises an exception, `b` receives the same exception."""
    loop = asyncio.get_running_loop()
    a = loop.create_future()
    b = loop.create_future()

    chain_future(a, b)

    # Resolve `a` with an exception
    exc = ValueError("boom")
    a.set_exception(exc)

    # Awaiting `b` should raise the same exception
    with pytest.raises(ValueError) as e:
        await b
    assert str(e.value) == "boom", "b should propagate the exception from a"


def test_chain_future_b_already_done():
    """If `b` is already completed before `a` finishes, its value should not be overwritten."""
    # Use concurrent.futures.Future for `a` and asyncio.Future for `b`
    a = concurrent.futures.Future()
    b = asyncio.get_event_loop().create_future()

    # Pre-complete `b` with a specific value
    b.set_result("pre-completed")

    # Chain them
    chain_future(a, b)

    # Resolve `a` after a short delay
    def resolve_a():
        a.set_result("new value")

    IOLoop.current().add_timeout(0, resolve_a)

    # Run the IOLoop briefly to allow callbacks to execute
    IOLoop.current().add_timeout(0.01, IOLoop.current().stop)
    IOLoop.current().start()

    # Verify that `b` still holds the original value
    assert b.result() == "pre-completed", "b should not be overwritten if already done"
