import math
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokenizer import tokenize
from parser import parse
from RPN import evaluate

# ── helpers ──────────────────────────────────────────────────────────────────


def calc(expr, memory=None, ans=0, n=None, stat=False, deg=True):
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
    result = evaluate(
        parsed, memory, ans, guide=None, debug_mode=False, n=n, STAT=stat, deg=deg
    )
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


def test_large_numbers():
    assert calc("999999*999999") == 999999**2


def test_division_result_float():
    assert calc("1/3") == pytest.approx(1 / 3)


def test_zero_addition():
    assert calc("0+0") == 0.0


def test_negative_result():
    assert calc("3-10") == -7.0


def test_chained_addition():
    assert calc("1+2+3+4+5") == 15.0


def test_chained_subtraction():
    assert calc("10-1-2-3") == 4.0


def test_chained_multiplication():
    assert calc("2*3*4") == 24.0


def test_chained_division():
    assert calc("100/5/4") == 5.0


# ── operator precedence ───────────────────────────────────────────────────────


def test_precedence_add_mul():
    assert calc("2+3*4") == 14.0


def test_precedence_mul_add():
    assert calc("2*3+4") == 10.0


def test_precedence_pow():
    assert calc("2+3^2") == 11.0


def test_precedence_chain():
    assert calc("2+3*4-1") == 13.0


def test_precedence_div_before_add():
    assert calc("10+10/2") == 15.0


def test_precedence_pow_before_mul():
    assert calc("3*2^3") == 24.0


def test_precedence_complex():
    assert calc("2+3*4^2-1") == 49.0


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


def test_parens_overrides_precedence():
    assert calc("(2+3)*(4+5)") == 45.0


def test_parens_deep_nested():
    assert calc("((((2))))") == 2.0


def test_parens_with_pow():
    assert calc("(2+3)^2") == 25.0


def test_parens_in_exponent():
    assert calc("2^(3+1)") == 16.0


def test_parens_subtraction():
    assert calc("10-(2+3)") == 5.0


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


def test_unary_chain_add():
    assert calc("5+-3+2") == 4.0


def test_unary_in_parens():
    assert calc("(-5+3)") == -2.0


def test_unary_times_parens():
    assert calc("-2*(3+4)") == -14.0


def test_unary_on_pi():
    assert approx(calc("-pi"), -math.pi)


# ── trig functions (degrees) ──────────────────────────────────────────────────


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


def test_sin_0():
    assert approx(calc("sin(0)"), 0.0)


def test_cos_0():
    assert approx(calc("cos(0)"), 1.0)


def test_sin_90():
    assert approx(calc("sin(90)"), 1.0)


def test_cos_90():
    assert approx(calc("cos(90)"), 0.0)


def test_sin_270():
    assert approx(calc("sin(270)"), -1.0)


def test_tan_0():
    assert approx(calc("tan(0)"), 0.0)


def test_asin_0():
    assert approx(calc("asin(0)"), 0.0)


def test_acos_1():
    assert approx(calc("acos(1)"), 0.0)


def test_atan_0():
    assert approx(calc("atan(0)"), 0.0)


def test_sin_negative():
    assert approx(calc("sin(-30)"), -0.5)


def test_cos_negative():
    assert approx(calc("cos(-60)"), 0.5)


def test_trig_in_expression():
    assert approx(calc("sin(30)*2"), 1.0)


def test_trig_chained():
    assert approx(calc("sin(30)+cos(60)+tan(45)"), 2.0)


def test_sin_times_cos():
    assert approx(calc("sin(45)*cos(45)"), 0.5)


# ── trig functions (radians) ──────────────────────────────────────────────────


def test_sin_rad_pi_over_6():
    assert approx(calc("sin(pi/6)", deg=False), 0.5)


def test_cos_rad_pi_over_3():
    assert approx(calc("cos(pi/3)", deg=False), 0.5)


def test_tan_rad_pi_over_4():
    assert approx(calc("tan(pi/4)", deg=False), 1.0)


def test_asin_rad():
    assert approx(calc("asin(0.5)", deg=False), math.pi / 6)


def test_acos_rad():
    assert approx(calc("acos(0.5)", deg=False), math.pi / 3)


def test_atan_rad():
    assert approx(calc("atan(1)", deg=False), math.pi / 4)


def test_sin_rad_0():
    assert approx(calc("sin(0)", deg=False), 0.0)


def test_cos_rad_0():
    assert approx(calc("cos(0)", deg=False), 1.0)


def test_sin_rad_pi():
    assert approx(calc("sin(pi)", deg=False), 0.0, tol=1e-10)


def test_cos_rad_pi():
    assert approx(calc("cos(pi)", deg=False), -1.0)


def test_sin_rad_negative():
    assert approx(calc("sin(-pi/6)", deg=False), -0.5)


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


def test_log_10():
    assert approx(calc("log(10)"), 1.0)


def test_log_1000():
    assert approx(calc("log(1000)"), 3.0)


def test_ln_e_squared():
    assert approx(calc("ln(e^2)"), 2.0)


def test_log_in_expression():
    assert approx(calc("log(100)*5"), 10.0)


def test_ln_in_expression():
    assert approx(calc("ln(e)*3"), 3.0)


def test_log_pow():
    assert approx(calc("log(10^3)"), 3.0)


# ── constants ─────────────────────────────────────────────────────────────────


def test_pi():
    assert approx(calc("pi"), math.pi)


def test_e():
    assert approx(calc("e"), math.e)


def test_pi_multiply():
    assert approx(calc("2*pi"), 2 * math.pi)


def test_e_multiply():
    assert approx(calc("3*e"), 3 * math.e)


def test_pi_squared():
    assert approx(calc("pi^2"), math.pi**2)


def test_e_squared():
    assert approx(calc("e^2"), math.e**2)


def test_pi_plus_e():
    assert approx(calc("pi+e"), math.pi + math.e)


def test_pi_times_e():
    assert approx(calc("pi*e"), math.pi * math.e)


def test_implicit_2pi():
    assert approx(calc("2*pi"), 2 * math.pi)


def test_implicit_3e():
    assert approx(calc("3*e"), 3 * math.e)


def test_pi_in_trig():
    assert approx(
        calc("sin(pi/6)"), 0.009138395397176044
    )  # sin(30 degrees expressed as pi/6 radians fed as degrees)


def test_e_pow():
    assert approx(calc("e^1"), math.e)


def test_log_e_pow():
    assert approx(calc("log(e^2)"), 2 * math.log10(math.e))


# ── factorial ─────────────────────────────────────────────────────────────────


def test_factorial_5():
    assert calc("5!") == 120.0


def test_factorial_0():
    assert calc("0!") == 1.0


def test_factorial_1():
    assert calc("1!") == 1.0


def test_factorial_in_expr():
    assert calc("5!+1") == 121.0


def test_factorial_10():
    assert calc("10!") == 3628800.0


def test_factorial_multiply():
    assert calc("5!*2") == 240.0


def test_double_factorial():
    assert calc("3!!") == 720.0


def test_factorial_expression():
    assert calc("(2+1)!") == 6.0


def test_factorial_after_parens():
    assert calc("(5-2)!") == 6.0


def test_factorial_in_division():
    assert calc("5!/4!") == 5.0


# ── combinatorics ─────────────────────────────────────────────────────────────


def test_ncr():
    assert calc("5 ncr 2") == 10.0


def test_npr():
    assert calc("5 npr 2") == 20.0


def test_ncr_zero():
    assert calc("5 ncr 0") == 1.0


def test_ncr_self():
    assert calc("5 ncr 5") == 1.0


def test_ncr_zero_zero():
    assert calc("0 ncr 0") == 1.0


def test_npr_zero_zero():
    assert calc("0 npr 0") == 1.0


def test_ncr_in_expression():
    assert calc("(5 ncr 2)+1") == 11.0


def test_npr_in_expression():
    assert calc("(5 npr 2)*2") == 40.0


def test_ncr_large():
    assert calc("10 ncr 3") == 120.0


def test_npr_large2():
    assert calc("10 npr 3") == 720.0


def test_ncr_times_2():
    assert calc("5 ncr 2 * 2") == 5


# ── memory store/recall ───────────────────────────────────────────────────────


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


def test_store_float():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("3.14 sto A", memory=mem)
    assert approx(calc("A", memory=mem), 3.14)


def test_store_expression_result():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("2+3 sto A", memory=mem)
    assert calc("A", memory=mem) == 5.0


def test_store_negative():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("-7 sto B", memory=mem)
    assert calc("B", memory=mem) == -7.0


def test_var_in_trig():
    mem = {"A": 30, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert approx(calc("sin(A)", memory=mem), 0.5)


def test_two_vars_expression():
    mem = {"A": 3, "B": 4, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert approx(calc("(A^2+B^2)^0.5", memory=mem), 5.0)


# ── M+ M- comp mode ───────────────────────────────────────────────────────────


def test_m_plus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 5, "X": 0, "Y": 0}
    calc("3 M+", memory=mem)
    assert mem["M"] == 8.0


def test_m_minus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 5, "X": 0, "Y": 0}
    calc("3 M-", memory=mem)
    assert mem["M"] == 2.0


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


def test_mplus_after_expression():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("2+3 M+", memory=mem)
    assert mem["M"] == 5.0


def test_mplus_after_trig():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30) M+", memory=mem)
    assert approx(mem["M"], 0.5)


def test_mplus_after_complex_expr():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30)*2+1 M+", memory=mem)
    assert approx(mem["M"], 2.0)


def test_mplus_after_pi():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("pi M+", memory=mem)
    assert approx(mem["M"], math.pi)


def test_mplus_expression_with_pi():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30)*7-pi M+", memory=mem)
    expected = math.sin(math.radians(30)) * 7 - math.pi
    assert approx(mem["M"], expected)


def test_mplus_negative_result():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 5, "X": 0, "Y": 0}
    calc("-3 M+", memory=mem)
    assert mem["M"] == 2.0


def test_mminus_goes_negative():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 2, "X": 0, "Y": 0}
    calc("5 M-", memory=mem)
    assert mem["M"] == -3.0


# ── ans ───────────────────────────────────────────────────────────────────────


def test_ans():
    result = calc("ans+1", ans=5)
    assert result == 6.0


def test_ans_in_expression():
    result = calc("ans*2+1", ans=3)
    assert result == 7.0


def test_ans_after_factorial():
    result = calc("ans!", ans=5)
    assert result == 120.0


def test_ans_in_trig():
    result = calc("sin(ans)", ans=30)
    assert approx(result, 0.5)


def test_ans_negative():
    result = calc("ans+10", ans=-5)
    assert result == 5.0


def test_ans_zero():
    result = calc("ans+5", ans=0)
    assert result == 5.0


def test_ans_in_pow():
    result = calc("ans^2", ans=4)
    assert result == 16.0


def test_ans_in_log2():
    result = calc("log(ans)", ans=100)
    assert approx(result, 2.0)


def test_ans_chained():
    result = calc("ans*ans", ans=5)
    assert result == 25.0


def test_ans_in_ncr2():
    result = calc("ans ncr 2", ans=5)
    assert result == 10.0


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


def test_stat_sdev1():
    import statistics as s

    n = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    assert approx(calc("sdev1", n=n, stat=True), s.stdev(n))


def test_stat_sdev1_two_points():
    n = [2.0, 4.0]
    assert approx(calc("sdev1", n=n, stat=True), math.sqrt(2))


def test_stat_n_empty():
    n = []
    assert calc("n", n=n, stat=True) == 0.0


def test_stat_sumx_single():
    n = [7.0]
    assert calc("sumx", n=n, stat=True) == 7.0


def test_stat_sumx2_single():
    n = [3.0]
    assert calc("sumx2", n=n, stat=True) == 9.0


def test_stat_sumx2_negative():
    n = [-3.0, -4.0]
    assert calc("sumx2", n=n, stat=True) == 25.0


def test_stat_mean_negative():
    n = [-3.0, -1.0, 2.0]
    assert approx(calc("mean", n=n, stat=True), -2 / 3)


def test_stat_negative_entry():
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("-5 M+", memory=mem, n=n, stat=True)
    assert n == [-5.0]


def test_stat_mixed_negative():
    n = [-5.0, 3.0, -2.0]
    assert approx(calc("sumx", n=n, stat=True), -4.0)


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


def test_stat_mplus_count():
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    result = None
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


def test_stat_mean_single():
    n = [42.0]
    assert approx(calc("mean", n=n, stat=True), 42.0)


def test_stat_sumx_large():
    n = list(range(1, 101))
    assert calc("sumx", n=n, stat=True) == 5050.0


# ── stat error cases ──────────────────────────────────────────────────────────


def test_stat_mean_empty():
    with pytest.raises(Exception):
        calc("mean", n=[], stat=True)


def test_stat_sdev_empty():
    with pytest.raises(Exception):
        calc("sdev", n=[], stat=True)


def test_stat_func_in_comp_mode():
    with pytest.raises(SyntaxError):
        calc("mean", n=[1.0, 2.0], stat=False)


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


def test_x10_with_float_base():
    assert approx(calc("2.5 x10 2"), 250.0)


def test_x10_negative_large():
    assert approx(calc("1 x10 -6"), 1e-6)


# ── implicit multiplication ───────────────────────────────────────────────────


def test_implicit_number_paren():
    assert calc("2(3+4)") == 14.0


def test_implicit_pi():
    assert approx(calc("2pi"), 2 * math.pi)


def test_implicit_e():
    assert approx(calc("2e"), 2 * math.e)


def test_implicit_var():
    mem = {"A": 5, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("2A", memory=mem) == 10.0


def test_implicit_pi_squared():
    assert approx(calc("pi^2"), math.pi**2)


def test_implicit_paren_paren():
    assert calc("(2+3)(4+5)") == 45.0


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


def test_log_zero():
    with pytest.raises(ValueError):
        calc("log(0)")


def test_ln_zero():
    with pytest.raises(ValueError):
        calc("ln(0)")


def test_asin_gt_1():
    with pytest.raises(ValueError):
        calc("asin(1.5)")


def test_acos_lt_neg1():
    with pytest.raises(ValueError):
        calc("acos(-2)")


def test_tan_270():
    with pytest.raises(ValueError):
        calc("tan(270)")


def test_cos_no_parens():
    with pytest.raises(SyntaxError):
        calc("cos90")


def test_log_no_parens():
    with pytest.raises(SyntaxError):
        calc("log100")


# ── complex nested expressions ────────────────────────────────────────────────


def test_nested_parens_deep():
    assert calc("((2+3)*(4-1))^2") == 225.0


def test_mixed_ops_complex():
    assert approx(calc("2^3+4*5-6/2"), 25.0)


def test_trig_pow_expression():
    assert approx(calc("sin(30)^2+cos(30)^2"), 1.0)


def test_log_trig():
    assert approx(calc("log(sin(30)*200)"), math.log10(100))


def test_factorial_ncr():
    assert calc("5!/3!") == 20.0


def test_nested_trig():
    assert approx(calc("sin(asin(0.5))"), 0.5)


def test_nested_log():
    assert approx(calc("log(10^log(100))"), 2.0)


def test_complex_memory():
    mem = {"A": 3, "B": 4, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert approx(
        calc("sin(A*10)*B+log(100)", memory=mem), math.sin(math.radians(30)) * 4 + 2
    )


def test_ans_in_complex_expr():
    assert approx(calc("sin(ans)*2+log(100)", ans=30), 3.0)


def test_pi_e_combined():
    assert approx(calc("pi/e"), math.pi / math.e)


def test_double_trig():
    assert approx(calc("sin(30)+cos(60)"), 1.0)


def test_pow_chain():
    assert calc("2^2^2") == 16.0  # left associative: (2^2)^2


def test_expression_with_all_ops():
    assert approx(calc("2+3*4-6/2+1^5"), 12.0)


# ── arithmetic edge cases ─────────────────────────────────────────────────────


def test_zero_times_anything():
    assert calc("0*999999") == 0.0


def test_zero_pow_zero():
    assert calc("0^0") == 1.0


def test_one_pow_large():
    assert calc("1^9999") == 1.0


def test_negative_pow_even():
    assert calc("(-2)^2") == 4.0


def test_negative_pow_odd():
    assert calc("(-2)^3") == -8.0


def test_large_pow():
    assert calc("2^32") == 4294967296.0


def test_fraction_plus_fraction():
    assert approx(calc("1/3+1/6"), 0.5)


def test_multiply_by_zero():
    assert calc("12345*0") == 0.0


def test_divide_by_one():
    assert calc("999/1") == 999.0


def test_subtract_self():
    assert calc("pi-pi") == 0.0


def test_add_inverse():
    assert approx(calc("e+-e"), 0.0)


def test_double_negative_in_expr():
    assert calc("10--5") == 15.0


def test_triple_negative():
    assert calc("---3") == -3.0


def test_large_addition():
    assert calc("999999999+1") == 1000000000.0


def test_very_small_division():
    assert approx(calc("1/1000000"), 1e-6)


def test_power_of_fraction():
    assert approx(calc("4^0.5"), 2.0)


def test_power_of_fraction_2():
    assert approx(calc("27^(1/3)"), 3.0)


def test_negative_base_even_pow():
    assert calc("(-3)^2") == 9.0


def test_negative_base_odd_pow():
    assert calc("(-3)^3") == -27.0


def test_chained_pow():
    assert calc("2^3^1") == 8.0


def test_subtraction_negative_result():
    assert calc("3-100") == -97.0


def test_multiply_fractions():
    assert approx(calc("0.1*0.2"), 0.02)


def test_division_less_than_one():
    assert approx(calc("1/4"), 0.25)


def test_zero_divided_by_nonzero():
    assert calc("0/5") == 0.0


def test_negative_divided_by_negative():
    assert calc("-10/-2") == 5.0


def test_positive_divided_by_negative():
    assert calc("10/-2") == -5.0


# ── trig identities ───────────────────────────────────────────────────────────


def test_pythagorean_identity_30():
    assert approx(calc("sin(30)^2+cos(30)^2"), 1.0)


def test_pythagorean_identity_45():
    assert approx(calc("sin(45)^2+cos(45)^2"), 1.0)


def test_pythagorean_identity_60():
    assert approx(calc("sin(60)^2+cos(60)^2"), 1.0)


def test_tan_identity():
    assert approx(calc("sin(45)/cos(45)"), calc("tan(45)"))


def test_sin_double_angle():
    assert approx(calc("2*sin(30)*cos(30)"), calc("sin(60)"))


def test_asin_acos_complement():
    assert approx(calc("asin(0.5)+acos(0.5)"), 90.0)


def test_sin_360():
    assert approx(calc("sin(360)"), 0.0, tol=1e-9)


def test_cos_360():
    assert approx(calc("cos(360)"), 1.0)


# def test_sin_negative_angle():
#     assert approx(calc("sin(-45)"), -calc("sin(45)"))


def test_cos_negative_angle():
    assert approx(calc("cos(-45)"), calc("cos(45)"))


def test_tan_negative_angle():
    assert approx(calc("tan(-45)"), -1.0)


def test_sin_large_angle():
    assert approx(calc("sin(720)"), 0.0, tol=1e-9)


def test_cos_large_angle():
    assert approx(calc("cos(720)"), 1.0)


def test_atan_large():
    assert approx(calc("atan(1000000)"), 90.0, tol=0.001)


def test_asin_minus_1():
    assert approx(calc("asin(-1)"), -90.0)


def test_acos_minus_1():
    assert approx(calc("acos(-1)"), 180.0)


def test_atan_minus_1():
    assert approx(calc("atan(-1)"), -45.0)


def test_sin_in_fraction():
    assert approx(calc("sin(30)/sin(90)"), 0.5)


# ── trig RAD mode identities ──────────────────────────────────────────────────


def test_rad_pythagorean_identity():
    assert approx(calc("sin(pi/4)^2+cos(pi/4)^2", deg=False), 1.0)


def test_rad_tan_identity():
    assert approx(calc("sin(pi/4)/cos(pi/4)", deg=False), 1.0)


def test_rad_asin_acos_complement():
    assert approx(calc("asin(0.5)+acos(0.5)", deg=False), math.pi / 2)


def test_rad_sin_negative():
    assert approx(calc("sin(-pi/6)", deg=False), -0.5)


def test_rad_cos_2pi():
    assert approx(calc("cos(2*pi)", deg=False), 1.0)


def test_rad_sin_2pi():
    assert approx(calc("sin(2*pi)", deg=False), 0.0, tol=1e-9)


def test_rad_atan_returns_radians():
    assert approx(calc("atan(1)", deg=False), math.pi / 4)


def test_rad_asin_returns_radians():
    assert approx(calc("asin(1)", deg=False), math.pi / 2)


def test_rad_acos_returns_radians():
    assert approx(calc("acos(0)", deg=False), math.pi / 2)


# ── logarithm identities ──────────────────────────────────────────────────────


def test_log_power_rule():
    assert approx(calc("log(2^10)"), 10 * math.log10(2))


def test_ln_power_rule():
    assert approx(calc("ln(e^5)"), 5.0)


def test_log_quotient():
    assert approx(calc("log(100/10)"), 1.0)


def test_ln_product():
    assert approx(calc("ln(e*e)"), 2.0)


def test_log_reciprocal():
    assert approx(calc("log(1/10)"), -1.0)


def test_ln_reciprocal():
    assert approx(calc("ln(1/e)"), -1.0)


def test_log_sqrt():
    assert approx(calc("log(10^0.5)"), 0.5)


def test_ln_sqrt_e():
    assert approx(calc("ln(e^0.5)"), 0.5)


def test_log_large():
    assert approx(calc("log(1000000)"), 6.0)


def test_ln_large():
    assert approx(calc("ln(e^10)"), 10.0)


# ── factorial edge cases ──────────────────────────────────────────────────────


def test_factorial_2():
    assert calc("2!") == 2.0


def test_factorial_3():
    assert calc("3!") == 6.0


def test_factorial_7():
    assert calc("7!") == 5040.0


def test_factorial_in_trig():
    assert approx(calc("sin(3!)"), calc("sin(6)"))


def test_factorial_in_log():
    assert approx(calc("log(5!)"), math.log10(120))


def test_factorial_divided():
    assert calc("6!/5!") == 6.0


def test_factorial_squared():
    assert calc("3!^2") == 36.0


def test_factorial_in_ncr():
    assert calc("(4!) ncr 2") == calc("24 ncr 2")


# ── combinatorics edge cases ──────────────────────────────────────────────────


def test_ncr_1():
    assert calc("10 ncr 1") == 10.0


def test_ncr_n_minus_1():
    assert calc("10 ncr 9") == 10.0


def test_npr_1():
    assert calc("10 npr 1") == 10.0


def test_ncr_symmetry():
    assert calc("10 ncr 3") == calc("10 ncr 7")


def test_npr_large():
    assert calc("8 npr 3") == 336.0


def test_ncr_large_2():
    assert calc("20 ncr 10") == 184756.0


def test_ncr_in_sum():
    assert calc("(5 ncr 2)+(5 ncr 3)") == calc("6 ncr 3")


def test_npr_equals_factorial_ratio():
    assert approx(calc("5 npr 3"), calc("5!/2!"))


# ── memory advanced ───────────────────────────────────────────────────────────


def test_store_pi():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("pi sto A", memory=mem)
    assert approx(mem["A"], math.pi)


def test_store_trig_result():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30) sto A", memory=mem)
    assert approx(mem["A"], 0.5)


def test_store_overwrites():
    mem = {"A": 99, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("7 sto A", memory=mem)
    assert mem["A"] == 7.0


def test_var_in_factorial():
    mem = {"A": 5, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("A!", memory=mem) == 120.0


def test_var_in_ncr():
    mem = {"A": 5, "B": 2, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("A ncr B", memory=mem) == 10.0


def test_var_in_log():
    mem = {"A": 100, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert approx(calc("log(A)", memory=mem), 2.0)


def test_mplus_multiple_accumulate():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    for v in [1, 2, 3, 4, 5]:
        calc(f"{v} M+", memory=mem)
    assert mem["M"] == 15.0


def test_mplus_then_mminus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("10 M+", memory=mem)
    calc("3 M-", memory=mem)
    assert mem["M"] == 7.0


def test_store_recall_chain():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5 sto A", memory=mem)
    calc("A sto B", memory=mem)
    assert mem["B"] == 5.0


def test_store_complex_expr():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("2^8 sto X", memory=mem)
    assert mem["X"] == 256.0


def test_mplus_trig_accumulate():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30) M+", memory=mem)
    calc("sin(30) M+", memory=mem)
    assert approx(mem["M"], 1.0)


# ── ans advanced ──────────────────────────────────────────────────────────────


def test_ans_times_ans():
    assert calc("ans*ans", ans=7) == 49.0


def test_ans_in_factorial():
    assert calc("ans!", ans=6) == 720.0


def test_ans_in_ncr():
    assert calc("ans ncr 3", ans=6) == 20.0


def test_ans_in_complex():
    assert approx(calc("sin(ans)+cos(ans)", ans=45), math.sqrt(2))


def test_ans_negative_factorial():
    with pytest.raises(Exception):
        calc("ans!", ans=-1)


def test_ans_pi():
    assert approx(calc("ans*pi", ans=2), 2 * math.pi)


def test_ans_stored():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("ans sto A", memory=mem, ans=42)
    assert mem["A"] == 42.0


def test_ans_in_log():
    assert approx(calc("log(ans)", ans=1000), 3.0)


def test_ans_subtracted():
    assert calc("100-ans", ans=37) == 63.0


# ── stat advanced ─────────────────────────────────────────────────────────────


def test_stat_sumx_floats():
    n = [1.1, 2.2, 3.3]
    assert approx(calc("sumx", n=n, stat=True), 6.6)


def test_stat_sumx2_floats():
    n = [1.0, 2.0, 3.0]
    assert approx(calc("sumx2", n=n, stat=True), 14.0)


def test_stat_mean_two_points():
    n = [10.0, 20.0]
    assert approx(calc("mean", n=n, stat=True), 15.0)


def test_stat_sdev_identical():
    n = [5.0, 5.0, 5.0, 5.0]
    assert approx(calc("sdev", n=n, stat=True), 0.0)


def test_stat_n_large():
    n = list(range(1, 51))
    assert calc("n", n=n, stat=True) == 50.0


def test_stat_mean_large():
    n = list(range(1, 101))
    assert approx(calc("mean", n=n, stat=True), 50.5)


def test_stat_sumx_negative_all():
    n = [-1.0, -2.0, -3.0]
    assert approx(calc("sumx", n=n, stat=True), -6.0)


def test_stat_sumx2_all_same():
    n = [3.0, 3.0, 3.0]
    assert approx(calc("sumx2", n=n, stat=True), 27.0)


def test_stat_mplus_float():
    n = []
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("3.14 M+", memory=mem, n=n, stat=True)
    assert approx(n[0], 3.14)


def test_stat_mminus_nonexistent():
    n = [1.0, 2.0, 3.0]
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("99 M-", memory=mem, n=n, stat=True)
    assert n == [1.0, 2.0, 3.0]


def test_stat_sdev1_identical():
    with pytest.raises(Exception):
        n = [5.0]
        calc("sdev1", n=n, stat=True)


def test_stat_n_after_mminus():
    n = [1.0, 2.0, 3.0]
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("M-", memory=mem, n=n, stat=True)
    assert calc("n", n=n, stat=True) == 2.0


# ── scientific notation advanced ──────────────────────────────────────────────


def test_x10_small_base():
    assert approx(calc("0.001 x10 3"), 1.0)


def test_x10_result_in_expr():
    assert approx(calc("(1 x10 3)*2"), 2000.0)


def test_x10_negative_exp_in_expr():
    assert approx(calc("1 x10 -2 + 0.5"), 0.51)


def test_x10_with_pi():
    assert approx(calc("pi x10 2"), math.pi * 100)


# ── implicit multiply advanced ────────────────────────────────────────────────


def test_implicit_pi_in_trig():
    assert approx(calc("sin(2pi)", deg=False), 0.0, tol=1e-9)


def test_implicit_2_e_pow():
    assert approx(calc("2e^0"), 2.0)


def test_implicit_var_trig():
    mem = {"A": 45, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert approx(calc("sin(A)", memory=mem), calc("sin(45)"))


def test_implicit_paren_var():
    mem = {"A": 3, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    assert calc("(2+3)A", memory=mem) == 15.0


# ── complex combined expressions ──────────────────────────────────────────────


def test_sin_squared_plus_cos_squared_pi():
    assert approx(calc("sin(pi/4)^2+cos(pi/4)^2"), 1.0)


def test_log_of_trig():
    assert approx(calc("log(cos(0)*100)"), 2.0)


def test_trig_of_factorial():
    assert approx(calc("cos(3!)"), calc("cos(6)"))


def test_ncr_in_trig():
    assert approx(calc("sin((5 ncr 2)*3)"), calc("sin(30)"))


def test_ans_mplus():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("ans M+", memory=mem, ans=10)
    assert mem["M"] == 10.0


def test_var_mplus():
    mem = {"A": 5, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 10, "X": 0, "Y": 0}
    calc("A M+", memory=mem)
    assert mem["M"] == 15.0


def test_factorial_then_store():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("5! sto A", memory=mem)
    assert mem["A"] == 120.0


def test_trig_stored_used():
    mem = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    calc("sin(30) sto A", memory=mem)
    calc("A sto B", memory=mem)
    assert approx(mem["B"], 0.5)


def test_complex_with_ans_and_memory():
    mem = {"A": 3, "B": 4, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
    result = calc("(A^2+B^2)^0.5+ans", memory=mem, ans=5)
    assert approx(result, 10.0)


def test_deeply_nested_trig():
    assert approx(calc("sin(asin(cos(acos(0.5))))"), 0.5)


def test_log_then_pow():
    assert approx(calc("10^log(100)"), 100.0)


def test_e_ln_identity():
    assert approx(calc("e^ln(5)"), 5.0)


def test_sum_of_ncr():
    # C(4,0)+C(4,1)+C(4,2)+C(4,3)+C(4,4) = 16 = 2^4
    assert calc("(4 ncr 0)+(4 ncr 1)+(4 ncr 2)+(4 ncr 3)+(4 ncr 4)") == 16.0


def test_pi_precision():
    assert approx(calc("355/113"), math.pi, tol=0.001)


def test_golden_ratio():
    assert approx(calc("(1+5^0.5)/2"), (1 + math.sqrt(5)) / 2)


def test_euler_identity_cos():
    assert approx(calc("cos(180)"), -1.0)


def test_euler_identity_sin():
    assert approx(calc("sin(180)"), 0.0, tol=1e-10)
