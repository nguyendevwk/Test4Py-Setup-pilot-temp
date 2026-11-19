import pytest
from pycg.machinery.imports import get_custom_loader

class DummyImportManager:
    def __init__(self):
        self.edges = []
        self.nodes = {}
        self.filepaths = {}
        self.create_node_calls = 0

    def create_edge(self, fullname):
        self.edges.append(fullname)

    def get_node(self, fullname):
        return self.nodes.get(fullname)

    def create_node(self, fullname):
        self.create_node_calls += 1
        self.nodes[fullname] = {}

    def set_filepath(self, fullname, path):
        self.filepaths[fullname] = path

def test_get_custom_loader_creates_node_and_edge_and_returns_loader():
    ig = DummyImportManager()
    fullname = "pkg.module"
    path = "/path/to/module.py"

    # Scenario 1: node does not exist
    Loader = get_custom_loader(ig)
    loader1 = Loader(fullname, path)
    assert ig.edges == [fullname]
    assert ig.nodes == {fullname: {}}
    assert ig.filepaths[fullname] == path
    assert ig.create_node_calls == 1
    assert loader1.get_filename(fullname) == path
    assert loader1.get_data(path) == ""

    # Scenario 2: node already exists
    ig2 = DummyImportManager()
    ig2.create_node(fullname)
    ig2.set_filepath(fullname, "/old/path")
    Loader2 = get_custom_loader(ig2)
    loader2 = Loader2(fullname, path)
    assert ig2.edges == [fullname]
    assert ig2.filepaths[fullname] == path  # updated to new path
    assert ig2.create_node_calls == 0
    assert loader2.get_filename(fullname) == path
    assert loader2.get_data(path) == ""
