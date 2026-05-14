def evaluate(rpn):
    stack = []
    for token in rpn:
        ttype, value = token

        if ttype == "NUMBER":
            stack.append(value)

        elif ttype == "OP":
            if len(stack) < 2:
                raise ValueError(f"Invalid RPN: stack too small at {token}.")
            b = stack.pop()
            a = stack.pop()

            if value == "PLUS":
                result = a + b
                stack.append(result)

            if value == "MINUS":
                result = a - b
                stack.append(result)

            if value == "MULTIPLY":
                result = a * b
                stack.append(result)

            if value == "DIVIDE":
                result = a / b
                stack.append(result)

            if value == "POW":
                result = a**b
                stack.append(result)
    return stack
