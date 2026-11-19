"""Isolated, no-retry Groq client. Prices are configured estimates, not invoices.

Artifacts: ledger.jsonl and immutable <request-id>.{request,response}.json,
plus <request-id>.response.meta.json with HTTP status and safe diagnostics.
A reservation remains charged until a response with valid usage is settled.
"""
import fcntl
import hashlib
import json
import os
import math
import re
import time
from email.utils import parsedate_to_datetime
from pathlib import Path
import urllib.error
import urllib.request
import uuid
from decimal import Decimal

PRICE_SOURCE = 'https://console.groq.com/docs/model/openai/gpt-oss-20b'
ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')


class BudgetExceeded(RuntimeError):
    pass


class RateLimited(RuntimeError):
    """HTTP 429; retry_after is seconds to wait before a parent-managed resume."""

    def __init__(self, retry_after):
        self.retry_after = retry_after
        self.http_status = 429
        super().__init__(f'Groq rate limited (HTTP 429); retry_after={retry_after:g}s; '
                         'reservation retained; no retry')


def _delay(value, now):
    """Parse Retry-After seconds/date or Groq reset durations (e.g. 1m2.5s)."""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        value = str(value or '').strip()
        parts = re.findall(r'(\d+(?:\.\d+)?)(ms|s|m|h)', value)
        if parts and ''.join(n + unit for n, unit in parts) == value:
            seconds = sum(float(n) * {'ms': .001, 's': 1, 'm': 60, 'h': 3600}[unit]
                          for n, unit in parts)
        else:
            try:
                seconds = parsedate_to_datetime(value).timestamp() - now
            except (ValueError, TypeError, OverflowError):
                return 0.0
    return max(0.0, seconds) if math.isfinite(seconds) else 0.0


def _key():
    value = os.environ.get('GROQ_API_KEY', '').strip()
    if not value:
        path = Path('.env')
        if path.is_file():
            for line in path.read_text().splitlines():
                name, sep, candidate = line.strip().partition('=')
                if sep and name.strip() == 'GROQ_API_KEY':
                    value = candidate.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    if not value:
        raise RuntimeError('GROQ_API_KEY is required')
    return value


def _json(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True).encode('utf-8')


def _write(path, data):
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


class StudyClient:
    def __init__(self, work: Path, budget_usd=3, model='openai/gpt-oss-20b',
                 input_price=.075, output_price=.30, max_tokens=2048):
        self.work = Path(work)
        self.work.mkdir(parents=True, exist_ok=True)
        self.budget = Decimal(str(budget_usd))
        self.input_price = Decimal(str(input_price))
        self.output_price = Decimal(str(output_price))
        if not self.budget.is_finite() or not 0 < self.budget <= 3:
            raise ValueError('budget_usd must be positive and at most 3')
        if any(not p.is_finite() or p <= 0 for p in (self.input_price, self.output_price)):
            raise ValueError('prices must be finite and positive')
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError('max_tokens must be a positive integer')
        self.model, self.max_tokens = model, max_tokens
        self.ledger = self.work / 'ledger.jsonl'

    def _balances(self):
        balances = {}
        if self.ledger.exists():
            for line in self.ledger.read_text().splitlines():
                event = json.loads(line)
                rid = event['id']
                charge = Decimal(event['charge_usd'])
                if not charge.is_finite() or charge < 0:
                    raise ValueError('Invalid ledger charge')
                if event['event'] == 'reserve' and rid not in balances:
                    balances[rid] = charge
                elif event['event'] == 'settle' and rid in balances:
                    balances[rid] = charge
                else:
                    raise ValueError('Invalid ledger event')
        return sum(balances.values(), Decimal(0))

    def _append(self, event):
        with self.ledger.open('ab') as stream:
            stream.write(_json(event) + b'\n')
            stream.flush()
            os.fsync(stream.fileno())

    def _pace(self, token_bound):
        """Called under the shared lock, before reserving or sending a request."""
        reservations = []
        if self.ledger.exists():
            reservations = [event for line in self.ledger.read_text().splitlines()
                            if (event := json.loads(line))['event'] == 'reserve']
        now = time.time()
        deadline = now
        request_deadline = now
        token_deadline = now
        header_resources = set()
        recent = []
        for event in reservations:
            path = self.work / (event['id'] + '.request.json')
            sent = event.get('requested_at')
            if sent is None:
                sent = path.stat().st_mtime
            request_deadline = max(request_deadline, sent + 3)
            if sent + 60 > now:
                recent.append((sent, event['input_token_bound'] + event['max_tokens']))
        # Sliding minute token budget; retain bounds even for unknown failures.
        total = sum(tokens for _, tokens in recent) + token_bound
        for sent, tokens in sorted(recent):
            if total <= 100000:
                break
            token_deadline = max(token_deadline, sent + 60)
            total -= tokens
        # Locate the latest persisted response using ledger order, not directory order.
        for event in reversed(reservations):
            path = self.work / (event['id'] + '.response.meta.json')
            if not path.exists():
                continue
            meta = json.loads(path.read_text())
            headers = meta.get('headers', {})
            received = meta.get('received_at', path.stat().st_mtime)
            deadline = max(deadline, received + _delay(headers.get('retry-after'), received))
            for resource, needed in [('requests', 1), ('tokens', token_bound)]:
                try:
                    remaining = float(headers['x-ratelimit-remaining-' + resource])
                except (KeyError, TypeError, ValueError):
                    continue
                if not math.isfinite(remaining) or remaining < 0:
                    continue
                reset = _delay(headers.get('x-ratelimit-reset-' + resource), received)
                # A newer uncertain request makes this snapshot insufficient.
                if event == reservations[-1] and reset > 0:
                    header_resources.add(resource)
                if remaining < needed:
                    deadline = max(deadline, received + (reset or 60))
            break
        if 'requests' not in header_resources:
            deadline = max(deadline, request_deadline)
        if 'tokens' not in header_resources:
            if token_bound > 100000:
                raise ValueError('Request exceeds conservative 100k TPM allowance')
            deadline = max(deadline, token_deadline)
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                return
            time.sleep(min(30, remaining))

    @property
    def spent_usd(self):
        """Settled configured costs plus full outstanding reservations."""
        with (self.work / '.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            return float(self._balances())

    def call(self, messages, seed, label):
        key = _key()
        payload = dict(model=self.model, messages=messages, seed=seed,
                       max_tokens=self.max_tokens, temperature=0.2)
        if self.model.startswith('openai/gpt-oss-'):
            payload['reasoning_effort'] = 'low'
        body = _json(payload)
        if key.encode() in body or key in str(label):
            raise ValueError('Request contains API credential')
        # UTF-8 bytes upper-bound byte-level tokens; double plus generous framing.
        input_bound = 2 * len(body) + 4096
        reserved = (input_bound * self.input_price + self.max_tokens * self.output_price) / 1000000
        with (self.work / '.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if self._balances() + reserved > self.budget:
                raise BudgetExceeded('Request reservation would exceed campaign budget')
            self._pace(input_bound + self.max_tokens)
            rid = uuid.uuid4().hex
            request_path = self.work / (rid + '.request.json')
            _write(request_path, body)
            self._append(dict(event='reserve', id=rid, label=label,
                              requested_at=time.time(),
                              charge_usd=str(reserved), model=self.model,
                              input_token_bound=input_bound, max_tokens=self.max_tokens,
                              input_price_per_million=str(self.input_price),
                              output_price_per_million=str(self.output_price),
                              price_source=PRICE_SOURCE, pricing='configured estimate',
                              request_sha256=hashlib.sha256(body).hexdigest()))
            request = urllib.request.Request(ENDPOINT, data=body, headers={
                'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
                'Accept': 'application/json', 'User-Agent': USER_AGENT})
            http_error = False
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    status = getattr(response, 'status', None) or 200
                    headers = getattr(response, 'headers', {})
                    raw = response.read()
            except urllib.error.HTTPError as exc:
                status = exc.code
                headers = exc.headers or {}
                raw = exc.read()
                http_error = True
            except Exception:
                raise RuntimeError('Groq transport failed; reservation retained; no retry') from None
            # Defensive redaction if a remote error echoes credentials.
            raw = raw.replace(key.encode(), b'[REDACTED]')
            _write(self.work / (rid + '.response.json'), raw)
            response_hash = hashlib.sha256(raw).hexdigest()
            received_at = time.time()
            rate_headers = {str(name).lower(): str(value).replace(key, '[REDACTED]')
                            for name, value in headers.items()
                            if str(name).lower().startswith('x-ratelimit')
                            or str(name).lower() == 'retry-after'}
            metadata = dict(id=rid, http_status=status, http_error=http_error,
                            received_at=received_at, headers=rate_headers,
                            response_sha256=response_hash, response_bytes=len(raw),
                            content_type=str(headers.get('Content-Type', '')).replace(key, '[REDACTED]'))
            _write(self.work / (rid + '.response.meta.json'), _json(metadata))
            if status == 429:
                retry_after = _delay(rate_headers.get('retry-after'), received_at)
                if not retry_after:
                    retry_after = max([3] + [_delay(value, received_at)
                                          for name, value in rate_headers.items()
                                          if name.startswith('x-ratelimit-reset-')])
                raise RateLimited(retry_after)
            try:
                result = json.loads(raw)
                usage = result.get('usage', {})
                tokens = [usage.get('prompt_tokens'), usage.get('completion_tokens')]
                if all(type(n) is int and n >= 0 for n in tokens):
                    cost = (tokens[0] * self.input_price + tokens[1] * self.output_price) / 1000000
                    self._append(dict(event='settle', id=rid, charge_usd=str(cost),
                                      usage=usage, http_status=status,
                                      response_sha256=response_hash))
                if http_error:
                    raise ValueError('HTTP error')
                choice = result['choices'][0]
                result['content'] = choice['message'].get('content')
                result['finish_reason'] = choice.get('finish_reason')
                result['usage'] = usage
                result['http_status'] = status
                return result
            except Exception:
                raise RuntimeError(f'Groq response failed (HTTP {status}); '
                                   f'inspect {rid}.response.json; no retry') from None
