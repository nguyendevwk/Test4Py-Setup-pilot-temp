from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count_attribute():
    # The function should not have the attribute before decoration
    def dummy_test(self):
        pass

    assert not hasattr(dummy_test, "genty_repeat_count")

    # Apply the decorator with a positive count
    decorated = genty_repeat(3)(dummy_test)

    # The decorator should return the original function object
    assert decorated is dummy_test

    # After decoration, the attribute should be set correctly
    assert getattr(dummy_test, "genty_repeat_count") == 3
