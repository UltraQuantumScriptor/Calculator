from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from os import system, name


def boot_up_actions():
    system("cls" if name == "nt" else "clear")
    print("Type 'exit' to exit the program")
    print("Type 'clear' to clear the terminal")
    print("Type 'guide' to print a basic guide for this calculator")


boot_up_actions()


def guide():
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"

    print(f"\n{CYAN}===== Calculator Guide ====={RESET}\n")

    print(f"{GREEN}Operators:{RESET} + - * / ^")
    print(f"{GREEN}Trig:{RESET} sin, cos, tan (degrees)")
    print(f"{GREEN}Inverse trig:{RESET} asin, acos, atan")
    print(f"{GREEN}Logarithms:{RESET} log, ln")
    print(f"{GREEN}Negative numbers:{RESET} -3, --3")
    print(f"{GREEN}Parentheses:{RESET} (2+3)*4")

    print(f"{YELLOW}Combinatorics:{RESET} x ncr y, x npr y")

    print(f"{MAGENTA}Memory Store:{RESET} X storeY")
    print(f"{MAGENTA}Memory Recall:{RESET} X recallY")

    print(f"{MAGENTA}Memory Cells:{RESET} A,B,C,D,E,F,M,X,Y")

    print(f"{GREEN}Factorial:{RESET} X!")
    print(f"{GREEN}Variables:{RESET} A+1")
    print(f"{GREEN}Previous Answer:{RESET} ans")
    print(f"{GREEN}Memory Add/Subtract:{RESET} M+, M-")


memory = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
ans = 0
while True:

    equation = input("\n> ")
    if equation == "exit":
        exit()
    if equation == "clear":
        boot_up_actions()
        continue

    try:
        tokens = tokenize(equation)
        parsed = parse(tokens)

        def debug():
            print("tokenized:", tokens)
            print("parsed:", parsed)

        debug()

        evaluated = evaluate(parsed, memory, ans, guide)
        if evaluated:
            try:
                print(f"= {evaluated[0]:0.10g}")
                ans = evaluated[0]
            except OverflowError:
                print(evaluated[0])
        else:
            if equation not in ("guide"):
                print("= 0")
    except ZeroDivisionError:
        print("Math Error: Zero Division")
    except ValueError as e:
        if "math domain error" in str(e):
            print("Math Error: Math domain error")
        else:
            print(f"Math Error: {e}")
    except NameError as e:
        print(f"Error: {e}")
    except OverflowError:
        print(float("inf"))
    except IndexError:
        print("Invalid expression")
    except KeyError as e:
        print(f"Unkown function: {e}")
