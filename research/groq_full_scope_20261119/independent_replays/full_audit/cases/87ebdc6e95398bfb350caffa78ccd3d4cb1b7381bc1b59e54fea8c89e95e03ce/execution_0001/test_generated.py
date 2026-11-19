import re
import pytest
from youtube_dl.extractor.fourtube import PornTubeIE


def test_valid_url_regex_matches_expected_groups():
    """The _VALID_URL regex should correctly capture id and display_id."""
    ie = PornTubeIE()
    url = "https://www.porntube.com/videos/teen-couple-doing-anal_7089759"
    m = re.match(ie._VALID_URL, url)
    assert m is not None, "URL should match the regex"
    assert m.group('id') == "7089759"
    assert m.group('display_id') == "teen-couple-doing-anal"
    # Test the mobile variant
    url_mobile = "https://m.porntube.com/videos/teen-couple-doing-anal_7089759"
    m_mobile = re.match(ie._VALID_URL, url_mobile)
    assert m_mobile is not None
    assert m_mobile.group('id') == "7089759"
    assert m_mobile.group('display_id') == "teen-couple-doing-anal"
    # Test the embed variant
    url_embed = "https://www.porntube.com/embed/7089759"
    m_embed = re.match(ie._VALID_URL, url_embed)
    assert m_embed is not None
    assert m_embed.group('id') == "7089759"
    assert m_embed.group('display_id') is None


def test_real_extract_raises_on_invalid_url():
    """_real_extract should raise an AttributeError when the URL does not match the regex."""
    ie = PornTubeIE()
    invalid_url = "https://example.com/not-a-porn-tube-url"
    with pytest.raises(AttributeError):
        ie._real_extract(invalid_url)


def test_url_template_placeholder():
    """The _URL_TEMPLATE should contain a single %s placeholder for the video id."""
    ie = PornTubeIE()
    assert isinstance(ie._URL_TEMPLATE, str)
    assert ie._URL_TEMPLATE.count("%s") == 1
    # Ensure that formatting with an id produces a valid URL
    formatted = ie._URL_TEMPLATE % "123456"
    assert formatted == "https://www.porntube.com/videos/video_123456"
