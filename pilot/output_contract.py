"""Opt-in prompt and structural contracts for generated pytest modules.

The AST check here verifies collection shape only. It does not establish that a
test has a correct or meaningful behavioral oracle.
"""
import ast

from pilot.quality import extract_code

POLICY = 'single-test-v1'


class OutputContractError(ValueError):
    """Candidate output violates an enabled generation/repair contract."""

GENERATION_OPERATIONS = frozenset({
    'generate_test_case_normal',
    'generate_test_case_easy',
    'generate_test_case_evol',
})
REPAIR_OPERATIONS = frozenset({'repair_syntax_error', 'repair_assert_error'})

GENERATION_CONTRACT = (
    'Output contract: return exactly one complete pytest test for the current '
    'target function in one Python code block. Keep the test concise and include '
    'meaningful assertions grounded in the supplied source. Imports, fixtures, '
    'and helper setup are allowed as needed. Do not include prose or additional '
    'test functions.'
)

REPAIR_CONTRACT = (
    'Repair contract: return one complete Python test module in one code block. '
    'Preserve every existing test and its assertions; do not delete, weaken, or '
    'replace checks to make the suite pass. Correct only supported setup, import, '
    'or execution errors. This repair contract does not impose a one-test limit.'
)


def append_prompt_contract(system_prompt, user_prompt, operation):
    """Append the operation-specific prompt contract; leave other calls intact."""
    if operation in GENERATION_OPERATIONS:
        contract = GENERATION_CONTRACT
    elif operation in REPAIR_OPERATIONS:
        contract = REPAIR_CONTRACT
    else:
        return system_prompt, user_prompt
    return system_prompt, user_prompt.rstrip() + '\n\n' + contract


def contract_kind(operation):
    """Return the applied contract label for a known operation, else None."""
    if operation in GENERATION_OPERATIONS:
        return 'generation'
    if operation in REPAIR_OPERATIONS:
        return 'repair'
    return None


def _static_test_shape_count(tree):
    """Count test-shaped defs at module/direct Test* class scope.

    This shape check is deliberately approximate; pytest collection is
    authoritative and no AST result establishes semantic correctness.
    """
    def is_test(node):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False
        if not node.name.startswith('test'):
            return False
        # pytest fixtures are not collected as tests, even if named test_*.
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator
            if isinstance(target, ast.Name) and target.id == 'fixture':
                return False
            if isinstance(target, ast.Attribute) and target.attr == 'fixture':
                return False
        return True

    count = sum(
        is_test(node)
        for node in tree.body
    )
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name.startswith('Test'):
            count += sum(
                is_test(member)
                for member in node.body
            )
    return count


def validate_initial_generation(raw_module):
    """Require one statically test-shaped definition in a complete Python module.

    Returns the extracted source verbatim. It never removes or rewrites code.
    It does not prove pytest will collect the test or assess assertion semantics.
    """
    try:
        source = extract_code(raw_module)
    except ValueError as exc:
        raise OutputContractError(str(exc)) from exc
    try:
        tree = ast.parse(source)
        compile(tree, '<generated-test-module>', 'exec')
    except SyntaxError as exc:
        raise OutputContractError('Generated Python module is malformed') from exc
    count = _static_test_shape_count(tree)
    if count == 0:
        raise OutputContractError('Generated module contains no statically test-shaped definition')
    if count != 1:
        raise OutputContractError(f'Generated module must contain exactly one statically test-shaped definition; found {count}')
    return source


def validate_repair_module(raw_module):
    """Require a complete, syntactically valid repair module, without test count limits."""
    try:
        source = extract_code(raw_module)
    except ValueError as exc:
        raise OutputContractError(str(exc)) from exc
    try:
        tree = ast.parse(source)
        compile(tree, '<repaired-test-module>', 'exec')
    except SyntaxError as exc:
        raise OutputContractError('Repaired Python module is malformed') from exc
    return source
