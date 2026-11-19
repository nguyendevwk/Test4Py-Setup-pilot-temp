import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import chain_future, Future, future_set_exc_info

# Test 1: Successful chaining of two asyncio.Future objects
@pytest.mark.asyncio
async def test_chain_future_success():
    a = Future()
    b = Future()
    chain_future(a, b)

    # Resolve a and check that b receives the same result
    a.set_result(42)
    await asyncio.sleep(0)  # allow callbacks to run
    assert b.done()
    assert not b.cancelled()
    assert b.result() == 42

# Test 2: Failure propagation from a to b using concurrent.futures.Future
def test_chain_future_failure():
    loop = asyncio.get_event_loop()
    a = concurrent.futures.Future()
    b = Future()

    chain_future(a, b)

    # Resolve a with an exception
    a.set_exception(ValueError("boom"))
    loop.run_until_complete(asyncio.sleep(0))  # allow callbacks to run

    assert b.done()
    assert not b.cancelled()
    exc = b.exception()
    assert isinstance(exc, ValueError)
    assert str(exc) == "boom"

# Test 3: b already completed before a finishes – b should remain unchanged
@pytest.mark.asyncio
async def test_chain_future_b_already_done():
    a = Future()
    b = Future()
    b.set_result("already")
    chain_future(a, b)

    # Resolve a with a different result
    a.set_result(99)
    await asyncio.sleep(0)  # allow callbacks to run

    # b should keep its original result
    assert b.done()
    assert b.result() == "already"
