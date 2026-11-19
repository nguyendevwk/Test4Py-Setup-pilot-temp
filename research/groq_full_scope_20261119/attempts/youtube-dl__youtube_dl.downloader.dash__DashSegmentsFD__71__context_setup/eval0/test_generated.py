import io
import pytest
import urllib.error
from youtube_dl.downloader.dash import DashSegmentsFD
from youtube_dl.utils import DownloadError

class DummyDashSegmentsFD(DashSegmentsFD):
    """A test double that records calls and simulates fragment downloads."""

    def __init__(self, ydl, params):
        super().__init__(ydl, params)
        self.download_calls = []
        self.append_calls = []
        self.finish_called = False
        self.retries = 0
        self.skip_reports = []

    def _prepare_and_start_frag_download(self, ctx):
        ctx['fragment_index'] = 0

    def _download_fragment(self, ctx, fragment_url, info_dict):
        self.download_calls.append((fragment_url, ctx['fragment_index']))
        # Simulate a successful download returning dummy bytes
        return True, b'dummy_fragment_content'

    def _append_fragment(self, ctx, frag_content):
        self.append_calls.append(frag_content)

    def _finish_frag_download(self, ctx):
        self.finish_called = True

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        self.retries += 1

    def report_skip_fragment(self, frag_index):
        self.skip_reports.append(frag_index)

    def report_error(self, msg):
        raise RuntimeError(msg)


def test_normal_single_fragment(tmp_path):
    """Test that a single fragment is downloaded and appended."""
    fd = DummyDashSegmentsFD(ydl=None, params={})
    filename = tmp_path / "output.mp4"
    info = {
        'fragments': [{'url': 'http://example.com/seg1.mp4'}],
    }
    assert fd.real_download(str(filename), info) is True
    assert len(fd.download_calls) == 1
    assert fd.download_calls[0][0] == 'http://example.com/seg1.mp4'
    assert fd.append_calls == [b'dummy_fragment_content']
    assert fd.finish_called is True
    assert fd.retries == 0
    assert fd.skip_reports == []


def test_retry_on_http_error(tmp_path):
    """Test that a fragment is retried on HTTPError and succeeds."""
    class RetryFD(DummyDashSegmentsFD):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.attempt = 0

        def _download_fragment(self, ctx, fragment_url, info_dict):
            self.attempt += 1
            if self.attempt == 1:
                raise urllib.error.HTTPError(fragment_url, 404, "Not Found", {}, io.BytesIO())
            return True, b'success'

    fd = RetryFD(ydl=None, params={'fragment_retries': 2})
    filename = tmp_path / "output.mp4"
    info = {
        'fragments': [{'url': 'http://example.com/seg1.mp4'}],
    }
    assert fd.real_download(str(filename), info) is True
    assert fd.attempt == 2  # first failed, second succeeded
    assert fd.retries == 1  # one retry recorded
    assert fd.append_calls == [b'success']


def test_skip_unavailable_fragment(tmp_path):
    """Test that a missing fragment is skipped when skip_unavailable_fragments is True."""
    class SkipFD(DummyDashSegmentsFD):
        def _download_fragment(self, ctx, fragment_url, info_dict):
            raise DownloadError("network issue")

    fd = SkipFD(ydl=None, params={'skip_unavailable_fragments': True})
    filename = tmp_path / "output.mp4"
    info = {
        'fragments': [{'url': 'http://example.com/seg1.mp4'}],
    }
    # Should return True because fragment is skipped
    assert fd.real_download(str(filename), info) is True
    assert fd.skip_reports == [1]  # fragment index 1 is skipped
    assert fd.append_calls == []   # nothing appended
    assert fd.finish_called is True
