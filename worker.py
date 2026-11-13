"""One isolated upstream pipeline and checkout per arm."""
import asyncio
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import time
import traceback

from pilot.common import append_json, digest, write_json


def main():
    root, mode, manifest = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    settings = json.loads(manifest.read_text())
    work = root.parent
    started = time.perf_counter()
    report = dict(mode=mode, status='running', settings=settings, stages={}, versions={},
                  input_tokens=0, output_tokens=0)
    for filename in ('model_calls.jsonl', 'probes.jsonl', 'test_attempts.jsonl', 'errors.jsonl'):
        (work / filename).touch()
    write_json(work / 'report.json', report)
    backend = None
    try:
        stage = time.perf_counter()
        from pilot.backend import TransformersBackend
        backend = TransformersBackend(settings, work)
        report['stages']['model_load'] = time.perf_counter() - stage
        report['versions'] = dict(python=platform.python_version(), **backend.versions)
        report['versions']['packages'] = {dist.metadata['Name']: dist.version
                                          for dist in importlib.metadata.distributions()}
        os.environ['OPENAI_API_KEY'] = 'local-inference'
        from test4dt import gptapi
        from pilot.setup import extract, select, production
        # Install before importing modules holding references to the shared object.
        gptapi.model.aask = backend.ask
        from test4dt import testcase
        from test4dt.message import ProjectMessage
        from test4dt.recorder import recoder
        # Uniform newline fix for upstream's module-comment concatenation.
        original_get_code = testcase.get_code
        testcase.get_code = lambda text: '\n' + original_get_code(text)

        original_set = testcase.Testcase.set_code
        def archive_code(self, code):
            original_set(self, code)
            archive = work / 'attempts'
            archive.mkdir(exist_ok=True)
            index = len(list(archive.glob('*.py')))
            path = archive / f'{index:04d}.py'
            path.write_text(code)
            append_json(work / 'test_attempts.jsonl', dict(file=str(path),
                        upstream_test=self.test_path, stage=backend.phase, sha256=digest(code)))
        testcase.Testcase.set_code = archive_code
        from pilot.scoring import classify, score
        for name in ('find_syntax_error', 'find_assert_error'):
            original = getattr(testcase.Testcase, name)
            def observe(self, original=original, name=name):
                value = original(self)
                if value:
                    append_json(work / 'errors.jsonl', dict(check=name, test=self.test_path,
                                category=classify(self.error_message), message=self.error_message))
                return value
            setattr(testcase.Testcase, name, observe)

        class PilotProject(ProjectMessage):
            def _get_files(self):
                return [p for p in sorted(super()._get_files())
                        if production(Path(p).relative_to(root))]

            async def generate_test_case(self):
                await self.target.test_manager.generate_test_case()

        stage = time.perf_counter()
        # Only the treatment arms incur extraction cost. Validation independently
        # checks that extraction is deterministic across clean source checkouts.
        context = ''
        if mode != 'baseline':
            extraction = extract(root)
            write_json(work / 'candidates.json', extraction)
            context, selection = select(root, extraction, mode, work, settings)
            report['selection'] = selection
            report['stages']['ast_analysis'] = extraction['seconds']
            report['stages']['selection_and_probes'] = selection['seconds']
        else:
            write_json(work / 'selection.json', dict(mode=mode, selected={}, probes=0))
        report['stages']['setup_total'] = time.perf_counter() - stage
        # Inject only into direct generation/repair prompts, after upstream type
        # inference. No probe observations or internal oracle are ever appended.
        original_ask = backend.ask
        async def ask(system, user):
            import inspect
            direct = inspect.stack()[1].function
            if direct in {'generate_test_case_normal', 'generate_test_case_easy',
                          'generate_test_case_evol', 'repair_syntax_error', 'repair_assert_error'}:
                user += '\n\n' + settings['scenario_prompt']
                if context:
                    user += '\n\n' + context
            return await original_ask(system, user)
        gptapi.model.aask = ask

        backend.phase = 'initialization'
        stage = time.perf_counter()
        project = PilotProject(str(root), settings['source_path'])
        asyncio.run(project.init())
        project.target, = (fn for file in project.file_messages
                           if file.mod_name == settings['target_module']
                           for fn in file.functions if fn.func_name == settings['target_function'])
        report['stages']['initialization'] = time.perf_counter() - stage
        stage = time.perf_counter()
        for index in range(settings['rounds']):
            backend.phase = f'generation_round_{index + 1}'
            project.generate_once()
            recoder.score.first_run = False
            write_json(work / f'round_{index + 1}.json', recoder.score.to_json())
        report['stages']['generation_repair_coverage'] = time.perf_counter() - stage
        report['retained_pytest_files'] = len(project.target.test_manager.testcases)
        report['generation_stats'] = recoder.score.to_json()
        report['upstream_coverage'] = str(root / project.dir_type / 'coverage.json')
        backend.phase = 'scoring'
        stage = time.perf_counter()
        report['score'] = score(root, work, settings)
        report['stages']['scoring'] = time.perf_counter() - stage
        score_ok = report['score']['status'] in {'scored', 'no_generated_tests'}
        mutant_ok = all(m['verdict'] in {'killed', 'survived', 'no_eligible_tests'}
                        for m in report['score'].get('mutants', []))
        report['status'] = 'complete' if score_ok and mutant_ok else 'failed'
        if report['status'] == 'failed':
            report['error'] = 'Scoring incomplete; inspect score.json and process artifacts'
    except Exception as exc:
        report.update(status='failed', error=repr(exc), traceback=traceback.format_exc())
        (work / 'failure.txt').write_text(report['traceback'])
    finally:
        calls = [json.loads(line) for line in (work / 'model_calls.jsonl').read_text().splitlines()]
        report['input_tokens'] = sum(row['input_tokens'] for row in calls)
        report['output_tokens'] = sum(row.get('output_tokens', 0) for row in calls)
        report['model_seconds_by_phase'] = {}
        report['tokens_by_phase'] = {}
        report['tokens_by_operation'] = {}
        for row in calls:
            phase = row['phase']
            report['model_seconds_by_phase'][phase] = report['model_seconds_by_phase'].get(phase, 0) + row['seconds']
            totals = report['tokens_by_phase'].setdefault(phase, dict(input=0, output=0))
            totals['input'] += row['input_tokens']
            totals['output'] += row.get('output_tokens', 0)
            operation = row.get('upstream_operation') or 'analysis_or_retrieval'
            detail = report['tokens_by_operation'].setdefault(operation, dict(input=0, output=0, seconds=0))
            detail['input'] += row['input_tokens']
            detail['output'] += row.get('output_tokens', 0)
            detail['seconds'] += row['seconds']
        report['worker_seconds'] = time.perf_counter() - started
        write_json(work / 'report.json', report)
    return 0 if report['status'] == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
