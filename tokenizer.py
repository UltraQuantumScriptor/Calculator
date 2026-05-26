import math as m
import re

comp_list = (
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "log",
    "abs",
    "ln",
)

stat_list = (
    "mean",
    "sumx",
    "sumx2",
    "sdev",
    "sdev1",
)


def tokenize(equation, n=[]):
    tokens = []
    NUMBER_PATTERN = r"[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?"
    i = 0
    while i < len(equation):
        match = re.match(NUMBER_PATTERN, equation[i:])
        if match:
            num = match.group(0)
            tokens.append(("NUMBER", float(num)))
            i += len(num)
            continue
        char = equation[i]

        # if char.isalpha():
        #     print(f"is_command check: '{char}' → {is_command(equation, i)}")
        # print(f"i={i} | last={tokens[-1] if tokens else None} | char='{char}'")
        # if tokens and tokens[-1][0] == "FUNC" and char != "(":
        #     raise SyntaxError("Functions MUST have parenthesis")

        if char.isdigit():
            num_string = ""
            while i < len(equation) and (equation[i].isdigit() or equation[i] == "."):
                num_string += equation[i]
                i += 1

            tokens.append(("NUMBER", float(num_string)))
            continue
        elif char == "+":
            tokens.append(("PLUS", "+"))
        elif char == "-":
            if not tokens or tokens[-1][0] in (
                "PLUS",
                "MINUS",
                "MULTIPLY",
                "DIVIDE",
                "POW",
                "LPAREN",
                "UMINUS",
                "NCR",
                "NPR",
            ):
                tokens.append(("UMINUS", "-"))
            else:
                tokens.append(("MINUS", "-"))
        elif char == "*":
            tokens.append(("MULTIPLY", "*"))
        elif char == "/":
            tokens.append(("DIVIDE", "/"))
        elif char == "^":
            tokens.append(("POW", "^"))
        elif char == "(":
            tokens.append(("LPAREN", "("))
        elif char == ")":
            tokens.append(("RPAREN", ")"))
        elif char == "!":
            tokens.append(("FACT", "!"))

        elif char.isalpha():
            func_string = ""
            while i < len(equation) and equation[i].isalpha() and equation[i].islower():
                func_string += equation[i]
                i += 1

            if i < len(equation) and equation[i].isdigit():
                if func_string + equation[i] in stat_list:
                    func_string += equation[i]
                    i += 1

            while i < len(equation) and equation[i].isspace():
                i += 1
            if func_string in comp_list:
                tokens.append(("FUNC", func_string))
                continue
            elif func_string in stat_list:
                tokens.append(("STAT_FUNC", func_string))
                continue
            elif (
                i < len(equation)
                and equation[i].isupper()
                and (func_string in ("sto", "rcl"))
            ):
                variable = equation[i]
                i += 1
                tokens.append(("STORE" if func_string == "sto" else "RECALL", variable))
            elif func_string == "ncr":
                tokens.append(("NCR", "ncr"))
            elif func_string == "npr":
                tokens.append(("NPR", "npr"))
            elif func_string == "pi":
                tokens.append(("CONSTANT", "pi"))
            elif func_string == "e":
                tokens.append(("CONSTANT", "e"))
            elif func_string == "n":
                tokens.append(("NUMBER", len(n)))
            elif func_string == "ans":
                tokens.append(("ANS", "ans"))
            elif i < len(equation) and equation[i].isupper():
                if (
                    equation[i] == "M"
                    and i + 1 < len(equation)
                    and equation[i + 1] in ("+", "-")
                    and (i + 2 >= len(equation) or equation[i + 2].isspace())
                ):
                    variable = equation[i]
                    op = equation[i + 1]
                    i += 2
                    tokens.append(("MPLUS" if op == "+" else "MMINUS", "M"))
                else:
                    variable = equation[i]
                    i += 1
                    tokens.append(("VAR", variable))
            elif (
                func_string == "x"
                and i < len(equation)
                and equation[i] == "1"
                and i + 1 < len(equation)
                and equation[i + 1] == "0"
            ):
                i += 2
                exp_string = ""
                while i < len(equation) and equation[i].isspace():
                    i += 1
                if i < len(equation) and equation[i] in ("+", "-"):
                    exp_string += equation[i]
                    i += 1
                while i < len(equation) and equation[i].isdigit():
                    exp_string += equation[i]
                    i += 1
                exp = int(exp_string) if exp_string else 0
                tokens.append(("X10", exp))
            else:
                tokens.append(("FUNC", func_string))
            continue
        elif char.isspace():
            i += 1
            continue

        else:
            raise NameError(f"Unknown character: {char}")

        i += 1

    # merge Unary Minus with the number in basic cases(e.g -5), can't handle more complex cases(e.g -(3+2) or --3)
    merged = []
    j = 0
    while j < len(tokens):
        if (
            tokens[j][0] == "UMINUS"
            and j + 1 < len(tokens)
            and tokens[j + 1][0] == "NUMBER"
        ):
            merged.append(("NUMBER", -tokens[j + 1][1]))
            j += 2
        else:
            merged.append(tokens[j])
            j += 1

    mplus = [t for t in merged if t[0] in ("MPLUS", "MMINUS", "STORE", "RECALL")]
    rest = [t for t in merged if t[0] not in ("MPLUS", "MMINUS", "STORE", "RECALL")]
    return rest + mplus
    # return merged
    # return tokens
