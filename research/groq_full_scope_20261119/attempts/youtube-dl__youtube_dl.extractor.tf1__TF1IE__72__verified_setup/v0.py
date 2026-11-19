import re
import pytest
from youtube_dl.extractor.tf1 import TF1IE

def test_valid_url_parsing():
    """The _VALID_URL regex should correctly capture program_slug and id."""
    url = "https://www.tf1.fr/tmc/quotidien-avec-yann-barthes/videos/quotidien-premiere-partie-11-juin-2019.html"
    match = re.match(TF1IE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    program_slug, slug = match.groups()
    assert program_slug == "tmc/quotidien-avec-yann-barthes", "program_slug extraction failed"
    assert slug == "quotidien-premiere-partie-11-juin-2019", "slug extraction failed"

def test_test_cases_structure():
    """Each test case in _TESTS should contain the expected keys."""
    for test in TF1IE._TESTS:
        # Only check the first test which contains full info_dict
        if 'info_dict' in test:
            info = test['info_dict']
            required_keys = {
                'id', 'ext', 'title', 'description',
                'upload_date', 'timestamp', 'duration',
                'series', 'tags'
            }
            assert required_keys.issubset(info.keys()), f"Missing keys in info_dict: {required_keys - set(info.keys())}"
            # Ensure tags is a list
            assert isinstance(info['tags'], list), "tags should be a list"
        # Ensure each test has either 'only_matching' or 'info_dict'
        assert 'only_matching' in test or 'info_dict' in test, "Test case must specify either only_matching or info_dict"

def test_invalid_url_raises():
    """Providing a URL that does not match _VALID_URL should raise an AttributeError due to .groups() on None."""
    ie = TF1IE()
    bad_url = "https://example.com/not-a-tf1-url"
    with pytest.raises(AttributeError):
        ie._real_extract(bad_url)
