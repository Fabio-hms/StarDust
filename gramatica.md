G = (V, Σ, P, S)


  V (variáveis / não-terminais):
    `{Program, FunctionDeclaration, Statement, Expression, TermExpression, FactorExpression, ConditionExpression, RelationalOperator, AssignmentOperator, AdditiveOperator, MultiplicativeOperator, Identifier, NumberLiteral, StringLiteral, BooleanLiteral}`

  Σ (terminais): Palavras reservadas, operadores, delimitadores e identificadores:
    `{if, else, elsif, for, while, return, def, function, true, false, null, and, or,
      Identifier, IntegerNumber, FloatNumber, StringLiteral, 
      +, -, *, /, //, %, ==, !=, >, >=, <, <=, =, 
      (, ), {, }, ;}`

  S (símbolo inicial):
    `Program`

  P (regras de produção):
    O conjunto de produções segue abaixo, no formato EBNF.




Program                 = { FunctionDeclaration } .

FunctionDeclaration     = "function" Identifier "(" [ ParameterList ] ")" "{" { Statement } "}" .

ParameterList           = Identifier { "," Identifier } .

Statement               = AssignmentStatement
                        | ConditionalStatement
                        | LoopStatement
                        | ReturnStatement
                        | Expression ";"
                        | "{" { Statement } "}"
                        | ";" .

AssignmentStatement     = Identifier AssignmentOperator Expression ";" .

ConditionalStatement    = "if" "(" ConditionExpression ")" Statement 
                        { "elsif" "(" ConditionExpression ")" Statement } 
                        [ "else" Statement ] .

LoopStatement           = "while" "(" ConditionExpression ")" Statement
                        | "for" "(" AssignmentStatement ConditionExpression ";" Expression ")" Statement .

ReturnStatement         = "return" [ Expression ] ";" .

ConditionExpression     = Expression RelationalOperator Expression .
RelationalOperator      = "==" | "!=" | ">" | ">=" | "<" | "<=" .

Expression              = TermExpression { AdditiveOperator TermExpression } .
AdditiveOperator        = "+" | "-" | "and" | "or" .

TermExpression          = FactorExpression { MultiplicativeOperator FactorExpression } .
MultiplicativeOperator  = "*" | "/" | "//" | "%" .

FactorExpression        = Identifier
                        | NumberLiteral
                        | StringLiteral
                        | BooleanLiteral
                        | "null"
                        | "(" Expression ")"
                        | "-" FactorExpression .

AssignmentOperator      = "=" .

NumberLiteral           = IntegerNumber | FloatNumber .

BooleanLiteral          = "true" | "false" .

Identifier              = Letter { Letter | Digit | "_" } .
Letter                  = "A" | ... | "Z" | "a" | ... | "z" .
Digit                   = "0" | ... | "9" .
StringLiteral           = '"' { qualquer_caractere_exceto_"_ou_\ } '"' 
                        | "'" { qualquer_caractere_exceto_'_ou_\ } "'" .



<Program>                   ::= <FunctionDeclarationList>

<FunctionDeclarationList>    ::= <FunctionDeclaration> <FunctionDeclarationList> | ε

<FunctionDeclaration>        ::= "function" Identifier "(" <ParameterListOpt> ")" "{" <StatementList> "}"

<ParameterListOpt>           ::= <ParameterList> | ε

<ParameterList>              ::= Identifier <ParameterListTail>

<ParameterListTail>          ::= "," Identifier <ParameterListTail> | ε

<StatementList>              ::= <Statement> <StatementList> | ε

<Statement>                  ::= <AssignmentStatement>
                               | <ConditionalStatement>
                               | <LoopStatement>
                               | <ReturnStatement>
                               | <Expression> ";"
                               | "{" <StatementList> "}"
                               | ";"

<AssignmentStatement>        ::= Identifier "=" <Expression> ";"

<ConditionalStatement>       ::= "if" "(" <ConditionExpression> ")" <Statement> <ElsifPart> <ElsePart>

<ElsifPart>                  ::= "elsif" "(" <ConditionExpression> ")" <Statement> <ElsifPart> | ε

<ElsePart>                   ::= "else" <Statement> | ε

<LoopStatement>              ::= "while" "(" <ConditionExpression> ")" <Statement>
                               | "for" "(" <AssignmentStatement> <ConditionExpression> ";" <Expression> ")" <Statement>

<ReturnStatement>            ::= "return" <ExpressionOpt> ";"

<ExpressionOpt>              ::= <Expression> | ε

<ConditionExpression>        ::= <Expression> <RelationalOperator> <Expression>

<RelationalOperator>         ::= "==" | "!=" | ">" | ">=" | "<" | "<="

<Expression>                 ::= <TermExpression> <ExpressionTail>

<ExpressionTail>             ::= <AdditiveOperator> <TermExpression> <ExpressionTail> | ε

<AdditiveOperator>           ::= "+" | "-" | "and" | "or"

<TermExpression>             ::= <FactorExpression> <TermTail>

<TermTail>                   ::= <MultiplicativeOperator> <FactorExpression> <TermTail> | ε

<MultiplicativeOperator>     ::= "*" | "/" | "//" | "%"

<FactorExpression>           ::= Identifier
                               | <NumberLiteral>
                               | <StringLiteral>
                               | "true"
                               | "false"
                               | "null"
                               | "(" <Expression> ")"
                               | "-" <FactorExpression>

<NumberLiteral>              ::= <IntegerNumber> | <FloatNumber>

<IntegerNumber>              ::= [+-]? Digit { Digit }

<FloatNumber>                ::= [+-]? ( Digit+ "." Digit* | "." Digit+ ) [ ( "e" | "E" ) [+-]? Digit+ ]

<StringLiteral>              ::= '"' { any_char_except_"_or_\ } '"' 
                               | "'" { any_char_except_'_or_\ } "'"

<Identifier>                 ::= [a-z_] { [a-zA-Z0-9_] }


