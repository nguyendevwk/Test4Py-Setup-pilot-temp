import pytest
from prompt_toolkit.completion import Completion
from kafkashell.completer import KafkaCompleter


class DummySettings:
    def __init__(self):
        self.commands = {
            "start": {"description": "Start the service"},
            "stop": {"description": "Stop the service"},
            "status": {"description": "Show status"},
        }
        self.enable_help = True
        self.enable_fuzzy_search = False
        self.user_config = {"clusters": {}}  # required attribute for other methods


def test_yield_commands_with_help_enabled():
    settings = DummySettings()
    completer = KafkaCompleter(settings)

    # Word before cursor that matches two commands
    word = "st"
    completions = list(completer.yield_commands(word))

    # Expect completions for "stop" and "status"
    expected_keys = {"stop", "status"}
    returned_keys = {c.text for c in completions}
    assert returned_keys == expected_keys

    # Each completion should have correct start_position and display_meta
    for c in completions:
        assert c.start_position == -len(word)
        # display_meta should be the description from settings.commands
        assert c.display_meta == settings.commands[c.text]["description"]
