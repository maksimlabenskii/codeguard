import ast
from codeguard.rules.exceptions_rules import (
    check_broad_except,
    check_missing_raise,
    check_empty_except
)
from codeguard.rules.many_cycles_rule import check_loops
from codeguard.rules.arguments_rule import check_many_arguments
from codeguard.rules.naming_rule import check_naming_convention
from codeguard.rules.unused_var_rule import check_unused_var

def analyze_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return [{
                "line": e.lineno,
                "rule": "02_SYNTAX_ERROR",
                'message': ""
            }]

    issues = []

    rules = [
        check_broad_except,
        check_missing_raise,
        check_empty_except,
        check_loops,
        check_many_arguments,
        check_naming_convention,
        check_unused_var,
    ]

    for rule in rules:
        issues.extend(rule(tree))

    return issues

