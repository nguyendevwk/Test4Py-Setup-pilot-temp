import io
import json
import urllib.error
from unittest.mock import patch

import pytest

from scripts.study_groq_client import BudgetExceeded, StudyClient, PRICE_SOURCE, USER_AGENT


@pytest.fixture(autouse=True)
def key(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'test-secret-key')


def reply(finish='stop', usage=None):
    return json.dumps({'choices': [{'message': {'content': 'hello'},
                                  'finish_reason': finish}],
                       'usage': usage or {'prompt_tokens': 20, 'completion_tokens': 10}}).encode()


def events(path):
    return [json.loads(line) for line in (path / 'ledger.jsonl').read_text().splitlines()]


@pytest.mark.parametrize('finish', ['stop', 'length'])
def test_success_and_truncation(tmp_path, finish):
    client = StudyClient(tmp_path)
    def transport(request, timeout):
        assert len(events(tmp_path)) == 1
        assert list(tmp_path.glob('*.request.json'))
        payload = json.loads(request.data)
        assert payload['seed'] == 42
        assert payload['reasoning_effort'] == 'low'
        assert timeout == 120
        assert request.get_header('User-agent') == USER_AGENT
        assert request.get_header('Accept') == 'application/json'
        return io.BytesIO(reply(finish))
    with patch('urllib.request.urlopen', side_effect=transport) as send:
        result = client.call([{'role': 'user', 'content': 'hi'}], 42, 'case')
    assert send.call_count == 1
    assert result['content'] == 'hello'
    assert result['http_status'] == 200
    assert result['finish_reason'] == finish
    assert result['usage']['completion_tokens'] == 10
    assert client.spent_usd == pytest.approx(.0000045)
    assert events(tmp_path)[0]['price_source'] == PRICE_SOURCE
    for artifact in tmp_path.glob('*.json*'):
        assert 'test-secret-key' not in artifact.read_text()


def test_reservation_blocks_before_transport(tmp_path):
    client = StudyClient(tmp_path, budget_usd=.000001)
    with patch('urllib.request.urlopen') as send, pytest.raises(BudgetExceeded):
        client.call([{'role': 'user', 'content': '你好'}], 1, 'cap')
    send.assert_not_called()
    assert not list(tmp_path.glob('*.request.json'))


def test_unknown_network_retains_reservation_on_resume(tmp_path):
    client = StudyClient(tmp_path, budget_usd=.001)
    with patch('urllib.request.urlopen', side_effect=TimeoutError('test-secret-key')) as send:
        with pytest.raises(RuntimeError, match='reservation retained') as error:
            client.call([], 1, 'timeout')
    assert 'test-secret-key' not in str(error.value)
    assert send.call_count == 1
    reservation = float(events(tmp_path)[0]['charge_usd'])
    assert StudyClient(tmp_path).spent_usd == reservation
    with patch('urllib.request.urlopen') as send, pytest.raises(BudgetExceeded):
        StudyClient(tmp_path, budget_usd=.001).call([], 2, 'resume')
    send.assert_not_called()


@pytest.mark.parametrize('raw', [b'broken', b'{"choices": []}', reply(usage={'prompt_tokens': -1})])
def test_invalid_response_keeps_full_reservation(tmp_path, raw):
    with patch('urllib.request.urlopen', return_value=io.BytesIO(raw)):
        try:
            StudyClient(tmp_path).call([], 1, 'invalid')
        except RuntimeError:
            pass
    assert len(events(tmp_path)) == 1
    assert list(tmp_path.glob('*.response.json'))[0].read_bytes() == raw
    assert StudyClient(tmp_path).spent_usd == float(events(tmp_path)[0]['charge_usd'])


def test_http_error_saved_no_retry(tmp_path):
    error = urllib.error.HTTPError('url', 429, 'rate limit', {}, io.BytesIO(b'error test-secret-key'))
    with patch('urllib.request.urlopen', side_effect=error) as send:
        with pytest.raises(RuntimeError):
            StudyClient(tmp_path).call([], 1, 'http')
    assert send.call_count == 1
    assert list(tmp_path.glob('*.response.json'))[0].read_bytes() == b'error [REDACTED]'
    assert len(events(tmp_path)) == 1


def test_edge_rejection_records_status_without_retry_or_release(tmp_path):
    raw = b'error code: 1010\n'
    error = urllib.error.HTTPError('url', 403, 'Forbidden',
                                  {'Content-Type': 'text/plain; test-secret-key'}, io.BytesIO(raw))
    with patch('urllib.request.urlopen', side_effect=error) as send:
        with pytest.raises(RuntimeError, match=r'HTTP 403'):
            StudyClient(tmp_path).call([], 1, 'edge')
    assert send.call_count == 1
    rid = events(tmp_path)[0]['id']
    metadata = json.loads((tmp_path / (rid + '.response.meta.json')).read_text())
    assert metadata['http_status'] == 403
    assert metadata['http_error'] is True
    assert 'test-secret-key' not in json.dumps(metadata)
    assert (tmp_path / (rid + '.response.json')).read_bytes() == raw
    assert StudyClient(tmp_path).spent_usd == float(events(tmp_path)[0]['charge_usd'])


def test_explicit_env_key_only(tmp_path, monkeypatch):
    monkeypatch.delenv('GROQ_API_KEY')
    monkeypatch.chdir(tmp_path)
    (tmp_path / '.env').write_text('OTHER_KEY=ignore\nGROQ_API_KEY="test-secret-key"\n')
    with patch('urllib.request.urlopen', return_value=io.BytesIO(reply())) as send:
        StudyClient(tmp_path / 'work').call([], 1, 'env')
    assert send.call_args.args[0].get_header('Authorization') == 'Bearer test-secret-key'


def test_corrupt_ledger_fails_closed(tmp_path):
    (tmp_path / 'ledger.jsonl').write_text('{broken\n')
    with patch('urllib.request.urlopen') as send, pytest.raises(ValueError):
        StudyClient(tmp_path).call([], 1, 'corrupt')
    send.assert_not_called()


def test_hard_campaign_limit(tmp_path):
    assert StudyClient(tmp_path).budget == 3
    assert StudyClient(tmp_path, budget_usd=3).budget == 3
    assert StudyClient(tmp_path, budget_usd=2.5).budget == 2.5
    with pytest.raises(ValueError):
        StudyClient(tmp_path, budget_usd=3.01)


def test_raised_cap_preserves_charges_and_reservations(tmp_path):
    client = StudyClient(tmp_path, budget_usd=2)
    client._append(dict(event='reserve', id='settled', charge_usd='1.5'))
    client._append(dict(event='settle', id='settled', charge_usd='1.25'))
    client._append(dict(event='reserve', id='unknown', charge_usd='1.749999'))
    original = client.ledger.read_bytes()
    resumed = StudyClient(tmp_path)
    assert resumed.spent_usd == pytest.approx(2.999999)
    with patch('urllib.request.urlopen') as send, pytest.raises(BudgetExceeded):
        resumed.call([], 1, 'cap')
    send.assert_not_called()
    assert client.ledger.read_bytes() == original


def test_external_balance_allocation_counts_without_rewriting(tmp_path, monkeypatch):
    client = StudyClient(tmp_path)
    client._append(dict(event='reserve', id='local', charge_usd='.134',
                        requested_at=0, input_token_bound=0, max_tokens=0))
    external = dict(event='reserve', id='user_balance_snapshot_20261119',
                    charge_usd='.366', requested_at=0,
                    input_token_bound=0, max_tokens=0,
                    label='External allocation; see budget_reconciliation.json')
    client._append(external)
    original = client.ledger.read_bytes()
    assert StudyClient(tmp_path).spent_usd == .5
    monkeypatch.setattr('scripts.study_groq_client.time.time', lambda: 1000.)
    with patch('scripts.study_groq_client.time.sleep') as sleep:
        StudyClient(tmp_path)._pace(100)
    sleep.assert_not_called()
    assert client.ledger.read_bytes() == original
    with patch('urllib.request.urlopen') as send, pytest.raises(BudgetExceeded):
        StudyClient(tmp_path, budget_usd=.500001).call([], 1, 'cap')
    send.assert_not_called()
    assert client.ledger.read_bytes() == original
    with patch('urllib.request.urlopen', return_value=io.BytesIO(reply())):
        StudyClient(tmp_path).call([], 2, 'next')
    assert client.ledger.read_bytes().startswith(original)
    assert events(tmp_path)[1] == external
    assert 'usage' not in events(tmp_path)[1]
    assert StudyClient(tmp_path).spent_usd == pytest.approx(.5000045)
    assert not (tmp_path / (external['id'] + '.request.json')).exists()


def test_utf8_reservation_and_configured_prices(tmp_path):
    client = StudyClient(tmp_path, input_price=.15, output_price=.60)
    with patch('urllib.request.urlopen', side_effect=TimeoutError):
        with pytest.raises(RuntimeError):
            client.call([{'role': 'user', 'content': '你好🙂'}], 7, 'unicode')
    body = list(tmp_path.glob('*.request.json'))[0].read_bytes()
    event = events(tmp_path)[0]
    assert event['input_token_bound'] == 2 * len(body) + 4096
    expected = (event['input_token_bound'] * .15 + 2048 * .60) / 1000000
    assert client.spent_usd == pytest.approx(expected)
    assert event['pricing'] == 'configured estimate'


def test_settled_cost_survives_price_change(tmp_path):
    with patch('urllib.request.urlopen', return_value=io.BytesIO(reply())):
        StudyClient(tmp_path).call([], 1, 'settled')
    assert StudyClient(tmp_path, input_price=.15, output_price=.60).spent_usd == pytest.approx(.0000045)


def test_rate_headers_control_wait_and_no_secret_artifacts(tmp_path, monkeypatch):
    from scripts.study_groq_client import RateLimited
    clock = [1000.0]
    sleeps = []
    monkeypatch.setattr('scripts.study_groq_client.time.time', lambda: clock[0])
    def sleep(seconds):
        assert 0 < seconds <= 30
        sleeps.append(seconds)
        clock[0] += seconds
    monkeypatch.setattr('scripts.study_groq_client.time.sleep', sleep)
    headers = {'Retry-After': '65', 'X-RateLimit-Remaining-Requests': '0',
               'X-RateLimit-Reset-Requests': '1m5s',
               'X-RateLimit-Remaining-Tokens': '90000',
               'X-RateLimit-Reset-Tokens': '1s',
               'X-RateLimit-Diagnostic': 'test-secret-key',
               'Authorization': 'Bearer test-secret-key'}
    error = urllib.error.HTTPError('url', 429, 'limited', headers, io.BytesIO(b'limited'))
    with patch('urllib.request.urlopen', side_effect=error) as send:
        with pytest.raises(RateLimited) as raised:
            StudyClient(tmp_path).call([], 1, 'limited')
    assert raised.value.retry_after == 65
    assert raised.value.http_status == 429
    assert send.call_count == 1
    assert len(events(tmp_path)) == 1
    charge = StudyClient(tmp_path).spent_usd
    assert charge > 0
    metadata_path = next(tmp_path.glob('*.response.meta.json'))
    meta = json.loads(metadata_path.read_text())
    assert meta['http_status'] == 429
    assert meta['headers']['retry-after'] == '65'
    assert 'authorization' not in meta['headers']
    for path in tmp_path.glob('*.json*'):
        assert 'test-secret-key' not in path.read_text()
    with patch('urllib.request.urlopen', return_value=io.BytesIO(reply())):
        StudyClient(tmp_path).call([], 2, 'resume')
    assert sleeps == [30, 30, 5]
    assert clock[0] == 1065
    assert StudyClient(tmp_path).spent_usd > charge


def test_available_header_capacity_avoids_static_delay(tmp_path, monkeypatch):
    client = StudyClient(tmp_path)
    client._append(dict(event='reserve', id='prior', requested_at=1000,
                        input_token_bound=90000, max_tokens=1, charge_usd='.01'))
    (tmp_path / 'prior.response.meta.json').write_text(json.dumps({
        'received_at': 1000, 'headers': {
            'x-ratelimit-remaining-requests': '100', 'x-ratelimit-reset-requests': '1m',
            'x-ratelimit-remaining-tokens': '90000', 'x-ratelimit-reset-tokens': '1s'}}))
    monkeypatch.setattr('scripts.study_groq_client.time.time', lambda: 1000)
    with patch('scripts.study_groq_client.time.sleep') as sleep:
        client._pace(20000)
    sleep.assert_not_called()


def test_missing_headers_enforces_fallback(tmp_path, monkeypatch):
    client = StudyClient(tmp_path)
    client._append(dict(event='reserve', id='prior', requested_at=1000,
                        input_token_bound=60000, max_tokens=1, charge_usd='.01'))
    clock = [1000.]
    monkeypatch.setattr('scripts.study_groq_client.time.time', lambda: clock[0])
    def sleep(seconds):
        assert seconds <= 30
        clock[0] += seconds
    monkeypatch.setattr('scripts.study_groq_client.time.sleep', sleep)
    client._pace(100)
    assert clock[0] == 1003
    client._pace(50000)
    assert clock[0] == 1060
