import math
import sys
import os
import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from hypothesis import settings

settings.register_profile(
    "thorough", max_examples=1000, suppress_health_check=[HealthCheck.too_slow]
)
settings.load_profile("thorough")


def calc(expr, deg=True, memory=None):
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
    tokens = tokenize(expr)
    parsed = parse(tokens)
    result = evaluate(parsed, memory, 0, guide=None, debug_mode=False, deg=deg)
    return result[0] if result else None


# ── strategies ────────────────────────────────────────────────────────────────

safe_angle = st.floats(
    min_value=-360, max_value=360, allow_nan=False, allow_infinity=False
).filter(lambda x: abs(x % 180 - 90) > 0.1)

positive = st.floats(
    min_value=0.001, max_value=1e6, allow_nan=False, allow_infinity=False
)

any_float = st.floats(
    min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False
)

unit = st.floats(
    min_value=-0.9999, max_value=0.9999, allow_nan=False, allow_infinity=False
)

rad_range = st.floats(
    min_value=-1.5, max_value=1.5, allow_nan=False, allow_infinity=False
)

small_positive = st.floats(
    min_value=0.001, max_value=100, allow_nan=False, allow_infinity=False
)

small_int = st.integers(min_value=0, max_value=12)

nonzero = st.floats(
    min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False
).filter(lambda x: abs(x) > 0.001)


# ── trig identities ───────────────────────────────────────────────────────────


@given(safe_angle)
def test_pythagorean_identity_any_angle(angle):
    result = calc(f"sin({angle})^2+cos({angle})^2")
    assert abs(result - 1.0) < 1e-6


@given(safe_angle)
def test_tan_identity_any_angle(angle):
    c = calc(f"cos({angle})")
    assume(abs(c) > 1e-6)
    assert abs(calc(f"sin({angle})/cos({angle})") - calc(f"tan({angle})")) < 1e-6


@given(safe_angle)
def test_sin_negative_angle(angle):
    assert abs(calc(f"sin({angle})") + calc(f"sin(-{angle})")) < 1e-6


@given(safe_angle)
def test_cos_even_function(angle):
    assert abs(calc(f"cos({angle})") - calc(f"cos(-{angle})")) < 1e-6


@given(safe_angle)
def test_sin_range(angle):
    result = calc(f"sin({angle})")
    assert -1.0 - 1e-9 <= result <= 1.0 + 1e-9


@given(safe_angle)
def test_cos_range(angle):
    result = calc(f"cos({angle})")
    assert -1.0 - 1e-9 <= result <= 1.0 + 1e-9


@given(safe_angle)
def test_sin_periodicity(angle):
    assert abs(calc(f"sin({angle})") - calc(f"sin({angle}+360)")) < 1e-6


@given(safe_angle)
def test_cos_periodicity(angle):
    assert abs(calc(f"cos({angle})") - calc(f"cos({angle}+360)")) < 1e-6


@given(safe_angle)
def test_sin_cos_shift(angle):
    # sin(x + 90) = cos(x)
    assume(abs((angle + 90) % 180 - 90) > 0.1)
    assert abs(calc(f"sin({angle}+90)") - calc(f"cos({angle})")) < 1e-6


# ── inverse trig identities ───────────────────────────────────────────────────


@given(unit)
def test_asin_sin_identity(x):
    assert abs(calc(f"sin(asin({x}))") - x) < 1e-6


@given(unit)
def test_acos_cos_identity(x):
    assert abs(calc(f"cos(acos({x}))") - x) < 1e-6


@given(rad_range)
def test_atan_tan_identity(x):
    # only valid for x in (-pi/2, pi/2)
    assume(abs(x) < 1.5707)
    assert abs(calc(f"atan(tan({x}))", deg=False) - x) < 1e-6


@given(unit)
def test_asin_acos_complement(x):
    # asin(x) + acos(x) = 90 in degrees
    assert abs(calc(f"asin({x})+acos({x})") - 90.0) < 1e-6


@given(unit)
def test_asin_range(x):
    result = calc(f"asin({x})")
    assert -90.0 - 1e-9 <= result <= 90.0 + 1e-9


@given(unit)
def test_acos_range(x):
    result = calc(f"acos({x})")
    assert 0.0 - 1e-9 <= result <= 180.0 + 1e-9


@given(any_float)
def test_atan_range(x):
    result = calc(f"atan({x})")
    assert -90.0 - 1e-9 <= result <= 90.0 + 1e-9


# ── RAD mode trig ─────────────────────────────────────────────────────────────


@given(rad_range)
def test_rad_pythagorean_identity(angle):
    result = calc(f"sin({angle})^2+cos({angle})^2", deg=False)
    assert abs(result - 1.0) < 1e-6


@given(unit)
def test_rad_asin_acos_complement(x):
    assert abs(calc(f"asin({x})+acos({x})", deg=False) - math.pi / 2) < 1e-6


@given(rad_range)
def test_rad_sin_range(angle):
    result = calc(f"sin({angle})", deg=False)
    assert -1.0 - 1e-9 <= result <= 1.0 + 1e-9


# ── logarithm identities ──────────────────────────────────────────────────────


@given(positive)
def test_log_inverse(x):
    assert abs(calc(f"10^log({x})") - x) < 1e-4


@given(positive)
def test_ln_inverse(x):
    assert abs(calc(f"e^ln({x})") - x) < 1e-4


@given(positive)
def test_log_power_rule(x):
    assert abs(calc(f"log({x}^2)") - 2 * calc(f"log({x})")) < 1e-6


@given(positive)
def test_ln_power_rule(x):
    assert abs(calc(f"ln({x}^2)") - 2 * calc(f"ln({x})")) < 1e-6


@given(positive, positive)
def test_log_product_rule(a, b):
    assume(not math.isinf(a * b) and a * b > 0)
    assert abs(calc(f"log({a})+log({b})") - calc(f"log({a*b})")) < 1e-4


@given(positive, positive)
def test_ln_product_rule(a, b):
    assume(not math.isinf(a * b) and a * b > 0)
    assert abs(calc(f"ln({a})+ln({b})") - calc(f"ln({a*b})")) < 1e-4


@given(positive, positive)
def test_log_quotient_rule(a, b):
    assert abs(calc(f"log({a})-log({b})") - calc(f"log({a}/{b})")) < 1e-4


@given(positive, positive)
def test_ln_quotient_rule(a, b):
    assert abs(calc(f"ln({a})-ln({b})") - calc(f"ln({a}/{b})")) < 1e-4


@given(positive)
def test_log_always_defined(x):
    result = calc(f"log({x})")
    assert not math.isnan(result) and not math.isinf(result)


@given(positive)
def test_ln_always_defined(x):
    result = calc(f"ln({x})")
    assert not math.isnan(result) and not math.isinf(result)


# ── arithmetic properties ─────────────────────────────────────────────────────


@given(any_float, any_float)
def test_addition_commutative(a, b):
    assert abs(calc(f"{a}+{b}") - calc(f"{b}+{a}")) < 1e-9


@given(any_float, any_float)
def test_multiplication_commutative(a, b):
    assert abs(calc(f"{a}*{b}") - calc(f"{b}*{a}")) < 1e-9


@given(any_float, any_float, any_float)
def test_addition_associative(a, b, c):
    assert abs(calc(f"({a}+{b})+{c}") - calc(f"{a}+({b}+{c})")) < 1e-6


@given(any_float)
def test_add_zero_identity(x):
    assert abs(calc(f"{x}+0") - x) < 1e-9


@given(any_float)
def test_multiply_one_identity(x):
    assert abs(calc(f"{x}*1") - x) < 1e-9


@given(any_float)
def test_multiply_zero(x):
    assert calc(f"{x}*0") == 0.0


@given(nonzero)
def test_divide_self(x):
    assert abs(calc(f"{x}/{x}") - 1.0) < 1e-9


@given(any_float)
def test_subtract_self(x):
    assert abs(calc(f"{x}-{x}")) < 1e-9


@given(nonzero)
def test_reciprocal(x):
    assert abs(calc(f"{x}*(1/{x})") - 1.0) < 1e-6


@given(any_float, any_float)
def test_subtraction_antisymmetric(a, b):
    assert abs(calc(f"{a}-{b}") + calc(f"{b}-{a}")) < 1e-9


@given(small_positive)
def test_sqrt_squared(x):
    assert abs(calc(f"({x}^0.5)^2") - x) < 1e-4


@given(small_positive)
def test_square_sqrt(x):
    assert abs(calc(f"({x}^2)^0.5") - x) < 1e-4


@given(any_float)
def test_double_negation(x):
    assert abs(calc(f"--{x}") - x) < 1e-9


@given(
    x=small_positive,
    a=st.integers(min_value=1, max_value=5),
    b=st.integers(min_value=1, max_value=5),
)
def test_power_product_rule(x, a, b):
    assume(not math.isinf(x ** (a + b)))
    a_val = calc(f"{x}^{a}*{x}^{b}")
    b_val = calc(f"{x}^{a+b}")
    assert abs(a_val - b_val) / max(abs(b_val), 1) < 1e-9


@given(
    x=small_positive,
    a=st.integers(min_value=1, max_value=5),
    b=st.integers(min_value=1, max_value=5),
)
def test_power_chain_rule(x, a, b):
    assume(not math.isinf(x ** (a * b)))
    a_val = calc(f"({x}^{a})^{b}")
    b_val = calc(f"{x}^{a*b}")
    assert abs(a_val - b_val) / max(abs(b_val), 1) < 1e-9


# ── factorial properties ──────────────────────────────────────────────────────


@given(small_int)
def test_factorial_recursive(n):
    if n == 0:
        assert calc(f"{n}!") == 1.0
    else:
        assert abs(calc(f"{n}!") - n * calc(f"{n-1}!")) < 1e-6


@given(small_int)
def test_factorial_positive(n):
    assert calc(f"{n}!") > 0


@given(st.integers(min_value=1, max_value=12))
def test_factorial_ratio(n):
    # n! / (n-1)! = n
    assert abs(calc(f"{n}!/{n-1}!") - n) < 1e-6


# ── combinatorics properties ──────────────────────────────────────────────────


@given(st.integers(min_value=0, max_value=20), st.integers(min_value=0, max_value=20))
def test_ncr_symmetry(n, k):
    assume(k <= n)
    assert calc(f"{n} ncr {k}") == calc(f"{n} ncr {n-k}")


@given(st.integers(min_value=0, max_value=20))
def test_ncr_zero(n):
    assert calc(f"{n} ncr 0") == 1.0


@given(st.integers(min_value=0, max_value=20))
def test_ncr_self(n):
    assert calc(f"{n} ncr {n}") == 1.0


@given(st.integers(min_value=1, max_value=20))
def test_ncr_one(n):
    assert calc(f"{n} ncr 1") == float(n)


@given(st.integers(min_value=0, max_value=15))
def test_ncr_nonnegative(n):
    for k in range(n + 1):
        assert calc(f"{n} ncr {k}") >= 0


@given(st.integers(min_value=1, max_value=10), st.integers(min_value=0, max_value=10))
def test_pascal_identity(n, k):
    assume(k < n)
    # C(n,k) + C(n,k+1) = C(n+1,k+1)
    assert abs(calc(f"({n} ncr {k})+({n} ncr {k+1})") - calc(f"{n+1} ncr {k+1}")) < 1e-6


@given(st.integers(min_value=0, max_value=15), st.integers(min_value=0, max_value=15))
def test_npr_ncr_relationship(n, k):
    assume(k <= n)
    # nPr = nCr * k!
    assert abs(calc(f"{n} npr {k}") - calc(f"({n} ncr {k})*{k}!")) < 1e-6


# ── abs properties ────────────────────────────────────────────────────────────


@given(any_float)
def test_abs_nonnegative(x):
    assert calc(f"abs({x})") >= 0


@given(any_float)
def test_abs_correct(x):
    assert abs(calc(f"abs({x})") - abs(x)) < 1e-6


@given(any_float)
def test_abs_idempotent(x):
    assert abs(calc(f"abs(abs({x}))") - calc(f"abs({x})")) < 1e-9


@given(any_float)
def test_abs_even(x):
    assert abs(calc(f"abs({x})") - calc(f"abs(-{x})")) < 1e-9


@given(any_float, any_float)
def test_abs_triangle_inequality(a, b):
    assume(not math.isinf(a + b))
    assert calc(f"abs({a}+{b})") <= calc(f"abs({a})") + calc(f"abs({b})") + 1e-9
