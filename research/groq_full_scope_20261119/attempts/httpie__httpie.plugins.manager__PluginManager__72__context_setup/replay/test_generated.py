import pytest
from httpie.plugins.manager import PluginManager, AuthPlugin, ConverterPlugin, FormatterPlugin, TransportPlugin
from httpie.plugins.base import BasePlugin

# Dummy plugin classes for testing
class DummyAuth(AuthPlugin):
    auth_type = "dummy"

class DummyConverter(ConverterPlugin):
    pass

class DummyFormatter(FormatterPlugin):
    group_name = "dummy_group"

class DummyTransport(TransportPlugin):
    pass

def test_register_and_filter():
    pm = PluginManager()
    # Register multiple plugins
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)
    # Ensure all are registered
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

def test_get_auth_plugin_mapping_and_lookup():
    pm = PluginManager()
    pm.register(DummyAuth)
    mapping = pm.get_auth_plugin_mapping()
    # Mapping should contain the dummy auth type
    assert mapping == {"dummy": DummyAuth}
    # Lookup by auth_type should return the correct plugin
    assert pm.get_auth_plugin("dummy") is DummyAuth
    # Lookup for non-existent type should raise KeyError
    with pytest.raises(KeyError):
        pm.get_auth_plugin("nonexistent")

def test_get_formatters_grouped_and_str_repr():
    pm = PluginManager()
    pm.register(DummyFormatter)
    grouped = pm.get_formatters_grouped()
    # Grouped dict should have one group with the dummy formatter
    assert grouped == {"dummy_group": [DummyFormatter]}
    # __str__ should include the formatter in its representation
    s = str(pm)
    assert "DummyFormatter" in s
    # __repr__ should start with the class name
    r = repr(pm)
    assert r.startswith("<PluginManager")
