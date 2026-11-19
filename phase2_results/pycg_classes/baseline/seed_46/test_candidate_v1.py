import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_behavior():
    manager = ClassManager()
    # get should return None for unknown names
    assert manager.get('foo') is None

    module = object()
    instance = manager.create('foo', module)
    assert isinstance(instance, ClassNode)
    # subsequent get returns the same instance
    assert instance is manager.get('foo')
    # get_classes returns the internal dict
    assert manager.get_classes() is manager.names
    assert 'foo' in manager.get_classes()
    assert manager.get_classes()['foo'] is instance

    # creating the same name again returns the same instance
    instance2 = manager.create('foo', module)
    assert instance is instance2

    module2 = object()
    instance_bar = manager.create('bar', module2)
    assert instance_bar is not instance
    assert instance_bar is manager.get('bar')
    assert 'bar' in manager.get_classes()
    assert manager.get_classes()['bar'] is instance_bar

    # unknown names still return None
    assert manager.get('baz') is None
