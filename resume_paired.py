"""Validate same-session evidence reuse before the real small A/B screen."""
import argparse
from pathlib import Path
import json
import sys
from paired_study import build_plan,validate_plan,make_bundle
from pilot.reuse import reuse_preparation,import_initialization_prefix
from pilot.common import write_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('previous','diagnostic','output'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--initialization-from',type=Path)
    args=parser.parse_args();root=args.output.resolve()
    saved=json.loads((root/'plan.json').read_text())
    plan=build_plan(saved['settings']['max_input_tokens'],saved['settings']['max_new_tokens'],
                    saved['settings'].get('test_output_contract'),saved['settings'].get('mechanism'))
    validate_plan(root,plan)
    try:
        reuse_preparation(root,args.previous,args.diagnostic,plan)
        if args.initialization_from:
            runtime=json.loads((root/'resume-provenance.json').read_text())['runtime']
            import_initialization_prefix(root,args.initialization_from,plan,runtime)
        print('Preparation and real GPU calibration validated for reuse. No inference or installation performed.')
        return 0
    except Exception as exc:
        write_json(root/'resume-failure.json',dict(error=repr(exc)))
        print('Resume stopped:',repr(exc));return 2
    finally:make_bundle(root)


if __name__=='__main__':sys.exit(main())
