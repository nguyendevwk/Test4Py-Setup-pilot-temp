import os
import pytest
from youtube_dl.postprocessor.common import PostProcessor
from youtube_dl.utils import PostProcessingError

class DummyDownloader:
    def __init__(self):
        self.warnings = []

    def report_warning(self, msg):
        self.warnings.append(msg)

    @property
    def params(self):
        return {}

def test_run_returns_identity(tmp_path):
    """PostProcessor.run should return unchanged information and no files to delete."""
    pp = PostProcessor()
    info = {"filepath": str(tmp_path / "file.mp4"), "title": "test"}
    files_to_delete, updated_info = pp.run(info)
    assert files_to_delete == []
    assert updated_info is info

def test_try_utime_reports_warning_on_error(tmp_path):
    """try_utime should call report_warning when os.utime fails."""
    pp = PostProcessor(DummyDownloader())
    # create a file and make it read-only to trigger an error on some platforms
    file_path = tmp_path / "readonly.txt"
    file_path.write_text("content")
    os.chmod(file_path, 0o444)  # read-only
    pp.try_utime(file_path, 0, 0, errnote="Custom warning")
    assert "Custom warning" in pp._downloader.warnings

def test_configuration_args_returns_default_when_none(tmp_path):
    """_configuration_args should return the default list when no args are set."""
    pp = PostProcessor(DummyDownloader())
    default = ["--example"]
    result = pp._configuration_args(default)
    assert result == default
