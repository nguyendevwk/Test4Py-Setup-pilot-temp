import asyncio
import pytest
from tornado.locks import Lock
from tornado import gen

@pytest.mark.asyncio
async def test_lock_acquire_and_release():
    lock = Lock()
    # Initially unlocked: acquire should succeed immediately
    await lock.acquire()
    # After acquiring, lock is held; releasing should free it
    lock.release()
    # Acquire again to confirm lock can be reused
    await lock.acquire()
    lock.release()

@pytest.mark.asyncio
async def test_lock_context_manager():
    lock = Lock()
    # Use async with to acquire and release automatically
    async with lock:
        # Inside context, lock should be held; attempting to acquire again
        # should block until released, so we schedule a task that will
        # acquire after a short delay
        async def delayed_acquire():
            await asyncio.sleep(0.01)
            await lock.acquire()
            lock.release()
        task = asyncio.create_task(delayed_acquire())
        # Wait a bit to ensure delayed_acquire is waiting
        await asyncio.sleep(0.02)
        # The task should still be pending because lock is held
        assert not task.done()
        # Exiting context releases the lock, allowing the task to proceed
    await task  # ensure task completes without exception

@pytest.mark.asyncio
async def test_lock_release_unlocked_raises():
    lock = Lock()
    # Releasing an unlocked lock should raise RuntimeError
    with pytest.raises(RuntimeError, match="release unlocked lock"):
        lock.release()
