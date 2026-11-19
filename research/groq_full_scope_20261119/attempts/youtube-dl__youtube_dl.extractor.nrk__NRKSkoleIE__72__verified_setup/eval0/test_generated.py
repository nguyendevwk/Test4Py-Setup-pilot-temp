import pytest
from youtube_dl.extractor.nrk import NRKSkoleIE

def test_valid_url_parsing():
    """The extractor should correctly parse the mediaId from a valid URL."""
    ie = NRKSkoleIE()
    url = 'https://www.nrk.no/skole/?page=search&q=&mediaId=14099'
    video_id = ie._match_id(url)
    assert video_id == '14099', f"Expected mediaId '14099', got {video_id}"

def test_only_matching_url():
    """The second test case should only match the URL and not attempt extraction."""
    ie = NRKSkoleIE()
    url = 'https://www.nrk.no/skole/?page=objectives&subject=naturfag&objective=K15114&mediaId=19355'
    # The extractor should match the URL but the test data indicates only_matching,
    # so we just confirm that _match_id works and no further extraction is attempted.
    video_id = ie._match_id(url)
    assert video_id == '19355', f"Expected mediaId '19355', got {video_id}"

def test_real_extract(monkeypatch):
    """_real_extract should return a url_result with the correct NRK ID format."""
    ie = NRKSkoleIE()
    # Monkeypatch _download_json to avoid network calls and return a controlled response
    def fake_download_json(url, video_id):
        # The URL passed to _download_json should contain the video_id
        assert video_id == '14099'
        assert f'/media/{video_id}' in url
        return {'psId': '6021'}
    monkeypatch.setattr(ie, '_download_json', fake_download_json)

    url = 'https://www.nrk.no/skole/?page=search&q=&mediaId=14099'
    result = ie._real_extract(url)
    # The result should be a url_result with the NRK ID prefixed by 'nrk:'
    assert result.url == 'nrk:6021', f"Expected 'nrk:6021', got {result.url}"
    assert result._type == 'url', f"Expected result type 'url', got {result._type}"
