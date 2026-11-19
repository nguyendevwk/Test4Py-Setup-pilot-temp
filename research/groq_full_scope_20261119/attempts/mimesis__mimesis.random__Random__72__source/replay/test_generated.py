import pytest
from mimesis.random import Random


def test_randints_normal_and_boundary():
    rnd = Random()
    # Normal case: generate 5 integers between 10 and 20
    result = rnd.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x < 20 for x in result)

    # Boundary case: n <= 0 should raise ValueError
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rnd.randints(n=0, a=1, b=10)


def test_generate_string_by_mask_custom_placeholders():
    rnd = Random()
    # Use distinct placeholders: '@' for letters, '#' for digits
    code = rnd.generate_string_by_mask(mask="@@##", char="@", digit="#")
    assert len(code) == 4
    # First two characters should be uppercase letters
    assert code[0].isupper() and code[1].isupper()
    # Last two characters should be digits
    assert code[2].isdigit() and code[3].isdigit()

    # Using same placeholder for both should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder cannot be used"):
        rnd.generate_string_by_mask(mask="@@##", char="#", digit="#")


def test_weighted_choice_and_choice_enum_item():
    rnd = Random()
    # Weighted choice: keys 1,2,3 with weights 1,2,3
    weights = {1: 1, 2: 2, 3: 3}
    chosen = rnd.weighted_choice(weights)
    assert chosen in weights

    # Empty dict should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rnd.weighted_choice({})

    # choice_enum_item: use a simple enum
    import enum

    class Color(enum.Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    enum_choice = rnd.choice_enum_item(Color)
    assert enum_choice in list(Color)
