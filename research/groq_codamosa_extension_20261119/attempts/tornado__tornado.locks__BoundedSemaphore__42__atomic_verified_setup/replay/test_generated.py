import pytest
from tornado.locks import BoundedSemaphore
from tornado import ioloop


def test_normal_acquire_and_release():
    """Acquire and release within bounds should succeed and restore the initial value."""
    async def _test():
        sem = BoundedSemaphore(2)
        await sem.acquire()
        await sem.acquire()
        sem.release()
        sem.release()
        # After releasing twice, the semaphore should be back to its initial value.
        # Acquire twice again to confirm no exception is raised.
        await sem.acquire()
        await sem.acquire()
        sem.release()
        sem.release()
    ioloop.IOLoop.current().run_sync(_test)


def test_release_at_initial_value_raises():
    """Releasing when the semaphore is already at its initial value should raise ValueError."""
    async def _test():
        sem = BoundedSemaphore(1)
        await sem.acquire()
        sem.release()
        with pytest.raises(ValueError, match="Semaphore released too many times"):
            sem.release()
    ioloop.IOLoop.current().run_sync(_test)


def test_excessive_release_after_multiple_acquires():
    """Releasing more times than acquired should raise ValueError."""
    async def _test():
        sem = BoundedSemaphore(3)
        await sem.acquire()
        await sem.acquire()
        await sem.acquire()
        sem.release()
        sem.release()
        sem.release()
        with pytest.raises(ValueError, match="Semaphore released too many times"):
            sem.release()
    ioloop.IOLoop.current().run_sync(_test)
