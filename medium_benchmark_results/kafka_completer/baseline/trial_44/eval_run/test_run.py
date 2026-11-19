import pytest
from kafkashell.completer import KafkaCompleter

class DummySettings:
    def __init__(self):
        self.commands = {
            "create-topic": {"description": "Create a topic"},
            "delete-topic": {"description": "Delete a topic"},
        }
        self.enable_help = True
        self.enable_fuzzy_search = False
        self.user_config = {"clusters": {}}

def test_kafka_completer_yield_commands_display_meta_when_help_enabled():
    settings = DummySettings()
    completer = KafkaCompleter(settings)

    completions = list(completer.yield_commands("cre"))
    assert len(completions) == 1
    completion = completions[0]
    assert completion.text == "create-topic"
    assert completion.start_position == -len("cre")
    assert completion.display_meta == "Create a topic"
