import pytest
from prompt_toolkit.completion import Completion
from kafkashell.completer import KafkaCompleter


class DummyDocument:
    def __init__(self, text: str):
        self.text = text
        self.text_before_cursor = text

    def get_word_before_cursor(self, WORD=True):
        return self.text.split()[-1] if self.text.split() else ""


class DummySettings:
    def __init__(self, enable_help: bool, enable_fuzzy_search: bool):
        self.commands = {
            "kafka-topics": {"description": "Manage topics", "options": {}},
            "kafka-configs": {"description": "Manage configs", "options": {}},
        }
        self.enable_help = enable_help
        self.enable_fuzzy_search = enable_fuzzy_search
        self.user_config = {"clusters": {"cluster1": {}, "cluster2": {}}}


def test_kafka_completer_yield_commands_display_meta():
    # Setup settings with help enabled
    settings_help = DummySettings(enable_help=True, enable_fuzzy_search=False)
    completer_help = KafkaCompleter(settings_help)
    doc = DummyDocument("kafka")
    completions_help = list(completer_help.get_completions(doc, None))

    # Expect two completions: kafka-topics and kafka-configs
    assert len(completions_help) == 2
    texts_help = [c.text for c in completions_help]
    assert texts_help == ["kafka-topics", "kafka-configs"]
    # start_position should be negative length of word before cursor
    assert all(c.start_position == -len("kafka") for c in completions_help)
    # display_meta should be the command description
    assert [c.display_meta for c in completions_help] == [
        "Manage topics",
        "Manage configs",
    ]

    # Setup settings with help disabled
    settings_no_help = DummySettings(enable_help=False, enable_fuzzy_search=False)
    completer_no_help = KafkaCompleter(settings_no_help)
    completions_no_help = list(completer_no_help.get_completions(doc, None))

    # Expect same completions but without display_meta
    assert len(completions_no_help) == 2
    texts_no_help = [c.text for c in completions_no_help]
    assert texts_no_help == ["kafka-topics", "kafka-configs"]
    assert all(c.display_meta is None for c in completions_no_help)
