import pytest
from mimesis.random import Random
from enum import Enum

class SampleEnum(Enum):
    A = 1
    B = 2
    C = 3

def test_randints_within_range_and_length():
    rnd = Random(seed=42)
    result = rnd.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x <= 19 for x in result)  # b is exclusive

def test_generate_string_by_mask_custom_placeholders():
    rnd = Random(seed=99)
    mask = "X-#-Y"
    code = rnd.generate_string_by_mask(mask=mask, char="X", digit="#")
    # The mask has 3 placeholders: X, #, Y (literal)
    assert len(code) == len(mask)
    # X should be an uppercase letter
    assert code[0].isupper() and code[0].isalpha()
    # # should be a digit
    assert code[2].isdigit()
    # Y should remain literal
    assert code[4] == "Y"

def test_weighted_choice_empty_dict_raises_value_error():
    rnd = Random(seed=7)
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rnd.weighted_choice({})
