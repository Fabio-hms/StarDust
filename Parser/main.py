# main.py
import os
from stardust_ll1 import tokenize
import stardust_ll1.lexer as L
from stardust_ll1.parser_table import LL1Parser

# garante que o arquivo ll1_table.json é procurado em relação à pasta do main.py
file_dir = os.path.dirname(__file__)
LL1_JSON = os.path.join(file_dir, "stardust_ll1", "ll1_table.json")

# cria o parser (vai gerar a tabela em memória a partir da gramática se necessário)
parser = LL1Parser()

def print_tree(node, indent=0):
    space = " " * indent
    if isinstance(node, (str, int, float)):
        print(f"{space}{node}")
        return
    if hasattr(node, "type") and hasattr(node, "value"):
        print(f"{space}{node.type}({node.value})")
        return
    if isinstance(node, list):
        if len(node) == 0:
            print(f"{space}[]")
            return
        A, children = node[0], node[1] if len(node) > 1 else []
        print(f"{space}{A}")
        for ch in children:
            if isinstance(ch, tuple) and len(ch) == 1 and isinstance(ch[0], tuple):
                # safety: nested single tuple
                print_tree(ch[0], indent + 2)
            else:
                print_tree(ch, indent + 2)
        return
    print(f"{space}{repr(node)}")

# exemplo de código (você pode alterar)
code = "function test() {} function f(x) { return x; }"

print("RAW:")
import re
for mo in L.master_pat.finditer(code):
    print(repr(mo.group()))

tokens = tokenize(code)

print("\nTOKENS:")
for t in tokens:
    print(t)

print("\nARVORE")
tree = parser.parse(tokens)
print_tree(tree)
