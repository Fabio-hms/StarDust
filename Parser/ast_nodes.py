# stardust_ll1/ast_nodes.py
from dataclasses import dataclass
from typing import List, Optional, Any, Tuple

@dataclass
class Node: pass

@dataclass
class Program(Node):
    items: List[Any]

@dataclass
class FunctionDecl(Node):
    name: str
    params: List[str]
    body: Any

@dataclass
class Block(Node):
    statements: List[Any]

@dataclass
class ReturnStmt(Node):
    expr: Optional[Any]

@dataclass
class IfStmt(Node):
    cond: Any
    then_branch: Block
    elsif_branches: List[Tuple[Any, Block]]
    else_branch: Optional[Block]

@dataclass
class WhileStmt(Node):
    cond: Any
    body: Block

@dataclass
class ForStmt(Node):
    init: Optional[Any]
    cond: Optional[Any]
    step: Optional[Any]
    body: Block

@dataclass
class ExprStmt(Node):
    expr: Any

@dataclass
class Assign(Node):
    target: str
    value: Any

@dataclass
class Call(Node):
    callee: Any
    args: List[Any]

@dataclass
class BinaryOp(Node):
    op: str
    left: Any
    right: Any

@dataclass
class UnaryOp(Node):
    op: str
    operand: Any

@dataclass
class Literal(Node):
    value: Any

@dataclass
class Identifier(Node):
    name: str
