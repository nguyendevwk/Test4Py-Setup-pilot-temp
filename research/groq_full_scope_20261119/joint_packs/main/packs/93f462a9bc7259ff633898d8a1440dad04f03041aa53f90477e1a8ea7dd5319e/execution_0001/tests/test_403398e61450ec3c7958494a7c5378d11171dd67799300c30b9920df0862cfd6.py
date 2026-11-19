import pytest
from httpie.plugins.manager import PluginManager
from httpie.plugins.base import BasePlugin
from httpie.plugins import AuthPlugin, ConverterPlugin, FormatterPlugin, TransportPlugin

# Dummy plugin classes for testing
class DummyAuth(AuthPlugin):
    auth_type = "dummy"

class DummyConverter(ConverterPlugin):
    pass

class DummyFormatter(FormatterPlugin):
    group_name = "dummy_group"

class DummyTransport(TransportPlugin):
    pass

def test_register_and_unregister_and_filter():
    pm = PluginManager()
    # Register multiple plugins
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)
    # All plugins should be present
    assert set(pm) == {DummyAuth, DummyConverter, DummyFormatter, DummyTransport}
    # Filter by type
    auth_plugins = pm.filter(AuthPlugin)
    assert auth_plugins == [DummyAuth]
    converter_plugins = pm.filter(ConverterPlugin)
    assert converter_plugins == [DummyConverter]
    formatter_plugins = pm.filter(FormatterPlugin)
    assert formatter_plugins == [DummyFormatter]
    transport_plugins = pm.filter(TransportPlugin)
    assert transport_plugins == [DummyTransport]
    # Unregister a plugin and verify removal
    pm.unregister(DummyConverter)
    assert DummyConverter not in pm
    # After removal, filter should not return it
    assert pm.filter(ConverterPlugin) == []

def test_get_auth_plugin_mapping_and_lookup():
    pm = PluginManager()
    pm.register(DummyAuth)
    mapping = pm.get_auth_plugin_mapping()
    # Mapping should contain the auth_type key
    assert "dummy" in mapping
    assert mapping["dummy"] is DummyAuth
    # get_auth_plugin should return the same class
    assert pm.get_auth_plugin("dummy") is DummyAuth
    # Requesting a non-existent auth_type should raise KeyError
    with pytest.raises(KeyError):
        pm.get_auth_plugin("nonexistent")

def test_get_formatters_grouped_and_str_repr():
    pm = PluginManager()
    pm.register(DummyFormatter, DummyFormatter)  # register twice to test grouping
    grouped = pm.get_formatters_grouped()
    # All formatters should be grouped under 'dummy_group'
    assert "dummy_group" in grouped
    assert grouped["dummy_group"] == [DummyFormatter, DummyFormatter]
    # __str__ should include all plugin categories
    s = str(pm)
    # It should contain the class names of each plugin type
    assert "DummyAuth" not in s  # not registered
    assert "DummyFormatter" in s
    assert "DummyTransport" not in s
    # __repr__ should start with the class name
    r = repr(pm)
    assert r.startswith("<PluginManager ")
