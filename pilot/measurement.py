"""Explicit retained-suite counts; never infer oracle correctness from pytest."""


def retained_counts(process, report, files):
    files=set(files)
    tests=[r for r in report.get('tests',[]) if r.get('nodeid','').split('::')[0] in files]
    passed=sum(r.get('outcome')=='passed' and all(r.get(p,{}).get('outcome')=='passed'
               for p in ('setup','call','teardown')) for r in tests)
    clean=bool(not process.get('timeout',False) and process.get('returncode') in (0,1)
               and not report.get('summary',{}).get('errors',0)
               and not any(c.get('outcome')=='failed' for c in report.get('collectors',[])))
    return dict(retained_collected_nodes=len(tests),retained_passed_nodes=passed,
                retained_failed_nodes=sum(r.get('outcome')=='failed' for r in tests),
                retained_error_nodes=sum(r.get('outcome')=='error' for r in tests),
                retained_skipped_nodes=sum(r.get('outcome')=='skipped' for r in tests),
                retained_suite_all_pass=bool(clean and tests and passed==len(tests)),
                retained_collection_complete=clean,
                suite_scope='retained generated tests only; upstream reductions are audited separately')
