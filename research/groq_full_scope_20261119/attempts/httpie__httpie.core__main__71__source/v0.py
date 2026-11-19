import pytest
from httpie.core import main
from httpie.status import ExitStatus

def test_main_returns_exitstatus_type(tmp_path):
    """Calling main with no arguments should return an ExitStatus instance."""
    status = main(args=[str(tmp_path)])
    assert isinstance(status, ExitStatus)

def test_main_with_invalid_argument_raises_systemexit(tmp_path):
    """Providing an invalid argument should cause the program to exit with a SystemExit."""
    with pytest.raises(SystemExit):
        main(args=[str(tmp_path), "--unknown-flag"])

def test_main_with_environment_override(tmp_path):
    """Passing a custom Environment should not alter the type of the returned status."""
    from httpie.context import Environment
    env = Environment()
    status = main(args=[str(tmp_path)], env=env)
    assert isinstance(status, ExitStatus)
