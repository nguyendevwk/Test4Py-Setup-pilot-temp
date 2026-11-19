import pytest
from types import SimpleNamespace
from urllib.error import HTTPError

# Import the target class
from youtube_dl.downloader.dash import DashSegmentsFD
from youtube_dl.utils import DownloadError


class DummyDashSegmentsFD(DashSegmentsFD):
    """A test double that records calls and simulates fragment download."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_calls = []
        self.append_calls = []
        self.finish_called = False
        self.retry_reports = []
        self.skip_reports = []
        self.error_reports = []

    def _prepare_and_start_frag_download(self, ctx):
        ctx['fragment_index'] = 0  # start from first fragment

    def _download_fragment(self, ctx, url, info_dict):
        self.download_calls.append((url, ctx['filename']))
        # Simulate success for all URLs except those containing "fail"
        if "fail" in url:
            return False, None
        return True, b"content_of_" + url.encode()

    def _append_fragment(self, ctx, frag_content):
        self.append_calls.append(frag_content)

    def _finish_frag_download(self, ctx):
        self.finish_called = True

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        self.retry_reports.append((frag_index, count, max_retries))

    def report_skip_fragment(self, frag_index):
        self.skip_reports.append(frag_index)

    def report_error(self, msg):
        self.error_reports.append(msg)


def test_successful_download(tmp_path):
    """Normal download of two fragments succeeds."""
    fd = DummyDashSegmentsFD()
    filename = str(tmp_path / "video.mp4")
    info = {
        "fragment_base_url": "http://example.com/",
        "fragments": [
            {"url": "http://example.com/seg1.mp4"},
            {"url": "http://example.com/seg2.mp4"},
        ],
    }
    result = fd.real_download(filename, info)
    assert result is True
    assert fd.download_calls == [
        ("http://example.com/seg1.mp4", filename),
        ("http://example.com/seg2.mp4", filename),
    ]
    assert fd.append_calls == [
        b"content_of_http://example.com/seg1.mp4",
        b"content_of_http://example.com/seg2.mp4",
    ]
    assert fd.finish_called
    assert not fd.retry_reports
    assert not fd.skip_reports
    assert not fd.error_reports


def test_retry_on_http_error(tmp_path):
    """Fragment download retries on HTTPError and succeeds."""
    class ErroringFD(DummyDashSegmentsFD):
        def _download_fragment(self, ctx, url, info_dict):
            self.download_calls.append((url, ctx['filename']))
            if "retry" in url and not hasattr(self, "retried"):
                self.retried = True
                raise HTTPError(url, 404, "Not Found", {}, None)
            return True, b"content_of_" + url.encode()

    fd = ErroringFD(params={"fragment_retries": 2})
    filename = str(tmp_path / "video.mp4")
    info = {
        "fragment_base_url": "http://example.com/",
        "fragments": [
            {"url": "http://example.com/retry.mp4"},
            {"url": "http://example.com/seg2.mp4"},
        ],
    }
    result = fd.real_download(filename, info)
    assert result is True
    # First fragment retried once
    assert fd.retry_reports == [(1, 1, 2)]
    assert fd.append_calls == [
        b"content_of_http://example.com/retry.mp4",
        b"content_of_http://example.com/seg2.mp4",
    ]


def test_skip_nonfatal_fragment_on_download_error(tmp_path):
    """Non‑fatal fragment that fails is skipped after retries."""
    class SkippingFD(DummyDashSegmentsFD):
        def _download_fragment(self, ctx, url, info_dict):
            self.download_calls.append((url, ctx['filename']))
            # Simulate failure for the second fragment
            if "bad" in url:
                return False, None
            return True, b"content_of_" + url.encode()

    fd = SkippingFD(params={"fragment_retries": 1, "skip_unavailable_fragments": True})
    filename = str(tmp_path / "video.mp4")
    info = {
        "fragment_base_url": "http://example.com/",
        "fragments": [
            {"url": "http://example.com/seg1.mp4"},
            {"url": "http://example.com/bad.mp4"},
            {"url": "http://example.com/seg3.mp4"},
        ],
    }
    result = fd.real_download(filename, info)
    assert result is True
    # Second fragment should be skipped
    assert fd.skip_reports == [2]
    # Third fragment should still be downloaded
    assert fd.append_calls[-1] == b"content_of_http://example.com/seg3.mp4"
    assert fd.finish_called
