import pytest
from sanic.mixins.exceptions import ExceptionMixin, FutureException


class DummyMixin(ExceptionMixin):
    """Concrete subclass that records applied handlers."""

    def __init__(self):
        super().__init__()
        self.applied = []

    def _apply_exception_handler(self, handler: FutureException):
        self.applied.append(handler)


def test_exception_decorator_adds_to_set_and_applies():
    mixin = DummyMixin()

    @mixin.exception(ValueError, KeyError, apply=True)
    def handler(request, exc):
        return "handled"

    # The decorator returns the original function
    assert handler.__name__ == "handler"

    # A FutureException should be created and stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert isinstance(future_exc, FutureException)
    assert future_exc.handler is handler
    assert future_exc.exceptions == (ValueError, KeyError)

    # Since apply=True, _apply_exception_handler should have been called
    assert mixin.applied == [future_exc]


def test_exception_decorator_with_list_and_no_apply():
    mixin = DummyMixin()

    @mixin.exception([TypeError, RuntimeError], apply=False)
    def handler(request, exc):
        return "handled"

    # No handler should have been applied
    assert mixin.applied == []

    # The FutureException should still be stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert future_exc.exceptions == (TypeError, RuntimeError)


def test_all_exceptions_delegates_to_exception():
    mixin = DummyMixin()

    @mixin.all_exceptions
    def handler(request, exc):
        return "handled"

    # The handler should be registered for the generic Exception type
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert future_exc.exceptions == (Exception,)
    # The handler should have been applied
    assert mixin.applied == [future_exc]
