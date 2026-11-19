import io
import os
import shlex
import pytest
from thefuck.shells.generic import Generic, ShellConfiguration
from thefuck.conf import settings

class TestGeneric:
    def test_split_command_with_escaped_spaces_and_quotes(self):
        g = Generic()
        # Command with escaped space and quoted string
        cmd = r'echo "Hello\ World" \\"quoted\\"'
        parts = g.split_command(cmd)
        # shlex should split into ['echo', 'Hello World', '"quoted"']
        assert parts == ['echo', 'Hello World', '"quoted"']

    def test_quote_escapes_special_characters(self):
        g = Generic()
        # String containing spaces and quotes
        s = 'a b "c"'
        quoted = g.quote(s)
        # The quoted string should be safe for shell execution
        # For example, shlex.quote('a b "c"') -> "'a b \"c\"'"
        assert quoted == shlex.quote(s)
        # Ensure that quoting preserves the original string when evaluated
        eval_cmd = f'echo {quoted}'
        # Using shlex.split to simulate shell parsing
        parsed = shlex.split(eval_cmd)
        assert parsed == ['echo', 'a b "c"']

    def test_get_history_respects_limit_and_caches(self, tmp_path):
        # Create a temporary history file with 5 lines
        history_file = tmp_path / "history.txt"
        lines = [f"cmd{i}\n" for i in range(5)]
        history_file.write_text(''.join(lines), encoding='utf-8')

        class TestGeneric(Generic):
            def _get_history_file_name(self):
                return str(history_file)

        # Set history limit to 3
        original_limit = settings.history_limit
        settings.history_limit = 3
        try:
            g = TestGeneric()
            history = g.get_history()
            # Should return last 3 commands
            assert history == ['cmd2', 'cmd3', 'cmd4']
            # Subsequent call should return cached result
            history_again = g.get_history()
            assert history_again is history
        finally:
            settings.history_limit = original_limit
