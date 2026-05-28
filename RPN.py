import math as m
import statistics as s
import random


def evaluate(rpn, memory, ans, guide, debug_mode=False, n=[], STAT=False, deg=True):

    def to_number(x):
        if isinstance(x, str):
            try:
                return float(x)
            except:
                raise TypeError(f"Invalid numeric value: {x}")
        return x

    if debug_mode:
        print("RPN Stack Track:\n")
    stack = []

    to_rad = (m.pi / 180) if deg else 1
    from_rad = (180 / m.pi) if deg else 1

    func_map = {
        "sqrt": lambda x: m.sqrt(x),
        "cbrt": lambda x: m.cbrt(x),
        "sin": lambda x: m.sin(x * to_rad),
        "cos": lambda x: m.cos(x * to_rad),
        "tan": lambda x: m.tan(x * to_rad),
        "asin": lambda x: m.asin(x) * from_rad,
        "acos": lambda x: m.acos(x) * from_rad,
        "atan": lambda x: m.atan(x) * from_rad,
        "log": lambda x: m.log10(x),
        "abs": lambda x: abs(x),
        "ran": lambda x: (random.random()) * x,
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
        if ttype == "NUMBER" and not isinstance(value, (int, float)):
            raise TypeError(f"Invalid NUMBER token: {value}")
        if value == "exit":
            exit()
        if ttype == "NUMBER":
            stack.append(to_number(value))
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
                        if abs(n[idx] - val) < 1e-9:
                            n.pop(idx)
                            print(f"Removed {val}")
                            stack.append(len(n))
                            break
                    else:
                        print(f"Couldn't find {val}")
                        stack.append(len(n))
                        continue
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
            elif value == "ran":
                arg = stack.pop()
                stack.append(func_map["ran"](arg))
            elif value == "pol":

                y = stack.pop()
                x = stack.pop()

                r = m.hypot(x, y)
                theta = m.degrees(m.atan2(y, x)) if deg else m.atan2(y, x)

                stack.append(r)

                memory["E"] = r
                memory["F"] = theta

                print(f"{r:.10g} -> E")
                print(f"{theta:.10g} -> F")

            elif value == "rec":
                theta = stack.pop()
                r = stack.pop()

                if deg:
                    theta = m.radians(theta)

                x = r * m.cos(theta)
                y = r * m.sin(theta)

                stack.append(x)

                memory["E"] = x
                memory["F"] = y

                print(f"{x:.10g} -> E")
                print(f"{y:.10g} -> F")

            else:
                number = stack.pop()
                if value == "tan" and deg:
                    if abs(number % 180 - 90) < 1e-9:
                        raise ValueError("tan(90) is undefined")
                number = to_number(number)
                stack.append(func_map[value](number))  # type: ignore
        elif ttype == "STAT_FUNC":
            if not STAT:
                raise SyntaxError("Function available in STAT mode only")
            stack.append(stat_func_map[value]())  # type: ignore

        elif ttype == "OP":
            if value == "UMINUS":
                stack.append(to_number(-stack.pop()))
            else:

                if len(stack) < 2:
                    # raise ValueError(f"Invalid RPN: stack too small at {token}.")
                    raise ValueError(f"Invalid Expression for {token[1]}")
                b = to_number(stack.pop())
                a = to_number(stack.pop())

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

    if isinstance(stack[0], complex):
        stack.pop()  # remove the complex number
        raise ValueError("Complex result not supported")

    if len(stack) > 1:
        raise SyntaxError("Invalid expression")

    return stack
