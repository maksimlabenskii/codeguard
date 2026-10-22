import ast
import textwrap

from codeguard.rules.exceptions_rules import (
    check_empty_except,
    check_broad_except,
    check_missing_raise
)

def parse_code(source_code):
    return ast.parse(textwrap.dedent(source_code))

def test_empty_except():
    tree = parse_code("""
        try:
            operation()
        except Exception:
            pass
""")

    issues = check_empty_except(tree)

    assert len(issues) == 1
    assert issues[0]["rule"] == "01_EMPTY_EXCEPTION"

def test_broad_except():
    tree = parse_code("""
        try:
            operation()
        except Exception:
            print("Error")
""")

    issues = check_broad_except(tree)

    assert len(issues) == 1
    assert issues[0]["rule"] == "01_BROAD_EXCEPTION"

def test_missing_raise():
    tree = parse_code("""
        try:
            operation()
        except ValueError:
            print("Error")
""")

    issues = check_missing_raise(tree)

    assert len(issues) == 1
    assert issues[0]["rule"] == "01_MISSING_RAISE_EXCEPTION"