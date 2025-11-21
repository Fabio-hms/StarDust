# ==========================
#   SISTEMA DE TIPOS
# ==========================

class Tipo:
    def mostrar(self):
        raise NotImplementedError()

    def igual(self, outro):
        return self.mostrar() == outro.mostrar()


class TipoPrimitivo(Tipo):
    def __init__(self, nome):
        self.nome = nome  # inteiro, real, texto, booleano, void, erro

    def mostrar(self):
        return self.nome


class TipoLista(Tipo):
    def __init__(self, tipo_elemento):
        self.tipo_elemento = tipo_elemento

    def mostrar(self):
        return f"lista<{self.tipo_elemento.mostrar()}>"


class TipoFuncao(Tipo):
    def __init__(self, parametros, retorno):
        self.parametros = parametros  # lista de Tipo
        self.retorno = retorno        # Tipo

    def mostrar(self):
        params = ", ".join(p.mostrar() for p in self.parametros)
        return f"({params}) -> {self.retorno.mostrar()}"
