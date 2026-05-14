from tokenizer import tokenize
from parser import parse
from RPN import evaluate

equation = input("Enter your equation: ")

with open("raw_string.txt", "w") as file:
    file.write(equation)

with open("raw_string.txt", "r") as file:
    raw_string = file.read()

tokens = tokenize(raw_string)
parsed = parse(tokens)
evaluated = evaluate(parsed)

print("tokenized:", tokens)
print("parsed:", parsed)
print("result:", evaluated[0])
