import pytest
from isort.exceptions import FileSkipSetting


def test_file_skip_setting_initialization_and_message():
    """Normal initialization should store the file path and produce the expected message."""
    fp = "example.py"
    exc = FileSkipSetting(fp)
    assert exc.file_path == fp
    expected_msg = (
        f"{fp} was skipped as it's listed in 'skip' setting or matches a glob in 'skip_glob' setting"
    )
    assert str(exc) == expected_msg
    assert expected_msg in exc.args[0]


def test_file_skip_setting_with_additional_kwargs():
    """Passing additional keyword arguments should not affect the exception."""
    fp = "module.py"
    exc = FileSkipSetting(fp, extra="ignored")
    assert exc.file_path == fp
    assert "ignored" not in exc.args[0]
    assert isinstance(exc, FileSkipSetting)


def test_file_skip_setting_missing_file_path_raises_type_error():
    """The constructor requires a file_path argument; omitting it should raise TypeError."""
    with pytest.raises(TypeError):
        FileSkipSetting()
