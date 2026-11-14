import json
from pathlib import Path
import tempfile
import unittest
from pilot.benchmark import select_modules,locate_module,module_coverage
from pilot.common import BASE

class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        data=BASE/'research/benchmark'
        self.projects=json.loads((data/'projects-upstream.json').read_text())
        self.registry=json.loads((data/'na-projects.json').read_text())
    def test_frame_and_nineteen_unique_modules(self):
        self.assertEqual(sum(map(len,self.projects.values())),183)
        self.assertEqual(sum(len(self.projects[p]) for p in self.registry),58)
        selected=select_modules(self.projects,self.registry)
        self.assertEqual(len(selected),19)
        self.assertEqual(len({(x['project'],x['module']) for x in selected}),19)
        self.assertEqual(len({x['project'] for x in selected}),9)
        self.assertEqual(selected,select_modules(self.projects,self.registry))
        self.assertNotEqual(selected,select_modules(self.projects,self.registry,seed=43))
    def test_missing_source_does_not_choose_a_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):locate_module(root,'pkg.mod')
            (root/'src/pkg').mkdir(parents=True);(root/'src/pkg/mod.py').write_text('x=1')
            path,imports,source=locate_module(root,'pkg.mod')
            self.assertEqual(imports,root/'src');self.assertEqual(source,Path('src/pkg'))
    def test_coverage_missing_and_zero_are_distinct(self):
        self.assertIsNone(module_coverage({},Path('pkg/m.py'))['line_pct'])
        r=module_coverage(dict(files={'/tmp/src/pkg/m.py':dict(summary=dict(covered_lines=0,num_statements=5,covered_branches=0,num_branches=2))}),Path('pkg/m.py'))
        self.assertEqual(r['line_pct'],0)
        self.assertEqual(r['branch_pct'],0)
    def test_no_branch_denominator_is_not_one_hundred(self):
        r=module_coverage(dict(files={'m.py':dict(summary=dict(num_branches=0,covered_branches=0))}),Path('m.py'))
        self.assertIsNone(r['branch_pct'])

    def test_report_keeps_failed_modules_missing(self):
        from benchmark19 import export_report
        import csv
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            plan=dict(selected=[dict(project='x',module='pkg.a'),dict(project='y',module='pkg.b')])
            state=dict(projects={'x':dict(status='preflight_failed')})
            export_report(root,plan,state)
            rows=list(csv.DictReader((root/'modules.csv').open()))
            self.assertEqual(rows[0]['passed'],'')
            self.assertEqual(rows[0]['line_pct'],'')
            self.assertEqual(state['quality']['scored_modules'],0)
            self.assertIsNone(state['quality']['mean_line_pct'])
