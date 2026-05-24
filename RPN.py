import math as m
import statistics as s


def evaluate(rpn, memory, ans, guide, debug_mode=False, n=[], STAT=False):
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

    stat_func_map = {
        "mean": lambda: s.mean(n),
        "sumx": lambda: sum(n),
        "sumx2": lambda: sum(i**2 for i in n),
        "sdev": lambda: s.pstdev(n),
        "sdev1": lambda: s.stdev(n),
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
            if not STAT:
                memory["M"] += stack.pop()
                stack.append(memory["M"])
            else:
                n.append(stack.pop())
                stack.append(len(n))
        elif ttype == "MMINUS":
            if not STAT:
                memory["M"] -= stack.pop()
                stack.append(memory["M"])
            else:
                if stack:
                    val = stack.pop()
                    for idx in range(len(n) - 1, -1, -1):
                        if n[idx] == val:
                            n.pop(idx)
                            stack.append(len(n))
                            break
                else:
                    if n:
                        n.pop()
                        stack.append(len(n))
        elif ttype == "STORE":
            memory[value] = stack.pop()
            stack.append(memory[value])
        elif ttype == "RECALL":
            stack.append(memory[value])
        elif ttype == "FUNC":
            if value == "guide":
                func_map["guide"]()
                return []
            elif value in ("recall", "rcl"):
                for cell, num in memory.items():
                    print(f"{cell}: {num}")
            else:
                number = stack.pop()
                if value == "tan":
                    if abs(number % 180 - 90) < 1e-9:
                        raise ValueError("tan(90) is undefined")
                stack.append(func_map[value](number))
        elif ttype == "STAT_FUNC":
            if not STAT:
                raise SyntaxError("Function available in STAT mode only")
            stack.append(stat_func_map[value]())

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
