import pytest
from flutils.packages import bump_version

def test_bump_major_and_minor_and_patch():
    # Normal bump of patch (default position 2)
    assert bump_version("1.2.3") == "1.2.4"
    # Bump minor part
    assert bump_version("1.2.3", position=1) == "1.3"
    # Bump major part
    assert bump_version("1.2.3", position=0) == "2.0"

def test_prerelease_handling_and_clearing():
    # Create a new alpha prerelease
    assert bump_version("1.2.3", pre_release="a") == "1.2.4a0"
    # Increment alpha prerelease
    assert bump_version("1.2.4a0", pre_release="a") == "1.2.4a1"
    # Switch from alpha to beta
    assert bump_version("1.2.4a1", pre_release="b") == "1.2.4b0"
    # Clear prerelease by bumping patch without pre_release
    assert bump_version("1.2.4b0") == "1.2.4"

def test_invalid_position_and_pre_release():
    # Position out of allowed range raises ValueError
    with pytest.raises(ValueError, match="must be an 'int' between"):
        bump_version("1.2.3", position=3)
    # Invalid pre_release string raises ValueError
    with pytest.raises(ValueError, match="can only be one of"):
        bump_version("1.2.3", pre_release="rc")
    # Trying to add prerelease to major part raises ValueError
    with pytest.raises(ValueError, match="Only the 'minor' or 'patch'"):
        bump_version("1.2.3", position=0, pre_release="a")
