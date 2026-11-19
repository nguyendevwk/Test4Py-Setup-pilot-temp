import pytest
from httpie.plugins.manager import PluginManager
from httpie.plugins.base import BasePlugin
from httpie.plugins import AuthPlugin, ConverterPlugin, FormatterPlugin, TransportPlugin


# Dummy plugin classes for testing
class DummyAuth(AuthPlugin):
    auth_type = "dummy_auth"


class DummyConverter(ConverterPlugin):
    pass


class DummyFormatter(FormatterPlugin):
    group_name = "dummy_group"


class DummyTransport(TransportPlugin):
    pass


def test_register_and_unregister():
    pm = PluginManager()
    # Register multiple plugins
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)
    assert set(pm) == {DummyAuth, DummyConverter, DummyFormatter, DummyTransport}

    # Unregister one plugin
    pm.unregister(DummyConverter)
    assert DummyConverter not in pm
    assert set(pm) == {DummyAuth, DummyFormatter, DummyTransport}

    # Unregistering a non‑registered plugin should raise ValueError
    with pytest.raises(ValueError):
        pm.unregister(DummyConverter)


def test_filter_and_getters():
    pm = PluginManager()
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)

    # filter by type
    assert pm.filter(AuthPlugin) == [DummyAuth]
    assert pm.filter(ConverterPlugin) == [DummyConverter]
    assert pm.filter(FormatterPlugin) == [DummyFormatter]
    assert pm.filter(TransportPlugin) == [DummyTransport]

    # auth plugin mapping
    mapping = pm.get_auth_plugin_mapping()
    assert mapping == {"dummy_auth": DummyAuth}
    assert pm.get_auth_plugin("dummy_auth") is DummyAuth

    # formatters grouped
    grouped = pm.get_formatters_grouped()
    assert grouped == {"dummy_group": [DummyFormatter]}

    # converters list
    assert pm.get_converters() == [DummyConverter]

    # transport plugins list
    assert pm.get_transport_plugins() == [DummyTransport]


def test_str_and_repr_output(tmp_path):
    pm = PluginManager()
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)

    # __str__ should contain the plugin classes in the correct keys
    s = str(pm)
    assert "'adapters': [<class 'httpie.plugins.manager.DummyTransport'>]" in s
    assert "'auth': [<class 'httpie.plugins.manager.DummyAuth'>]" in s
    assert "'converters': [<class 'httpie.plugins.manager.DummyConverter'>]" in s
    assert "'formatters': [<class 'httpie.plugins.manager.DummyFormatter'>]" in s

    # __repr__ should wrap the __str__ output
    r = repr(pm)
    assert r.startswith("<PluginManager ")
    assert r.endswith(">")
    assert s in r
