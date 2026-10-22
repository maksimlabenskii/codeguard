import ast
import textwrap

from codeguard.rules.many_cycles_rule import check_loops


def parse_code(source):
    return ast.parse(textwrap.dedent(source))

def test_loops_two_return_ok():
    tree = parse_code("""
        for i in range(10):
            for j in range(10):
                print(i, j)
    """)

    assert check_loops(tree) == []

def test_loops_three_return_error():
    tree = parse_code("""
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    print(i, j, k)
    """)

    issues = check_loops(tree)

    assert len(issues) == 1
    assert issues[0]["rule"] == "02_TOO_MANY_LOOPS"


def test_loops_mixed_return_error():
    tree = parse_code("""
        for i in range(10):
            while True:
                for j in range(10):
                    print(i, j)
    """)

    issues = check_loops(tree)

    assert len(issues) == 1
    assert issues[0]["rule"] == "02_TOO_MANY_LOOPS"

def test_loops_not_nested_return_ok():
    tree = parse_code("""
        for i in range(10):
            print(i)
        for j in range(10):
            print(j)
        while True:
            print(hi)
    """)

    assert check_loops(tree) == []