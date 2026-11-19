import pytest
from pymonet.maybe import Maybe


def test_just_and_nothing_equality_and_identity():
    a = Maybe.just(10)
    b = Maybe.just(10)
    c = Maybe.nothing()
    d = Maybe.nothing()

    # Equality checks
    assert a == b
    assert c == d
    assert a != c
    assert a != d

    # Identity of value
    assert a.value == 10
    with pytest.raises(AttributeError):
        _ = c.value  # nothing has no value attribute


def test_map_on_just_and_nothing():
    # Map should apply function to value
    m = Maybe.just(5)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert mapped.value == 10

    # Map on nothing returns nothing
    n = Maybe.nothing()
    mapped_n = n.map(lambda x: x * 2)
    assert mapped_n.is_nothing
    assert mapped_n == Maybe.nothing()


def test_bind_on_just_and_nothing():
    # Bind should return result of mapper
    m = Maybe.just(3)
    bound = m.bind(lambda x: Maybe.just(x + 4))
    assert bound.value == 7

    # Bind on nothing returns nothing
    n = Maybe.nothing()
    bound_n = n.bind(lambda x: Maybe.just(x + 4))
    assert bound_n.is_nothing
    assert bound_n == Maybe.nothing()


def test_ap_on_just_and_nothing():
    # ap applies function inside self to applicative
    f = Maybe.just(lambda x: x * 3)
    a = Maybe.just(7)
    result = f.ap(a)
    assert result.value == 21

    # ap on nothing returns nothing
    f_nothing = Maybe.nothing()
    result_nothing = f_nothing.ap(a)
    assert result_nothing.is_nothing
    assert result_nothing == Maybe.nothing()


def test_filter_on_just_and_nothing():
    m = Maybe.just(4)
    # filter passes
    filtered = m.filter(lambda x: x > 2)
    assert filtered.value == 4

    # filter fails
    filtered_fail = m.filter(lambda x: x > 5)
    assert filtered_fail.is_nothing
    assert filtered_fail == Maybe.nothing()

    # filter on nothing stays nothing
    n = Maybe.nothing()
    filtered_n = n.filter(lambda x: True)
    assert filtered_n.is_nothing
    assert filtered_n == Maybe.nothing()


def test_get_or_else_on_just_and_nothing():
    m = Maybe.just("hello")
    assert m.get_or_else("default") == "hello"

    n = Maybe.nothing()
    assert n.get_or_else("default") == "default"


def test_to_either_and_to_box_and_to_lazy_and_to_try_and_to_validation():
    # These conversions rely on other modules; we just check types and values
    m = Maybe.just(42)
    e = m.to_either()
    assert hasattr(e, "value") and e.value == 42
    assert hasattr(e, "is_left") and not e.is_left

    b = m.to_box()
    assert hasattr(b, "value") and b.value == 42

    l = m.to_lazy()
    assert callable(l.value) and l.value() == 42

    t = m.to_try()
    assert t.is_success and t.value == 42

    v = m.to_validation()
    assert v.is_success and v.value == 42

    # For nothing
    n = Maybe.nothing()
    e_n = n.to_either()
    assert e_n.is_left

    b_n = n.to_box()
    assert b_n.value is None

    l_n = n.to_lazy()
    assert l_n.value() is None

    t_n = n.to_try()
    assert not t_n.is_success and t_n.value is None

    v_n = n.to_validation()
    assert v_n.is_success and v_n.value is None
