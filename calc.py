from tokenizer import tokenize
from parser import parse
from RPN import evaluate
from os import system

system("cls")
print("Type 'exit' to exit the program")
print("Operators: + - * / ^")
print("Trig: sin, cos, tan (degrees)")
print("Inverse trig: asin, acos, atan (returns degrees)")
print("Logarithms: log (base10), ln (natural log)")
print("Negative numbers: -3, --3")
print("Parentheses: (2+3)*4")
print("Type x ncr y, or x npr y for permutations(lower case)")
print("Use: X storeY to store a value in the memory cell")
print("Use: X recallY to recall the stored value in the memory cell(0 by default)")
print("The types of Memory cells include: A,B,C,D,E,F,M,X,Y")
print("Factorial: X!")
print("Variables: A+1 (use stored memory cells directly in expressions)")
print("Use the keyword 'ans' to use the result of the previous answer ")
print("M+, M-: 5 M+")

memory = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "M": 0, "X": 0, "Y": 0}
ans = 0
while True:

    equation = input("\n> ")
    if equation == "exit":
        exit()

    try:
        tokens = tokenize(equation)
        parsed = parse(tokens)

        def debug():
            print("tokenized:", tokens)
            print("parsed:", parsed)

        debug()

        evaluated = evaluate(parsed, memory, ans)
        if evaluated:
            print(f"= {evaluated[0]:0.10g}")
            ans = evaluated[0]
        else:
            print("= 0")
    except ZeroDivisionError:
        print("Math Error: Zero Division")
    except ValueError as e:
        print(f"Error: {e}")
    except NameError as e:
        print(f"Error: {e}")
    # except IndexError:
    #     print("Invalid expression")
