## Conjuntos FIRST
(agrupados por não-terminais principais da BNF fornecida)

- **FIRST(Program)** = { `function`, ε }

- **FIRST(FunctionDeclarationList)** = { `function`, ε }

- **FIRST(FunctionDeclaration)** = { `function` }

- **FIRST(ParameterListOpt)** = { `Identifier`, ε }

- **FIRST(ParameterList)** = { `Identifier` }

- **FIRST(ParameterListTail)** = { `,`, ε }

- **FIRST(StatementList)** = { `Identifier`, `if`, `while`, `for`, `return`, `{`, `;`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-`, ε }
  - Observação: os símbolos `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(` e `-` aparecem porque uma `Expression` (que pode ser um `Statement` quando seguida por `;`) pode começar com esses tokens.

- **FIRST(Statement)** = { `Identifier`, `if`, `while`, `for`, `return`, `{`, `;`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FIRST(AssignmentStatement)** = { `Identifier` }

- **FIRST(ConditionalStatement)** = { `if` }

- **FIRST(ElsifPart)** = { `elsif`, ε }

- **FIRST(ElsePart)** = { `else`, ε }

- **FIRST(LoopStatement)** = { `while`, `for` }

- **FIRST(ReturnStatement)** = { `return` }

- **FIRST(ExpressionOpt)** = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-`, ε }

- **FIRST(ConditionExpression)** = FIRST(Expression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FIRST(RelationalOperator)** = { `==`, `!=`, `>`, `>=`, `<`, `<=` }

- **FIRST(Expression)** = FIRST(TermExpression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FIRST(ExpressionTail)** = { `+`, `-`, `and`, `or`, ε }

- **FIRST(AdditiveOperator)** = { `+`, `-`, `and`, `or` }

- **FIRST(TermExpression)** = FIRST(FactorExpression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FIRST(TermTail)** = { `*`, `/`, `//`, `%`, ε }

- **FIRST(MultiplicativeOperator)** = { `*`, `/`, `//`, `%` }

- **FIRST(FactorExpression)** = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FIRST(NumberLiteral)** = { `IntegerNumber`, `FloatNumber` }

- **FIRST(StringLiteral)** = { token `StringLiteral` }

- **FIRST(Identifier)** = { token `Identifier` }


> Observação: muitos FIRSTs coincidem porque a gramática está escrita com níveis de precedência explícitos (Expression → TermExpression → FactorExpression), então os símbolos iniciais de `Expression`, `TermExpression` e `FactorExpression` são os mesmos.

---

## Conjuntos FOLLOW
(para os mesmos não-terminais — incluo `$` para o final de arquivo)

- **FOLLOW(Program)** = { `$` }

- **FOLLOW(FunctionDeclarationList)** = FOLLOW(Program) = { `$` }

- **FOLLOW(FunctionDeclaration)** = { `function`, `$` }
  - explicação: em `<FunctionDeclarationList> ::= <FunctionDeclaration> <FunctionDeclarationList>`, após uma `FunctionDeclaration` pode vir outra `function` (início de próximo) ou, se a lista terminar, o FOLLOW da lista (que é `$`).

- **FOLLOW(ParameterListOpt)** = { `)` }

- **FOLLOW(ParameterList)** = { `)` }

- **FOLLOW(ParameterListTail)** = { `)` }

- **FOLLOW(StatementList)** = { `}` }
  - aparece dentro de `{ <StatementList> }`.

- **FOLLOW(Statement)** = { `Identifier`, `if`, `while`, `for`, `return`, `{`, `;`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-`, `}` }
  - justificação: `StatementList ::= Statement StatementList` faz com que o FOLLOW de `Statement` contenha FIRST(StatementList) (que inclui os mesmos símbolos que iniciam um `Statement`) e, quando a lista termina, `}` (o delimitador do bloco).

- **FOLLOW(AssignmentStatement)** = { `Identifier`, `if`, `while`, `for`, `return`, `{`, `;`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-`, `}` }
  - porque um `AssignmentStatement` aparece como um `Statement` em `StatementList`.

- **FOLLOW(ConditionalStatement)** = mesmo conjunto de `FOLLOW(AssignmentStatement)` (mesma razão — é uma forma de `Statement`).

- **FOLLOW(ElsifPart)** = FOLLOW(ConditionalStatement) (pois `ElsifPart` aparece dentro da `ConditionalStatement`) — resumido como símbolos que podem suceder a `if (...) Statement` (i.e., `elsif`, `else`, ou qualquer token que pode iniciar o próximo `Statement` ou o delimitador `}` dependendo do contexto). Para simplicidade: { `elsif`, `else`, `Identifier`, `if`, `while`, `for`, `return`, `{`, `;`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-`, `}` }.

- **FOLLOW(ElsePart)** = FOLLOW(ConditionalStatement) (mesma justificativa) — na prática inclui os mesmos símbolos que sucedem `ConditionalStatement` em um bloco.

- **FOLLOW(LoopStatement)** = mesmo conjunto de `FOLLOW(Statement)` (porque `LoopStatement` também é um `Statement`).

- **FOLLOW(ReturnStatement)** = mesmo conjunto de `FOLLOW(Statement)`.

- **FOLLOW(ExpressionOpt)** = { `;` }

- **FOLLOW(ConditionExpression)** = { `)`, `;` }
  - aparece em `if` e `while` entre parênteses; em `for`, o `ConditionExpression` é seguido por `;` (o segundo `;` do `for`). Portanto `)` e `;` aparecem em FOLLOW.

- **FOLLOW(RelationalOperator)** = FIRST(Expression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }
  - por `ConditionExpression ::= Expression RelationalOperator Expression` o que sucede um `RelationalOperator` é um `Expression`.

- **FOLLOW(Expression)** = { `==`, `!=`, `>`, `>=`, `<`, `<=`, `+`, `-`, `and`, `or`, `*`, `/`, `//`, `%`, `)`, `;`, `,`, `}` }
  - razões:
    - à esquerda numa `ConditionExpression` a seguir pode vir um `RelationalOperator`.
    - à direita numa expressão dentro de `(` `)` a seguir pode vir `)`.
    - quando `Expression` forma `Expression ";"` (statement), segue `;`.
    - em lista de parâmetros (se houvesse chamada de função) poderia ser `,` (não explicitada nas produções dadas para chamadas, mas incluí `,` caso o `Expression` apareça em contexto separado por vírgulas — no `for` o terceiro campo é um `Expression` seguido por `)` então incluí `)` também).
    - operadores multiplicativos ou aditivos podem seguir por causa de recursão esquerda-por-direita (por exemplo `Expression -> Term ExpressionTail`).

- **FOLLOW(ExpressionTail)** = FOLLOW(Expression) (pois `ExpressionTail` pode desaparecer — ε — então o que segue `Expression` segue também `ExpressionTail`).

- **FOLLOW(AdditiveOperator)** = FIRST(TermExpression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FOLLOW(TermExpression)** = { `+`, `-`, `and`, `or`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `)`, `;`, `,`, `}` }
  - porque após `TermExpression` podem vir operadores aditivos (formando `ExpressionTail`) ou comparadores (quando usado numa `ConditionExpression`) ou parênteses/terminadores finais.

- **FOLLOW(TermTail)** = FOLLOW(TermExpression)

- **FOLLOW(MultiplicativeOperator)** = FIRST(FactorExpression) = { `Identifier`, `IntegerNumber`, `FloatNumber`, `StringLiteral`, `true`, `false`, `null`, `(`, `-` }

- **FOLLOW(FactorExpression)** = { `*`, `/`, `//`, `%`, `+`, `-`, `and`, `or`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `)`, `;`, `,`, `}` }
  - razões semelhantes às do `Expression` e `TermExpression` (operadores que podem seguir um fator dentro de termos e expressões, ou fechamento de parênteses, ou terminadores `;`, etc.).

- **FOLLOW(NumberLiteral)** = FOLLOW(FactorExpression)

- **FOLLOW(StringLiteral)** = FOLLOW(FactorExpression)

- **FOLLOW(Identifier)** (quando aparece como `FactorExpression`) = FOLLOW(FactorExpression)


> Observação: os conjuntos FOLLOW acima foram expandidos para listar terminais relevantes em todos os contextos onde o não-terminal pode aparecer. Em gramáticas reais / implementações, costuma-se calcular FOLLOW por propagação iterativa; aqui dei o conjunto final resumido e explicitei as razões principais.

---

## Verificação LL(1)
**Pergunta:** a gramática é LL(1)?

**Resposta curta:** **Não, a gramática como está não é LL(1).**

**Justificativa (exemplos concretos de conflito):**

1. **Conflito entre `AssignmentStatement` e `Expression` dentro de `Statement`:**
   - `Statement ::= AssignmentStatement | ... | Expression ";" | ...`
   - `FIRST(AssignmentStatement) = { Identifier }`
   - `FIRST(Expression ";")` contém `Identifier` porque `Expression` pode começar por `Identifier`.

   Logo, `FIRST(AssignmentStatement)` ∩ `FIRST(Expression ";")` ≠ ∅ (`Identifier`), então, ao ver um token `Identifier`, o parser LL(1) com apenas 1 símbolo de lookahead não consegue decidir entre a produção de atribuição (`Identifier "=" ...`) e a produção de expressão-`Statement` (uma expressão iniciada por `Identifier`).

   Observação: em muitas implementações reais esse conflito é resolvido no analisador léxico/ sintático usando *left-factoring* ou verificando o token seguinte (lookahead extra) para ver se há um `=`; mas isso requer modificar a gramática (ou um lookahead maior que 1). Assim, **como gramática BNF pura e sem left-factoring ela não é LL(1)**.

2. **Ambiguidade/overlap envolvendo `-` (menos unário vs. binário):**
   - `FactorExpression ::= "-" FactorExpression | ...`
   - `AdditiveOperator ::= "+" | "-" | "and" | "or"`
   - `ExpressionTail ::= AdditiveOperator TermExpression ...`

   `FIRST(FactorExpression)` contém `-` (unário) e `FIRST(ExpressionTail)` contém `-` (binário). Ao analisar algo que começa com `-` dentro de um contexto onde o parser precisa decidir se trata-se de um `FactorExpression` iniciando uma expressão ou um operador aditivo conectando termos, o parser LL(1) pode ter dificuldade sem reescrever/left-factorizar ou usar contexto (por exemplo distinguir posição inicial de expressão versus posição entre termos).

3. **Operadores lógicos (`and`, `or`) aparecem em `AdditiveOperator` em um mesmo nível de `+`/`-`, o que mistura categorias e torna mais difícil criar uma tabela LL(1) unívoca sem regras adicionais de precedência.**

**Conclusão:**
- A gramática precisa de **left-factoring** (ex.: factorizar produções que começam com `Identifier` em `Statement`) e/ou remoção de ambiguidades (por exemplo, separar explicitamente `Assignment` de `Expression` em um único `Statement` através de uma produção `Statement -> Identifier StatementSuffix`), ou será necessário usar **mais de 1 token de lookahead** (LL(k), k>1) ou um analisador com outra técnica (LR(1), LALR, etc.) para parsear sem problemas.

---
