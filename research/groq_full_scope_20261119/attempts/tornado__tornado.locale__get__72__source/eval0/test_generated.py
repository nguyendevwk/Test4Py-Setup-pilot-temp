import pytest
from tornado.locale import get

def test_default_locale_returns_en_us(tmp_path):
    """When no matching locale is found, the default en_US is returned."""
    locale = get("xx_YY")  # unlikely to exist
    # The default locale name should be 'en_US'
    assert hasattr(locale, "locale_name")
    assert locale.locale_name == "en_US"

def test_specific_locale_returns_requested(tmp_path):
    """Providing a specific locale code returns that locale if available."""
    # 'en_US' is guaranteed to exist in the standard distribution
    locale = get("en_US")
    assert locale.locale_name == "en_US"

def test_multiple_codes_prioritizes_first_match(tmp_path):
    """When multiple locale codes are supplied, the first matching one is chosen."""
    # 'xx_YY' is unlikely to exist, so the next should be used
    locale = get("xx_YY", "en_GB")
    # 'en_GB' should be returned if available; otherwise fallback to default
    if hasattr(locale, "locale_name"):
        assert locale.locale_name in ("en_GB", "en_US")
    else:
        pytest.fail("Locale object does not have locale_name attribute")
