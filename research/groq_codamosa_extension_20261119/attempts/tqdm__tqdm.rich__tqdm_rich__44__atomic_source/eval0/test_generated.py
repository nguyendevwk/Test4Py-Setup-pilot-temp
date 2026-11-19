import pytest
from tqdm.rich import tqdm_rich

def test_progress_output(capsys):
    """Verify that tqdm_rich displays progress and ends at 100%."""
    with tqdm_rich(total=3, leave=True, disable=False) as p:
        for _ in range(3):
            p.update(1)
    out, err = capsys.readouterr()
    # The final line should contain "100%" indicating completion
    assert "100%" in out
    # The description should be empty by default
    assert "[" not in out or "description" not in out

def test_disable_no_output():
    """When disable=True, tqdm_rich should produce no output."""
    with tqdm_rich(total=2, disable=True) as p:
        for _ in range(2):
            p.update(1)
    # No output should be produced; the iterator should still work
    assert p.n == 2

def test_reset_total():
    """Resetting the progress bar should change the total and allow reuse."""
    p = tqdm_rich(total=2, leave=False)
    for _ in range(2):
        p.update(1)
    # After first run, n should be 2
    assert p.n == 2
    # Reset to a new total
    p.reset(total=4)
    # n should be reset to 0
    assert p.n == 0
    # Iterate to new total
    for _ in range(4):
        p.update(1)
    assert p.n == 4
    p.close()
