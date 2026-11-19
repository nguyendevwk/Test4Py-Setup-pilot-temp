import pytest
from tornado.locale import CSVLocale

def test_translate_singular_and_plural():
    # translations dict with singular and plural entries
    translations = {
        "singular": {"apple": "manzana"},
        "plural": {"apple": "manzanas"},
        "unknown": {"banana": "plátano"},
    }
    locale = CSVLocale("es", translations)

    # singular case
    assert locale.translate("apple", count=1) == "manzana"
    # plural case
    assert locale.translate("apple", count=3) == "manzanas"
    # unknown message falls back to key
    assert locale.translate("banana") == "plátano"
    # message not in dict falls back to original
    assert locale.translate("orange") == "orange"

def test_translate_with_plural_message_and_count():
    translations = {
        "singular": {"car": "coche"},
        "plural": {"car": "coches"},
    }
    locale = CSVLocale("es", translations)

    # use plural_message explicitly
    assert locale.translate("car", plural_message="cars", count=1) == "coche"
    assert locale.translate("car", plural_message="cars", count=2) == "coches"
    # when count is 1, plural_message should be ignored
    assert locale.translate("car", plural_message="cars", count=1) == "coche"

def test_pgettext_logs_warning_and_falls_back_to_translate(tmp_path, caplog):
    translations = {"singular": {"hello": "hola"}}
    locale = CSVLocale("es", translations)

    caplog.set_level("WARNING")
    result = locale.pgettext("greeting", "hello")
    assert result == "hola"
    # Verify that a warning was logged
    assert any(
        record.message == "pgettext is not supported by CSVLocale"
        for record in caplog.records
    )
