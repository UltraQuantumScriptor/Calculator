def parse(tokens):
    output = []
    ops = []

    prec = {
        "PLUS": 1,
        "MINUS": 1,
        "NCR": 2,
        "NPR": 2,
        "MULTIPLY": 3,
        "DIVIDE": 3,
        "POW": 4,
        "UMINUS": 5,
    }

    for token in tokens:
        ttype, value = token

        if ttype == "NUMBER":
            output.append((ttype, value))

        elif ttype in prec:
            while ops:
                top = ops[-1]

                if (
                    top in prec
                    and prec[top] >= prec[ttype]
                    and ttype not in ("POW", "UMINUS")
                ):
                    output.append(("OP", ops.pop()))
                else:
                    break

            ops.append(ttype)

        elif ttype == "LPAREN":
            ops.append(ttype)

        elif ttype == "RPAREN":
            while ops and ops[-1] != "LPAREN":
                output.append(("OP", ops.pop()))
            ops.pop()  # remove LPAREN

        elif ttype == "FACT":
            output.append(("FACT", value))

        elif ttype == "FUNC":
            output.append(("FUNC", value))

        elif ttype == "VAR":
            output.append(("VAR", value))

        elif ttype in ("STORE", "RECALL"):
            output.append((ttype, value))

    while ops:
        output.append(("OP", ops.pop()))

    return output
