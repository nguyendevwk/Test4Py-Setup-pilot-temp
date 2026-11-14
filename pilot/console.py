"""Bounded terminal summaries; raw logs are written before filtering."""
import threading
import time


class Console:
    def __init__(self, mode='compact', limit=120, interval=30):
        if mode not in ('compact', 'full', 'quiet'):
            raise ValueError('Unknown console mode')
        self.mode, self.limit, self.interval = mode, limit, interval
        self.lines = 0
        self.last = {}
        self.lock = threading.Lock()
        self.notified = False

    def write(self, text, label='process'):
        with self.lock:
            if self.mode == 'quiet':
                return
            if self.mode == 'full':
                print(text, end='' if text.endswith('\n') else '\n', flush=True)
                return
            if not text.startswith(('[', 'Starting ', 'Environment ready:', 'Reusing Torch',
                                    'Status:', 'Reports:', 'Complete.', 'Stopped at')):
                return
            repetitive = 'model_call_' in text or text.startswith('[GPU]') or 'waiting for next event' in text
            now = time.monotonic()
            if repetitive and now - self.last.get(label, float('-inf')) < self.interval:
                return
            if self.lines >= self.limit:
                if not self.notified:
                    print('[console] Display limit reached; experiment continues. Full output remains in log files.', flush=True)
                    self.notified = True
                return
            self.last[label] = now
            self.lines += 1
            print(text.strip()[:600], flush=True)
