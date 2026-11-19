import asyncio
import contextlib
import io
import json
from pathlib import Path
import tempfile
import types
import unittest

from tqdm import tqdm
from pilot.instrumentation import instrument_initialization
from pilot.progress import live_summary
from pilot.console import Console


class ProgressCountTests(unittest.TestCase):
    def test_real_item_counts_preserve_async_results_and_disabled_tqdm(self):
        class Project:
            async def generate_summary(self):
                with tqdm(total=3,disable=True) as pbar:
                    for i in range(3):pbar.update()
                return 'unchanged'
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            work=Path(tmp);project=Project();original=tqdm
            instrument_initialization(project,work)
            self.assertEqual(asyncio.run(project.generate_summary()),'unchanged')
            self.assertIs(globals()['tqdm'],original)
            state=json.loads((work/'progress.json').read_text())
            self.assertEqual(state['analysis_units_completed'],3)
            self.assertEqual(state['analysis_units_total'],3)
            self.assertEqual(state['analysis_steps_completed'],1)

    def test_function_counter_is_not_a_model_call_percentage(self):
        state=dict(phase='generation_round_1',round_index=1,rounds_total=3,functions_completed=2,
                   functions_total=7,current_function='GentyArgs.args',model_calls_finished=118)
        text=live_summary(state)
        self.assertIn('2/7',text);self.assertIn('round=1/3',text)
        self.assertIn('118 (total dynamic)',text);self.assertNotIn('118/7',text)

    def test_progress_and_stage_boundaries_survive_compact_limit(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            console=Console('compact',limit=1,interval=0)
            console.write('[w] model_call_start')
            console.write('[w] initialization/step_end analysis_steps_completed=2')
            console.write('[progress:w] functions=2/7')
        self.assertIn('analysis_steps_completed=2',out.getvalue())
        self.assertIn('functions=2/7',out.getvalue())
