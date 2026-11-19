import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

@pytest.mark.asyncio
async def test_normal_acquire_release():
    sem = BoundedSemaphore(value=2)
    # Acquire twice should succeed
    await sem.acquire()
    await sem.acquire()
    # No more permits available; next acquire should block until a release
    async def try_acquire():
        await sem.acquire()
        return "acquired"
    task = ioloop.IOLoop.current().spawn_callback(try_acquire)
    # Give the loop a moment to schedule the task
    await gen.sleep(0.01)
    assert not task.done()
    # Release one permit and ensure the blocked acquire proceeds
    sem.release()
    await task
    assert task.result() == "acquired"

def test_release_too_many_times_raises():
    sem = BoundedSemaphore(value=1)
    # Acquire once, release once
    sem.acquire()
    sem.release()
    # Releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_initial_value_boundary():
    sem = BoundedSemaphore(value=3)
    # Acquire all permits
    await sem.acquire()
    await sem.acquire()
    await sem.acquire()
    # All permits used; next acquire should block
    async def block_acquire():
        await sem.acquire()
        return "done"
    task = ioloop.IOLoop.current().spawn_callback(block_acquire)
    await gen.sleep(0.01)
    assert not task.done()
    # Release one permit
    sem.release()
    await task
    assert task.result() == "done"
    # Now the semaphore value should be back to 3
    assert sem._value == 3
