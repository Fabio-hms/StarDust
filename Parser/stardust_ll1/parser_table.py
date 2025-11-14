from typing import List, Tuple, Any
from stardust_ll1.grammar import make_grammar, compute_first, compute_follow, build_parsing_table
from stardust_ll1.lexer import Token

class ParseError(Exception):
    pass

class LL1Parser:
    def __init__(self, generate_table: bool = True):
        """
        Se generate_table=True: gera a tabela usando grammar.py
        (padrão). Se você já gerou ll1_table.json e quer carregar,
        pode ajustar aqui.
        """
        if generate_table:
            G = make_grammar()
            FIRST = compute_first(G)
            FOLLOW = compute_follow(G, FIRST)
            self.table = build_parsing_table(G, FIRST, FOLLOW)
            self.G = G
        else:
            raise RuntimeError("generate_table=False não implementado neste helper")

    # ----------------------
    # Utilities
    # ----------------------
    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        # sentinel EOF
        return Token("EOF", "", -1, -1)

    def _advance(self):
        self.pos += 1

    def dump_tokens(self):
        """Debug: imprime a lista de tokens (type, value)."""
        print("Tokens:")
        for t in self.tokens:
            print(f"  [{t.line}:{t.column}] type={t.type!r}, value={t.value!r}")

    # Decide o lookahead que corresponde às chaves da tabela:
    def _look_label(self, tok: Token) -> str:
        """
        Retorna o label usado na tabela LL(1):
        - Se token.type for categoria léxica (IDENT/INT/FLOAT/STRING) -> retorna token.type
        - Se token.type == 'EOF' -> retorna '$'
        - Senão -> retorna token.value (palavras-chave e símbolos)
        """
        if tok.type == "EOF":
            return "$"
        # categorias léxicas (sempre por type)
        if tok.type in ("IDENT", "INT", "FLOAT", "STRING"):
            return tok.type
        # palavras-chave o lexer já produziu token.type == 'if' etc. (dependendo do lexer),
        # para segurança, se token.type é igual ao valor da palavra-chave, também aceitamos:
        if tok.type in self.G and isinstance(tok.type, str) and tok.type == tok.value:
            return tok.type
        # default: use token.value (símbolos e operadores normalizados pelo lexer)
        return tok.value

    # Match terminal X (X é string que pode ser 'IDENT', 'INT', '+', 'if', etc.)
    def _match_terminal(self, X: str):
        tok = self._current()
        if X in ("IDENT", "INT", "FLOAT", "STRING"):
            if tok.type == X:
                self._advance()
                return
            raise ParseError(f"Esperado token do tipo {X}, encontrado '{tok.value}' (type={tok.type}) at {tok.line}:{tok.column}")
        # X is literal (symbol or keyword)
        if X == "$":
            # only valid when expecting EOF
            if tok.type == "EOF":
                return
            raise ParseError(f"Esperado EOF ('$'), encontrado '{tok.value}' at {tok.line}:{tok.column}")
        # Otherwise compare by value
        if tok.value == X:
            self._advance()
            return
        # As fallback, às vezes the lexer set token.type to the keyword string (e value same),
        # so also allow matching token.type == X
        if tok.type == X:
            self._advance()
            return
        raise ParseError(f"Esperado literal '{X}', encontrado '{tok.value}' (type={tok.type}) at {tok.line}:{tok.column}")

    # ----------------------
    # Parse entry
    # ----------------------
    def parse(self, tokens: List[Token]) -> Any:
        """
        Retorna uma árvore concreta (parse tree) em forma de lista aninhada:
        [NonTerminal, [child1, child2, ...]]
        Isso é intencionalmente simples — você pode transformar em AST depois.
        """
        self.tokens = tokens
        self.pos = 0

        # debug: opcional, descomente se quiser ver tokens na execução
        # self.dump_tokens()

        return self._parse_nonterminal("Program")

    # ----------------------
    # Core: parse nonterminal A using the LL(1) table
    # ----------------------
    def _parse_nonterminal(self, A: str):
        tok = self._current()
        look = self._look_label(tok)
        key = (A, look)

        if key not in self.table:
            # produce helpful error message including nearby tokens
            # show current token and next few
            lookahead_seq = []
            for i in range(self.pos, min(self.pos + 6, len(self.tokens))):
                t = self.tokens[i]
                lookahead_seq.append(f"{t.type}/{t.value}")
            la = ", ".join(lookahead_seq)
            raise ParseError(f"Erro de sintaxe: token '{tok.value}' inesperado em {A} (lookahead seq: {la})")

        prod = self.table[key]
        node_children = []

        # If production is epsilon (empty list), return empty node
        if prod == []:
            return [A, []]

        for X in prod:
            # epsilon symbol (some grammars use explicit "ε" but here epsilons are [] productions)
            if X == "ε":
                continue
            # nonterminal
            if X in self.G:
                node_children.append(self._parse_nonterminal(X))
            else:
                # terminal expected
                self._match_terminal(X)
                node_children.append((X,))  # leaf represented as tuple for simplicity

        return [A, node_children]
