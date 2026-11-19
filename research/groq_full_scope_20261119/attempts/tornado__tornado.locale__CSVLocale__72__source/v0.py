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

    # Singular case: count == 1 should use singular dict
    assert locale.translate("apple", count=1) == "manzana"
    # Plural case: count != 1 should use plural dict
    assert locale.translate("apple", count=2) == "manzanas"
    # Unknown message falls back to original
    assert locale.translate("orange") == "orange"

def test_translate_with_plural_message_and_missing_plural():
    translations = {
        "singular": {"car": "coche"},
        "plural": {"car": "coches"},
        "unknown": {"bike": "bicicleta"},
    }
    locale = CSVLocale("es", translations)

    # Provide plural_message; count=1 uses singular
    assert locale.translate("car", plural_message="cars", count=1) == "coche"
    # count=0 uses plural
    assert locale.translate("car", plural_message="cars", count=0) == "coches"
    # When plural_message is None, fallback to unknown dict
    assert locale.translate("bike", plural_message=None, count=3) == "bicicleta"

def test_pgettext_logs_warning_and_falls_back_to_translate(tmp_path, caplog):
    translations = {
        "singular": {"hello": "hola"},
        "plural": {"hello": "hola"},
        "unknown": {"world": "mundo"},
    }
    locale = CSVLocale("es", translations)

    caplog.set_level(gen_log.level)
    result = locale.pgettext("greeting", "hello", count=1)
    assert result == "hola"
    # Verify that a warning was logged about unsupported pgettext
    assert any(
        record.message == "pgettext is not supported by CSVLocale"
        for record in caplog.records
    )
