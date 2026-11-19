import pytest
from prompt_toolkit.completion import Completion
from kafkashell.completer import KafkaCompleter

class DummySettings:
    def __init__(self, commands, enable_help, enable_fuzzy_search):
        self.commands = commands
        self.enable_help = enable_help
        self.enable_fuzzy_search = enable_fuzzy_search
        self.user_config = {"clusters": {}}  # required for yield_clusters

def test_yield_commands_display_meta():
    # Setup settings with two commands and help enabled
    commands = {
        "create-topic": {"description": "Create a topic"},
        "delete-topic": {"description": "Delete a topic"},
    }
    settings = DummySettings(commands, enable_help=True, enable_fuzzy_search=False)
    completer = KafkaCompleter(settings)

    # Capture completions for partial word 'cre'
    completions = list(completer.yield_commands("cre"))
    assert len(completions) == 1
    comp = completions[0]
    assert isinstance(comp, Completion)
    assert comp.text == "create-topic"
    assert comp.start_position == -3
    assert comp.display_meta == "Create a topic"

    # Now disable help and verify display_meta is None
    settings.enable_help = False
    completions_no_help = list(completer.yield_commands("cre"))
    assert len(completions_no_help) == 1
    comp_no_help = completions_no_help[0]
    assert comp_no_help.display_meta is None
