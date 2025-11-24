from llvmlite import ir, binding

class GeradorCodigo:
    def __init__(self):
        self.modulo = ir.Module(name="module")
        self.builder = None
        self.funcao_atual = None
        self.simbolos = {}
        self._inicializar_llvm()

    def _inicializar_llvm(self):
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

    def gerar(self, ast):
        return self._gerar_programa(ast)

    def _gerar_programa(self, programa):
        for decl in programa.declaracoes:
            self._gerar_declaracao(decl)
        return str(self.modulo)

    def _gerar_declaracao(self, decl):
        metodo = "_gerar_" + decl.__class__.__name__
        return getattr(self, metodo)(decl)

    def _gerar_DeclaracaoFuncaoNode(self, func):
        tipo_retorno = ir.IntType(32) if func.tipoRetorno == "int" else ir.VoidType()

        tipos_params = [ir.IntType(32) for _ in func.parametros]
        tipo_func = ir.FunctionType(tipo_retorno, tipos_params)
        funcao = ir.Function(self.modulo, tipo_func, name=func.nome)

        bloco = funcao.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(bloco)
        self.funcao_atual = funcao

        for i, param in enumerate(func.parametros):
            self.simbolos[param.nome] = funcao.args[i]

        for comando in func.corpo:
            self._gerar_comando(comando)

        if not self.builder.block.is_terminated:
            if isinstance(tipo_retorno, ir.VoidType):
                self.builder.ret_void()
            else:
                self.builder.ret(ir.IntType(32)(0))

    def _gerar_comando(self, comando):
        metodo = "_gerar_" + comando.__class__.__name__
        return getattr(self, metodo)(comando)

    def _gerar_AtribuicaoNode(self, atrib):
        valor = self._gerar_expressao(atrib.valor)
        var = self.builder.alloca(ir.IntType(32), name=atrib.variavel)
        self.builder.store(valor, var)
        self.simbolos[atrib.variavel] = var

    def _gerar_RetornaNode(self, ret):
        if ret.valor:
            valor = self._gerar_expressao(ret.valor)
            self.builder.ret(valor)
        else:
            self.builder.ret_void()

    def _gerar_expressao(self, expr):
        metodo = "_gerar_" + expr.__class__.__name__
        return getattr(self, metodo)(expr)

    def _gerar_LiteralInteiroNode(self, lit):
        return ir.IntType(32)(lit.valor)

    def _gerar_IdentificadorNode(self, ident):
        ptr = self.simbolos.get(ident.nome)
        return self.builder.load(ptr)

    def _gerar_ExpressaoBinariaNode(self, bin):
        esq = self._gerar_expressao(bin.esquerda)
        dir = self._gerar_expressao(bin.direita)

        if bin.operador == "+":
            return self.builder.add(esq, dir)
        if bin.operador == "-":
            return self.builder.sub(esq, dir)
        if bin.operador == "*":
            return self.builder.mul(esq, dir)
        if bin.operador == "/":
            return self.builder.sdiv(esq, dir)

        raise Exception("Operador não suportado")
