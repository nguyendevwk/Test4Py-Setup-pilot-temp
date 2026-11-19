import unittest

from pilot.api_probe_analysis import analyze


class ApiProbeAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.plan=dict(arms=['source_only','api_contract'],targets=[
            dict(id='x-42',target_id='x',project='one',module='one.x',seed=42),
            dict(id='x-43',target_id='x',project='one',module='one.x',seed=43),
            dict(id='y-42',target_id='y',project='two',module='two.y',seed=42)])

    def test_missing_attempts_remain_unknown_and_seeds_are_not_new_targets(self):
        out=analyze(self.plan,dict(rows=[dict(id='x-42',arm='api_contract',status='scored',meaningful_target_test=True)]))
        self.assertEqual(out['planned'],6)
        self.assertEqual(out['overall']['source_only']['unknown'],3)
        self.assertEqual(out['overall']['api_contract']['successful'],1)
        self.assertIsNone(out['projects'][0]['paired_delta_pp'])
        self.assertEqual(out['distinct_targets'],2)
        self.assertEqual(out['project_clusters'],2)

    def test_pairing_preserves_wins_losses_and_project_heterogeneity(self):
        rows=[]
        for t,values in zip(self.plan['targets'],[(False,True),(True,False),(False,True)]):
            for arm,value in zip(self.plan['arms'],values):
                rows.append(dict(id=t['id'],arm=arm,status='scored',meaningful_target_test=value))
        out=analyze(self.plan,dict(rows=rows))
        self.assertEqual(out['paired_counts'],{'1':2,'-1':1})
        self.assertEqual([p['paired_delta_pp'] for p in out['projects']],[0,100])

    def test_duplicate_or_unknown_attempts_are_rejected(self):
        row=dict(id='x-42',arm='source_only',status='scored',meaningful_target_test=True)
        with self.assertRaises(ValueError):analyze(self.plan,dict(rows=[row,row]))
        with self.assertRaises(ValueError):analyze(self.plan,dict(rows=[dict(row,id='other')]))
