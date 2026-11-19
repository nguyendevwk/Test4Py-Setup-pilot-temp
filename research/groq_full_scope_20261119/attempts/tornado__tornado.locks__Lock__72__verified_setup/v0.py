import pytest
import asyncio
from tornado import ioloop
from tornado.locks import Lock


@pytest.mark.asyncio
async def test_lock_acquire_and_release():
    """Normal acquire and release should work without errors."""
    lock = Lock()
    # Acquire the lock
    await lock.acquire()
    # After acquiring, the lock should be held; attempting to acquire again
    # should block until released. We test this by starting a second coroutine
    # that will wait for the lock to be released.
    async def waiter():
        await lock.acquire()
        return "acquired"

    # Schedule the waiter; it should not complete immediately
    task = asyncio.create_task(waiter())
    await asyncio.sleep(0.1)  # give the task a chance to run
    assert not task.done(), "waiter should be blocked while lock is held"

    # Release the lock; waiter should now complete
    lock.release()
    result = await task
    assert result == "acquired", "waiter should acquire the lock after release"


def test_lock_release_unlocked_raises():
    """Releasing an unlocked lock should raise RuntimeError."""
    lock = Lock()
    with pytest.raises(RuntimeError, match="release unlocked lock"):
        lock.release()


@pytest.mark.asyncio
async def test_lock_async_context_manager():
    """Using the lock as an async context manager should acquire and release automatically."""
    lock = Lock()
    # Ensure lock is initially unlocked by acquiring it directly
    await lock.acquire()
    lock.release()

    async def inner():
        async with lock:
            # Inside the context, the lock should be held
            # Attempt to acquire again should block
            async def waiter():
                await lock.acquire()
                return "acquired"

            task = asyncio.create_task(waiter())
            await asyncio.sleep(0.1)
            assert not task.done(), "waiter should be blocked inside context"
            # Exiting context will release the lock
        # After context exit, lock should be free
        await lock.acquire()
        lock.release()

    await inner()
