import asyncio
import datetime

import pytest
from tornado.locks import Lock
from tornado import gen, ioloop


@pytest.mark.asyncio
async def test_lock_acquire_and_release(tmp_path):
    """Normal acquire/release sequence should work and allow re‑acquisition."""
    lock = Lock()
    # Acquire the lock
    await lock.acquire()
    assert lock._block._value == 0  # internal semaphore value is 0 when locked
    # Release the lock
    lock.release()
    assert lock._block._value == 1  # semaphore value restored
    # Re‑acquire to ensure lock can be reused
    await lock.acquire()
    assert lock._block._value == 0
    lock.release()


@pytest.mark.asyncio
async def test_lock_release_unlocked_raises():
    """Releasing an unlocked lock must raise RuntimeError."""
    lock = Lock()
    with pytest.raises(RuntimeError, match="release unlocked lock"):
        lock.release()


@pytest.mark.asyncio
async def test_lock_async_context_manager():
    """Using the lock as an async context manager should lock and unlock correctly."""
    lock = Lock()
    # Before entering context, lock should be unlocked
    assert lock._block._value == 1
    async with lock:
        # Inside context, lock should be acquired
        assert lock._block._value == 0
        # While inside, a second acquire should block until exit
        async def try_acquire():
            await lock.acquire()
            lock.release()
        # Schedule the second acquire
        task = asyncio.create_task(try_acquire())
        # Give the task a moment to start and block
        await asyncio.sleep(0.1)
        assert task.done() is False
    # After exiting context, lock should be released
    assert lock._block._value == 1
    # Ensure the second acquire eventually completes
    await task
