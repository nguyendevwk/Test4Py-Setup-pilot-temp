"""Independent processes per arm; at most one arm per visible GPU slot."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from queue import Queue
import sys
import traceback
from pilot.common import checked


def gpu_slots(jobs, selection='auto'):
    if jobs == 1 and selection == 'auto':
        return [None]  # preserve the serial runtime's original CUDA visibility
    count = int(checked([sys.executable, '-c', 'import torch; print(torch.cuda.device_count())']))
    inherited = os.environ.get('CUDA_VISIBLE_DEVICES')
    visible = inherited.split(',')[:count] if inherited is not None else list(map(str, range(count)))
    visible = [value.strip() for value in visible if value.strip() and value.strip() != '-1']
    if selection == 'auto':
        chosen = visible
    else:
        try:
            indices = [int(value) for value in selection.split(',')]
            if len(set(indices)) != len(indices) or any(i < 0 for i in indices):
                raise ValueError('GPU indices must be unique and nonnegative')
            chosen = [visible[i] for i in indices]
        except (ValueError, IndexError) as exc:
            raise ValueError('GPU indices are relative to parent-visible CUDA devices') from exc
    if not chosen:
        raise RuntimeError('No visible CUDA GPU; enable GPU in Kaggle Settings')
    return chosen[:jobs]


def execute_modes(modes, slots, run_one):
    if len(slots) == 1:
        for mode in modes:
            yield mode, run_one(mode, slots[0])
        return
    available = Queue()
    for slot in slots:
        available.put(slot)

    def invoke(mode):
        slot = available.get()
        try:
            return run_one(mode, slot)
        except Exception as exc:
            return dict(status='failed', error=repr(exc), traceback=traceback.format_exc(), gpu=slot)
        finally:
            available.put(slot)

    with ThreadPoolExecutor(max_workers=len(slots)) as executor:
        pending = {executor.submit(invoke, mode): mode for mode in modes}
        for future in as_completed(pending):
            yield pending[future], future.result()
