# stardust_ll1/parser_table.py
import json
from typing import List, Tuple, Any
from .lexer import Token
from .ast_nodes import *
from .grammar import make_grammar, compute_first, compute_follow, build_parsing_table

class ParseError(Exception):
    pass

class LL1Parser:
    def __init__(self, table=None):
        if table is None:
            # generate table at init (can be expensive)
            G = make_grammar()
            FIRST = compute_first(G)
            FOLLOW = compute_follow(G, FIRST, "Program")
            self.table = build_parsing_table(G, FIRST, FOLLOW)
            self.G = G
        else:
            self.table = table
            self.G = make_grammar()

    def parse(self, tokens: List[Token]):
        # convert token stream into terminal names expected by table:
        # tokens are Token.type values (e.g. IDENT, INT, "+", "if", etc.)
        input_stream = [t.type for t in tokens]
        # pointer
        i = 0
        def peek():
            return input_stream[i] if i < len(input_stream) else "$"
        # stack: start symbol
        stack = ["$", "Program"]
        # For building a simple parse trace or AST we need semantic actions.
        # For simplicity this parser will build a concrete parse tree as a nested list of symbols,
        # after which we can run a transformer to build AST nodes.
        parse_tree_stack = []
        # We'll store an output list of matched terminals to later reconstruct tree
        matched = []
        while stack:
            top = stack.pop()
            look = input_stream[i] if i < len(input_stream) else "$"
            if top == "$" and look == "EOF":
                # successful parse
                break
            if top not in self.G:  # top is terminal
                if top == look:
                    # match consuming input
                    matched.append((top, look))
                    i += 1
                    continue
                else:
                    raise ParseError(f"Unexpected token: {look}, expected: {top}")
            # top is nonterminal
            key = (top, look)
            prod = self.table.get(key)
            if prod is None:
                # try to provide helpful message
                raise ParseError(f"No rule for nonterminal {top} with lookahead {look}")
            # push production RHS to stack in reverse (ε is [])
            if prod != []:
                for sym in reversed(prod):
                    stack.append(sym)
            # if prod is epsilon, nothing pushed
            # continue
        # If we reached here without raising, parse succeeded
        # Note: above code only validates sequence; to produce AST we need a full parse-tree builder
        # For the deliverable we will build a simple AST using a separate recursive descent mapping
        # because mapping table-driven parse into AST with semantic actions is verbose.
        # So we'll do: call a small recursive-descent consumer that trusts the grammar shape but uses tokens.
        return self.build_ast_from_tokens(tokens)

    # For pragmatic reasons (clear AST generation), build AST using a small deterministic recursive-descent
    # that follows the same grammar (this keeps conformance with LL(1) table but produces clean AST).
    def build_ast_from_tokens(self, tokens: List[Token]):
        # We'll implement a small predictive recursive-descent parser that consumes the token list
        # but uses LL(1)-style decisions (no backtracking).
        self.tokens = tokens
        self.pos = 0
        def peek():
            return self.tokens[self.pos] if self.pos < len(self.tokens) else Token("EOF","",0,0)
        def next_token():
            t = self.tokens[self.pos]
            self.pos += 1
            return t

        # Helper match/expect
        def match(*types):
            if peek().type in types:
                return next_token()
            return None
        def expect(t):
            tok = peek()
            if tok.type == t:
                return next_token()
            raise ParseError(f"Expected {t} but got {tok.type} ({tok.value}) at {tok.line}:{tok.col}")

        # Implementation mirrors the grammar in grammar.make_grammar()
        def parse_program():
            items = []
            while peek().type != "EOF":
                if peek().type in ("function","FUNCTION"):
                    items.append(parse_function())
                else:
                    items.append(parse_statement())
            return Program(items)

        def parse_function():
            match("function","FUNCTION")
            name = expect("IDENT").value
            expect("(")
            params = []
            if peek().type == "IDENT":
                params.append(next_token().value)
                while match(","):
                    params.append(expect("IDENT").value)
            expect(")")
            body = parse_block()
            return FunctionDecl(name, params, body)

        def parse_block():
            expect("{")
            stmts = []
            while peek().type != "}":
                if peek().type == "EOF":
                    raise ParseError("Unexpected EOF inside block")
                stmts.append(parse_statement())
            expect("}")
            return Block(stmts)

        def parse_statement():
            tok = peek()
            if tok.type in ("if","IF"):
                return parse_if()
            if tok.type in ("while","WHILE"):
                return parse_while()
            if tok.type in ("for","FOR"):
                return parse_for()
            if tok.type in ("return","RETURN"):
                next_token()
                if peek().type != ";":
                    expr = parse_expression()
                else:
                    expr = None
                expect(";")
                return ReturnStmt(expr)
            if tok.type == "{":
                return parse_block()
            if tok.type == ";":
                next_token()
                return ExprStmt(Literal(None))
            if tok.type == "IDENT":
                # disambiguate assignment vs expression by peeking next token
                nxt = self.tokens[self.pos+1] if (self.pos+1) < len(self.tokens) else Token("EOF","",0,0)
                if nxt.type == "=":
                    name = next_token().value
                    expect("=")
                    val = parse_expression()
                    expect(";")
                    return Assign(name, val)
                else:
                    expr = parse_expression()
                    expect(";")
                    return ExprStmt(expr)
            if tok.type in ("INT","FLOAT","STRING","true","TRUE","false","FALSE","null","NULL","(","-"):
                expr = parse_expression()
                expect(";")
                return ExprStmt(expr)
            raise ParseError(f"Unexpected token in statement: {tok.type} ({tok.value}) at {tok.line}:{tok.col}")

        def parse_if():
            match("if","IF")
            expect("(")
            cond = parse_expression()
            expect(")")
            then_block = parse_block()
            elsifs = []
            else_block = None
            while peek().type in ("elsif","ELSIF"):
                next_token()
                expect("(")
                c = parse_expression()
                expect(")")
                b = parse_block()
                elsifs.append((c,b))
            if peek().type in ("else","ELSE"):
                next_token()
                else_block = parse_block()
            return IfStmt(cond, then_block, elsifs, else_block)

        def parse_while():
            next_token()
            expect("(")
            cond = parse_expression()
            expect(")")
            body = parse_block()
            return WhileStmt(cond, body)

        def parse_for():
            next_token()
            expect("(")
            init = None
            if peek().type != ";":
                if peek().type == "IDENT" and (self.pos+1) < len(self.tokens) and self.tokens[self.pos+1].type == "=":
                    name = next_token().value
                    expect("=")
                    init = Assign(name, parse_expression())
                else:
                    init = parse_expression()
            expect(";")
            cond = None
            if peek().type != ";":
                cond = parse_expression()
            expect(";")
            step = None
            if peek().type != ")":
                step = parse_expression()
            expect(")")
            body = parse_block()
            return ForStmt(init, cond, step, body)

        # Pratt-style expression parser for precedence (but deterministic)
        def parse_expression(rbp=0):
            t = next_token()
            left = nud(t)
            while rbp < lbp(peek()):
                op = next_token()
                left = led(op, left)
            return left

        def nud(tok):
            if tok.type == "INT":
                return Literal(int(tok.value))
            if tok.type == "FLOAT":
                return Literal(float(tok.value))
            if tok.type == "STRING":
                return Literal(tok.value)
            if tok.type in ("true","TRUE"):
                return Literal(True)
            if tok.type in ("false","FALSE"):
                return Literal(False)
            if tok.type in ("null","NULL"):
                return Literal(None)
            if tok.type == "IDENT":
                if peek().type == "(":
                    # call
                    next_token()  # consume '('
                    args = []
                    if peek().type != ")":
                        args.append(parse_expression())
                        while match(","):
                            args.append(parse_expression())
                    expect(")")
                    return Call(Identifier(tok.value), args)
                return Identifier(tok.value)
            if tok.type == "(":
                e = parse_expression()
                expect(")")
                return e
            if tok.type == "-":
                r = parse_expression(70)
                return UnaryOp("-", r)
            raise ParseError(f"Unexpected token in expression: {tok.type} ({tok.value}) at {tok.line}:{tok.col}")

        def lbp(tok):
            t = tok.type
            if t in ("*","/","//","%"): return 60
            if t in ("+","-"): return 50
            if t in ("==","!=","<",">","<=",">="): return 40
            if t in ("and","AND"): return 30
            if t in ("or","OR"): return 20
            return 0

        def led(op_tok, left):
            t = op_tok.type
            if t in ("+","-","*","/","//","%","==","!=","<",">","<=",">=","and","AND","or","OR"):
                rbp = lbp(op_tok)
                right = parse_expression(rbp)
                return BinaryOp(t, left, right)
            raise ParseError(f"Unexpected operator {t} at {op_tok.line}:{op_tok.col}")

        prog = parse_program()
        return prog
