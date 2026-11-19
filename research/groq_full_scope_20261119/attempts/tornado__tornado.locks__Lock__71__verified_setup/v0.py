import asyncio
import datetime
import pytest
from tornado import ioloop, gen
from tornado.locks import Lock

# Helper to run async coroutines in Tornado's IOLoop
def run_async(coro):
    return ioloop.IOLoop.current().run_sync(lambda: gen.convert_yielded(coro))

@pytest.mark.asyncio
async def test_lock_basic_acquire_release():
    lock = Lock()
    # Initially unlocked: acquire should succeed immediately
    await lock.acquire()
    # After acquiring, lock is held; attempting to acquire again should block
    # We'll start a coroutine that tries to acquire and set a flag after acquiring
    flag = {"acquired": False}
    async def waiter():
        await lock.acquire()
        flag["acquired"] = True
        lock.release()
    # Schedule waiter; it should block until we release
    ioloop.IOLoop.current().add_callback(waiter)
    # Give the loop a moment to schedule waiter
    await asyncio.sleep(0.01)
    assert not flag["acquired"], "waiter acquired lock prematurely"
    # Release the lock; waiter should now acquire
    lock.release()
    # Wait a bit for waiter to run
    await asyncio.sleep(0.01)
    assert flag["acquired"], "waiter did not acquire lock after release"

@pytest.mark.asyncio
async def test_lock_async_context_manager():
    lock = Lock()
    # Use async with to acquire and release automatically
    async with lock:
        # Inside context, lock should be held; attempting to acquire again should block
        flag = {"acquired": False}
        async def waiter():
            await lock.acquire()
            flag["acquired"] = True
            lock.release()
        ioloop.IOLoop.current().add_callback(waiter)
        await asyncio.sleep(0.01)
        assert not flag["acquired"], "waiter acquired lock inside context prematurely"
    # After exiting context, lock should be released; waiter should acquire
    await asyncio.sleep(0.01)
    assert flag["acquired"], "waiter did not acquire lock after context exit"

def test_release_unlocked_raises_runtime_error():
    lock = Lock()
    # Releasing an unlocked lock should raise RuntimeError
    with pytest.raises(RuntimeError, match="release unlocked lock"):
        lock.release()
