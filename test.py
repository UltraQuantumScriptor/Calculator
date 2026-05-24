import math
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokenizer import tokenize
from parser import parse
from RPN import evaluate

# ── helpers ──────────────────────────────────────────────────────────────────


def calc(expr, memory=None, ans=0, n=None, stat=False):
    if memory is None:
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
    if n is None:
        n = []
    tokens = tokenize(expr, n)
    parsed = parse(tokens)
    result = evaluate(parsed, memory, ans, guide=None, debug_mode=False, n=n, STAT=stat)
    return result[0] if result else None


def approx(a, b, tol=1e-6):
    return abs(a - b) < tol


# ── basic arithmetic ──────────────────────────────────────────────────────────


def test_addition():
    assert calc("2+3") == 5.0


def test_subtraction():
    assert calc("10-4") == 6.0


def test_multiplication():
    assert calc("3*4") == 12.0


def test_division():
    assert calc("10/4") == 2.5


def test_exponentiation():
    assert calc("2^10") == 1024.0


def test_float():
    assert calc("1.5+2.5") == 4.0


# ── operator precedence ───────────────────────────────────────────────────────


def test_precedence_add_mul():
    assert calc("2+3*4") == 14.0


def test_precedence_mul_add():
    assert calc("2*3+4") == 10.0


def test_precedence_pow():
    assert calc("2+3^2") == 11.0


def test_precedence_chain():
    assert calc("2+3*4-1") == 13.0


# ── parentheses ───────────────────────────────────────────────────────────────


def test_parens_basic():
    assert calc("(2+3)*4") == 20.0


def test_parens_nested():
    assert calc("((2+3)*4)+1") == 21.0


def test_parens_division():
    assert calc("(10+2)/4") == 3.0


def test_implicit_multiply_parens():
    assert calc("2(2+3)") == 10.0


def test_implicit_multiply_parens_both():
    assert calc("(2+3)(4+5)") == 45.0


# ── unary minus ───────────────────────────────────────────────────────────────


def test_unary_basic():
    assert calc("-3") == -3.0


def test_unary_double():
    assert calc("--3") == 3.0


def test_unary_multiply():
    assert calc("-3*-2") == 6.0


def test_unary_parens():
    assert calc("-(3+2)") == -5.0


def test_unary_in_expr():
    assert calc("2+-3") == -1.0


def test_unary_pow():
    assert approx(calc("2^-3"), 0.125)


# ── trig functions ────────────────────────────────────────────────────────────


def test_sin_30():
    assert approx(calc("sin(30)"), 0.5)


def test_cos_60():
    assert approx(calc("cos(60)"), 0.5)


def test_tan_45():
    assert approx(calc("tan(45)"), 1.0)


def test_asin_half():
    assert approx(calc("asin(0.5)"), 30.0)


def test_acos_half():
    assert approx(calc("acos(0.5)"), 60.0)


def test_atan_1():
    assert approx(calc("atan(1)"), 45.0)


def test_sin_expression():
    assert approx(calc("sin(30)+cos(60)"), 1.0)


def test_sin_pow():
    assert approx(calc("sin(30)^2"), 0.25)


# ── logarithms ────────────────────────────────────────────────────────────────


def test_log_100():
    assert approx(calc("log(100)"), 2.0)


def test_log_1():
    assert approx(calc("log(1)"), 0.0)


def test_ln_e():
    assert approx(calc("ln(e)"), 1.0)


def test_ln_1():
    assert approx(calc("ln(1)"), 0.0)


def test_log_product():
    assert approx(calc("log(1635)+log(170)"), math.log10(1635 * 170))


# ── constants ─────────────────────────────────────────────────────────────────


def test_pi():
    assert approx(calc("pi"), math.pi)


def test_e():
    assert approx(calc("e"), math.e)


def test_pi_multiply():
    assert approx(calc("2*pi"), 2 * math.pi)


def test_e_multiply():
    assert approx(calc("3*e"), 3 * math.e)


# ── factorial ─────────────────────────────────────────────────────────────────


def test_factorial_5():
    assert calc("5!") == 120.0


def test_factorial_0():
    assert calc("0!") == 1.0


def test_factorial_1():
    assert calc("1!") == 1.0


def test_factorial_in_expr():
    assert calc("5!+1") == 121.0


# ── combinatorics ─────────────────────────────────────────────────────────────


def test_ncr():
    assert calc("5 ncr 2") == 10.0


def test_npr():
    assert calc("5 npr 2") == 20.0


def test_ncr_zero():
    assert calc("5 ncr 0") == 1.0


def test_ncr_self():
    assert calc("5 ncr 5") == 1.0


# ── memory ────────────────────────────────────────────────────────────────────


def test_store_recall():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5 sto A", memory=mem)
    assert calc("A", memory=mem) == 5.0


def test_var_in_expression():
    mem = {"A": 5, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("A+1", memory=mem) == 6.0


def test_var_multiply():
    mem = {"A": 3, "B": 4, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("A*B", memory=mem) == 12.0


def test_m_plus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 5, "X": 0, "Y": 0}
    calc("3 M+", memory=mem)
    assert mem["M"] == 8.0


def test_m_minus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 5, "X": 0, "Y": 0}
    calc("3 M-", memory=mem)
    assert mem["M"] == 2.0


# ── ans ───────────────────────────────────────────────────────────────────────


def test_ans():
    result = calc("ans+1", ans=5)
    assert result == 6.0


def test_ans_in_expression():
    result = calc("ans*2+1", ans=3)
    assert result == 7.0


# ── stat functions ────────────────────────────────────────────────────────────


def test_stat_n():
    n = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert calc("n", n=n, stat=True) == 5.0


def test_stat_mean():
    n = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert approx(calc("mean", n=n, stat=True), 3.0)


def test_stat_sumx():
    n = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert calc("sumx", n=n, stat=True) == 15.0


def test_stat_sumx2():
    n = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert calc("sumx2", n=n, stat=True) == 55.0


def test_stat_sdev():
    n = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    assert approx(calc("sdev", n=n, stat=True), 2.0)


def test_stat_mplus():
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5 M+", memory=mem, n=n, stat=True)
    calc("3 M+", memory=mem, n=n, stat=True)
    assert n == [5.0, 3.0]


def test_stat_mminus_value():
    n = [5.0, 3.0, 5.0]
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5 M-", memory=mem, n=n, stat=True)
    assert n == [5.0, 3.0]


def test_stat_mminus_last():
    n = [5.0, 3.0, 8.0]
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("M-", memory=mem, n=n, stat=True)
    assert n == [5.0, 3.0]


# ── error cases ───────────────────────────────────────────────────────────────


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calc("1/0")


def test_asin_domain():
    with pytest.raises(ValueError):
        calc("asin(2)")


def test_acos_domain():
    with pytest.raises(ValueError):
        calc("acos(2)")


def test_log_negative():
    with pytest.raises(ValueError):
        calc("log(-1)")


def test_ln_negative():
    with pytest.raises(ValueError):
        calc("ln(-1)")


def test_func_no_parens():
    with pytest.raises(SyntaxError):
        calc("sin5")


def test_invalid_expression():
    with pytest.raises(SyntaxError):
        calc("2 2")


def test_tan_90():
    with pytest.raises(ValueError):
        calc("tan(90)")
