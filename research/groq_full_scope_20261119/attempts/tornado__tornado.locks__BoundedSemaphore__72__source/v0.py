import pytest
import asyncio
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

# Helper to run a coroutine in the Tornado IOLoop
def run_sync(coro):
    return ioloop.IOLoop.current().run_sync(coro)

# Test 1: Normal acquire and release sequence
def test_bounded_semaphore_basic():
    sem = BoundedSemaphore(value=2)
    # Acquire twice, should succeed
    run_sync(sem.acquire())
    run_sync(sem.acquire())
    # Now the semaphore is exhausted; a third acquire would block
    # We test that the value is zero by attempting a non-blocking acquire
    # which should raise a RuntimeError in Tornado's implementation
    with pytest.raises(RuntimeError):
        run_sync(sem.acquire(blocking=False))
    # Release once and acquire again
    sem.release()
    run_sync(sem.acquire())
    # After releasing twice, the semaphore should be back to initial value
    assert sem._value == 2

# Test 2: Releasing more times than the initial value raises ValueError
def test_bounded_semaphore_over_release():
    sem = BoundedSemaphore(value=1)
    run_sync(sem.acquire())
    sem.release()
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

# Test 3: Using the semaphore as an async context manager
@pytest.mark.asyncio
async def test_bounded_semaphore_async_context():
    sem = BoundedSemaphore(value=1)
    async with sem:
        # Inside the context, the semaphore should be acquired
        assert sem._value == 0
    # After exiting the context, the semaphore should be released
    assert sem._value == 1
