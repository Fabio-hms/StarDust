from llvmlite import ir, binding
from codegen.gerador_codigo import GeradorCodigo

class DeclaracaoFuncaoNode:
    def __init__(self, nome, parametros, tipoRetorno, corpo):
        self.nome = nome
        self.parametros = parametros
        self.tipoRetorno = tipoRetorno
        self.corpo = corpo

def main():
    prog = []
    f = DeclaracaoFuncaoNode(nome="main", parametros=[], tipoRetorno="int", corpo=[])
    prog.append(f)
    gen = GeradorCodigo()
    # gerador expects a programa node with declaracoes attribute OR accepts list? It expects 'ast' in gerar to have 'declaracoes'
    class Programa:
        def __init__(self, decls):
            self.declaracoes = decls
    programa = Programa(prog)
    ll = gen.gerar(programa)
    print("Generated LLVM IR (truncated):")
    print(ll[:800])

if __name__ == "__main__":
    main()
