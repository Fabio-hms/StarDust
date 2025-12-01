from llvmlite import binding

class Otimizador:
    def __init__(self):
        self.passes = binding.PassManagerBuilder()
        self.passes.opt_level = 3
        self.module_pm = binding.ModulePassManager()
        self.passes.populate(self.module_pm)

    def otimizar(self, llvm_ir):
        modulo = binding.parse_assembly(llvm_ir)
        modulo.verify()
        self.module_pm.run(modulo)
        return str(modulo)
