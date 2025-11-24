from dataclasses import dataclass
from typing import List

@dataclass
class Tipo:
    def mostrar(self) -> str:
        return "tipo"

@dataclass
class TipoPrimitivo(Tipo):
    nome: str
    def mostrar(self) -> str:
        return self.nome
    def igual(self, other) -> bool:
        return isinstance(other, TipoPrimitivo) and self.nome == other.nome

@dataclass
class TipoLista(Tipo):
    elemento: Tipo
    def mostrar(self) -> str:
        return f"lista<{self.elemento.mostrar()}>"

@dataclass
class TipoFuncao(Tipo):
    parametros: List[Tipo]
    retorno: Tipo
    def mostrar(self) -> str:
        params = ", ".join(p.mostrar() for p in self.parametros)
        return f"({params}) -> {self.retorno.mostrar()}"
