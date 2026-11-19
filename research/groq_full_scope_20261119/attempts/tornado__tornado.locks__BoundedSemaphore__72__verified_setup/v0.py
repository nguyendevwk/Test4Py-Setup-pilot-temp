import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

@pytest.mark.asyncio
async def test_normal_acquire_release():
    """Acquire and release within bounds should succeed."""
    sem = BoundedSemaphore(value=2)
    # Acquire twice, should succeed
    await sem.acquire()
    await sem.acquire()
    # Now value should be 0
    assert sem._value == 0
    # Release twice, should return to initial value
    sem.release()
    sem.release()
    assert sem._value == 2
    # Further acquire should block until a release
    async def delayed_release():
        await gen.sleep(0.01)
        sem.release()
    ioloop.IOLoop.current().add_callback(delayed_release)
    await sem.acquire()  # should succeed after delayed release
    assert sem._value == 1

@pytest.mark.asyncio
async def test_release_too_many_times_raises():
    """Releasing more times than initial value raises ValueError."""
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Value is 0 now
    sem.release()  # back to 1
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()  # would exceed initial value

@pytest.mark.asyncio
async def test_acquire_blocks_until_available():
    """Acquire should block until a release frees a slot."""
    sem = BoundedSemaphore(value=1)
    await sem.acquire()  # consume the only slot
    # Start a coroutine that will acquire after a release
    async def waiter():
        await sem.acquire()
        return "acquired"
    future = gen.convert_yielded(waiter())
    # Ensure the future is not done immediately
    assert not future.done()
    # Release after a short delay
    async def delayed_release():
        await gen.sleep(0.01)
        sem.release()
    ioloop.IOLoop.current().add_callback(delayed_release)
    result = await future
    assert result == "acquired"
    # After acquisition, value should be 0 again
    assert sem._value == 0
