# ==========================
#   TABELA DE SÍMBOLOS
# ==========================

class Simbolo:
    def __init__(self, nome, tipo, linha, categoria="variavel", inicializado=False):
        self.nome = nome
        self.tipo = tipo     # string do tipo
        self.linha = linha
        self.categoria = categoria
        self.inicializado = inicializado


class Escopo:
    def __init__(self):
        self.simbolos = {}

    def declarar(self, simbolo: Simbolo):
        if simbolo.nome in self.simbolos:
            return False
        self.simbolos[simbolo.nome] = simbolo
        return True

    def buscar(self, nome: str):
        return self.simbolos.get(nome)

    def todos(self):
        return list(self.simbolos.values())


class TabelaSimbolos:
    def __init__(self):
        self.pilha = [Escopo()]  # escopo global

    # --- Escopos ---
    def entrar_escopo(self):
        self.pilha.append(Escopo())

    def sair_escopo(self):
        self.pilha.pop()

    # --- Declaração ---
    def declarar(self, nome, tipo, linha, categoria="variavel", inicializado=False):
        simbolo = Simbolo(nome, tipo, linha, categoria, inicializado)
        return self.pilha[-1].declarar(simbolo)

    # --- Busca ---
    def buscar(self, nome):
        for escopo in reversed(self.pilha):
            s = escopo.buscar(nome)
            if s:
                return s
        return None

    def buscar_no_escopo_atual(self, nome):
        return self.pilha[-1].buscar(nome)

    def obter_todos_os_simbolos(self):
        todos = []
        for e in self.pilha:
            todos.extend(e.todos())
        return todos
