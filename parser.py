# def is_command(equation, i):
#     while i < len(equation) and equation[i].isspace():
#         i += 1
#     if equation[i] == "M" and i + 1 < len(equation) and equation[i + 1] in ("+", "-"):
#         return True
#     word = ""
#     j = i
#     while j < len(equation) and (
#         equation[j].isalpha() and equation[j].islower() or equation[j].isdigit()
#     ):
#         word += equation[j]
#         j += 1
#     return word in ("sto", "rcl", "ncr", "npr", "ans", "x10")


import math as m


def insert_implicit_multiplication(tokens):
    result = []

    for i in range(len(tokens)):
        a = tokens[i]
        result.append(a)

        if i + 1 >= len(tokens):
            continue

        b = tokens[i + 1]

        a_type = a[0]
        b_type = b[0]

        if a_type in ("NUMBER", "CONSTANT", "RPAREN", "VAR", "FACT") and b_type in (
            "CONSTANT",
            "FUNC",
            "LPAREN",
            "VAR",
        ):
            result.append(("MULTIPLY", "*"))

    return result


def parse(tokens):
    tokens = insert_implicit_multiplication(tokens)
    output = []
    ops = []

    prec = {
        "SEMICOL": 0.5,
        "PLUS": 1,
        "MINUS": 1,
        "NCR": 2,
        "NPR": 2,
        "MULTIPLY": 3,
        "DIVIDE": 3,
        "POW": 4,
        "UMINUS": 6,
    }

    for token in tokens:
        ttype, value = token

        if ops and ops[-1][0] == "FUNC" and ttype != "LPAREN":
            raise SyntaxError("Functions MUST have parenthesis")

        if ttype == "NUMBER":
            output.append((ttype, value))

        elif ttype == "X10":
            mantissa = output.pop()
            if mantissa[0] == "CONSTANT":
                val = m.pi if mantissa[1] == "pi" else m.e
            else:
                val = mantissa[1]
            output.append(("NUMBER", val * (10**value)))

        elif ttype in prec:
            while ops:
                top = ops[-1]
                top_ttype = top[0] if isinstance(top, tuple) else top

                if (
                    top_ttype in prec
                    and prec[top_ttype] >= prec[ttype]
                    and ttype not in ("POW", "UMINUS")
                    and top_ttype != "UMINUS"
                    and top_ttype != "FUNC"
                ):
                    output.append(
                        ops.pop() if isinstance(top, tuple) else ("OP", ops.pop())
                    )
                else:
                    break

            ops.append(ttype)

        elif ttype == "CONSTANT":
            output.append(("NUMBER", m.pi) if value == "pi" else ("NUMBER", m.e))

        elif ttype == "LPAREN":
            # ops.append(("OP", ttype))
            ops.append(ttype)

        elif ttype == "RPAREN":
            while ops and ops[-1] != "LPAREN":
                top = ops.pop()
                if isinstance(top, tuple):
                    output.append(top)
                else:
                    output.append(("OP", top))
            ops.pop()  # remove LPAREN
            if ops and isinstance(ops[-1], tuple) and ops[-1][0] == "FUNC":
                output.append(ops.pop())

        elif ttype == "FACT":
            output.append(("FACT", value))

        elif ttype == "FUNC":
            ops.append(("FUNC", value))

        elif ttype == "STAT_FUNC":
            output.append(("STAT_FUNC", value))

        elif ttype == "ANS":
            output.append(("ANS", "ans"))

        elif ttype == "VAR":
            output.append(("VAR", value))

        # elif ttype in ("STORE", "RECALL"):
        #     output.append((ttype, value))

        elif ttype in ("MPLUS", "MMINUS", "STORE", "RECALL"):
            while ops:
                top = ops.pop()
                if isinstance(top, tuple):
                    output.append(top)
                else:
                    output.append(("OP", top))
            output.append((ttype, value))

    while ops:
        top = ops.pop()
        if isinstance(top, tuple):
            output.append(top)
        else:
            output.append(("OP", top))

    return output
