import pytest
from sanic.mixins.exceptions import ExceptionMixin, FutureException


class DummyMixin(ExceptionMixin):
    """Concrete implementation of ExceptionMixin for testing."""

    def __init__(self):
        super().__init__()
        self.applied_exceptions = []

    def _apply_exception_handler(self, handler: FutureException):
        # Record the applied handler for later inspection
        self.applied_exceptions.append(handler)


def test_exception_decorator_with_apply_and_list():
    """Decorator should register FutureException and apply it when apply=True."""
    mixin = DummyMixin()

    @mixin.exception([ValueError, KeyError], apply=True)
    def handler(request, exc):
        return "handled"

    # The decorator returns the original handler
    assert handler.__name__ == "handler"

    # One FutureException should be stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert isinstance(future_exc, FutureException)
    # The exception types should be stored correctly
    assert set(future_exc.exceptions) == {ValueError, KeyError}

    # The handler should have been applied
    assert mixin.applied_exceptions == [future_exc]


def test_exception_decorator_without_apply_and_single_exception():
    """Decorator should register FutureException but not apply it when apply=False."""
    mixin = DummyMixin()

    @mixin.exception(ValueError, apply=False)
    def handler(request, exc):
        return "handled"

    # No FutureException should be applied
    assert mixin.applied_exceptions == []

    # The FutureException should still be stored
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert set(future_exc.exceptions) == {ValueError}


def test_all_exceptions_decorator_equivalence():
    """all_exceptions should behave like exception(Exception)."""
    mixin = DummyMixin()

    @mixin.all_exceptions
    def handler(request, exc):
        return "handled"

    # The handler should be registered for the generic Exception
    assert len(mixin._future_exceptions) == 1
    future_exc = next(iter(mixin._future_exceptions))
    assert set(future_exc.exceptions) == {Exception}

    # The handler should have been applied
    assert mixin.applied_exceptions == [future_exc]
