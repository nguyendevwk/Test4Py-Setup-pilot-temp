import pytest
from datetime import datetime, timedelta
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Amount, isum

def test_readjournalentries_is_protocol():
    """Ensure that ReadJournalEntries is a Protocol subclass."""
    from typing import Protocol
    assert issubclass(ReadJournalEntries, Protocol), "ReadJournalEntries should be a Protocol"

def test_date_range_iterable_and_bounds():
    """Verify DateRange correctly iterates over days and respects bounds."""
    start = datetime(2023, 1, 1)
    end = datetime(2023, 1, 3)
    dr = DateRange(start, end)
    dates = list(dr)
    assert dates == [start, start + timedelta(days=1), start + timedelta(days=2)], "DateRange should iterate over each day"
    # Boundary check: ensure end is exclusive
    assert dates[-1] < end, "DateRange should not include the end date"

def test_amount_sum_with_isum():
    """Test that isum correctly sums Amount objects."""
    amounts = [Amount(10), Amount(20), Amount(30)]
    total = isum(amounts)
    assert isinstance(total, Amount), "Result of isum should be an Amount"
    assert total.value == 60, "Sum of amounts should be 60"
