import pytest
from httpie.plugins.manager import PluginManager
from httpie.plugins.base import BasePlugin
from httpie.plugins import AuthPlugin, FormatterPlugin, ConverterPlugin, TransportPlugin

# Dummy plugin classes for testing
class DummyAuth(AuthPlugin):
    auth_type = "dummy"

class DummyFormatter(FormatterPlugin):
    group_name = "group1"

class DummyFormatter2(FormatterPlugin):
    group_name = "group2"

class DummyConverter(ConverterPlugin):
    pass

class DummyTransport(TransportPlugin):
    pass

def test_register_unregister_and_filter():
    pm = PluginManager()
    # Register multiple plugins
    pm.register(DummyAuth, DummyFormatter, DummyConverter, DummyTransport)
    assert set(pm) == {DummyAuth, DummyFormatter, DummyConverter, DummyTransport}

    # Unregister one plugin
    pm.unregister(DummyConverter)
    assert DummyConverter not in pm
    assert len(pm) == 3

    # Filter by type
    auth_plugins = pm.filter(AuthPlugin)
    assert auth_plugins == [DummyAuth]
    formatter_plugins = pm.filter(FormatterPlugin)
    assert formatter_plugins == [DummyFormatter]
    # Ensure other types are not returned
    assert pm.filter(ConverterPlugin) == []

def test_get_auth_plugin_mapping_and_retrieval():
    pm = PluginManager()
    pm.register(DummyAuth)
    mapping = pm.get_auth_plugin_mapping()
    assert isinstance(mapping, dict)
    assert "dummy" in mapping
    assert mapping["dummy"] is DummyAuth

    # Retrieval by auth_type
    plugin_cls = pm.get_auth_plugin("dummy")
    assert plugin_cls is DummyAuth

    # Ensure KeyError is raised for unknown auth_type
    with pytest.raises(KeyError):
        pm.get_auth_plugin("unknown")

def test_get_formatters_grouped_and_str_repr():
    pm = PluginManager()
    pm.register(DummyFormatter, DummyFormatter2)
    grouped = pm.get_formatters_grouped()
    assert isinstance(grouped, dict)
    assert set(grouped.keys()) == {"group1", "group2"}
    assert grouped["group1"] == [DummyFormatter]
    assert grouped["group2"] == [DummyFormatter2]

    # Test __str__ representation includes all plugin types
    s = str(pm)
    # The string should contain the class names of the registered plugins
    assert "DummyFormatter" in s
    assert "DummyFormatter2" in s
    # It should not contain unregistered plugin types
    assert "DummyAuth" not in s
