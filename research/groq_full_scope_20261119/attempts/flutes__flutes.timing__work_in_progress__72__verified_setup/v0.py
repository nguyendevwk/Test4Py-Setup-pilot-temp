import pytest
import time
from flutes.timing import work_in_progress

def test_work_in_progress_normal_block(capsys, tmp_path):
    """Verify normal usage prints start and end messages with elapsed time."""
    start = time.time()
    with work_in_progress("Test normal"):
        time.sleep(0.1)
    end = time.time()
    out, _ = capsys.readouterr()
    assert out.startswith("Test normal... ")
    assert out.endswith(f"done. ({end - start:.2f}s)\n")
    # elapsed time should be close to 0.1s
    elapsed = float(out.split('(')[-1].split('s')[0])
    assert 0.09 <= elapsed <= 0.2

def test_work_in_progress_zero_sleep(capsys):
    """Boundary case: zero sleep should still print elapsed time."""
    with work_in_progress("Zero sleep"):
        pass
    out, _ = capsys.readouterr()
    assert out.startswith("Zero sleep... ")
    assert out.endswith("done. (0.00s)\n")
    elapsed = float(out.split('(')[-1].split('s')[0])
    assert elapsed == 0.0

def test_work_in_progress_exception(capsys):
    """Ensure that an exception inside the block still triggers the end message."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Exception test"):
            raise RuntimeError("boom")
    out, _ = capsys.readouterr()
    assert out.startswith("Exception test... ")
    assert out.endswith("done. (0.00s)\n")
    elapsed = float(out.split('(')[-1].split('s')[0])
    assert elapsed == 0.0
