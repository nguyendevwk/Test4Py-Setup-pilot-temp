import asyncio
import pytest
from tornado.locks import Lock
from tornado import gen

@pytest.mark.asyncio
async def test_lock_acquire_release():
    lock = Lock()
    # Initially unlocked: acquire should succeed immediately
    await lock.acquire()
    # After acquiring, the lock should be held; a second acquire will block
    async def try_acquire():
        await lock.acquire()
    task = asyncio.create_task(try_acquire())
    await asyncio.sleep(0.1)  # give the task time to start and block
    assert not task.done(), "Second acquire should be blocked while lock is held"
    # Release the lock and ensure the waiting task completes
    lock.release()
    await task
    assert task.done(), "Waiting acquire should complete after release"

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
    async def use_lock():
        async with lock:
            # Inside the context, the lock is held
            assert lock._block._value == 0, "Lock should be held inside async with"
        # After exiting, the lock should be released
        assert lock._block._value == 1, "Lock should be released after async with"
    await use_lock()
