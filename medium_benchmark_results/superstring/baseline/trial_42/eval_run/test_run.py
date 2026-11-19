from superstring.superstring import SuperString

def test_superstring_to_printable_slices_correctly():
    s = SuperString("hello world")
    # Default slice returns the full content
    assert s.to_printable() == "hello world"
    # Explicit start and end indices slice correctly
    assert s.to_printable(6, 11) == "world"
    # Passing None for indices behaves like the default
    assert s.to_printable(None, None) == "hello world"
