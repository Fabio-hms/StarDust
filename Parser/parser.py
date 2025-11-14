# tests/test_ll1_parser.py
import pytest
from stardust_ll1.lexer import tokenize
from stardust_ll1.parser_table import LL1Parser, ParseError

def test_simple_assignment():
    src = "x = 1 + 2 * 3;"
    toks = tokenize(src)
    p = LL1Parser()
    prog = p.parse(toks)
    # program should parse without raising
    assert prog is not None

def test_function_if_else():
    src = '''
    function f(a,b) {
      if (a < b) { return a; } elsif (a == b) { return 0; } else { return b; }
    }
    '''
    toks = tokenize(src)
    p = LL1Parser()
    prog = p.parse(toks)
    assert any(hasattr(i, "name") and i.name == "f" for i in prog.items)

def test_syntax_error():
    src = "x = ;"
    toks = tokenize(src)
    p = LL1Parser()
    with pytest.raises(ParseError):
        p.parse(toks)
