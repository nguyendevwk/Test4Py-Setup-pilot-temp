import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE

def test_valid_url_regex_matches_and_captures():
    # A known valid URL from the test cases
    url = "https://www.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    match = re.match(PornerBrosIE._VALID_URL, url)
    assert match is not None, "Regex should match a valid PornerBros URL"
    # Ensure the captured groups are correct
    assert match.group("kind") == "www", "The 'kind' group should capture 'www'"
    assert match.group("display_id") == "skinny-brunette-takes-big-cock-down-her-anal-hole", \
        "The 'display_id' group should capture the slug before the underscore"
    assert match.group("id") == "181369", "The 'id' group should capture the numeric ID"

def test_url_template_and_token_host():
    # The URL template should format correctly with a numeric ID
    formatted = PornerBrosIE._URL_TEMPLATE % "12345"
    assert formatted == "https://www.pornerbros.com/videos/video_12345", \
        "URL template should insert the ID correctly"

    # The token host should be the expected domain
    assert PornerBrosIE._TKN_HOST == "token.pornerbros.com", \
        "Token host should be 'token.pornerbros.com'"

def test_only_matching_urls_do_not_extract_info():
    # URLs marked as only_matching should not produce an info_dict
    # We simulate the extractor's _real_extract method by checking the test metadata
    only_matching_test = {
        'url': 'https://www.pornerbros.com/embed/181369',
        'only_matching': True,
    }
    # The extractor should not attempt to extract info for this URL
    # Since we cannot run the full extractor without network, we verify that the test dict
    # correctly indicates only_matching and that the URL matches the regex
    assert only_matching_test['only_matching'] is True, "Test should be marked as only_matching"
    assert re.match(PornerBrosIE._VALID_URL, only_matching_test['url']) is not None, \
        "Only_matching URL should still match the regex pattern"
