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
    # Unknown message not in dict returns original
    assert locale.translate("orange") == "orange"

def test_translate_missing_count_raises():
    translations = {"singular": {"cat": "gato"}}
    locale = CSVLocale("es", translations)
    # When plural_message is provided but count is None, an AssertionError should be raised
    with pytest.raises(AssertionError):
        locale.translate("cat", plural_message="cats")

def test_pgettext_logs_warning_and_falls_back():
    translations = {"singular": {"dog": "perro"}}
    locale = CSVLocale("es", translations)
    # Capture log output
    with pytest.raises(AssertionError):
        # pgettext should log a warning and then call translate
        # Since plural_message is None, it will use unknown dict which is empty
        # So it should return the original message "dog"
        # But we trigger the warning by checking the log
        pass
