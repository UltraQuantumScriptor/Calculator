from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from os import system, name

debug_mode = False


def boot_up_actions():
    RED = "\033[31m"
    RESET = "\033[0m"
    system("cls" if name == "nt" else "clear")
    print("Type 'exit' to exit the program")
    print("Type 'clear' to clear the terminal")
    print("Type 'guide' to print a basic guide for this calculator")
    print(
        f"{RED}ALL FUNCTIONS ARE REQUIRED TO HAVE PARENTHESIS FOR THEIR ARGUMENTS(e.g sin(5), log(10), ln(2)){RESET}"
    )


boot_up_actions()


def guide():
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    RESET = "\033[0m"

    print(f"\n\n{CYAN}╔════════════════════════════╗")
    print(f"║     Calculator Guide       ║")
    print(f"╚════════════════════════════╝{RESET}\n")

    print(f"{RED}ALL FUNCTIONS ARE REQUIRED TO HAVE PARENTHESIS FOR THEIR ARGUMENTS")
    print(f"{GREEN}{'Operators:':<20}{RESET} |  + - * / ^")
    print(f"{GREEN}{'Trig:':<20}{RESET} |  sin, cos, tan (degrees)")
    print(f"{GREEN}{'Inverse trig:':<20}{RESET} |  asin, acos, atan")
    print(f"{GREEN}{'Logarithms:':<20}{RESET} |  log(base 10), ln(natural log)")
    print(f"{GREEN}{'Negative numbers:':<20}{RESET} |  -3, --3")
    print(f"{GREEN}{'Parentheses:':<20}{RESET} |  (2+3)*4")

    print(f"{YELLOW}{'Constants:':<20}{RESET} |  pi & e")

    print(f"{YELLOW}{'Combinatorics:':<20}{RESET} |  x ncr y, x npr y")

    print(f"{MAGENTA}{'Memory Store:':<20}{RESET} |  X sto Y")
    print(f"{MAGENTA}{'Memory Recall:':<20}{RESET} |  X rcl Y")
    print(
        f"{MAGENTA}{'Recall(no args):':<20}{RESET} |  recall or rcl -> All values in all memories printed"
    )
    print(f"{MAGENTA}{'Memory Cells:':<20}{RESET} |  A, B, C, D, E, F, M, X, Y")
    print(f"{MAGENTA}{'Variables:':<20}{RESET} |  A+1")

    print(f"{GREEN}{'Factorial:':<20}{RESET} |  X!")
    print(f"{GREEN}{'Previous Answer:':<20}{RESET} |  ans")
    print(f"{GREEN}{'Memory Add/Subtract:':<20}{RESET} |  M+, M-")

    print(
        f"{RED}{'RESET Memory:':<20}{RESET} |  RESETMEM (Sets all Memory Cells back to 0)"
    )
    print(f"{RED}{'RESET STAT:':<20}{RESET} |  RESETSTAT (Clears all Data points)")
    print(f"{RED}{'RESET ALL:':<20}{RESET} |  RESETALL (Mode still remains)")

    print(
        f"{BLUE}{'Modes:':<20}{RESET} |  type 'mode' to view the current mode you're in"
    )
    print(f"{BLUE}{'Stat Mode:':<20}{RESET} |  type 'stat' to enter statistic mode")
    print(f"{BLUE}{'Comp Mode:':<20}{RESET} |  type 'comp' to enter computational mode")
    print(f"{BLUE}{'Stat Entry:':<20}{RESET} |  5 M+ (adds 5 to dataset)")
    print(
        f"{BLUE}{'Stat Deletion:':<20}{RESET} |  5 M- (removes the last occurrence of 5 from the dataset)"
    )
    print(
        f"{BLUE}{'Stat Functions:':<20}{RESET} |  n(number of data points added), mean, sumx, sumx2(sum of x squared), sdev, sdev1"
    )


memory = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
ans = 0
history = []
n = []


##### STAT MODE
def Stat_Mode(equation):
    while True:
        global debug_mode, ans, n
        equation = input("\n> ")
        if equation == "exit":
            exit()
        elif equation == "clear":
            boot_up_actions()
            continue
        elif equation.upper() == "COMP":
            print("COMP MODE ACTIVATED")
            break
        elif equation.upper() == "MODE":
            print("STAT mode")
            continue
        elif equation.upper() == "RESETMEM":
            memory.update({k: 0 for k in memory})
            print("Memory cleared")
            continue
        elif equation.upper() == "RESETSTAT":
            n.clear()
            print("Stat data cleared")
            continue
        elif equation.upper() == "RESETALL":
            memory.update({k: 0 for k in memory})
            n.clear()
            ans = 0
            print("All data cleared")
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
            tokens = tokenize(equation, n)
            parsed = parse(tokens)

            def debug():
                print("tokenized:", tokens)
                print("parsed:", parsed)

            if debug_mode:
                debug()

            evaluated = evaluate(parsed, memory, ans, guide, debug_mode, n=n, STAT=True)

            if evaluated:
                try:
                    print(f"= {evaluated[0]:0.10g}")
                    ans = evaluated[0]
                except OverflowError:
                    print(evaluated[0])
            else:
                if equation not in ("guide", "recall", "rcl"):
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


##### COMP MODE

while True:

    equation = input("\n> ")
    if equation == "exit":
        exit()
    elif equation == "clear":
        boot_up_actions()
        continue
    elif equation.upper() == "COMP":
        continue
    elif equation.upper() == "STAT":
        print("STAT MODE ACTIVATED")
        Stat_Mode(equation)
        continue
    elif equation.upper() == "MODE":
        print("COMP mode")
        continue
    elif equation.upper() == "RESETMEM":
        memory.update({k: 0 for k in memory})
        print("Memory cleared")
        continue
    elif equation.upper() == "RESETSTAT":
        n.clear()
        print("Stat data cleared")
        continue
    elif equation.upper() == "RESETALL":
        memory.update({k: 0 for k in memory})
        n.clear()
        ans = 0
        print("All data cleared")
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
            if equation not in ("guide", "recall", "rcl"):
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
