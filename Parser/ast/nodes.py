# nodes.py
from dataclasses import dataclass
from typing import List, Optional, Any

# Nodos mínimos — expanda conforme a gramática que você usa
@dataclass
class ASTNode:
    linha: int

@dataclass
class ProgramaNode(ASTNode):
    declaracoes: List[Any]

@dataclass
class DeclaracaoFuncaoNode(ASTNode):
    nome: str
    parametros: List[str]
    corpo: List[Any]
    linha: int
    def __init__(self, nome, parametros, corpo, linha):
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo
        self.linha = linha

@dataclass
class IdentificadorNode(ASTNode):
    nome: str
    linha: int

@dataclass
class LiteralNode(ASTNode):
    valor: Any
    tipo: str
    linha: int

@dataclass
class AtribuicaoNode(ASTNode):
    nome: str
    valor: Any
    linha: int

# converter simples do parse tree (lista) para AST minimalista
def convert_parse_tree(pt) -> ProgramaNode:
    # pt is [Program, children]
    # This converter is intentionally simple: detect function declarations only (example)
    root = ProgramaNode(declaracoes=[], linha=1)
    if pt[0] != "Program":
        raise ValueError("esperava Program")
    fdecls = pt[1][0]  # FunctionDeclList
    # walk FunctionDeclList recursively
    def walk_FDL(node):
        # node = ['FunctionDeclList', [child1, child2...]]
        if node[0] != "FunctionDeclList":
            return
        children = node[1]
        for child in children:
            if isinstance(child, list) and child and child[0] == "FunctionDecl":
                fd = child
                # child structure: ['FunctionDecl', [ ('function',), ('IDENT',), ('(',), ('ParameterListOpt', ...), (')',), ('Block',...) ]]
                # Extract name
                elems = fd[1]
                name_tok = elems[1] if len(elems)>1 else None
                name = None
                if isinstance(name_tok, tuple):
                    name = name_tok[0]  # not perfect, but we keep example
                # simplified: append empty function node
                root.declaracoes.append(DeclaracaoFuncaoNode(name or "f", [], [], 1))
            else:
                # could be recursive FunctionDeclList
                if isinstance(child, list) and child and child[0] == "FunctionDeclList":
                    walk_FDL(child)
    walk_FDL(fdecls)
    return root
