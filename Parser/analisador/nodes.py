from dataclasses import dataclass
from typing import List, Optional, Any

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

def convert_parse_tree(pt) -> ProgramaNode:
    root = ProgramaNode(declaracoes=[], linha=1)
    if pt[0] != "Program":
        raise ValueError("esperava Program")
    fdecls = pt[1][0]
    def walk_FDL(node):
        if node[0] != "FunctionDeclList":
            return
        children = node[1]
        for child in children:
            if isinstance(child, list) and child and child[0] == "FunctionDecl":
                fd = child
                elems = fd[1]
                name_tok = elems[1] if len(elems)>1 else None
                name = None
                if isinstance(name_tok, tuple):
                    name = name_tok[0]
                root.declaracoes.append(DeclaracaoFuncaoNode(name or "f", [], [], 1))
            else:
                if isinstance(child, list) and child and child[0] == "FunctionDeclList":
                    walk_FDL(child)
    walk_FDL(fdecls)
    return root
