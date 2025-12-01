from tabela_simbolos import TabelaSimbolos
from tipos import TipoPrimitivo, TipoFuncao
from nodes import ProgramaNode, DeclaracaoFuncaoNode
from typing import List

class ErroSemantico(Exception):
    pass

class AnalisadorSemantico:
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.erros: List[str] = []

    def analisar(self, programa: ProgramaNode):
        for decl in programa.declaracoes:
            if isinstance(decl, DeclaracaoFuncaoNode):
                nome = decl.nome
                if not self.tabela.declarar(nome, "(...) -> void", decl.linha, categoria="funcao", inicializado=True):
                    self.erros.append(f"Função {nome} redeclarada na linha {decl.linha}")

    def tem_erros(self):
        return len(self.erros) > 0
