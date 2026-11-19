import logging
import types
import pytest

import tqdm.contrib.logging as mod

# Helper dummy tqdm class
class DummyTqdm:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.entered = False
        self.exited = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exited = True
        return False  # propagate exceptions if any


def test_tqdm_logging_redirect_yields_pbar(tmp_path):
    """The context manager yields the tqdm instance created by the supplied class."""
    dummy = DummyTqdm
    with mod.tqdm_logging_redirect(10, total=10, tqdm_class=dummy) as pbar:
        # Inside the context, the yielded object should be our dummy instance
        assert isinstance(pbar, DummyTqdm)
        assert pbar.entered is True
        # The dummy should have received the correct arguments
        assert pbar.args == (10,)
        assert pbar.kwargs == {"total": 10}
    # After exiting, the dummy should have exited
    assert dummy.entered is True
    assert dummy.exited is True


def test_tqdm_logging_redirect_passes_loggers(monkeypatch):
    """The loggers argument is forwarded to logging_redirect_tqdm."""
    called = {}
    def fake_logging_redirect_tqdm(loggers=None, tqdm_class=None):
        called['loggers'] = loggers
        called['tqdm_class'] = tqdm_class
        # Return a dummy context manager that does nothing
        class DummyCtx:
            def __enter__(self): return None
            def __exit__(self, exc_type, exc_val, exc_tb): return False
        return DummyCtx()
    monkeypatch.setattr(mod, "logging_redirect_tqdm", fake_logging_redirect_tqdm)

    dummy = DummyTqdm
    logger1 = logging.getLogger("test1")
    logger2 = logging.getLogger("test2")
    with mod.tqdm_logging_redirect(5, total=5, loggers=[logger1, logger2], tqdm_class=dummy):
        pass

    assert called['loggers'] == [logger1, logger2]
    assert called['tqdm_class'] == dummy


def test_tqdm_logging_redirect_default_tqdm(monkeypatch):
    """When tqdm_class is not provided, the default std.tqdm is used."""
    # Patch the default tqdm to a dummy that records usage
    dummy = DummyTqdm
    monkeypatch.setattr(mod, "std_tqdm", dummy)

    with mod.tqdm_logging_redirect(3, total=3) as pbar:
        assert isinstance(pbar, DummyTqdm)
        assert pbar.args == (3,)
        assert pbar.kwargs == {"total": 3}
