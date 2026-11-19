import pytest
from superstring.superstring import SuperString

def test_character_at_out_of_bounds():
    s = SuperString("abc")
    # Valid index returns expected character
    assert s.character_at(0) == "a"
    # Out-of-range index raises IndexError
    with pytest.raises(IndexError):
        s.character_at(3)
