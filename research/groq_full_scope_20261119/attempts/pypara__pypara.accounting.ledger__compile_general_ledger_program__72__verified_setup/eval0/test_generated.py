import datetime
import pytest
from pypara.accounting.ledger import compile_general_ledger_program, GeneralLedger
from pypara.accounting.zeitgeist import DateRange
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting, ReadJournalEntries
from pypara.accounting.generic import Balance
from pypara.commons.numbers import Amount, Quantity

# Helper account and balance
ACC = Account("Cash")
BALANCE = Balance(Amount(1000), Quantity(1))

# Dummy read_initial_balances implementation
def dummy_read_initial_balances(period: DateRange) -> dict[Account, Balance]:
    return {ACC: BALANCE}

# Dummy read_journal_entries implementation
def dummy_read_journal_entries(period: DateRange) -> list[JournalEntry]:
    posting = Posting(account=ACC, amount=Amount(200), quantity=Quantity(1))
    return [JournalEntry(date=period.start, postings=[posting])]

def test_compile_general_ledger_program_normal(tmp_path):
    """Normal execution: ledger contains the expected period and entries."""
    program = compile_general_ledger_program(dummy_read_initial_balances, dummy_read_journal_entries)
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    ledger = program(period)

    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == period
    assert len(ledger.entries) == 1
    entry = ledger.entries[0]
    assert entry.date == period.start
    assert entry.postings[0].account == ACC
    assert entry.postings[0].amount == Amount(200)

def test_compile_general_ledger_program_empty_entries(tmp_path):
    """Boundary case: no journal entries should result in an empty ledger entries list."""
    def empty_entries(period: DateRange) -> list[JournalEntry]:
        return []

    program = compile_general_ledger_program(dummy_read_initial_balances, empty_entries)
    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 12, 31))
    ledger = program(period)

    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == period
    assert ledger.entries == []

def test_compile_general_ledger_program_initial_balance_error(tmp_path):
    """Error propagation: if reading initial balances raises, the program should propagate the exception."""
    def error_initial_balances(period: DateRange):
        raise RuntimeError("Failed to read balances")

    program = compile_general_ledger_program(error_initial_balances, dummy_read_journal_entries)
    period = DateRange(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))

    with pytest.raises(RuntimeError, match="Failed to read balances"):
        program(period)
