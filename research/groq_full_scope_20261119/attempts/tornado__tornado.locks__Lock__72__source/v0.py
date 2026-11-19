import pytest
import asyncio
from tornado.locks import Lock
from tornado import gen, ioloop
from tornado.util import TimeoutError

@pytest.mark.asyncio
async def test_lock_acquire_and_release():
    lock = Lock()
    # Initially unlocked, acquire should succeed immediately
    await lock.acquire()
    # After acquiring, lock should be held; attempting to acquire again should block
    acquire_task = asyncio.create_task(lock.acquire())
    await asyncio.sleep(0.1)  # give time for the task to start waiting
    assert not acquire_task.done(), "Second acquire should be pending"
    # Release the lock and ensure the waiting task completes
    lock.release()
    await acquire_task
    # After both acquisitions, release again to clean up
    lock.release()

@pytest.mark.asyncio
async def test_lock_release_unlocked_raises():
    lock = Lock()
    # Releasing an unlocked lock should raise RuntimeError
    with pytest.raises(RuntimeError, match="release unlocked lock"):
        lock.release()

@pytest.mark.asyncio
async def test_lock_async_context_manager():
    lock = Lock()
    # Use async with to acquire and release automatically
    async with lock:
        # Inside the context, the lock should be held; a second acquire should block
        acquire_task = asyncio.create_task(lock.acquire())
        await asyncio.sleep(0.1)
        assert not acquire_task.done(), "Acquire inside context should be pending"
    # After exiting the context, the lock is released; the pending task should now complete
    await acquire_task
    # Clean up by releasing the lock acquired by the pending task
    lock.release()
