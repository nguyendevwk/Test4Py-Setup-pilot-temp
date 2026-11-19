"""Recompute extension statistics from audited derived failure classifications."""
import argparse
from pathlib import Path
import analyze_groq_codamosa_extension as planned
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parents[1]/'research/groq_codamosa_extension_20261119/analysis_inputs');a=p.parse_args();planned.W=a.inputs.resolve();planned.main()
