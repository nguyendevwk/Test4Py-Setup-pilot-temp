import datetime
import pytest
from tornado import gen, ioloop
from tornado.locks import Condition
from tornado.concurrent import Future

@pytest.mark.asyncio
async def test_condition_notify_wakes_waiter():
    cond = Condition()
    # Waiter coroutine
    async def waiter():
        result = await cond.wait()
        return result

    # Notifier coroutine
    async def notifier():
        # Give the waiter a moment to register
        await gen.sleep(0.01)
        cond.notify()

    # Run both coroutines concurrently
    results = await gen.multi([waiter(), notifier()])
    # The waiter should receive True because it was notified
    assert results[0] is True
    # No pending waiters after notification
    assert len(cond._waiters) == 0

@pytest.mark.asyncio
async def test_condition_wait_timeout():
    cond = Condition()
    # Waiter with a short timeout
    async def waiter():
        # timeout as absolute timestamp
        timeout_ts = ioloop.IOLoop.current().time() + 0.05
        result = await cond.wait(timeout=timeout_ts)
        return result

    # Run waiter
    result = await waiter()
    # The waiter should time out and return False
    assert result is False
    # No pending waiters after timeout
    assert len(cond._waiters) == 0

@pytest.mark.asyncio
async def test_condition_notify_all_wakes_all_waiters():
    cond = Condition()
    # Create multiple waiters
    async def waiter():
        return await cond.wait()

    waiters = [waiter() for _ in range(3)]
    # Run all waiters concurrently
    async def run_waiters():
        return await gen.multi(waiters)

    # Notify all after a short delay
    async def notifier():
        await gen.sleep(0.01)
        cond.notify_all()

    # Run waiters and notifier concurrently
    results = await gen.multi([run_waiters(), notifier()])
    # All waiters should receive True
    assert all(r is True for r in results[0])
    # No pending waiters after notify_all
    assert len(cond._waiters) == 0
