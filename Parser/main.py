from stardust_ll1 import tokenize
import stardust_ll1.lexer as L
from stardust_ll1.parser_table import LL1Parser

code = "x = 1 + 2 * 3;"

# RAW text
print("RAW:")
for mo in L.master_pat.finditer(code):
    print(repr(mo.group()))

tokens = tokenize(code)

print("\nTOKENS:")
for t in tokens:
    print(t)
