"""Offline regression verification after the 2026-11-15 integrity fixes.

Run: python3 -m research.audit_reproduce
Uses synthetic inputs and mock I/O, never reports model efficacy.
The pre-fix observations are documented in AUDIT_INTEGRITY_2026-11-15.md.
"""
from pathlib import Path
import unittest


def main():
    tests = Path(__file__).resolve().parents[1]/'tests'
    suite = unittest.defaultTestLoader.discover(str(tests), pattern='test_council.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
