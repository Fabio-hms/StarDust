# stardust_ll1/lexer.py
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

KEYWORDS = {
    "if", "else", "elsif", "while", "for", "return", "function",
    "true", "false", "null", "and", "or"
}

# token spec: order matters (multi-char ops before single-char)
TOKEN_SPEC = [
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t\r]+"),
    ("COMMENT", r"//[^\n]*"),
    ("MCOMMENT", r"/\*.*?\*/"),
    ("FLOAT", r"\d+\.\d+"),
    ("INT", r"\d+"),
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP", r"==|!=|>=|<=|//|=>|<<|>>|[+\-*/%<>=,;(){}]"),
]

MASTER_RE = re.compile("|".join(f"(?P<{n}>{p})" for n,p in TOKEN_SPEC), re.S)

def tokenize(code: str):
    """
    Returns list[Token], final token is EOF.
    """
    tokens: List[Token] = []
    pos = 0
    line = 1
    col = 1
    length = len(code)
    while pos < length:
        m = MASTER_RE.match(code, pos)
        if not m:
            ch = code[pos]
            raise SyntaxError(f"Unexpected character {ch!r} at {line}:{col}")
        kind = m.lastgroup
        text = m.group(kind)
        if kind == "NEWLINE":
            line += 1
            col = 1
            pos += len(text)
            continue
        if kind in ("WHITESPACE", "COMMENT", "MCOMMENT"):
            pos += len(text)
            col += len(text)
            continue
        # normalize
        if kind == "IDENT":
            if text in KEYWORDS:
                ttype = text.upper()  # e.g. IF, RETURN
            else:
                ttype = "IDENT"
        elif kind == "INT":
            ttype = "INT"
        elif kind == "FLOAT":
            ttype = "FLOAT"
        elif kind == "STRING":
            ttype = "STRING"
            text = text[1:-1]  # remove surrounding quotes
        elif kind == "OP":
            ttype = text
        else:
            ttype = kind
        tokens.append(Token(ttype, text, line, col))
        advance = len(m.group(kind))
        pos += advance
        col += advance
    tokens.append(Token("EOF", "", line, col))
    return tokens
