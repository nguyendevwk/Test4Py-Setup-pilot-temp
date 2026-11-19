import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

# Test 1: Normal acquire and release cycle
def test_bounded_semaphore_basic_acquire_release():
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

# Test 2: Releasing more times than initial value raises ValueError
def test_bounded_semaphore_over_release():
    sem = BoundedSemaphore(value=1)
    sem.acquire()
    assert sem._value == 0
    sem.release()
    assert sem._value == 1
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

# Test 3: Asynchronous acquire with timeout using tornado.gen
def test_bounded_semaphore_async_acquire_timeout():
    sem = BoundedSemaphore(value=1)

    @gen.coroutine
    def acquire_and_wait():
        # Acquire the semaphore to block the next acquire
        sem.acquire()
        # Attempt to acquire again with a timeout; should raise TimeoutError
        try:
            yield gen.with_timeout(
                datetime.timedelta(seconds=0.1),
                sem.acquire()
            )
        except gen.TimeoutError:
            return "timeout"
        return "acquired"

    # Run the coroutine in the IOLoop
    result = ioloop.IOLoop.current().run_sync(acquire_and_wait)
    assert result == "timeout"
