import itertools
import math
import pytest
from tqdm.contrib.itertools import batched
from tqdm.auto import tqdm as tqdm_auto

def test_batched_basic():
    data = list(range(10))
    n = 3
    result = batched(data, n)
    # The returned object should be a tqdm instance
    assert isinstance(result, tqdm_auto)
    # Total should be ceil(len(data)/n)
    assert result.total == math.ceil(len(data) / n)
    # Collect batches and verify content
    batches = list(result)
    assert len(batches) == math.ceil(len(data) / n)
    expected = [data[i:i+n] for i in range(0, len(data), n)]
    assert batches == expected

def test_batched_file_iterable(tmp_path):
    # Create a temporary file with 5 lines
    file_path = tmp_path / "test.txt"
    file_path.write_text("\n".join(str(i) for i in range(5)))
    with file_path.open() as f:
        n = 2
        result = batched(f, n)
        # Total should be ceil(5/2) = 3
        assert result.total == 3
        # Collect batches and verify each batch contains the correct lines
        batches = list(result)
        assert len(batches) == 3
        expected = [file_path.read_text().splitlines()[i:i+n] for i in range(0, 5, n)]
        assert batches == expected

def test_batched_invalid():
    # Passing a non-iterable should raise a TypeError from itertools.batched
    with pytest.raises(TypeError):
        list(batched(42, 3))
