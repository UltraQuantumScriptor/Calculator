from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from os import system, name

debug_mode = False


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

    print(f"\n\n{CYAN}╔════════════════════════════╗")
    print(f"║     Calculator Guide       ║")
    print(f"╚════════════════════════════╝{RESET}\n")

    print(f"{GREEN}{'Operators:':<20}{RESET} |  + - * / ^")
    print(f"{GREEN}{'Trig:':<20}{RESET} |  sin, cos, tan (degrees)")
    print(f"{GREEN}{'Inverse trig:':<20}{RESET} |  asin, acos, atan")
    print(f"{GREEN}{'Logarithms:':<20}{RESET} |  log(base 10), ln(natural log)")
    print(f"{GREEN}{'Negative numbers:':<20}{RESET} |  -3, --3")
    print(f"{GREEN}{'Parentheses:':<20}{RESET} |  (2+3)*4")

    print(f"{YELLOW}{'Constants:':<20}{RESET} |  pi & e")

    print(f"{YELLOW}{'Combinatorics:':<20}{RESET} |  x ncr y, x npr y")

    print(f"{MAGENTA}{'Memory Store:':<20}{RESET} |  X storeY")
    print(f"{MAGENTA}{'Memory Recall:':<20}{RESET} |  X recallY")
    print(f"{MAGENTA}{'Memory Cells:':<20}{RESET} |  A, B, C, D, E, F, M, X, Y")
    print(f"{MAGENTA}{'Variables:':<20}{RESET} |  A+1")

    print(f"{GREEN}{'Factorial:':<20}{RESET} |  X!")
    print(f"{GREEN}{'Previous Answer:':<20}{RESET} |  ans")
    print(f"{GREEN}{'Memory Add/Subtract:':<20}{RESET} |  M+, M-")


memory = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
ans = 0
history = []

##### STAT MODE
# def Stat_Mode(equation):


##### COMP MODE

while True:

    equation = input("\n> ")
    if equation == "exit":
        exit()
    if equation == "clear":
        boot_up_actions()
        continue
    history.append(equation)
    if history[-3:] == ["debug", "on", "now"]:
        debug_mode = True
        print("Debug mode enabled")
        continue
    elif history[-3:] == ["debug", "off", "now"]:
        debug_mode = False
        print("Debug mode disabled")
        continue

    try:
        tokens = tokenize(equation)
        parsed = parse(tokens)

        def debug():
            print("tokenized:", tokens)
            print("parsed:", parsed)

        if debug_mode:
            debug()

        evaluated = evaluate(parsed, memory, ans, guide, debug_mode)
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
    except SyntaxError as e:
        print(f"Error: {e}")
