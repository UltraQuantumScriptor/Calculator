import math as m


def evaluate(rpn, memory, ans, guide, debug_mode=False):
    if debug_mode:
        print("RPN Stack Track:\n")
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
        "guide": guide,
    }
    for debug_num, token in enumerate(rpn):
        ttype, value = token
        if value == "exit":
            exit()
        if ttype == "NUMBER":
            stack.append(value)
        elif ttype == "FACT":
            stack.append(m.factorial(int(stack.pop())))
        elif ttype == "ANS":
            stack.append(ans)
        elif ttype == "VAR":
            stack.append(memory[value])
        elif ttype == "MPLUS":
            memory["M"] += stack.pop()
            stack.append(memory["M"])
        elif ttype == "MMINUS":
            memory["M"] -= stack.pop()
            stack.append(memory["M"])
        elif ttype == "STORE":
            memory[value] = stack.pop()
            stack.append(memory[value])
        elif ttype == "RECALL":
            stack.append(memory[value])
        elif ttype == "FUNC":
            if value == "guide":
                func_map["guide"]()
                return None
            else:
                number = stack.pop()
                stack.append(func_map[value](number))

        elif ttype == "OP":
            if value == "UMINUS":
                stack.append(-stack.pop())
            else:

                if len(stack) < 2:
                    # raise ValueError(f"Invalid RPN: stack too small at {token}.")
                    raise ValueError(f"Invalid Expression for {token[1]}")
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
        if debug_mode:
            print(f"{debug_num}  {token} → {stack}")

    if len(stack) > 1:
        raise SyntaxError("Invalid expression")
    return stack
