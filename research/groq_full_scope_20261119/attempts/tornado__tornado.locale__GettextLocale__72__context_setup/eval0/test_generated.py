import pytest
from tornado.locale import GettextLocale, CONTEXT_SEPARATOR

class DummyTranslations:
    """Simple mock of gettext translations that echoes inputs."""
    def gettext(self, msg):
        return f"translated:{msg}"
    def ngettext(self, singular, plural, count):
        return f"translated:{singular if count == 1 else plural}:{count}"

def test_translate_single_and_plural():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Single message
    assert locale.translate("hello") == "translated:hello"
    # Plural message with count 1
    assert locale.translate("apple", "apples", 1) == "translated:apple:1"
    # Plural message with count 5
    assert locale.translate("apple", "apples", 5) == "translated:apples:5"

def test_pgettext_context_and_plural():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Context without plural
    result = locale.pgettext("greeting", "hello")
    # DummyTranslations returns translated:context\x04hello
    assert result == "translated:greeting\x04hello"
    # Context with plural, count 1
    result = locale.pgettext("fruit", "apple", "apples", 1)
    assert result == "translated:apple:1"
    # Context with plural, count 3
    result = locale.pgettext("fruit", "apple", "apples", 3)
    assert result == "translated:apples:3"

def test_error_on_missing_count():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    with pytest.raises(AssertionError):
        locale.translate("apple", "apples")  # missing count
    with pytest.raises(AssertionError):
        locale.pgettext("fruit", "apple", "apples")  # missing count
