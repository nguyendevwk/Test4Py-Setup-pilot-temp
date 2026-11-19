import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from pilot.gpu_lease import gpu_lease


class GPULeaseTests(unittest.TestCase):
    def test_busy_vram_blocks_before_model_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('pilot.gpu_lease.gpu_inventory',return_value=[dict(index='0',uuid='GPU-fixture',free_mib=4000,total_mib=15000)]):
                with self.assertRaisesRegex(RuntimeError,'insufficient current free VRAM'):
                    with gpu_lease(root,['0'],'small',lock_directory=root/'locks'):
                        self.fail('GPU model work must never start')
            self.assertEqual(json.loads((root/'small-gpu-preflight.json').read_text())['status'],'blocked')

    def test_parallel_runner_cannot_reserve_same_gpu_and_release_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('pilot.gpu_lease.gpu_inventory',return_value=[dict(index='0',uuid='GPU-fixture',free_mib=15000,total_mib=16000)]):
                with gpu_lease(root,['0'],'first',lock_directory=root/'locks'):
                    with self.assertRaisesRegex(RuntimeError,'reserved by another'):
                        with gpu_lease(root,['0'],'second',lock_directory=root/'locks'):
                            self.fail('Duplicate GPU lease acquired')
                with gpu_lease(root,['0'],'third',lock_directory=root/'locks'):pass
            self.assertEqual(json.loads((root/'third-gpu-preflight.json').read_text())['status'],'passed')
