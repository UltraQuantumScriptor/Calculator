from hypothesis import given, settings, strategies as st
import string
from tokenizer import tokenize
from parser import parse
from RPN import evaluate

numbers = st.decimals(
    min_value=0,
    max_value=1000,
    places=3,
    allow_nan=False,
    allow_infinity=False,
).map(lambda x: format(x, "f").rstrip("0").rstrip(".") or "0")
constants = st.sampled_from(["pi", "e"])
functions = st.sampled_from(
    ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "abs", "ran"]
)
ops = st.sampled_from(["+", "-", "*", "/", "^"])


def x10_expr(base, exp):
    return f"{base}x10{exp}"


exponents = st.integers(-10, 10).map(str)

x10_numbers = st.builds(x10_expr, numbers, exponents)


def func_call(func, arg):
    return f"{func}({arg})"


func_expr = st.builds(func_call, functions, numbers)

base_expr = st.one_of(numbers, constants, x10_numbers, func_expr)

expr = st.deferred(lambda: base_expr)

expr = st.recursive(
    base_expr,
    lambda children: st.one_of(
        # binary operations
        st.builds(lambda a, op, b: f"({a}{op}{b})", children, ops, children),
        # nested function calls
        st.builds(lambda f, a: f"{f}({a})", functions, children),
    ),
    max_leaves=4,
)


# @settings(max_examples=1000, deadline=300)
# @given(expr)
# def test_calculator(e):
#     print("INPUT:", e)
#     tokens = tokenize(e)
#     try:
#         result = parse(tokens)
#     except Exception as e:
#         assert False, f"Crash on input {e!r}: {e}"
#     assert result is not None


@settings(max_examples=500, deadline=2000)
@given(expr)
def test_no_crash(e):
    try:
        print(f"\nTESTING: {e}")
        tokens = tokenize(e)
        parsed = parse(tokens)
        memory = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
            "M": 0,
            "X": 0,
            "Y": 0,
        }
        evaluate(parsed, memory, 0, guide=None, debug_mode=False)
    except (ValueError, ZeroDivisionError, SyntaxError, OverflowError):
        pass  # expected math errors, not crashes
    except Exception as e:
        assert False, f"Unexpected crash on {e!r}"
