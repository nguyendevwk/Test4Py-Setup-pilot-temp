from collections.abc import Mapping
from typesystem.base import ValidationError, Message

def test_validation_error_message_dict_and_messages():
    msg = Message(text='Field is required', code='required', index=['field_a', 'subfield'])
    err = ValidationError(messages=[msg])

    # The internal message dictionary is built correctly.
    assert err._message_dict == {'field_a': {'subfield': 'Field is required'}}

    # Iteration yields the top‑level keys of the message dictionary.
    assert list(iter(err)) == ['field_a']

    # messages() returns the original list of Message objects.
    assert err.messages() == [msg]

    # Adding a prefix changes the index of each returned message.
    prefixed = err.messages(add_prefix='parent')
    assert prefixed[0].index == ['parent', 'field_a', 'subfield']
    # The prefixed message is a new object, not the original.
    assert prefixed[0] is not msg

    # ValidationError is an Exception and a Mapping.
    assert isinstance(err, Exception)
    assert isinstance(err, Mapping)

    # The original messages list remains unchanged after adding a prefix.
    assert err.messages() == [msg]
