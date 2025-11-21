from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any, Union

@dataclass(eq=False)
class Type:
    name: str

    def __repr__(self):
        return self.name

INT = Type("int")
FLOAT = Type("float")
STRING = Type("string")
BOOL = Type("bool")
NULL = Type("null")
ANY = Type("any")   

@dataclass
class FunctionType(Type):
    param_types: List[Type]
    return_type: Type
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__("fn")
        self.param_types = param_types
        self.return_type = return_type
    def __repr__(self):
        pts = ", ".join(repr(t) for t in self.param_types)
        return f"fn({pts}) -> {repr(self.return_type)}"

class TypeVar(Type):
    _count = 0
    def __init__(self):
        self.id = TypeVar._count
        TypeVar._count += 1
        super().__init__(f"t{self.id}")
        self.instance: Optional[Type] = None
    def __repr__(self):
        if self.instance:
            return repr(self.instance)
        return self.name

@dataclass
class Symbol:
    name: str
    type: Type

class SymbolTable:
    def __init__(self, parent: Optional["SymbolTable"]=None):
        self.parent = parent
        self.table: Dict[str, Symbol] = {}

    def define(self, name: str, typ: Type):
        self.table[name] = Symbol(name, typ)

    def lookup(self, name: str) -> Optional[Symbol]:
        cur = self
        while cur:
            if name in cur.table:
                return cur.table[name]
            cur = cur.parent
        return None

def is_number_type(t: Type):
    t = resolve(t)
    return t in (INT, FLOAT)

def resolve(t: Type) -> Type:
    if isinstance(t, TypeVar) and t.instance is not None:
        t.instance = resolve(t.instance)
        return t.instance
    return t

def unify(a: Type, b: Type, errors: List[str], ctx=""):
    a = resolve(a)
    b = resolve(b)
    if a is b:
        return a
    if isinstance(a, TypeVar):
        a.instance = b
        return b
    if isinstance(b, TypeVar):
        b.instance = a
        return a
    if isinstance(a, FunctionType) and isinstance(b, FunctionType):
        if len(a.param_types) != len(b.param_types):
            errors.append(f"Mismatch function arity: {a} vs {b} {ctx}")
            return ANY
        for p,q in zip(a.param_types, b.param_types):
            unify(p, q, errors, ctx)
        unify(a.return_type, b.return_type, errors, ctx)
        return a
    if a.name == b.name:
        return a
    if (a in (INT, FLOAT) and b in (INT, FLOAT)):
        unify_res = FLOAT
        return unify_res
    errors.append(f"Type mismatch: {a} vs {b} {ctx}")
    return ANY

class SemanticAnalyzer:
    def __init__(self):
        self.errors: List[str] = []
        self.global_sym = SymbolTable()
        self._setup_builtins()

    def _setup_builtins(self):
        pass

    def analyze(self, tree: Any) -> Tuple[Optional[Type], SymbolTable]:
        """
        tree: parse tree as returned by parser.parse(tokens)
        returns (type_of_tree, global_symbol_table)
        """
        self.errors.clear()
        self.global_sym = SymbolTable()
        self._collect_functions(tree)
        self._infer_program(tree, self.global_sym)
        return None, self.global_sym

    def _collect_functions(self, node):
        if not isinstance(node, list):
            return
        A, children = node[0], node[1]
        if A == "Program":
            for ch in children:
                self._collect_functions(ch)
        elif A == "FunctionDeclList":
            for ch in children:
                self._collect_functions(ch)
        elif A == "FunctionDecl":
            name = None
            param_nodes = None
            for c in children:
                if isinstance(c, tuple) and len(c) >= 2 and c[0] == "IDENT":
                    name = c[1]
                    break
            for c in children:
                if isinstance(c, list) and c[0] == "ParameterListOpt":
                    param_nodes = c
                    break
            params = []
            if param_nodes:
                if len(param_nodes[1])>0:
                    plist = param_nodes[1][0]
                    ids = self._gather_idents_in_paramlist(plist)
                    params = ids
            param_tvars = [TypeVar() for _ in params]
            ret_tvar = TypeVar()
            ftype = FunctionType(param_tvars, ret_tvar)
            if name:
                self.global_sym.define(name, ftype)
        else:
            for ch in children:
                if isinstance(ch, list):
                    self._collect_functions(ch)

    def _gather_idents_in_paramlist(self, plist_node):
        ids = []
        if plist_node[0] == "ParameterList":
            for ch in plist_node[1]:
                if isinstance(ch, tuple) and ch[0]=="IDENT":
                    ids.append(ch[1])
        if not ids:
            def search(node):
                if isinstance(node, tuple) and node[0]=="IDENT":
                    return [node[1]]
                if isinstance(node, list):
                    res=[]
                    for c in node[1]:
                        res += search(c)
                    return res
                return []
            ids = search(plist_node)
        return ids

    def _infer_program(self, node, sym: SymbolTable):
        if not isinstance(node, list):
            return
        A = node[0]
        if A == "Program":
            for ch in node[1]:
                self._infer_program(ch, sym)
        elif A == "FunctionDeclList":
            for ch in node[1]:
                self._infer_program(ch, sym)
        elif A == "FunctionDecl":
            name = None
            param_names = []
            block_node = None
            for c in node[1]:
                if isinstance(c, tuple) and c[0]=="IDENT":
                    if name is None:
                        name = c[1]
                        continue
                if isinstance(c, list) and c[0]=="ParameterListOpt":
                    if len(c[1])>0:
                        param_names = self._gather_idents_in_paramlist(c[1][0])
                if isinstance(c, list) and c[0]=="Block":
                    block_node = c
            sym_func = self.global_sym.lookup(name)
            if not sym_func:
                self.errors.append(f"Function {name} not declared in header collection")
                return
            ftype: FunctionType = sym_func.type
            local = SymbolTable(parent=self.global_sym)
            for pname, ptype_var in zip(param_names, ftype.param_types):
                local.define(pname, ptype_var)
            self._infer_block(block_node, local, ftype.return_type)
        else:
            for ch in node[1]:
                if isinstance(ch, list):
                    self._infer_program(ch, sym)

    def _infer_block(self, block_node, sym: SymbolTable, func_return: Type):
        if not block_node:
            return
        for c in block_node[1]:
            if isinstance(c, list) and c[0]=="StatementList":
                for st in c[1]:
                    self._infer_statement(st, sym, func_return)

    def _infer_statement(self, node, sym: SymbolTable, func_return: Type):
        if not isinstance(node, list):
            return
        A = node[0]
        if A == "Statement":
            first = node[1][0] if node[1] else None
            if isinstance(first, tuple) and first[0]=="IDENT":
                name = first[1]
                sp = node[1][1] if len(node[1])>1 else None
                if isinstance(sp, list) and sp[0]=="StatementPrime":
                    expr = self._find_node(sp, "Expression") or self._find_node(sp, "ExpressionRest")
                    if expr:
                        t = self._infer_expression(expr, sym)
                        existing = sym.lookup(name)
                        if existing:
                            unify(existing.type, t, self.errors, f"assign {name}")
                        else:
                            sym.define(name, t)
            elif isinstance(first, tuple) and first[0] in ("if","while","for","return","{",";"):
                token_type = first[0]
                if token_type == "return":
                    exprnode = self._find_node(node, "ExpressionOpt")
                    t = NULL
                    if exprnode:
                        t = self._infer_expression(exprnode, sym)
                        unify(func_return, t, self.errors, "return")
                elif token_type == "{":
                    inner = self._find_node(node, "StatementList")
                    if inner:
                        self._infer_statement(["StatementList", inner[1]], sym, func_return)
                else:
                    for ch in node[1]:
                        if isinstance(ch, list):
                            self._infer_statement(ch, sym, func_return)
        elif A == "StatementList":
            for ch in node[1]:
                self._infer_statement(ch, sym, func_return)
        else:
            # fallback: traverse children
            for ch in node[1]:
                if isinstance(ch, list):
                    self._infer_statement(ch, sym, func_return)

    def _infer_expression(self, node, sym: SymbolTable) -> Type:
        if node is None:
            return ANY
        if isinstance(node, tuple):
            if node[0] == "IDENT":
                s = sym.lookup(node[1])
                if s:
                    return s.type
                g = self.global_sym.lookup(node[1])
                if g:
                    return g.type
                tv = TypeVar()
                sym.define(node[1], tv)
                return tv
            elif node[0] in ("INT","FLOAT","STRING","true","false","null"):
                if node[0] == "INT":
                    return INT
                if node[0] == "FLOAT":
                    return FLOAT
                if node[0] == "STRING":
                    return STRING
                if node[0] == "true" or node[0]=="false":
                    return BOOL
                if node[0] == "null":
                    return NULL
            else:
                return ANY

        if isinstance(node, list):
            A = node[0]
            if A == "Expression":
                left = self._infer_expression(node[1][0], sym)
                if len(node[1])>1 and isinstance(node[1][1], list) and node[1][1][0]=="ExpressionRel":
                    rel = node[1][1]
                    if rel and len(rel[1])>0:
                        right = self._infer_expression(rel[1][1], sym)
                        unify(left, right, self.errors, "rel op")
                        return BOOL
                return left
            if A == "AddExpr":
                left = self._infer_expression(node[1][0], sym)
                if len(node[1])>1 and isinstance(node[1][1], list) and node[1][1][0]=="AddExprPrime":
                    return self._infer_addexprprime(left, node[1][1], sym)
                return left
            if A == "TermExpression":
                left = self._infer_expression(node[1][0], sym)
                if len(node[1])>1 and isinstance(node[1][1], list) and node[1][1][0]=="TermTail":
                    return self._infer_termtail(left, node[1][1], sym)
                return left
            if A == "FactorExpression":
                child = node[1][0]
                if isinstance(child, tuple):
                    if child[0] == "IDENT":
                        return self._infer_expression(child, sym)
                    if child[0] == "INT":
                        return INT
                    if child[0] == "FLOAT":
                        return FLOAT
                    if child[0] == "STRING":
                        return STRING
                    if child[0] == "true" or child[0]=="false":
                        return BOOL
                    if child[0] == "null":
                        return NULL
                if isinstance(child, list) and child[0]=="Expression":
                    return self._infer_expression(child, sym)
                if isinstance(child, tuple) and child[0]=="-":
                    inner = node[1][1] if len(node[1])>1 else None
                    t = self._infer_expression(inner, sym)
                    if not is_number_type(t):
                        self.errors.append(f"Unary - applied to non-number {t}")
                    return t
                return ANY
            if A == "ExpressionOpt":
                if len(node[1])==0:
                    return NULL
                return self._infer_expression(node[1][0], sym)
            for ch in node[1]:
                if isinstance(ch, list):
                    return self._infer_expression(ch, sym)
                if isinstance(ch, tuple) and ch[0] in ("INT","FLOAT","STRING","IDENT","true","false","null"):
                    return self._infer_expression(ch, sym)
        return ANY

    def _infer_addexprprime(self, left, node, sym):
        if not node[1]:
            return left
        op = node[1][0]
        right_node = node[1][1]
        rtype = self._infer_expression(right_node, sym)
        if op and isinstance(op, list):
            pass
        if is_number_type(left) and is_number_type(rtype):
            if resolve(left)==FLOAT or resolve(rtype)==FLOAT:
                return FLOAT
            return INT
        if resolve(left)==STRING or resolve(rtype)==STRING:
            return STRING
        return ANY

    def _infer_termtail(self, left, node, sym):
        if not node[1]:
            return left
        right_node = node[1][1]
        rtype = self._infer_expression(right_node, sym)
        if is_number_type(left) and is_number_type(rtype):
            if resolve(left)==FLOAT or resolve(rtype)==FLOAT:
                return FLOAT
            return INT
        return ANY

    def _find_node(self, node, name):
        if not isinstance(node, list):
            return None
        if node[0] == name:
            return node
        for ch in node[1]:
            if isinstance(ch, list):
                r = self._find_node(ch, name)
                if r:
                    return r
        return None
