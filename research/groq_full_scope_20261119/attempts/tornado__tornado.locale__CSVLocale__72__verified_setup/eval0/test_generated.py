import pytest
from tornado.locale import CSVLocale
from tornado.log import gen_log

def test_translate_singular_and_plural():
    translations = {
        "singular": {"apple": "manzana"},
        "plural": {"apple": "manzanas"},
        "unknown": {"banana": "plátano"},
    }
    locale = CSVLocale("es", translations)

    # Singular case
    assert locale.translate("apple") == "manzana"
    # Plural case with count != 1
    assert locale.translate("apple", plural_message="apples", count=3) == "manzanas"
    # Plural case with count == 1 uses singular
    assert locale.translate("apple", plural_message="apples", count=1) == "manzana"
    # Unknown message falls back to original
    assert locale.translate("banana") == "plátano"
    # Unknown message not in translations returns original
    assert locale.translate("orange") == "orange"

def test_translate_missing_count_raises():
    translations = {"singular": {"cat": "gato"}}
    locale = CSVLocale("es", translations)
    # When plural_message is provided but count is None, an AssertionError should be raised
    with pytest.raises(AssertionError):
        locale.translate("cat", plural_message="cats", count=None)

def test_pgettext_logs_warning_and_falls_back():
    translations = {"singular": {"dog": "perro"}}
    locale = CSVLocale("es", translations)
    with pytest.warns(UserWarning) as record:
        result = locale.pgettext("animal", "dog")
    # The warning should be logged by gen_log
    assert any("pgettext is not supported by CSVLocale" in r.message for r in record)
    # The translation should still work
    assert result == "perro"
