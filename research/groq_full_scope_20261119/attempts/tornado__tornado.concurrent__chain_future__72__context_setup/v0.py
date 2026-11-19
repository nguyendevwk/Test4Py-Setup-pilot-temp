import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import chain_future, Future, future_set_exception_unless_cancelled


@pytest.mark.asyncio
async def test_chain_future_success():
    """When future `a` succeeds, `b` receives the same result."""
    a = Future()
    b = Future()
    chain_future(a, b)

    # Resolve `a` with a value
    a.set_result(42)

    # Await `b` to ensure propagation
    result = await b
    assert result == 42, "b should receive the result from a"


@pytest.mark.asyncio
async def test_chain_future_failure():
    """When future `a` fails, `b` receives the same exception."""
    a = Future()
    b = Future()
    chain_future(a, b)

    # Fail `a` with a ValueError
    a.set_exception(ValueError("boom"))

    # Await `b` and check exception type and message
    with pytest.raises(ValueError) as excinfo:
        await b
    assert str(excinfo.value) == "boom", "b should propagate the exception from a"


@pytest.mark.asyncio
async def test_chain_future_b_already_done():
    """If `b` is already done before `a` completes, `a`'s result is ignored."""
    a = Future()
    b = Future()
    # Pre-complete `b` with a different value
    b.set_result("pre-set")
    chain_future(a, b)

    # Complete `a` with a new value
    a.set_result(99)

    # Await `b` and ensure it still holds the pre-set value
    result = await b
    assert result == "pre-set", "b should not be overwritten after completion"
