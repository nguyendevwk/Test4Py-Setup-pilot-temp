import unittest
from pilot.measurement import retained_counts


class MeasurementTests(unittest.TestCase):
    def node(self,name,outcome='passed',**changes):
        row=dict(nodeid=name,outcome=outcome,**{p:dict(outcome='passed') for p in ('setup','call','teardown')})
        row.update(changes)
        return row

    def test_mixed_suite_does_not_receive_all_pass_credit(self):
        report=dict(tests=[self.node('t.py::a'),self.node('t.py::b','failed',call=dict(outcome='failed'))])
        counts=retained_counts(dict(returncode=1),report,['t.py'])
        self.assertFalse(counts['retained_suite_all_pass'])
        self.assertEqual(counts['retained_passed_nodes'],1)
        self.assertEqual(counts['retained_collected_nodes'],2)

    def test_other_module_failure_does_not_change_this_modules_outcomes(self):
        report=dict(tests=[self.node('a.py::a'),self.node('b.py::b','failed')])
        self.assertTrue(retained_counts(dict(returncode=1),report,['a.py'])['retained_suite_all_pass'])

    def test_collection_timeout_and_missing_teardown_never_pass(self):
        for process,report in [
            (dict(returncode=2),dict(tests=[self.node('t.py::a')],collectors=[dict(outcome='failed')])),
            (dict(returncode=0,timeout=True),dict(tests=[self.node('t.py::a')])),
            (dict(returncode=0),dict(tests=[self.node('t.py::a',teardown={})])),
            (dict(returncode=5),{}),
        ]:
            with self.subTest(process=process,report=report):
                self.assertFalse(retained_counts(process,report,['t.py'])['retained_suite_all_pass'])
