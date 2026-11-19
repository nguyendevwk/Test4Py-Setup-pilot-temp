import pytest
from cookiecutter.prompt import read_user_dict

def test_read_user_dict_raises_type_error_for_non_dict_default():
    """read_user_dict should raise TypeError if default_value is not a dict."""
    with pytest.raises(TypeError):
        read_user_dict("foo", default_value="not a dict")

def test_read_user_dict_raises_type_error_for_none_default():
    """read_user_dict should raise TypeError if default_value is None."""
    with pytest.raises(TypeError):
        read_user_dict("bar", default_value=None)

def test_read_user_dict_raises_type_error_for_list_default():
    """read_user_dict should raise TypeError if default_value is a list."""
    with pytest.raises(TypeError):
        read_user_dict("baz", default_value=[1, 2, 3])
