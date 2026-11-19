from superstring.superstring import SuperString

def test_superstring_slice_behavior():
    s = SuperString("HelloWorld")
    # slice from start to 5
    part1 = s[:5]
    assert isinstance(part1, SuperString)
    assert part1.to_printable() == "Hello"
    assert part1.length() == 5
    # slice from 2 to 7
    part2 = s[2:7]
    assert part2.to_printable() == "lloWo"
    assert part2.length() == 5
    # negative slice
    part3 = s[-5:]
    assert part3.to_printable() == "World"
    assert part3.length() == 5
