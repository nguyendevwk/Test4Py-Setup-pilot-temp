import pytest
from kafkashell.completer import KafkaCompleter


class DummySettings:
    def __init__(self, enable_help, enable_fuzzy_search):
        self.commands = {
            "create-topic": {"description": "Create a topic"},
            "delete-topic": {"description": "Delete a topic"},
        }
        self.enable_help = enable_help
        self.enable_fuzzy_search = enable_fuzzy_search
        self.user_config = {"clusters": {"cluster1": {}, "cluster2": {}}}


def test_yield_commands_help_and_start_position():
    # Enable help: display_meta should be the description
    settings_help = DummySettings(enable_help=True, enable_fuzzy_search=False)
    completer_help = KafkaCompleter(settings_help)
    completions = list(completer_help.yield_commands("cre"))
    assert len(completions) == 1
    comp = completions[0]
    assert comp.text == "create-topic"
    assert comp.start_position == -3  # len("cre") == 3
    assert comp.display_meta == "Create a topic"

    # Disable help: display_meta should be None
    settings_no_help = DummySettings(enable_help=False, enable_fuzzy_search=False)
    completer_no_help = KafkaCompleter(settings_no_help)
    completions_no_help = list(completer_no_help.yield_commands("cre"))
    assert len(completions_no_help) == 1
    comp_no_help = completions_no_help[0]
    assert comp_no_help.text == "create-topic"
    assert comp_no_help.start_position == -3
    assert comp_no_help.display_meta is None

    # Empty word_before_cursor should return all commands
    all_completions = list(completer_help.yield_commands(""))
    assert len(all_completions) == 2
    texts = {c.text for c in all_completions}
    assert texts == {"create-topic", "delete-topic"}
