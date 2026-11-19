import io
import pytest
from types import SimpleNamespace
from urllib.error import HTTPError

# Import the target class
from youtube_dl.downloader.dash import DashSegmentsFD
from youtube_dl.utils import DownloadError

class DummyDashFD(DashSegmentsFD):
    """A minimal subclass that records calls and simulates fragment download."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_calls = []
        self.append_calls = []
        self.finish_called = False
        self.prepare_called = False

    def _prepare_and_start_frag_download(self, ctx):
        self.prepare_called = True

    def _download_fragment(self, ctx, url, info_dict):
        self.download_calls.append((url, ctx['fragment_index']))
        # Simulate a successful download returning dummy bytes
        return True, b'dummy_fragment_content'

    def _append_fragment(self, ctx, frag_content):
        self.append_calls.append(frag_content)

    def _finish_frag_download(self, ctx):
        self.finish_called = True

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        pass

    def report_skip_fragment(self, frag_index):
        pass

    def report_error(self, msg):
        pass

@pytest.fixture
def dummy_fd(tmp_path):
    """Return a DummyDashFD instance with a temporary file path."""
    return DummyDashFD(ydl=None, params={})

def test_successful_single_fragment_download(tmp_path, dummy_fd):
    """Test that a single fragment is downloaded and appended correctly."""
    file_path = tmp_path / "output.mp4"
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'url': 'http://example.com/seg1.mp4'}],
    }
    result = dummy_fd.real_download(str(file_path), info)
    assert result is True
    assert dummy_fd.prepare_called
    assert dummy_fd.finish_called
    assert dummy_fd.download_calls == [('http://example.com/seg1.mp4', 1)]
    assert dummy_fd.append_calls == [b'dummy_fragment_content']

def test_retry_on_http_error(tmp_path, dummy_fd):
    """Test that a fragment is retried on HTTPError and succeeds."""
    file_path = tmp_path / "output.mp4"
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'url': 'http://example.com/seg1.mp4'}],
    }

    # Replace _download_fragment to raise HTTPError on first call, then succeed
    call_counter = {'count': 0}
    def flaky_download(ctx, url, info_dict):
        call_counter['count'] += 1
        if call_counter['count'] == 1:
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        return True, b'successful_content'

    dummy_fd._download_fragment = flaky_download

    result = dummy_fd.real_download(str(file_path), info)
    assert result is True
    # Ensure two download attempts were made
    assert call_counter['count'] == 2
    assert dummy_fd.append_calls == [b'successful_content']

def test_skip_unavailable_fragment(tmp_path, dummy_fd):
    """Test that a fragment with missing URL is skipped when skip_unavailable_fragments is True."""
    file_path = tmp_path / "output.mp4"
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'path': 'seg1.mp4'}],  # no 'url' key
    }
    # Override _download_fragment to raise DownloadError to simulate failure
    def fail_download(ctx, url, info_dict):
        raise DownloadError("Simulated download error")

    dummy_fd._download_fragment = fail_download

    result = dummy_fd.real_download(str(file_path), info)
    # Since skip_unavailable_fragments is True, the failure should be skipped and download succeeds
    assert result is True
    # No fragment should be appended
    assert dummy_fd.append_calls == []
    # The download call should have used the joined URL
    assert dummy_fd.download_calls[0][0] == 'http://example.com/seg1.mp4'
