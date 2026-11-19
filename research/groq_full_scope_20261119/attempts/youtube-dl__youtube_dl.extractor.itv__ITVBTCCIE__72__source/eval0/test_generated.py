import re
import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.extractor.brightcove import BrightcoveNewIE
from youtube_dl.utils import smuggle_url

# Test 1: URL matching extracts the correct ID from various ITV BTCC URLs
def test_itv_btcc_id_extraction():
    ie = ITVBTCCIE()
    # Valid URL with nested path
    url = 'https://www.itv.com/btcc/races/btcc-2018-all-the-action-from-brands-hatch'
    assert ie._match_id(url) == 'btcc-2018-all-the-action-from-brands-hatch'
    # URL without subpath
    url2 = 'http://itv.com/btcc/btcc-2020-something'
    assert ie._match_id(url2) == 'btcc-2020-something'
    # URL with trailing slash
    url3 = 'https://www.itv.com/btcc/btcc-2021/'
    assert ie._match_id(url3) == 'btcc-2021'
    # URL with query parameters
    url4 = 'https://www.itv.com/btcc/btcc-2022?foo=bar'
    assert ie._match_id(url4) == 'btcc-2022'

# Test 2: Brightcove URL template is correctly formatted and smuggled with geo blocks
def test_brightcove_url_template_and_smuggling():
    ie = ITVBTCCIE()
    video_id = '1234567890'
    expected_url = f'http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId={video_id}'
    smuggled = smuggle_url(expected_url, {
        'geo_ip_blocks': ['193.113.0.0/16', '54.36.162.0/23', '159.65.16.0/21'],
        'referrer': 'http://example.com'
    })
    # The smuggled URL should contain the original URL and the smuggled params
    assert smuggled.startswith(expected_url)
    # The smuggled params are encoded in the URL after a special marker
    assert 'geo_ip_blocks' in smuggled
    assert 'referrer' in smuggled

# Test 3: url_result produces a Brightcove IE result with the correct video ID
def test_url_result_with_brightcove_ie():
    ie = ITVBTCCIE()
    video_id = '987654321'
    smuggled_url = smuggle_url(
        f'http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId={video_id}',
        {'referrer': 'http://test.com'}
    )
    result = ie.url_result(smuggled_url, ie=BrightcoveNewIE.ie_key(), video_id=video_id)
    # The result should be a dict with the expected keys
    assert isinstance(result, dict)
    assert result['url'] == smuggled_url
    assert result['ie_key'] == BrightcoveNewIE.ie_key()
    assert result['video_id'] == video_id
