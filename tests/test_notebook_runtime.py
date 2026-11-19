import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock,patch

BASE=Path(__file__).resolve().parents[1]


class NotebookRuntimeTests(unittest.TestCase):
    def test_pip_delegation_targets_a_venv_without_installing_system_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            env=Path(tmp)/'tools'
            subprocess.run([sys.executable,'-m','venv','--without-pip',str(env)],check=True,capture_output=True)
            proc=subprocess.run([sys.executable,'-m','pip','--python',str(env/'bin/python'),'debug'],capture_output=True,text=True,timeout=60)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertIn(str(env/'bin/python'),proc.stdout)

    def test_notebook_failure_blocks_later_cells_before_launch(self):
        nb=json.loads((BASE/'notebooks/kaggle_upstream_nf4_paired.ipynb').read_text())
        source=next(''.join(c['source']) for c in nb['cells'] if 'def run_step(' in ''.join(c['source']))
        fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='run_step')
        display=types.ModuleType('IPython.display');display.display=lambda *a:None;display.FileLink=lambda p:p
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'report';root.mkdir()
            popen=Mock(return_value=types.SimpleNamespace(stdout=['synthetic failure\n'],wait=lambda:2))
            scope=dict(FAILED_STEP=None,ROOT=root,LOG=Path(tmp)/'launcher.log',WORKDIR=BASE,
                       PYTHON=sys.executable,subprocess=types.SimpleNamespace(Popen=popen,PIPE=-1,STDOUT=-2),
                       shutil=shutil,json=json)
            exec(compile(ast.Module(body=[fn],type_ignores=[]),'notebook-runner','exec'),scope)
            with patch.dict(sys.modules,{'IPython.display':display}):
                with self.assertRaisesRegex(RuntimeError,'Step exited 2'):
                    scope['run_step'](['paired_study.py','--action','stress'])
                with self.assertRaisesRegex(RuntimeError,'Previous step failed'):
                    scope['run_step'](['paired_study.py','--action','small'])
            self.assertEqual(popen.call_count,1)
            self.assertEqual(json.loads((root/'notebook-failure.json').read_text())['exit_code'],2)
