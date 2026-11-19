import pytest
from sanic.mixins.exceptions import ExceptionMixin, FutureException


class DummyMixin(ExceptionMixin):
    """Concrete implementation of ExceptionMixin for testing."""

    def __init__(self):
        super().__init__()
        self.applied_exceptions = []

    def _apply_exception_handler(self, handler: FutureException):
        # Record the handler for later inspection
        self.applied_exceptions.append(handler)


def test_exception_decorator_registers_and_applies():
    """Decorator should register the FutureException and apply it when requested."""
    mixin = DummyMixin()

    @mixin.exception(ValueError, KeyError, apply=True)
    def handler(request, exc):
        return "handled"

    # The decorator returns the original function
    assert handler.__name__ == "handler"

    # One FutureException should be stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert isinstance(future_exc, FutureException)
    # The exception types should be stored correctly
    assert set(future_exc.exceptions) == {ValueError, KeyError}

    # The handler should have been applied
    assert mixin.applied_exceptions == [future_exc]


def test_exception_decorator_without_apply():
    """Decorator should register but not apply when apply=False."""
    mixin = DummyMixin()

    @mixin.exception(RuntimeError, apply=False)
    def handler(request, exc):
        return "handled"

    # No FutureException should be applied
    assert mixin.applied_exceptions == []

    # The FutureException should still be stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert future_exc.exceptions == (RuntimeError,)


def test_all_exceptions_decorator_equivalence():
    """all_exceptions should behave like @exception(Exception)."""
    mixin = DummyMixin()

    @mixin.all_exceptions
    def handler(request, exc):
        return "global handled"

    # The handler should be registered as a FutureException for Exception
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert future_exc.exceptions == (Exception,)

    # The handler should have been applied
    assert mixin.applied_exceptions == [future_exc]
