import os
import pytest
from youtube_dl.postprocessor.common import PostProcessor
from youtube_dl.utils import PostProcessingError, cli_configuration_args, encodeFilename

class DummyDownloader:
    def __init__(self):
        self.warnings = []

    def report_warning(self, msg):
        self.warnings.append(msg)

class DummyPP(PostProcessor):
    def run(self, information):
        # Return a file to delete and modify information
        return [information["filepath"]], {"new": True, **information}

def test_run_returns_expected_tuple(tmp_path):
    """PostProcessor.run should return a tuple of deletable files and updated info."""
    downloader = DummyDownloader()
    pp = DummyPP(downloader)
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {"filepath": str(file_path), "title": "test"}
    deletable, updated = pp.run(info)
    assert deletable == [str(file_path)]
    assert updated["new"] is True
    assert updated["filepath"] == str(file_path)
    assert updated["title"] == "test"

def test_try_utime_updates_timestamp_and_reports_warning(tmp_path):
    """try_utime should update file timestamps or report a warning on failure."""
    downloader = DummyDownloader()
    pp = PostProcessor(downloader)
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    # Record original times
    orig_atime, orig_mtime = os.stat(file_path).st_atime, os.stat(file_path).st_mtime
    # Update times to zero
    pp.try_utime(file_path, 0, 0)
    new_atime, new_mtime = os.stat(file_path).st_atime, os.stat(file_path).st_mtime
    assert new_atime == 0
    assert new_mtime == 0
    # Now force an exception by passing an invalid path
    pp.try_utime("/nonexistent/path", 0, 0)
    assert "Cannot update utime of file" in downloader.warnings[0]

def test_configuration_args_returns_cli_overrides(tmp_path):
    """_configuration_args should return overridden arguments from downloader params."""
    class Params:
        def __init__(self, args):
            self.postprocessor_args = args
    downloader = DummyDownloader()
    downloader.params = Params(["--foo", "--bar"])
    pp = PostProcessor(downloader)
    # Default empty list should be overridden
    args = pp._configuration_args()
    assert args == ["--foo", "--bar"]
    # Providing a default list should be ignored when override exists
    args_with_default = pp._configuration_args(default=["--default"])
    assert args_with_default == ["--foo", "--bar"]
