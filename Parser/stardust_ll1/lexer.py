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

token_specification = [
    ("FLOAT", r'\d+\.\d+'),
    ("INT", r'\d+'),

    ("IDENT", r'[A-Za-z_][A-Za-z0-9_]*'),

    ("EQEQ", r'=='),
    ("NE", r'!='),
    ("LE", r'<='),
    ("GE", r'>='),
    ("DOUBLE_SLASH", r'//'),

    ("ASSIGN", r'='),
    ("LT", r'<'),
    ("GT", r'>'),
    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("STAR", r'\*'),
    ("SLASH", r'/'),
    ("PERCENT", r'%'),

    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("LBRACE", r'\{'),
    ("RBRACE", r'\}'),
    ("COMMA", r','),
    ("SEMICOLON", r';'),

    ("SKIP", r'[ \t\r]+'),
    ("NEWLINE", r'\n'),
    ("COMMENT", r'//[^\n]*'),
]

tok_regex = '|'.join(f"(?P<{name}>{regex})" for name, regex in token_specification)
master_pat = re.compile(tok_regex)

def tokenize(code: str) -> List[Token]:
    tokens = []
    line = 1
    line_start = 0

    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        text = mo.group()
        column = mo.start() - line_start + 1

        if kind == "NEWLINE":
            line += 1
            line_start = mo.end()
            continue

        if kind in ("SKIP", "COMMENT"):
            continue

        if kind == "IDENT" and text in KEYWORDS:
            kind = text

        tokens.append(Token(kind, text, line, column))

    tokens.append(Token("EOF", "", line, column))
    return tokens
