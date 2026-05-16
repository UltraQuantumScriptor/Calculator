def tokenize(equation):
    tokens = []
    i = 0
    while i < len(equation):
        char = equation[i]

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
                "RPAREN",
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
            if equation[i].isupper() and (
                func_string == "store" or func_string == "recall"
            ):
                variable = equation[i]
                i += 1
                tokens.append(
                    ("STORE" if func_string == "store" else "RECALL", variable)
                )
            elif equation[i].isupper():
                variable = equation[i]
                i += 1
                tokens.append(("VAR", variable))
            elif func_string == "ncr":
                tokens.append(("NCR", "ncr"))
            elif func_string == "npr":
                tokens.append(("NPR", "npr"))
            else:
                tokens.append(("FUNC", func_string))
            continue
        elif char.isspace:
            pass

        else:
            raise NameError(f"Unknown character: {char}")

        i += 1
    return tokens
