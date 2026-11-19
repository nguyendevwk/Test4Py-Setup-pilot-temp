import sys
import types
import pytest

# Provide a minimal dummy `six` module so that importing `genty` succeeds.
sys.modules["six"] = types.SimpleNamespace()

from genty.genty_repeat import genty_repeat


def test_genty_repeat_sets_count_and_raises_on_negative():
    count = 3
    decorator = genty_repeat(count)

    def dummy(self):  # pragma: no cover
        pass

    wrapped = decorator(dummy)
    assert wrapped is dummy
    assert getattr(wrapped, "genty_repeat_count") == count

    with pytest.raises(ValueError):
        genty_repeat(-1)
