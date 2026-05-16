import math as m


def evaluate(rpn, memory, ans):
    stack = []

    func_map = {
        "sin": lambda x: m.sin(m.radians(x)),
        "cos": lambda x: m.cos(m.radians(x)),
        "tan": lambda x: m.tan(m.radians(x)),
        "asin": lambda x: m.degrees(m.asin(x)),
        "acos": lambda x: m.degrees(m.acos(x)),
        "atan": lambda x: m.degrees(m.atan(x)),
        "log": lambda x: m.log10(x),
        "ln": lambda x: m.log(x),
    }
    for token in rpn:
        ttype, value = token
        if value == "exit":
            exit()
        if ttype == "NUMBER":
            if len(stack) != 0 and stack[-1] in func_map:
                func = func_map[stack.pop()]
                stack.append(func(value))
            else:
                stack.append(value)
        elif ttype == "FACT":
            stack.append(m.factorial(int(stack.pop())))
        elif ttype == "ANS":
            stack.append(ans)
        elif ttype == "VAR":
            stack.append(memory[value])
        elif ttype == "MPLUS":
            memory["M"] += stack.pop()
        elif ttype == "MMINUS":
            memory["M"] -= stack.pop()
        elif ttype == "STORE":
            memory[value] = stack.pop()
            stack.append(memory[value])
        elif ttype == "RECALL":
            stack.append(memory[value])
        elif ttype == "FUNC":
            stack.append(value)

        elif ttype == "OP":
            if value == "UMINUS":
                stack.append(-stack.pop())
            else:

                if len(stack) < 2:
                    raise ValueError(f"Invalid RPN: stack too small at {token}.")
                b = stack.pop()
                a = stack.pop()

                if value == "PLUS":
                    result = a + b
                    stack.append(result)

                elif value == "MINUS":
                    result = a - b
                    stack.append(result)

                elif value == "MULTIPLY":
                    result = a * b
                    stack.append(result)

                elif value == "DIVIDE":
                    result = a / b
                    stack.append(result)

                elif value == "POW":
                    result = a**b
                    stack.append(result)

                elif value == "NCR":
                    result = m.comb(int(a), int(b))
                    stack.append(result)

                elif value == "NPR":
                    result = m.perm(int(a), int(b))
                    stack.append(result)

    return stack
