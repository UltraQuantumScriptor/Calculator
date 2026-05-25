import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokenizer import tokenize
from parser import parse
from RPN import evaluate


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


# try:
#     calc("(-8)^(1/3)")
# except Exception as e:
#     print(type(e), e)
print(calc("(-8)^(1/3)"))
