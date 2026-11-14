"""Best-effort physical GPU telemetry, independent of CUDA model processes."""
import csv
import io
import subprocess
import threading
from datetime import datetime, timezone
from pilot.common import append_json, write_json


def sample_gpus():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=index,uuid,name,utilization.gpu,memory.used,memory.total',
                                 '--format=csv,noheader,nounits'], capture_output=True, text=True, timeout=5)
        if result.returncode:
            return []
        rows = []
        for row in csv.reader(io.StringIO(result.stdout)):
            index, uuid, name, util, used, total = [value.strip() for value in row]
            rows.append(dict(index=index, uuid=uuid, name=name, utilization_percent=float(util),
                             used_mib=float(used), total_mib=float(total)))
        return rows
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return []


class GPUMonitor:
    def __init__(self, output, interval=15, console=None):
        from pilot.console import Console
        self.console = console or Console('full')
        self.output, self.interval = output, interval
        self.stop = threading.Event()
        self.thread = None

    def __enter__(self):
        def monitor():
            while not self.stop.is_set():
                rows = sample_gpus()
                snapshot = dict(time=datetime.now(timezone.utc).isoformat(), gpus=rows)
                append_json(self.output / 'gpu_usage.jsonl', snapshot)
                write_json(self.output / 'gpu_latest.json', snapshot)
                if rows:
                    self.console.write('[GPU] ' + ' | '.join(f"{r['index']}: {r['utilization_percent']:.0f}% {r['used_mib']/1024:.1f}/{r['total_mib']/1024:.1f} GiB" for r in rows), label='gpu')
                self.stop.wait(self.interval)
        self.thread = threading.Thread(target=monitor, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.stop.set()
        self.thread.join(timeout=6)
