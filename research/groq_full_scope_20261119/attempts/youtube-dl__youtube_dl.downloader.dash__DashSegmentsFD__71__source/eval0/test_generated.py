import pytest
from youtube_dl.downloader.dash import DashSegmentsFD
from youtube_dl.utils import DownloadError
from urllib.error import HTTPError

class DummyDash(DashSegmentsFD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloaded_fragments = []
        self.retries = []

    def _prepare_and_start_frag_download(self, ctx):
        ctx['fragment_index'] = 0

    def _download_fragment(self, ctx, url, info_dict):
        # Simulate success for all fragments except those containing "fail"
        if "fail" in url:
            return False, None
        return True, f"content_of_{url}".encode()

    def _append_fragment(self, ctx, frag_content):
        self.downloaded_fragments.append(frag_content)

    def _finish_frag_download(self, ctx):
        pass

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        self.retries.append((frag_index, count))

    def report_skip_fragment(self, frag_index):
        self.downloaded_fragments.append(b"SKIPPED")

    def report_error(self, msg):
        self.error_msg = msg

def test_normal_download(tmp_path):
    fd = DummyDash()
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'url': 'http://example.com/seg1.mp4'}, {'url': 'http://example.com/seg2.mp4'}]
    }
    result = fd.real_download(tmp_path / 'video.mp4', info)
    assert result is True
    assert len(fd.downloaded_fragments) == 2
    assert fd.downloaded_fragments[0] == b'content_of_http://example.com/seg1.mp4'
    assert fd.downloaded_fragments[1] == b'content_of_http://example.com/seg2.mp4'
    assert fd.retries == []

def test_boundary_first_fragment_fatal(tmp_path):
    fd = DummyDash()
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'url': 'http://example.com/seg1.mp4'}, {'url': 'http://example.com/seg2.mp4'}]
    }
    # Set skip_unavailable_fragments to False to make first fragment fatal
    fd.params['skip_unavailable_fragments'] = False
    result = fd.real_download(tmp_path / 'video.mp4', info)
    assert result is False
    assert fd.error_msg == 'giving up after 0 fragment retries'
    assert fd.downloaded_fragments == []

def test_retry_on_http_error(tmp_path):
    fd = DummyDash()
    fd.params['fragment_retries'] = 2
    info = {
        'fragment_base_url': 'http://example.com/',
        'fragments': [{'url': 'http://example.com/fail.mp4'}, {'url': 'http://example.com/seg2.mp4'}]
    }

    # Override _download_fragment to raise HTTPError on first attempt
    def _download_fragment(ctx, url, info_dict):
        if "fail" in url:
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        return True, f"content_of_{url}".encode()
    fd._download_fragment = _download_fragment

    result = fd.real_download(tmp_path / 'video.mp4', info)
    assert result is False
    # First fragment should be skipped after retries
    assert fd.downloaded_fragments == [b"SKIPPED"]
    # Retries recorded
    assert fd.retries == [(1, 1), (1, 2)]
