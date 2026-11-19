import pytest
from kafkashell.completer import KafkaCompleter

class DummySettings:
    def __init__(self, enable_help=True, enable_fuzzy_search=False):
        self.commands = {
            "create": {"description": "Create something"},
            "delete": {"description": "Delete something"},
        }
        self.enable_help = enable_help
        self.enable_fuzzy_search = enable_fuzzy_search
        self.user_config = {"clusters": {}}

def test_yield_commands_display_meta_and_start_position():
    # When help is enabled, display_meta should be the command description
    settings = DummySettings(enable_help=True)
    completer = KafkaCompleter(settings)
    completions = list(completer.yield_commands("cr"))
    assert len(completions) == 1
    comp = completions[0]
    assert comp.text == "create"
    assert comp.start_position == -2  # length of "cr"
    assert comp.display_meta == "Create something"

    # When help is disabled, display_meta should be None
    settings.enable_help = False
    completer = KafkaCompleter(settings)
    completions = list(completer.yield_commands("cr"))
    assert len(completions) == 1
    comp = completions[0]
    assert comp.display_meta is None
