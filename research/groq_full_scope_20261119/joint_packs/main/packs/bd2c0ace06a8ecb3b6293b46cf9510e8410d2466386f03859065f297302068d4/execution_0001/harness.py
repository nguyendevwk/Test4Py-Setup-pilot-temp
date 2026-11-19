
import json, pathlib, sys, traceback
import coverage
import pytest
config = json.loads(pathlib.Path(sys.argv[1]).read_bytes())
cov = coverage.Coverage(data_file='.coverage', branch=True, include=config['source_files'])
cov.start()
exitcode = None
try:
    exitcode = int(pytest.main(['-q', '-o', 'addopts=', '--confcutdir='+config['cwd'],
        '-p', 'pytest_jsonreport.plugin', '--json-report',
        '--json-report-file=pytest.json', config['tests']]))
except BaseException:
    traceback.print_exc()
finally:
    cov.stop()
    cov.save()
    files = {}
    errors = {}
    data = cov.get_data()
    measured = {str(pathlib.Path(p).resolve()) for p in data.measured_files()}
    actual_data = any(data.lines(p) for p in data.measured_files())
    for file in config['source_files']:
        try:
            filename, statements, excluded, missing, formatted = cov.analysis2(file)
            files[file] = dict(statements=sorted(statements), missing=sorted(missing),
                excluded=sorted(excluded), measured_file=str(pathlib.Path(file).resolve()) in measured)
        except BaseException as exc:
            errors[file] = type(exc).__name__+': '+str(exc)
    pathlib.Path('locked_coverage.json').write_text(json.dumps(dict(
        actual_data=bool(actual_data), files=files, errors=errors), indent=2))
sys.exit(exitcode if exitcode is not None else 2)
