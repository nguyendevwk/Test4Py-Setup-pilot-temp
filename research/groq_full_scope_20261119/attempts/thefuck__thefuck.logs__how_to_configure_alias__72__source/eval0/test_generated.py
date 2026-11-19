import builtins
import types
import pytest
from thefuck.logs import how_to_configure_alias

class DummyDetails:
    def __init__(self, content, path, reload, can_configure_automatically):
        self.content = content
        self.path = path
        self.reload = reload
        self.can_configure_automatically = can_configure_automatically

    def _asdict(self):
        return {
            "content": self.content,
            "path": self.path,
            "reload": self.reload,
        }

def test_how_to_configure_alias_with_auto(capfd):
    details = DummyDetails(
        content="alias fuck='thefuck'",
        path="~/.bashrc",
        reload="source ~/.bashrc",
        can_configure_automatically=True,
    )
    how_to_configure_alias(details)
    out, err = capfd.readouterr()
    assert "Seems like fuck alias isn't configured!" in out
    assert "Please put alias fuck='thefuck' in your ~/.bashrc" in out
    assert "Or run fuck a second time to configure it automatically." in out
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in out
    assert err == ""

def test_how_to_configure_alias_without_auto(capfd):
    details = DummyDetails(
        content="alias fuck='thefuck'",
        path="~/.zshrc",
        reload="source ~/.zshrc",
        can_configure_automatically=False,
    )
    how_to_configure_alias(details)
    out, err = capfd.readouterr()
    assert "Seems like fuck alias isn't configured!" in out
    assert "Please put alias fuck='thefuck' in your ~/.zshrc" in out
    assert "Or run fuck a second time to configure" not in out
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in out
    assert err == ""

def test_how_to_configure_alias_no_details(capfd):
    how_to_configure_alias(None)
    out, err = capfd.readouterr()
    assert "Seems like fuck alias isn't configured!" in out
    assert "Please put" not in out
    assert "Or run fuck" not in out
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in out
    assert err == ""
