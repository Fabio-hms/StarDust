from dataclasses import dataclass
from typing import List, Optional, Any


# ====== BASE ======
@dataclass
class ASTNode:
    line: int
    column: int


# ====== PROGRAMA ======
@dataclass
class Program(ASTNode):
    functions: List["FunctionDecl"]


# ====== FUNÇÕES ======
@dataclass
class Parameter(ASTNode):
    name: str


@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List[Parameter]
    body: List["Statement"]


# ====== STATEMENTS ======

class Statement(ASTNode):
    pass


@dataclass
class Block(Statement):
    statements: List[Statement]


@dataclass
class ReturnStatement(Statement):
    expression: Optional["Expression"]


@dataclass
class ExpressionStatement(Statement):
    expression: "Expression"


@dataclass
class Assignment(Statement):
    name: str
    expression: "Expression"


# ====== EXPRESSÕES ======

class Expression(ASTNode):
    pass


@dataclass
class BinaryExpr(Expression):
    left: Expression
    op: str
    right: Expression


@dataclass
class UnaryExpr(Expression):
    op: str
    right: Expression


@dataclass
class Literal(Expression):
    value: Any


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class FunctionCall(Expression):
    name: str
    args: List[Expression]
