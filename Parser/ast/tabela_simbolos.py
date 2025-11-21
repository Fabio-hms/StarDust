# tabela_simbolos.py
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

@dataclass
class Simbolo:
    nome: str
    tipo: str
    linha: int
    categoria: str = "variavel"
    inicializado: bool = False

class TabelaSimbolos:
    def __init__(self):
        self._pilha: List[Dict[str, Simbolo]] = [{}]

    def entrar_escopo(self):
        self._pilha.append({})

    def sair_escopo(self):
        if len(self._pilha) > 1:
            self._pilha.pop()

    def declarar(self, nome: str, tipo: str, linha: int, categoria="variavel", inicializado=False) -> bool:
        atual = self._pilha[-1]
        if nome in atual:
            return False
        atual[nome] = Simbolo(nome, tipo, linha, categoria, inicializado)
        return True

    def buscar(self, nome: str) -> Optional[Simbolo]:
        for escopo in reversed(self._pilha):
            if nome in escopo:
                return escopo[nome]
        return None

    def buscar_no_escopo_atual(self, nome: str) -> Optional[Simbolo]:
        return self._pilha[-1].get(nome)

    def obter_todos_simbolos(self) -> List[Simbolo]:
        res = []
        for esc in self._pilha:
            res.extend(list(esc.values()))
        return res
