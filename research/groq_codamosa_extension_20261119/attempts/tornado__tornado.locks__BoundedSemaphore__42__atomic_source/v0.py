import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

@pytest.mark.asyncio
async def test_bounded_semaphore_normal_acquire_release():
    sem = BoundedSemaphore(value=2)
    # Acquire twice successfully
    await sem.acquire()
    await sem.acquire()
    # Value should be 0 after two acquires
    assert sem._value == 0
    # Release twice, value should return to 2
    sem.release()
    sem.release()
    assert sem._value == 2
    # Acquire again to confirm semaphore still works
    await sem.acquire()
    assert sem._value == 1

@pytest.mark.asyncio
async def test_bounded_semaphore_release_too_many():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Value is 0 now
    assert sem._value == 0
    # Release once, value becomes 1
    sem.release()
    assert sem._value == 1
    # Releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_bounded_semaphore_concurrent_acquire():
    sem = BoundedSemaphore(value=1)
    results = []

    async def worker(name):
        await sem.acquire()
        results.append(name)
        await gen.sleep(0.01)  # simulate work
        sem.release()

    # Start two workers concurrently
    await gen.multi([worker("first"), worker("second")])
    # Both should have acquired the semaphore in some order
    assert set(results) == {"first", "second"}
    # After both released, semaphore value should be back to initial
    assert sem._value == 1
