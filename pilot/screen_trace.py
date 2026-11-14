"""Passive per-test receiver trace for integration screening only; no prompt access."""
import json
import os
from pathlib import Path
import sys

_records=[]
_active={}
_previous=None
_node=None


def _profile(frame,event,arg):
    code=frame.f_code
    if code.co_name!='__init__' or not code.co_filename.replace('\\','/').endswith('/pycg/machinery/imports.py'):
        return
    values=frame.f_locals
    if 'ig_obj' not in values or 'fullname' not in values:return
    if event=='call':
        manager=values['ig_obj'];dest=values['fullname']
        try:
            _active[id(frame)]=dict(nodeid=_node,fullname=dest,path=values.get('path'),
                source_ready=manager.current_module=='pkg.main' and bool(manager.get_node('pkg.main')),
                destination_existed=bool(manager.get_node(dest)))
        except Exception as exc:
            _active[id(frame)]=dict(nodeid=_node,trace_error=repr(exc))
    elif event=='return':
        row=_active.pop(id(frame),None)
        if row is not None:_records.append(row)


def pytest_sessionstart(session):
    global _previous
    _records.clear();_active.clear();_previous=sys.getprofile();sys.setprofile(_profile)


def pytest_runtest_setup(item):
    global _node
    _node=item.nodeid


def pytest_sessionfinish(session,exitstatus):
    sys.setprofile(_previous)
    path=os.environ.get('PILOT_TRACE_FILE')
    if path:Path(path).write_text(json.dumps(_records,indent=2))
