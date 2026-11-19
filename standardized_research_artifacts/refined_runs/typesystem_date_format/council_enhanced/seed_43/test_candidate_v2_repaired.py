import datetime
import pytest
from typesystem.formats import DateFormat
from typesystem.base import ValidationError

def test_dateformat_behavior():
    fmt = DateFormat()

    # Valid date string
    dt = fmt.validate('2026-11-17')
    assert isinstance(dt, datetime.date) and dt.year == 2026

    # Invalid format
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate('2026/11/17')
    code = getattr(excinfo.value, 'code', getattr(excinfo.value, 'error_code', None))
    assert code == 'format'

    # Invalid real date
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate('2026-02-30')
    code = getattr(excinfo.value, 'code', getattr(excinfo.value, 'error_code', None))
    assert code == 'invalid'

    # Serialization
    assert fmt.serialize(None) is None
    assert fmt.serialize(dt) == '2026-11-17'

    # Native type check
    assert fmt.is_native_type(dt) is True
    assert fmt.is_native_type('2026-11-17') is False
