"""Prevent paid regeneration, outcome replacement and fake three-test acceptance."""
import json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import run_groq_full_scope as r

def test_recover_lost_local_response_without_regeneration(tmp_path,monkeypatch):
 api=tmp_path/'api';api.mkdir();dest=tmp_path/'case';dest.mkdir();monkeypatch.setattr(r,'API',api)
 event=dict(event='reserve',id='one',label='full_scope__case');(api/'ledger.jsonl').write_text(json.dumps(event)+'\n')
 original=dict(choices=[dict(message=dict(content='unchanged answer'),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=20))
 (api/'one.response.json').write_text(json.dumps(original));(api/'one.response.meta.json').write_text(json.dumps(dict(http_status=200)))
 assert r.recover_inference('case',dest)
 assert json.loads((dest/'inference.json').read_text())['content']=='unchanged answer'
 assert (api/'one.response.json').read_text()==json.dumps(original)

def test_unknown_paid_request_refuses_retry(tmp_path,monkeypatch):
 api=tmp_path/'api';api.mkdir();dest=tmp_path/'case';dest.mkdir();monkeypatch.setattr(r,'API',api)
 (api/'ledger.jsonl').write_text(json.dumps(dict(event='reserve',id='unknown',label='full_scope__case'))+'\n')
 with pytest.raises(RuntimeError,match='Uncertain prior API'):r.recover_inference('case',dest)
 assert not (dest/'inference.json').exists()

def test_completed_failure_is_reused_on_resume(tmp_path,monkeypatch):
 base=tmp_path/'eval0';base.mkdir();code='def test_a(): assert False\n';(base/'test_generated.py').write_text(code)
 result=dict(suite_pass=False,returncode=1);(base/'evaluation.json').write_text(json.dumps(result))
 def forbidden(*args):raise AssertionError('must not re-execute completed failure')
 monkeypatch.setattr(r,'execute',forbidden)
 assert r.cached_execute({},code,base)==(result,base)

def test_nested_function_names_do_not_fake_three_collected_tests(tmp_path):
 root=tmp_path/'source';root.mkdir();(root/'dummy_product.py').write_text('def value():\n    return 1\n')
 code='''import dummy_product
def test_outer():
    def test_inner_a(): assert True
    def test_inner_b(): assert True
    assert dummy_product.value() == 1
'''
 result=r.execute(dict(root=str(root),python=sys.executable,module='dummy_product'),code,tmp_path/'nested')
 assert result['returncode']==0 and result['nodes']==1
 assert not result['suite_pass']
