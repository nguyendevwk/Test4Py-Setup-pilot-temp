import pytest
from flutils.packages import bump_version


def test_bump_major_and_minor_and_patch():
    # Normal bump of patch
    assert bump_version("1.2.3") == "1.2.4"
    # Bump minor resets patch
    assert bump_version("1.2.3", position=1) == "1.3"
    # Bump major resets minor and patch
    assert bump_version("1.2.3", position=0) == "2.0"


def test_pre_release_transitions_and_increments():
    # Create alpha pre-release
    assert bump_version("1.2.3", pre_release="a") == "1.2.4a0"
    # Increment alpha pre-release
    assert bump_version("1.2.4a0", pre_release="a") == "1.2.4a1"
    # Switch from alpha to beta
    assert bump_version("1.2.4a1", pre_release="b") == "1.2.4b0"
    # Remove pre-release by bumping patch
    assert bump_version("1.2.4b0") == "1.2.4"
    # Bump minor with pre-release
    assert bump_version("2.1.3", position=1, pre_release="a") == "2.2a0"
    # Bump patch when pre-release exists
    assert bump_version("1.2b0", position=2) == "1.2.1"


def test_invalid_inputs_raise_value_error():
    # Invalid version string
    with pytest.raises(ValueError):
        bump_version("invalid.version")
    # Position out of range
    with pytest.raises(ValueError):
        bump_version("1.2.3", position=5)
    # Unsupported pre_release value
    with pytest.raises(ValueError):
        bump_version("1.2.3", pre_release="rc")
    # Trying to bump major part of a pre-release version
    with pytest.raises(ValueError):
        bump_version("1.2.3a0", position=0)
