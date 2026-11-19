import os
import io
import shlex
import pytest
from thefuck.shells.generic import Generic
from thefuck.conf import settings

class TestGenericShell:
    def test_alias_expansion_and_split_command(self):
        shell = Generic()
        # Define a custom alias mapping
        def custom_get_aliases():
            return {"ls": "ls --color=auto"}
        shell.get_aliases = custom_get_aliases

        # Alias should be expanded only for the first word
        expanded = shell._expand_aliases("ls -l /tmp")
        assert expanded == "ls --color=auto -l /tmp"

        # Splitting should preserve quoted spaces
        cmd = r'echo "Hello World"'
        parts = shell.split_command(cmd)
        assert parts == ['echo', 'Hello World']

        # Splitting should handle escaped spaces
        cmd2 = r'echo Hello\ World'
        parts2 = shell.split_command(cmd2)
        assert parts2 == ['echo', 'Hello World']

    def test_info_handles_exception_and_version(self):
        shell = Generic()
        # Override _get_version to raise an exception
        def bad_version():
            raise RuntimeError("no version")
        shell._get_version = bad_version

        # info should catch exception and return only friendly_name
        info = shell.info()
        assert info == "Generic Shell"

        # Now provide a valid version
        shell._get_version = lambda: "v1.2.3"
        info2 = shell.info()
        assert info2 == "Generic Shell v1.2.3"

    def test_get_history_with_history_limit_and_file(self, tmp_path):
        shell = Generic()
        # Create a temporary history file with more lines than the limit
        hist_file = tmp_path / "history.txt"
        lines = [f"cmd{i}\n" for i in range(10)]
        hist_file.write_text("".join(lines), encoding="utf-8")

        # Monkeypatch methods to use our temp file
        shell._get_history_file_name = lambda: str(hist_file)
        shell._script_from_history = lambda line: line.strip()

        # Set history limit to 5
        settings.history_limit = 5
        history = shell.get_history()
        # Should return the last 5 commands
        assert history == [f"cmd{i}" for i in range(5, 10)]
        # Reset history_limit to default (None)
        settings.history_limit = None
