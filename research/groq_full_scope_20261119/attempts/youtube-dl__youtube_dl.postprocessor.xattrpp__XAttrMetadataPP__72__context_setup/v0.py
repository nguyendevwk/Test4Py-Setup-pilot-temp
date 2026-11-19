import os
import pytest
from youtube_dl.postprocessor.xattrpp import XAttrMetadataPP, XAttrUnavailableError, XAttrMetadataError

class DummyDownloader:
    def __init__(self):
        self.messages = []
    def to_screen(self, msg):
        self.messages.append(('screen', msg))
    def report_error(self, msg):
        self.messages.append(('error', msg))
    def report_warning(self, msg):
        self.messages.append(('warning', msg))

def test_xattr_metadatapp_normal(tmp_path):
    # Create a temporary file to act as the downloaded file
    tmp_file = tmp_path / "video.mp4"
    tmp_file.write_text("dummy content")

    # Prepare info dict with all fields
    info = {
        'filepath': str(tmp_file),
        'webpage_url': 'https://example.com',
        'title': 'Test Video',
        'upload_date': '20240101',
        'description': 'A test video',
        'uploader': 'Tester',
        'format': 'mp4',
    }

    # Patch write_xattr to record calls instead of actually writing
    calls = []
    def fake_write_xattr(path, name, value):
        calls.append((path, name, value))

    downloader = DummyDownloader()
    pp = XAttrMetadataPP(downloader)
    pp._downloader = downloader
    original_write_xattr = XAttrMetadataPP.__dict__['write_xattr'] if 'write_xattr' in XAttrMetadataPP.__dict__ else None
    try:
        # Monkeypatch the function in the module
        import youtube_dl.postprocessor.xattrpp as mod
        mod.write_xattr = fake_write_xattr

        # Run the postprocessor
        pp.run(info)

        # Verify that all expected xattrs were attempted
        expected_names = {
            'user.xdg.referrer.url',
            'user.dublincore.title',
            'user.dublincore.date',
            'user.dublincore.description',
            'user.dublincore.contributor',
            'user.dublincore.format',
        }
        written_names = {name for _, name, _ in calls}
        assert expected_names == written_names

        # Verify that the date was hyphenated
        for _, name, value in calls:
            if name == 'user.dublincore.date':
                assert value.decode() == '2024-01-01'

        # No error or warning should have been reported
        assert all(msg[0] != 'error' for msg in downloader.messages)
        assert all(msg[0] != 'warning' for msg in downloader.messages)
    finally:
        if original_write_xattr is not None:
            mod.write_xattr = original_write_xattr

def test_xattr_metadatapp_unavailable(tmp_path):
    tmp_file = tmp_path / "video.mp4"
    tmp_file.write_text("dummy content")

    info = {'filepath': str(tmp_file), 'title': 'Test'}

    def fake_write_xattr(path, name, value):
        raise XAttrUnavailableError("xattr not supported")

    downloader = DummyDownloader()
    pp = XAttrMetadataPP(downloader)
    pp._downloader = downloader
    import youtube_dl.postprocessor.xattrpp as mod
    original_write_xattr = mod.write_xattr
    try:
        mod.write_xattr = fake_write_xattr
        pp.run(info)
        # Expect an error message reported
        assert any(msg[0] == 'error' and 'xattr not supported' in msg[1] for msg in downloader.messages)
    finally:
        mod.write_xattr = original_write_xattr

def test_xattr_metadatapp_no_space(tmp_path):
    tmp_file = tmp_path / "video.mp4"
    tmp_file.write_text("dummy content")

    info = {'filepath': str(tmp_file), 'title': 'Test'}

    def fake_write_xattr(path, name, value):
        raise XAttrMetadataError('NO_SPACE')

    downloader = DummyDownloader()
    pp = XAttrMetadataPP(downloader)
    pp._downloader = downloader
    import youtube_dl.postprocessor.xattrpp as mod
    original_write_xattr = mod.write_xattr
    try:
        mod.write_xattr = fake_write_xattr
        pp.run(info)
        # Expect a warning about no space
        assert any(msg[0] == 'warning' and 'no disk space' in msg[1] for msg in downloader.messages)
    finally:
        mod.write_xattr = original_write_xattr
