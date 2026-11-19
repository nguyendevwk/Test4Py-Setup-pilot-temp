import re
import pytest
from youtube_dl.extractor.tf1 import TF1IE

def test_valid_url_parsing():
    url = 'https://www.tf1.fr/tmc/quotidien-avec-yann-barthes/videos/quotidien-premiere-partie-11-juin-2019.html'
    match = re.match(TF1IE._VALID_URL, url)
    assert match is not None
    program_slug, slug = match.groups()
    assert program_slug == 'tmc'
    assert slug == 'quotidien-premiere-partie-11-juin-2019'

def test_invalid_url_no_match():
    url = 'https://www.example.com/not-a-tf1-url'
    assert re.match(TF1IE._VALID_URL, url) is None

def test_only_matching_urls():
    # URLs that should only match the pattern but not be fully processed
    urls = [
        'http://www.tf1.fr/tf1/koh-lanta/videos/replay-koh-lanta-22-mai-2015.html',
        'http://www.tf1.fr/hd1/documentaire/videos/mylene-farmer-d-une-icone.html',
    ]
    for url in urls:
        match = re.match(TF1IE._VALID_URL, url)
        assert match is not None
        program_slug, slug = match.groups()
        # The slug part should not contain a dot before .html
        assert '.' not in slug
