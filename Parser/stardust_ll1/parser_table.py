from typing import List, Tuple, Any
from .grammar import make_grammar, compute_first, compute_follow, build_parsing_table
from .lexer import Token

class ParseError(Exception):
    pass

class LL1Parser:
    def __init__(self, generate_table: bool = True):
        # constrói tabela a partir da gramática (se generate_table True)
        if generate_table:
            G = make_grammar()
            FIRST = compute_first(G)
            FOLLOW = compute_follow(G, FIRST)
            self.table = build_parsing_table(G, FIRST, FOLLOW)
            self.G = G
        else:
            raise RuntimeError("Only generation-from-grammar supported in this simple implementation.")

        # parser state
        self.tokens: List[Token] = []
        self.pos = 0

    def parse(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        return self._parse_nonterminal("Program")

    def lookahead(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "", 0, 0)

    def _match_terminal(self, X: str):
        # aceita X ser tanto um token.type (ex: LPAREN) quanto um exact token.value (ex: '(')
        tok = self.lookahead()
        if tok.type == X or tok.value == X:
            # consume
            self.pos += 1
            return tok
        raise ParseError(f"Erro de sintaxe: token '{tok.value}' esperado {X} (lookahead: {tok.type}/{tok.value})")

    def _parse_nonterminal(self, A: str):
        # seleciona produção via tabela (usando lookahead token type OR token value)
        tok = self.lookahead()
        # try keys using tok.type, then tok.value, then EOF
        key_type = (A, tok.type)
        key_val = (A, tok.value)
        prod = None
        if key_type in self.table:
            prod = self.table[key_type]
        elif key_val in self.table:
            prod = self.table[key_val]
        elif (A, "$") in self.table and tok.type == "EOF":
            prod = self.table[(A, "$")]
        else:
            la = tok
            raise ParseError(f"Erro de sintaxe: token '{la.value}' em {A} (lookahead seq: {la.type}/{la.value})")

        # epsilon production
        if prod == []:
            return [A, []]

        node_children = []
        for X in prod:
            if X == "ε":
                continue
            if X in self.G:  # nonterminal
                node_children.append(self._parse_nonterminal(X))
            else:  # terminal
                matched = self._match_terminal(X)
                node_children.append((X,))
        return [A, node_children]
