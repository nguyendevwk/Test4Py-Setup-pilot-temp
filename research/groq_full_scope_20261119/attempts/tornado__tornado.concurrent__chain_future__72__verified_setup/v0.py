import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import chain_future
from tornado.ioloop import IOLoop
from tornado import gen

# Test 1: Successful chaining of asyncio futures
@pytest.mark.asyncio
async def test_chain_future_success():
    loop = asyncio.get_running_loop()
    a = loop.create_future()
    b = loop.create_future()

    chain_future(a, b)

    # Resolve a and check that b receives the same result
    a.set_result(42)
    await b
    assert b.result() == 42
    assert a.done() and not a.cancelled()
    assert b.done() and not b.cancelled()

# Test 2: Exception propagation from a to b
@pytest.mark.asyncio
async def test_chain_future_exception():
    loop = asyncio.get_running_loop()
    a = loop.create_future()
    b = loop.create_future()

    chain_future(a, b)

    # Raise an exception in a and verify b receives it
    exc = ValueError("boom")
    a.set_exception(exc)
    with pytest.raises(ValueError) as e:
        await b
    assert str(e.value) == "boom"
    assert a.exception() is exc
    assert b.exception() is exc

# Test 3: Chaining with concurrent.futures.Future and cancellation
def test_chain_future_concurrent_and_cancel(tmp_path):
    # Use a ThreadPoolExecutor to create a concurrent future
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = executor.submit(lambda: 99)
        b = asyncio.get_event_loop().create_future()

        # Cancel b before a completes
        b.cancel()

        # Chain the futures
        chain_future(a, b)

        # Wait for a to finish
        result = a.result(timeout=1)
        assert result == 99

        # b should remain cancelled and not be set by a
        assert b.cancelled()
        assert not b.done()
