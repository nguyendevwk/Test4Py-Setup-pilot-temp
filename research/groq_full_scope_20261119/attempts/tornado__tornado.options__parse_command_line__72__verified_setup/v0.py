import sys
import pytest
from tornado.options import parse_command_line, options

def test_parse_command_line_remains(tmp_path):
    # Define a dummy option to ensure it is parsed correctly
    options.define("test_opt", default="default", type=str, help="test option")
    # Simulate command line arguments
    args = ["script.py", "--test_opt=hello", "positional1", "positional2"]
    remaining = parse_command_line(args=args[1:])  # skip script name
    # The parsed option should be set
    assert options.test_opt == "hello"
    # Remaining positional arguments should be returned unchanged
    assert remaining == ["positional1", "positional2"]

def test_parse_command_line_final_false(tmp_path):
    # Define another option
    options.define("final_opt", default=0, type=int, help="final option")
    # Pass arguments with final=False so parsing continues after unknown options
    args = ["--final_opt=42", "--unknown", "pos"]
    remaining = parse_command_line(args=args[1:], final=False)
    # Known option should be parsed
    assert options.final_opt == 42
    # Unknown option should remain in the returned list
    assert remaining == ["--unknown", "pos"]

def test_parse_command_line_invalid_option_raises():
    # Define a boolean option
    options.define("bool_opt", default=False, type=bool, help="boolean option")
    # Pass an invalid value for the boolean option
    args = ["--bool_opt=notaboolean"]
    with pytest.raises(SystemExit) as excinfo:
        parse_command_line(args=args[1:])
    # SystemExit should have exit code 2 for command line parsing errors
    assert excinfo.value.code == 2
