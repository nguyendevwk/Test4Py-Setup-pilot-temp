import pytest
from flutils.packages import bump_version

def test_bump_major_and_minor_and_patch():
    # Normal bump of patch
    assert bump_version("1.2.3") == "1.2.4"
    # Bump minor resets patch
    assert bump_version("1.2.3", position=1) == "1.3"
    # Bump major resets minor and patch
    assert bump_version("1.2.3", position=0) == "2.0"

def test_pre_release_handling():
    # Add alpha pre-release to patch
    assert bump_version("1.2.3", pre_release="a") == "1.2.4a0"
    # Increment alpha pre-release
    assert bump_version("1.2.4a0", pre_release="a") == "1.2.4a1"
    # Switch from alpha to beta
    assert bump_version("1.2.4a1", pre_release="b") == "1.2.4b0"
    # Remove pre-release by bumping patch without pre_release
    assert bump_version("1.2.4b0") == "1.2.4"

def test_invalid_inputs_raise_value_error():
    # Invalid position out of range
    with pytest.raises(ValueError):
        bump_version("1.2.3", position=3)
    # Invalid pre_release value
    with pytest.raises(ValueError):
        bump_version("1.2.3", pre_release="rc")
    # Trying to add pre_release to major part
    with pytest.raises(ValueError):
        bump_version("1.2.3", position=0, pre_release="a")
