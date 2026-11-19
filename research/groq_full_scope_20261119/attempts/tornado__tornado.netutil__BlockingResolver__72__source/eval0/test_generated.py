import pytest
from tornado.netutil import BlockingResolver
from tornado.concurrent import dummy_executor

def test_blocking_resolver_initialization(tmp_path):
    """BlockingResolver should initialize without raising exceptions."""
    resolver = BlockingResolver()
    # The initialize method should call the superclass initialize and not raise.
    resolver.initialize()
    # After initialization, the resolver should have an executor attribute set to dummy_executor.
    assert getattr(resolver, "executor", None) is dummy_executor

def test_blocking_resolver_is_executor_resolver(tmp_path):
    """BlockingResolver should be an instance of ExecutorResolver."""
    resolver = BlockingResolver()
    # ExecutorResolver is the base class; check isinstance.
    assert isinstance(resolver, BlockingResolver.__mro__[1])  # ExecutorResolver

def test_blocking_resolver_resolve_method_exists(tmp_path):
    """BlockingResolver should expose a resolve method that accepts a hostname."""
    resolver = BlockingResolver()
    resolver.initialize()
    # The resolve method should exist and be callable.
    assert hasattr(resolver, "resolve")
    assert callable(resolver.resolve)
    # Calling resolve with a simple hostname should return a list of addresses.
    addresses = resolver.resolve("localhost")
    assert isinstance(addresses, list)
    # Each address tuple should contain at least 5 elements as per socket.getaddrinfo.
    for addr in addresses:
        assert len(addr) >= 5
