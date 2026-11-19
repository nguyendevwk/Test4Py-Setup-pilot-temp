import pytest
from tornado.locale import CSVLocale

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
    # Plural case with count == 1 should still use singular
    assert locale.translate("apple", plural_message="apples", count=1) == "manzana"

def test_translate_unknown_message_returns_original():
    translations = {"singular": {"cat": "gato"}}
    locale = CSVLocale("es", translations)

    # Message not in any dict should return itself
    assert locale.translate("dog") == "dog"
    # Unknown with plural_message should still return original
    assert locale.translate("dog", plural_message="dogs", count=2) == "dogs"

def test_pgettext_logs_warning_and_falls_back_to_translate(tmp_path, caplog):
    translations = {"singular": {"hello": "hola"}}
    locale = CSVLocale("es", translations)

    caplog.set_level("WARNING")
    result = locale.pgettext("greeting", "hello")
    assert result == "hola"
    # Verify that a warning was logged
    assert any(
        "pgettext is not supported by CSVLocale" in rec.message
        for rec in caplog.records
    )
