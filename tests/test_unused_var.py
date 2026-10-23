import ast
import textwrap

from codeguard.rules.unused_var_rule import check_unused_var

def parse_code(source):
    return ast.parse(textwrap.dedent(source))

def test_local_unused_var():
    tree = parse_code("""
        def func():
            x = 10
            y = 10
            return x
    """)

    issues = check_unused_var(tree)
    assert len(issues) == 1
    assert "y" in issues[0]["message"]

def test_all_used_vars():
    tree = parse_code("""
        def func():
            x = 10
            y = 10
            return x + y
    """)

    assert check_unused_var(tree) == []

def test_underscore_ignore():
    tree = parse_code("""
        def func():
            _x = 10
    """)

    assert check_unused_var(tree) == []

def test_args_func_ignore():
    tree = parse_code("""
        def func(a, b, c):
            return a
    """)

    assert check_unused_var(tree) == []

def test_unused_var():
    tree = parse_code("""
        x = 10
        y = 10
        print(x)
    """)

    issues = check_unused_var(tree)
    assert len(issues) == 1
    assert "y" in issues[0]["message"]

def test_different_func():
    tree = parse_code("""
        def func():
            x = 10
            return x
        def func2():
            x = 20
    """)

    issues = check_unused_var(tree)
    assert len(issues) == 1

def test_for_loop_var_unused():
    tree = parse_code("""
        def func():
            for i in range(10):
                pass
    """)

    issues = check_unused_var(tree)
    assert len(issues) == 1
    assert "i" in issues[0]["message"]