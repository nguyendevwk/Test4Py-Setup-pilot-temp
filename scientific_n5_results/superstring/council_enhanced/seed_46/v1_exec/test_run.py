import pytest
from superstring.superstring import SuperString

def test_superstring_indexing_and_slicing():
    content = "Test String"
    s = SuperString(content)

    # length caching
    assert s.length() == len(content)
    assert s.length() == len(content)  # second call uses cached value

    # integer indexing
    assert s[0] == "T"
    assert s[1] == "e"
    assert s[-1] == "g"

    # positive slice
    sub = s[2:5]
    assert isinstance(sub, SuperString)
    assert str(sub) == content[2:5]

    # negative slice
    sub_neg = s[-3:-1]
    assert isinstance(sub_neg, SuperString)
    assert str(sub_neg) == content[-3:-1]

    # length via __len__
    assert len(s) == len(content)
