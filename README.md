Um compilador educacional da linguagem StarDust, contendo:

Analisador Léxico (Lexer)

Analisador Sintático LL(1)

Geração de Árvore Sintática (AST)

Analisador Semântico

Gerador de Código LLVM IR

Este repositório demonstra um pipeline completo de compilador, totalmente implementado em Python.

🔧 Requisitos
Componente	Versão Recomendada
Python	3.12.x
LLVM (opc.)	clang + llc para gerar executáveis
llvmlite	compatível com Python 3.12

⚠️ Python 3.13 e 3.14 NÃO devem ser usados (llvmlite não suporta).

🚀 Instalação
🟦 Windows
1. Navegue até a pasta do projeto:
cd "C:\Users\pedro\Downloads\StarDust_fixed"

2. Crie o ambiente virtual:
py -3.12 -m venv venv

3. Ative:
.\venv\Scripts\activate

4. Instale o llvmlite:
pip install llvmlite


🧪 Como Rodar Cada Etapa do Compilador

Todas as execuções devem ser feitas na raiz do projeto.

🔹 1. Analisador Léxico
python Lexer/main.py

🔹 2. Parser LL(1) — (OFICIAL)

⚠️ Deve ser executado como módulo, nunca como arquivo.

python -m Parser.stardust_ll1.main

🔹 3. AST Legada (opcional)
python Parser/ast/main.py

🔹 4. CodeGen

O codegen usa imports relativos — então NÃO execute:

python codegen/main.py   # ERRADO


Execute assim:

python -m codegen.main

🧵 Gerar LLVM IR em arquivo
python -m codegen.main > saida.ll

⚙️ Gerar Executável (opcional)

Requer llc e clang instalados.

llc saida.ll -filetype=obj -o saida.obj
clang saida.obj -o saida.exe


Executar:

.\saida.exe

🗂 Diagramas

Diagrama do AFD está em:

diagramas/afd_final.md

🧠 Sobre o Projeto

Este compilador implementa:

Autômato Finito Determinístico (AFD)

Tabela LL(1)

Parse Tree

AST simples

Analisador Semântico

Geração de IR com llvmlite

Ideal para estudos de linguagens e compiladores.


Se falhar, instale via wheel:

pip install llvmlite-*-cp312-win_amd64.whl
