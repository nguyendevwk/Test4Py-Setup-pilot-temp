import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

# Test 1: Normal acquire and release cycle
def test_bounded_semaphore_basic_acquire_release():
    sem = BoundedSemaphore(value=2)
    # Acquire twice should succeed
    sem.acquire()
    sem.acquire()
    # Now the semaphore is exhausted; a third acquire would block
    # We use a timeout to ensure it does not acquire immediately
    with pytest.raises(TimeoutError):
        # Attempt to acquire with a timeout of 0.1 seconds
        @gen.coroutine
        def try_acquire():
            yield gen.with_timeout(0.1, sem.acquire())
        ioloop.IOLoop.current().run_sync(try_acquire)
    # Release once and acquire again should succeed
    sem.release()
    sem.acquire()
    # After releasing twice, the semaphore should be back to initial value
    sem.release()
    sem.release()
    assert sem._value == 2  # internal state matches initial value

# Test 2: Releasing more times than the initial value raises ValueError
def test_bounded_semaphore_release_too_many_times():
    sem = BoundedSemaphore(value=1)
    sem.acquire()
    # Release once to return to initial state
    sem.release()
    # Now releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

# Test 3: Boundary condition with zero initial value
def test_bounded_semaphore_zero_initial_value():
    sem = BoundedSemaphore(value=0)
    # Acquire should block indefinitely; we test that it does not acquire immediately
    with pytest.raises(TimeoutError):
        @gen.coroutine
        def try_acquire():
            yield gen.with_timeout(0.1, sem.acquire())
        ioloop.IOLoop.current().run_sync(try_acquire)
    # Releasing should raise ValueError because _value == 0 == _initial_value
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()
