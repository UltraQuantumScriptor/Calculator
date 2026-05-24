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


# ── rcl / sto all cells ───────────────────────────────────────────────────────


def test_store_recall_all_cells():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    for i, cell in enumerate(["A", "B", "C", "D", "E", "F", "M", "X", "Y"]):
        calc(f"{i+1} sto {cell}", memory=mem)
    for i, cell in enumerate(["A", "B", "C", "D", "E", "F", "M", "X", "Y"]):
        assert calc(f"{cell}", memory=mem) == float(i + 1)


def test_rcl_expression():
    mem = {"A": 10, "B": 5, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("A/B", memory=mem) == 2.0


def test_store_then_use_in_expr():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("7 sto A", memory=mem)
    assert calc("A^2", memory=mem) == 49.0


# ── negative numbers in stat ──────────────────────────────────────────────────


def test_stat_negative_entry():
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("-5 M+", memory=mem, n=n, stat=True)
    assert n == [-5.0]


def test_stat_mixed_negative():
    n = [-5.0, 3.0, -2.0]
    assert approx(calc("sumx", n=n, stat=True), -4.0)


def test_stat_mean_negative():
    n = [-3.0, -1.0, 2.0]
    assert approx(calc("mean", n=n, stat=True), -2 / 3)


# ── sdev1 ─────────────────────────────────────────────────────────────────────


def test_stat_sdev1():
    import statistics as s

    n = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    assert approx(calc("sdev1", n=n, stat=True), s.stdev(n))


def test_stat_sdev1_two_points():
    n = [2.0, 4.0]
    assert approx(calc("sdev1", n=n, stat=True), math.sqrt(2))


# ── chained factorial ─────────────────────────────────────────────────────────


def test_double_factorial():
    # 3!! = (3!)! = 6! = 720
    assert calc("3!!") == 720.0


def test_factorial_expression():
    assert calc("(2+1)!") == 6.0


# ── ncr/npr edge cases ────────────────────────────────────────────────────────


def test_ncr_zero_zero():
    assert calc("0 ncr 0") == 1.0


def test_npr_zero_zero():
    assert calc("0 npr 0") == 1.0


def test_ncr_in_expression():
    assert calc("(5 ncr 2)+1") == 11.0


def test_npr_in_expression():
    assert calc("(5 npr 2)*2") == 40.0


# ── pi and e in expressions ───────────────────────────────────────────────────


def test_sin_pi_over_6():
    assert approx(calc("sin(pi/6)"), 0.009138395397176044)


def test_cos_pi_over_3():
    assert approx(calc("cos(pi/3)"), 0.9998329794591297)  # cos(60°) via pi


def test_e_pow():
    assert approx(calc("e^1"), math.e)


def test_log_e_pow():
    assert approx(calc("log(e^2)"), 2 * math.log10(math.e))


# ── implicit multiply with constants ─────────────────────────────────────────


def test_implicit_2pi():
    assert approx(calc("2*pi"), 2 * math.pi)


def test_implicit_3e():
    assert approx(calc("3*e"), 3 * math.e)


# ── ans after operations ──────────────────────────────────────────────────────


def test_ans_after_factorial():
    result = calc("ans!", ans=5)
    assert result == 120.0


def test_ans_in_trig():
    result = calc("sin(ans)", ans=30)
    assert approx(result, 0.5)


def test_ans_negative():
    result = calc("ans+10", ans=-5)
    assert result == 5.0


# ── stat empty list errors ────────────────────────────────────────────────────


def test_stat_mean_empty():
    with pytest.raises(Exception):
        calc("mean", n=[], stat=True)


def test_stat_sdev_empty():
    with pytest.raises(Exception):
        calc("sdev", n=[], stat=True)


# ── stat sumx2 various ────────────────────────────────────────────────────────


def test_stat_sumx2_single():
    n = [3.0]
    assert calc("sumx2", n=n, stat=True) == 9.0


def test_stat_sumx2_negative():
    n = [-3.0, -4.0]
    assert calc("sumx2", n=n, stat=True) == 25.0


# ── complex nested expressions ────────────────────────────────────────────────


def test_nested_parens_deep():
    assert calc("((2+3)*(4-1))^2") == 225.0


def test_mixed_ops_complex():
    assert approx(calc("2^3+4*5-6/2"), 25.0)


def test_trig_in_expression():
    assert approx(calc("sin(30)*2"), 1.0)


def test_log_in_expression():
    assert approx(calc("log(100)*5"), 10.0)


# ── M+ M- stat count ─────────────────────────────────────────────────────────


def test_stat_mplus_count():
    global result
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    for val in [1, 2, 3, 4, 5]:
        result = calc(f"{val} M+", memory=mem, n=n, stat=True)
    assert result == 5.0
    assert len(n) == 5


def test_stat_mminus_count():
    n = [1.0, 2.0, 3.0]
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    result = calc("M-", memory=mem, n=n, stat=True)
    assert result == 2.0
    assert len(n) == 2


# ── M+ M- comp mode ───────────────────────────────────────────────────────────


def test_comp_m_plus_accumulate():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5 M+", memory=mem)
    calc("3 M+", memory=mem)
    assert mem["M"] == 8.0


def test_comp_m_minus_subtract():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 10, "X": 0, "Y": 0}
    calc("3 M-", memory=mem)
    calc("2 M-", memory=mem)
    assert mem["M"] == 5.0


# ── scientific notation ───────────────────────────────────────────────────────


def test_x10_basic():
    assert calc("1.5 x10 3") == 1500.0


def test_x10_zero():
    assert calc("1 x10 0") == 1.0


def test_x10_negative():
    assert approx(calc("1 x10 -3"), 0.001)


def test_x10_in_expression():
    assert calc("1 x10 3 + 500") == 1500.0


def test_x10_multiply():
    assert calc("2 x10 3 * 2") == 2000.0 * 2


def test_x10_large():
    assert calc("1 x10 15") == 1e15
