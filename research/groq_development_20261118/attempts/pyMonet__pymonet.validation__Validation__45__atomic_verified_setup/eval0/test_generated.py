import pytest
from pymonet.validation import Validation

def test_success_and_equality():
    v1 = Validation.success(42)
    v2 = Validation(42, [])
    assert v1 == v2
    assert v1.is_success()
    assert not v1.is_fail()
    assert v1.value == 42
    assert v1.errors == []

def test_fail_and_error_accumulation():
    e1 = Validation.fail(['err1'])
    e2 = Validation.fail(['err2'])
    combined = Validation(e1.value, e1.errors + e2.errors)
    assert combined.is_fail()
    assert combined.errors == ['err1', 'err2']
    assert combined.value is None
    with pytest.raises(TypeError):
        Validation.fail('not a list')  # constructor expects list, but will still accept any iterable

def test_map_and_bind_operations():
    v = Validation.success(3)
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 6
    assert mapped.errors == []

    def folder(x):
        return Validation.success(x + 1)

    bound = v.bind(folder)
    assert bound.value == 4
    assert bound.errors == []

    # bind with failure
    def bad_folder(x):
        return Validation.fail(['bad'])

    bound_fail = v.bind(bad_folder)
    assert bound_fail.is_fail()
    assert bound_fail.errors == ['bad']
    assert bound_fail.value is None
