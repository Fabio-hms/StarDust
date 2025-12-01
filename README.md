# 🌌 StarDust — Compilador Educacional

O **StarDust** é um compilador educacional completo escrito em Python, projetado para demonstrar todas as etapas essenciais do processo de compilação:

- 🔤 **Analisador Léxico (Lexer)**
- 📘 **Analisador Sintático LL(1)**
- 🌳 **Geração da Árvore Sintática (AST)**
- 🧠 **Analisador Semântico**
- ⚙️ **Gerador de Código LLVM IR**

Este repositório implementa um pipeline funcional e serve como base para estudos de compiladores, linguagens formais e teoria de parsing.

---

# 🔧 Requisitos

| Componente | Versão Recomendada |
|-----------|---------------------|
| **Python** | 3.12.x |
| **LLVM** (opcional) | `clang` + `llc` para gerar executáveis |
| **llvmlite** | Compatível com Python 3.12 |

⚠️ **Python 3.13 e 3.14 não são suportados**, pois o `llvmlite` ainda não oferece compatibilidade completa.

---

# 🚀 Instalação (Windows)

### 1. Entre na pasta do projeto:
```powershell
cd "C:\Users\pedro\Downloads\StarDust_fixed"
2. Crie o ambiente virtual:
powershell
Copiar código
py -3.12 -m venv venv
3. Ative o ambiente:
powershell
Copiar código
.\venv\Scripts\activate
4. Instale o llvmlite:
powershell
Copiar código
pip install llvmlite
Se falhar, instale manualmente:

powershell
Copiar código
pip install llvmlite-*-cp312-win_amd64.whl
🧪 Como Rodar Cada Etapa do Compilador
⚠️ Execute sempre a partir da raiz do projeto.

🔹 1. Analisador Léxico
powershell
Copiar código
python Lexer/main.py
🔹 2. Analisador Sintático LL(1) (OFICIAL)
⚠️ Nunca execute o arquivo diretamente.
Use o módulo:

powershell
Copiar código
python -m Parser.stardust_ll1.main
🔹 3. AST Legada (Opcional)
powershell
Copiar código
python Parser/ast/main.py
🔹 4. Gerador de Código LLVM IR (CodeGen)
⚠️ O codegen contém imports relativos — não execute assim:

powershell
Copiar código
python codegen/main.py   # ❌ INCORRETO
Execute corretamente como módulo:

powershell
Copiar código
python -m codegen.main
🧵 Gerar um Arquivo LLVM IR
powershell
Copiar código
python -m codegen.main > saida.ll
⚙️ Gerar Executável (Opcional)
Requer llc + clang.

1. Gerar objeto:
powershell
Copiar código
llc saida.ll -filetype=obj -o saida.obj
2. Lincar:
powershell
Copiar código
clang saida.obj -o saida.exe
3. Executar:
powershell
Copiar código
.\saida.exe
🗂 Diagramas
O diagrama AFD da linguagem StarDust está em:

bash
Copiar código
diagramas/afd_final.md
🧠 Sobre o Projeto
Este compilador implementa:

Autômato Finito Determinístico (AFD)

Tabela LL(1)

Parse Tree

AST Simplificada

Analisador Semântico

Geração de IR com llvmlite

📘 Ideal para estudos de:
Compiladores, teoria de linguagens, sintaxe formal, análise semântica e geração de código.
