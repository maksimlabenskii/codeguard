import ast
import textwrap

from codeguard.rules.arguments_rule import check_many_arguments


def parse_code(source):
    return ast.parse(textwrap.dedent(source))


def test_few_arguments_ok():
    tree = parse_code("""
        def f(a, b, c):
            return a + b + c
    """)
    assert check_many_arguments(tree) == []


def test_boundary_ok():
    tree = parse_code("""
        def f(a, b, c, d):
            return a + b + c + d
    """)
    assert check_many_arguments(tree) == []


def test_too_many_arguments():
    tree = parse_code("""
        def f(a, b, c, d, e):
            return a + b + c + d + e
    """)
    issues = check_many_arguments(tree)
    assert len(issues) == 1
    assert issues[0]["rule"] == "06_TOO_MANY_ARGUMENTS"


def test_star_args_counted():
    tree = parse_code("""
        def f(a, b, c, *args, **kwargs):
            return a
    """)
    issues = check_many_arguments(tree)
    assert len(issues) == 1


def test_method_self_not_counted():
    tree = parse_code("""
        class C:
            def method(self, a, b, c, d):
                return a
    """)
    assert check_many_arguments(tree) == []


def test_async_function_checked():
    tree = parse_code("""
        async def f(a, b, c, d, e):
            return a
    """)
    issues = check_many_arguments(tree)
    assert len(issues) == 1