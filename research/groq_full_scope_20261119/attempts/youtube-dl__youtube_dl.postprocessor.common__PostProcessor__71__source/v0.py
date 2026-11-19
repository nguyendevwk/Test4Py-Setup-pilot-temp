import os
import time
import pytest
from youtube_dl.postprocessor.common import PostProcessor
from youtube_dl.utils import PostProcessingError, cli_configuration_args, encodeFilename

class DummyDownloader:
    def __init__(self):
        self.warnings = []

    def report_warning(self, msg):
        self.warnings.append(msg)

    @property
    def params(self):
        return {}

def test_run_returns_default(tmp_path):
    pp = PostProcessor()
    info = {"filepath": str(tmp_path / "file.mp4")}
    files_to_delete, updated_info = pp.run(info)
    assert files_to_delete == []
    assert updated_info is info

def test_try_utime_updates_file_times(tmp_path):
    downloader = DummyDownloader()
    pp = PostProcessor(downloader)
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    before = os.stat(file_path).st_mtime
    new_mtime = before + 100
    pp.try_utime(file_path, before, new_mtime)
    after = os.stat(file_path).st_mtime
    assert after == new_mtime
    assert downloader.warnings == []

def test_try_utime_raises_warning_on_error(tmp_path):
    downloader = DummyDownloader()
    pp = PostProcessor(downloader)
    file_path = tmp_path / "readonly.txt"
    file_path.write_text("content")
    file_path.chmod(0o444)  # read-only
    before = os.stat(file_path).st_mtime
    new_mtime = before + 100
    pp.try_utime(file_path, before, new_mtime, errnote="Failed to update")
    after = os.stat(file_path).st_mtime
    assert after == before
    assert downloader.warnings == ["Failed to update"]
