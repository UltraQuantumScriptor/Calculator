def tokenize(equation):
    tokens = []
    i = 0
    while i < len(equation):
        char = equation[i]

        if char.isdigit():
            num_string = ""
            while i < len(equation) and equation[i].isdigit():
                num_string += equation[i]
                i += 1

            tokens.append(("NUMBER", int(num_string)))
            continue
        elif char == "+":
            tokens.append(("PLUS", "+"))
        elif char == "-":
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
        elif char.isspace:
            pass

        else:
            raise NameError(f"Unknown character: {char}")

        i += 1
    return tokens
