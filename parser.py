def parse(tokens):
    output = []
    ops = []

    prec = {
        "PLUS": 1,
        "MINUS": 1,
        "MULTIPLY": 2,
        "DIVIDE": 2,
        "POW": 3,
    }

    for token in tokens:
        ttype, value = token

        if ttype == "NUMBER":
            output.append((ttype, value))

        elif ttype in prec:
            while ops:
                top = ops[-1]

                if top in prec and prec[top] >= prec[ttype]:
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

    while ops:
        output.append(("OP", ops.pop()))

    return output
