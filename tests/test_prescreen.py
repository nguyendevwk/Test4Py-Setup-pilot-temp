import unittest
from pilot.prescreen import sample_ids, summarize

class ScreenTests(unittest.TestCase):
    def test_ten_percent_is_ten_of_hundred(self):
        ids=sample_ids(100,.1,None,42)
        self.assertEqual(len(ids),10)
        self.assertEqual(ids,sample_ids(100,.1,None,42))
        self.assertEqual(len(set(ids)),10)
        self.assertEqual(len(sample_ids(100,.1,100,42)),100)
    def test_invalid_population_fraction(self):
        for args in ((0,.1,None,42),(100,0,None,42),(100,2,None,42)):
            with self.assertRaises(ValueError):sample_ids(*args)
    def test_failures_count_in_success_denominator(self):
        rows=[dict(status='generation_error'),dict(status='evaluated',passed=2,ast_parse=True,mutants=[dict(verdict='killed'),dict(verdict='survived')])]
        s=summarize(rows,10)
        self.assertEqual(s['finished_candidates'],2)
        self.assertEqual(s['remaining_candidates'],8)
        self.assertEqual(s['original_passing_candidate_rate'],.5)
        self.assertEqual(s['mutation_score'],.5)
        self.assertIsNone(s['semantic_assertion_accuracy'])
    def test_no_eligible_tests_are_not_mutation_zero(self):
        s=summarize([dict(status='evaluated',passed=0,mutants=[dict(verdict='no_eligible_tests')])],1)
        self.assertIsNone(s['mutation_score'])
    def test_empty_plan_has_no_quality_results(self):
        s=summarize([],10)
        self.assertIsNone(s['original_passing_candidate_rate'])
