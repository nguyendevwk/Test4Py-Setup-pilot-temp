import pytest
from flutils.packages import bump_version

def test_bump_major_and_minor():
    # Bump the major part (position 0) and minor part (position 1)
    assert bump_version('1.2.3', position=0) == '2.0'
    assert bump_version('1.2.3', position=1) == '1.3'

def test_pre_release_transitions_and_removal():
    # Transition from alpha to beta, and removal of pre-release
    assert bump_version('1.2.3', pre_release='a') == '1.2.4a0'
    assert bump_version('1.2.4a0', pre_release='a') == '1.2.4a1'
    assert bump_version('1.2.4a1', pre_release='b') == '1.2.4b0'
    assert bump_version('1.2.4b0') == '1.2.4'
    assert bump_version('1.2.4b0', pre_release='a') == '1.2.4a0'

def test_invalid_inputs_raise_value_error():
    # Invalid version string
    with pytest.raises(ValueError):
        bump_version('invalid.version')
    # Position out of range
    with pytest.raises(ValueError):
        bump_version('1.2.3', position=5)
    # Unsupported pre_release value
    with pytest.raises(ValueError):
        bump_version('1.2.3', pre_release='rc')
    # Trying to bump major on a pre-release version
    with pytest.raises(ValueError):
        bump_version('1.2.3a0', position=0)
