import ast
import textwrap
from codeguard.rules.naming_rule import check_naming_convention

def parse_code(source):
    return ast.parse(textwrap.dedent(source))

def test_valid_names():
    tree = parse_code("""
        class MyClass:
            def my_function(self, my_arg):
                my_var = my_arg + 1
                return my_var
    """)
    assert check_naming_convention(tree) == []


def test_invalid_class_name():
    tree = parse_code("""
        class my_class:
            pass
    """)
    issues = check_naming_convention(tree)
    assert len(issues) == 1
    assert issues[0]["rule"] == "05_CLASS_NAMING"


def test_invalid_function_name():
    tree = parse_code("""
        def MyFunction():
            pass
    """)
    issues = check_naming_convention(tree)
    assert len(issues) == 1
    assert issues[0]["rule"] == "05_FUNC_NAMING"


def test_invalid_variable_and_arg():
    tree = parse_code("""
        def test(myArg):
            BadVar = 1
    """)
    issues = check_naming_convention(tree)
    assert len(issues) == 2

    rules = {i["rule"] for i in issues}
    assert "05_ARG_NAMING" in rules
    assert "05_VAR_NAMING" in rules