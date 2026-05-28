from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from os import system, name
import atexit
import json
from time import sleep

debug_mode = False
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
RED = "\033[31m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"


def boot_up_actions() -> None:

    system("cls" if name == "nt" else "clear")
    print(
        f"{RED}Type 'exit' to exit the program(Retains all data, including previous answer/memory/STAT data){RESET}"
    )
    print("Type 'clear' to clear the terminal")
    print("Type 'guide' to print a basic guide for this calculator")
    print(
        f"{RED}ALL FUNCTIONS ARE REQUIRED TO HAVE PARENTHESIS FOR THEIR ARGUMENTS(e.g sin(5), log(10), ln(2)){RESET}"
    )


boot_up_actions()


def guide() -> None:
    global CYAN, GREEN, YELLOW, MAGENTA, BLUE, RED, RESET

    print(f"\n\n{CYAN}╔════════════════════════════╗")
    print(f"║     Calculator Guide       ║")
    print(f"╚════════════════════════════╝{RESET}\n")

    print(
        f"{RED}ALL DATA IS RETAINED EVEN AFTER THE PROGRAM IS CLOSED(including previous answer/memory/STAT data){RESET}"
    )
    print(
        f"{RED}ALL FUNCTIONS ARE REQUIRED TO HAVE PARENTHESIS FOR THEIR ARGUMENTS{RESET}"
    )
    print(
        f"{RED}ALL INPUTS ARE ARE SPACE & CASE-SENSITIVE(FUNCTIONS, VARIABLES, CONSTANTS, etc){RESET}"
    )
    print(
        f"{GREEN}{'Operators:':<25}{RESET} |  + - * / ^ sqrt(square root), cbrt(cube root)"
    )
    print(
        f"{GREEN}{'Deg < -- > Rad:':<25}{RESET} |  deg: radians -> degrees, rad: degrees -> radians"
    )
    print(f"{GREEN}{'Trig:':<25}{RESET} |  sin, cos, tan (degrees)")
    print(f"{GREEN}{'Inverse trig:':<25}{RESET} |  asin, acos, atan")
    print(f"{GREEN}{'Logarithms:':<25}{RESET} |  log(base 10), ln(natural log)")
    print(f"{GREEN}{'Negative numbers:':<25}{RESET} |  -3, --3")
    print(f"{GREEN}{'Parentheses:':<25}{RESET} |  (2+3)*4")
    print(f"{GREEN}{'Random number:':<25}{RESET} |  ran(5) -> random number 0-5")
    print(f"{GREEN}{'Absolute:':<25}{RESET} |  abs(-5) -> 5")

    print(f"{YELLOW}{'Scientific Notation:':<25}{RESET} |  X x10 Y (5 x10 5 = 500000)")
    print(f"{YELLOW}{'Constants:':<25}{RESET} |  pi & e")

    print(f"{YELLOW}{'Combinatorics:':<25}{RESET} |  x ncr y, x npr y")

    print(f"{MAGENTA}{'Memory Store:':<25}{RESET} |  X sto Y")
    print(f"{MAGENTA}{'Memory Recall:':<25}{RESET} |  X rcl Y")
    print(
        f"{MAGENTA}{'Recall(no args):':<25}{RESET} |  recall or rcl -> All values in all memories printed"
    )
    print(f"{MAGENTA}{'Memory Cells:':<25}{RESET} |  A, B, C, D, E, F, M, X, Y")
    print(f"{MAGENTA}{'Variables:':<25}{RESET} |  Use memory cells in expressions: A+1")

    print(f"{GREEN}{'Factorial:':<25}{RESET} |  X!")
    print(f"{GREEN}{'Previous Answer:':<25}{RESET} |  ans")
    print(f"{GREEN}{'Memory Add/Minus:':<25}{RESET} |  M+, M- (e.g 5 M+)")

    print(
        f"{RED}{'RESET Memory:':<25}{RESET} |  RESETMEM (Sets all Memory Cells back to 0)"
    )
    print(f"{RED}{'RESET STAT:':<25}{RESET} |  RESETSTAT (Clears all Data points)")
    print(f"{RED}{'RESET ALL:':<25}{RESET} |  RESETALL (Mode still remains)")

    print(
        f"{BLUE}{'Modes:':<25}{RESET} |  type 'mode' to view the current mode & angular unit you're in"
    )
    print(f"{BLUE}{'Stat Mode:':<25}{RESET} |  type 'stat' to enter statistic mode")
    print(f"{BLUE}{'Comp Mode:':<25}{RESET} |  type 'comp' to enter computational mode")
    print(f"{BLUE}{'Stat Entry:':<25}{RESET} |  5 M+ (adds 5 to dataset)")
    print(
        f"{BLUE}{'Stat Deletion:':<25}{RESET} |  5 M- (removes the last occurrence of 5 from the dataset)"
    )
    print(
        f"{BLUE}{'Stat Functions:':<25}{RESET} |  n(number of data points added), mean, sumx, sumx2(sum of x squared), sdev, sdev1"
    )
    print(
        f"{ORANGE}{'Coordinate Conversion:':<25}{RESET} |  Note that the functions' output are stored in the memory cells E (r, x) & F (θ, y)"
    )
    print(
        f"{ORANGE}{'Polar Coordinates:':<25}{RESET} |  pol(x,y) Cartesian -> Polar (x,y -> r,θ)"
    )
    print(
        f"{ORANGE}{'Rectangular Coordinates:':<25}{RESET} |  rec(x,y) Polar -> Cartesian (r,θ -> x,y)"
    )


# Export Current state of data into state.json
def save_state() -> None:
    with open("state.json", "w") as f:
        json.dump(
            {"memory": memory, "n": n, "ans": ans, "deg": deg, "stat_mode": STAT_MODE},
            f,
        )


memory = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
ans = 0
history = []
n = []
deg = True
STAT_MODE = False

# Load saved data
try:
    with open("state.json", "r") as f:
        state = json.load(f)
        memory.update(state["memory"])
        n.extend(state["n"])
        deg = state.get("deg", True)
        ans = state.get("ans", 0)
        STAT_MODE = state.get("stat_mode", False)
except FileNotFoundError:
    pass
except json.JSONDecodeError:
    pass
restored = any(v != 0 for v in memory.values()) or len(n) > 0 or ans != 0 or deg != True
if restored:
    print(f"{GREEN}Previous session restored successfully.{RESET}")
atexit.register(save_state)


def RESET_DATA(command: str) -> None:
    global ans, deg

    def RESETMEM():
        memory.update({k: 0 for k in memory})

    def RESETSTAT():
        n.clear()

    if command == "RESETMEM":
        RESETMEM()
        print("MEMORY CLEARED")
    elif command == "RESETSTAT":
        RESETSTAT()
        print("STAT DATA CLEARED")
    else:
        RESETMEM()
        RESETSTAT()
        ans = 0
        deg = True
        for _ in range(3):
            print(".", end="", flush=True)
            sleep(0.333333)
        print()
        print("ALL DATA CLEARED!")
    save_state()


def command_handler(equation: str) -> bool:
    global debug_mode, deg, STAT_MODE
    if equation == "exit":
        exit()
    elif equation == "clear":
        boot_up_actions()
        return True
    elif equation in ("deg", "rad"):
        deg = True if equation == "deg" else False
        return True
    elif equation in ("RESETMEM", "RESETSTAT", "RESETALL"):
        RESET_DATA(equation)
        return True
    elif equation.upper() in ("STAT", "COMP"):
        STAT_MODE = True if equation.upper() == "STAT" else False
        print("Stat Mode Activated" if STAT_MODE else "Comp Mode Activated")
        return True
    elif equation.upper() == "MODE":
        print("STAT" if STAT_MODE else "COMP")
        print("Degrees" if deg else "Radians")
        return True
    return False


def evaluate_equation(equation: str) -> None:
    global ans
    try:
        tokenized = tokenize(equation)  # Raw Equation -> Tokens
        parsed = parse(tokenized)  # Tokens -> RPN
        if debug_mode:
            print(f"Toknized: {tokenized}")
            print(f"Parsed: {parsed}")
        evaluated: list[float] = evaluate(
            parsed, memory, ans, guide, debug_mode, n, STAT_MODE
        )  # RPN -> Evaluated
        if evaluated:
            result: float = evaluated[0]
            ans = result
            formatted = f"{result:.10g}"
            if "e" in formatted:
                mantissa, exp = formatted.split("e")
                print(f"= {mantissa}x10{exp}")
            else:
                print(f"= {formatted}")
    except ZeroDivisionError:
        print("Math Error: Zero Division")
    except ValueError as e:
        print(
            f"Math Error: {e}"
            if "math domain error" not in str(e)
            else "Math Error: Math domain error"
        )
    except NameError as e:
        print(f"Error: {e}")
    except OverflowError:
        print(float("inf"))
    except IndexError:
        print("Invalid expression")
    except KeyError as e:
        print(f"Unknown function: {e}")
    except SyntaxError as e:
        print(f"Error: {e}")


##### MAIN LOOP

while True:
    save_state()
    equation = input("\n> ")
    if command_handler(equation):
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
    evaluate_equation(equation)
