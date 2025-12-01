import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

KEYWORDS = {
    "function", "if", "elsif", "else",
    "while", "for", "return",
    "true", "false", "null",
    "and", "or"
}

TOKEN_SPECIFICATION = [
    ("NUMBER",       r"\d+(\.\d+)?"),
    ("STRING",       r"\".*?\""),
    ("IDENT",        r"[A-Za-z_][A-Za-z0-9_]*"),
    ("LPAREN",       r"\("),
    ("RPAREN",       r"\)"),
    ("LBRACE",       r"\{"),
    ("RBRACE",       r"\}"),
    ("COMMA",        r","),
    ("SEMICOLON",    r";"),
    ("PLUS",         r"\+"),
    ("MINUS",        r"-"),
    ("MULT",         r"\*"),
    ("DIV",          r"/"),
    ("EQ",           r"=="),
    ("ASSIGN",       r"="),
    ("LT",           r"<"),
    ("GT",           r">"),
    ("LE",           r"<="),
    ("GE",           r">="),
    ("NE",           r"!="),
    ("AND",          r"and"),
    ("OR",           r"or"),
    ("SKIP",         r"[ \t\r]+"),
    ("NEWLINE",      r"\n"),
    ("MISMATCH",     r"."), 
]

TOKEN_REGEX = "|".join(
    f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION
)

master_pat = re.compile(TOKEN_REGEX)

def tokenize(text: str) -> List[Token]:
    tokens = []
    line = 1
    column = 1

    for mo in master_pat.finditer(text):
        kind = mo.lastgroup
        value = mo.group()

        if kind == "NUMBER":
            if "." in value:
                tok_type = "FLOAT"
            else:
                tok_type = "INT"

        elif kind == "IDENT":
            tok_type = value if value in KEYWORDS else "IDENT"

        elif kind == "STRING":
            tok_type = "STRING"

        elif kind == "SKIP":
            column += len(value)
            continue

        elif kind == "NEWLINE":
            line += 1
            column = 1
            continue

        elif kind == "MISMATCH":
            raise RuntimeError(f"Caractere inesperado {value!r} na linha {line}")

        else:
            tok_type = kind

        tokens.append(Token(tok_type, value, line, column))
        column += len(value)

    tokens.append(Token("EOF", "", line, column))
    return tokens
