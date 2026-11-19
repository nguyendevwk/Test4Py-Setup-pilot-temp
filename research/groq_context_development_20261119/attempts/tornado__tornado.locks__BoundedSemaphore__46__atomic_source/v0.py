import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

# Test 1: Normal acquire and release cycle
def test_bounded_semaphore_basic():
    sem = BoundedSemaphore(value=2)
    # Initially, value should be 2
    assert sem._value == 2

    # Acquire twice, value should decrement to 0
    sem.acquire()
    sem.acquire()
    assert sem._value == 0

    # Release twice, value should return to 2
    sem.release()
    sem.release()
    assert sem._value == 2

# Test 2: Releasing too many times raises ValueError
def test_bounded_semaphore_over_release():
    sem = BoundedSemaphore(value=1)
    sem.acquire()  # value becomes 0
    sem.release()  # value back to 1
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()  # attempting to release beyond initial value

# Test 3: Asynchronous acquire with timeout
@pytest.mark.asyncio
async def test_bounded_semaphore_async_acquire():
    sem = BoundedSemaphore(value=1)

    async def worker():
        await gen.sleep(0.01)  # simulate work
        sem.release()

    # Acquire the semaphore, then start a worker that will release it
    sem.acquire()
    assert sem._value == 0

    # Start worker in background
    ioloop.IOLoop.current().spawn_callback(worker)

    # Await until semaphore becomes available again
    await gen.sleep(0.05)
    assert sem._value == 1
