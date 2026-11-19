import pytest
from pycg.machinery.scopes import ScopeManager

def test_handle_module_creates_scopes_and_lists():
    sm = ScopeManager()
    code = "def foo(): pass\nclass Bar: pass\n"
    result = sm.handle_module('mymod', 'mymod.py', code)
    assert result == {"functions": ["mymod.foo"], "classes": ["mymod.Bar"]}

    scopes = sm.get_scopes()
    assert {"mymod", "mymod.foo", "mymod.Bar"}.issubset(set(scopes.keys()))
    assert scopes["mymod.foo"].parent is scopes["mymod"]
    assert scopes["mymod.Bar"].parent is scopes["mymod"]
