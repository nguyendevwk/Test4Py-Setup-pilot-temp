import ast
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from council.groq_engine import GroqCouncilEngine
from pilot.multitarget import clean_code_block

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "local_benchmark_repos"

SYMBOL_MAP = {
    "typesystem": {
        "canonical_imports": (
            "from typesystem import Schema, String, Integer, Float, Boolean, Choice, Array, Object\n"
            "from typesystem import ValidationError, Message\n"
            "from typesystem.fields import Field\n"
            "# NOTE: There is NO 'typesystem.exceptions' module. ValidationError is imported from 'typesystem' or 'typesystem.base'."
        ),
        "assertion_rules": (
            "# NOTE on ValidationError: excinfo.value does NOT have a '.code' attribute directly.\n"
            "# To check error code: [m.code for m in excinfo.value.messages()] or str(excinfo.value).\n"
            "# To check error message: str(excinfo.value) or [m.text for m in excinfo.value.messages()]."
        )
    },
    "genty": {
        "canonical_imports": (
            "import unittest\n"
            "from genty import genty, genty_dataset, genty_args, genty_repeat"
        ),
        "assertion_rules": (
            "# NOTE: genty decorators (@genty, @genty_dataset) MUST be applied to methods inside a class\n"
            "# that inherits from unittest.TestCase, and the class MUST be decorated with @genty."
        )
    }
}

def normalize_hallucinated_imports(code: str) -> str:
    """Rewrite known hallucinated imports before execution."""
    code = code.replace("from typesystem.exceptions import ValidationError", "from typesystem.base import ValidationError")
    code = code.replace("from typesystem.exceptions import Message", "from typesystem.base import Message")
    code = code.replace("import typesystem.exceptions", "import typesystem.base as exceptions")
    return code

print("Pilot helper defined.")
