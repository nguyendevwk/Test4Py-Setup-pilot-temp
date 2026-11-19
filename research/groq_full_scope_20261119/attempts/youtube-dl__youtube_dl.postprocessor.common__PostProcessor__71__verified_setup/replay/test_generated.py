import os
import pytest
from youtube_dl.postprocessor.common import PostProcessor, PostProcessingError
from youtube_dl.utils import encodeFilename

class DummyDownloader:
    def __init__(self, params=None):
        self.params = params or {}
        self.warnings = []

    def report_warning(self, msg):
        self.warnings.append(msg)

def test_default_run_returns_identity(tmp_path):
    """PostProcessor.run should return unchanged information and empty deletable list."""
    pp = PostProcessor()
    info = {"filepath": str(tmp_path / "file.txt"), "title": "test"}
    deletable, updated = pp.run(info)
    assert deletable == []
    assert updated is info  # same object returned

def test_try_utime_reports_warning_on_failure(tmp_path):
    """try_utime should call report_warning when os.utime fails."""
    downloader = DummyDownloader()
    pp = PostProcessor(downloader)
    # Use a non‑existent file path
    fake_path = tmp_path / "nonexistent.txt"
    pp.try_utime(fake_path, 0, 0, errnote="UTIME failed")
    assert "UTIME failed" in downloader.warnings

def test_configuration_args_returns_downloader_params(tmp_path):
    """_configuration_args should return the downloader's postprocessor_args."""
    params = {"postprocessor_args": ["--foo", "--bar"]}  # example args
    downloader = DummyDownloader(params=params)
    pp = PostProcessor(downloader)
    args = pp._configuration_args(default=["--default"])
    assert args == ["--foo", "--bar"]
