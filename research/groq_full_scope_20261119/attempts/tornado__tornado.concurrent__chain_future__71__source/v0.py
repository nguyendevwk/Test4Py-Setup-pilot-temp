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

    # Wait for `b` to be resolved and check the exception
    with pytest.raises(ValueError) as e:
        await b
    assert str(e.value) == "boom", "b should propagate the exception from a"


def test_chain_future_b_already_done():
    """If `b` is already completed before `a` finishes, its value should not change."""
    # Use concurrent.futures.Future for `a` to test the IOLoop path
    a = concurrent.futures.Future()
    b = asyncio.get_event_loop().create_future()

    # Complete `b` immediately
    b.set_result("original")

    # Chain the futures
    chain_future(a, b)

    # Resolve `a` with a different value
    a.set_result("new")

    # Give the IOLoop a chance to run callbacks
    IOLoop.current().add_callback(lambda: None)
    IOLoop.current().add_callback(lambda: None)

    # `b` should still hold the original result
    assert b.result() == "original", "b should not be overwritten if already done"
