import inspect
import types
import importlib

def test_main_is_callable_and_returns_none():
    mod = importlib.import_module("tornado.httpclient")
    assert hasattr(mod, "main"), "module should have a 'main' attribute"
    assert isinstance(mod.main, types.FunctionType), "'main' should be a function"
    sig = inspect.signature(mod.main)
    assert sig.return_annotation is inspect.Signature.empty or sig.return_annotation is None, \
        "main should return None (or no annotation)"
    assert sig.parameters == (), "main should take no parameters"

def test_main_imports_required_names():
    mod = importlib.import_module("tornado.httpclient")
    required = {"HTTPClient", "HTTPError"}
    for name in required:
        assert hasattr(mod, name), f"module should expose '{name}'"
    # Ensure that the imported names are the expected classes
    assert isinstance(mod.HTTPClient, type), "HTTPClient should be a class"
    assert isinstance(mod.HTTPError, type), "HTTPError should be a class"

def test_main_signature_and_docstring():
    mod = importlib.import_module("tornado.httpclient")
    main = mod.main
    # Verify that the function has a docstring (even if empty)
    assert main.__doc__ is not None, "main should have a docstring (can be empty)"
    # Verify that the signature has no parameters
    assert len(inspect.signature(main).parameters) == 0, "main should accept no arguments"
