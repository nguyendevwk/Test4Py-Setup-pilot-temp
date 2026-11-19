import pytest
from httpie.plugins.manager import PluginManager, AuthPlugin, ConverterPlugin, FormatterPlugin, TransportPlugin
from httpie.plugins.base import BasePlugin

# --------------------------------------------------------------------------- #
# Helper plugin classes for testing
# --------------------------------------------------------------------------- #
class DummyAuth(AuthPlugin):
    auth_type = "dummy"

class DummyConverter(ConverterPlugin):
    pass

class DummyFormatter(FormatterPlugin):
    group_name = "dummy_group"

class DummyTransport(TransportPlugin):
    pass

# --------------------------------------------------------------------------- #
# Test 1: Register, unregister and filter functionality
# --------------------------------------------------------------------------- #
def test_register_unregister_and_filter():
    pm = PluginManager()

    # Register multiple plugins
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)
    assert set(pm) == {DummyAuth, DummyConverter, DummyFormatter, DummyTransport}

    # Unregister one plugin
    pm.unregister(DummyConverter)
    assert DummyConverter not in pm
    assert set(pm) == {DummyAuth, DummyFormatter, DummyTransport}

    # Filter by type
    auth_plugins = pm.filter(AuthPlugin)
    assert auth_plugins == [DummyAuth]

    formatter_plugins = pm.filter(FormatterPlugin)
    assert formatter_plugins == [DummyFormatter]

    transport_plugins = pm.filter(TransportPlugin)
    assert transport_plugins == [DummyTransport]

    # Ensure filtering with a non-existent type returns empty list
    class DummyBase(BasePlugin):
        pass
    assert pm.filter(DummyBase) == []

# --------------------------------------------------------------------------- #
# Test 2: Auth plugin mapping and retrieval
# --------------------------------------------------------------------------- #
def test_auth_plugin_mapping_and_retrieval():
    pm = PluginManager()
    pm.register(DummyAuth)

    # Mapping should contain the auth_type key
    mapping = pm.get_auth_plugin_mapping()
    assert "dummy" in mapping
    assert mapping["dummy"] is DummyAuth

    # Retrieval by auth_type should return the correct class
    retrieved = pm.get_auth_plugin("dummy")
    assert retrieved is DummyAuth

    # Attempting to retrieve a non-existent auth_type should raise KeyError
    with pytest.raises(KeyError):
        pm.get_auth_plugin("nonexistent")

# --------------------------------------------------------------------------- #
# Test 3: String representation includes all plugin categories
# --------------------------------------------------------------------------- #
def test_str_representation_includes_all_categories():
    pm = PluginManager()
    pm.register(DummyAuth, DummyConverter, DummyFormatter, DummyTransport)

    representation = str(pm)

    # The representation should contain the class names of all plugin categories
    assert "DummyAuth" in representation
    assert "DummyConverter" in representation
    assert "DummyFormatter" in representation
    assert "DummyTransport" in representation

    # Ensure the representation is a dictionary-like string
    assert representation.startswith("{") and representation.endswith("}")
