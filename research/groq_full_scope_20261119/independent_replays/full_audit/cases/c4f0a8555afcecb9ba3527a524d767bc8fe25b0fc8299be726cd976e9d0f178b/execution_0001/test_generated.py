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
    assert DummyAuth in pm
    assert DummyConverter in pm
    assert DummyFormatter in pm
    assert DummyTransport in pm

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
    pm.unregister(DummyAuth)
    assert DummyAuth not in pm
    # Ensure other plugins remain
    assert DummyConverter in pm
    assert DummyFormatter in pm
    assert DummyTransport in pm

def test_get_auth_plugin_mapping_and_retrieval():
    pm = PluginManager()
    pm.register(DummyAuth)
    mapping = pm.get_auth_plugin_mapping()
    assert isinstance(mapping, dict)
    assert "dummy" in mapping
    assert mapping["dummy"] is DummyAuth

    # Retrieval by auth_type
    retrieved = pm.get_auth_plugin("dummy")
    assert retrieved is DummyAuth

    # Ensure KeyError is raised for unknown auth_type
    with pytest.raises(KeyError):
        pm.get_auth_plugin("nonexistent")

def test_get_formatters_grouped_and_str_repr():
    pm = PluginManager()
    pm.register(DummyFormatter)
    grouped = pm.get_formatters_grouped()
    assert isinstance(grouped, dict)
    assert "dummy_group" in grouped
    assert grouped["dummy_group"] == [DummyFormatter]

    # String representation should include the formatter list
    s = str(pm)
    assert "DummyFormatter" in s
    # Representation should be a valid Python representation
    r = repr(pm)
    assert r.startswith("<PluginManager ")
    assert "DummyFormatter" in r
