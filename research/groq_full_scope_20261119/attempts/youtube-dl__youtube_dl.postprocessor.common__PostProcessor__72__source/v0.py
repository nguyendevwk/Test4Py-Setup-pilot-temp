import os
import time
import pytest
from youtube_dl.postprocessor.common import PostProcessor
from youtube_dl.utils import PostProcessingError


class DummyDownloader:
    def __init__(self):
        self.warnings = []
        self.params = {}

    def report_warning(self, msg):
        self.warnings.append(msg)


def test_run_returns_identity(tmp_path):
    """PostProcessor.run should return unchanged information and no deletable files."""
    pp = PostProcessor()
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {"filepath": str(file_path), "title": "test"}
    deletable, updated = pp.run(info)
    assert deletable == []
    assert updated is info  # same object returned
    assert updated["filepath"] == str(file_path)


def test_try_utime_updates_and_reports(tmp_path):
    """try_utime should update file timestamps and report warning on failure."""
    pp = PostProcessor(DummyDownloader())
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    # set to old times
    old_atime = old_mtime = time.time() - 1000
    os.utime(str(file_path), (old_atime, old_mtime))
    # new times
    new_atime = new_mtime = time.time()
    pp.try_utime(str(file_path), new_atime, new_mtime)
    atime, mtime = os.stat(str(file_path)).st_atime, os.stat(str(file_path)).st_mtime
    assert abs(atime - new_atime) < 1
    assert abs(mtime - new_mtime) < 1
    # simulate failure by passing invalid path
    pp._downloader.report_warning = lambda msg: pp._downloader.warnings.append(msg)
    pp.try_utime("/non/existent/path", new_atime, new_mtime, errnote="Failed to update")
    assert "Failed to update" in pp._downloader.warnings


def test_configuration_args_returns_expected(tmp_path):
    """_configuration_args should return the configured postprocessor_args."""
    downloader = DummyDownloader()
    downloader.params = {"postprocessor_args": ["--foo", "--bar"]}
    pp = PostProcessor(downloader)
    args = pp._configuration_args(default=["--default"])
    assert args == ["--foo", "--bar"]
    # when no config, default is used
    downloader.params = {}
    args_default = pp._configuration_args(default=["--default"])
    assert args_default == ["--default"]
