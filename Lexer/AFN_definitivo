stateDiagram-v2
    [*] --> qa0
    qa0 --> qa1: [a-z_]
    qa1 --> qa1: [a-zA-Z0-9_]
    qa1 --> [*]: Fim
    [*] --> qn0
    qn0 --> qn1: [+-]
    qn0 --> qn2: [0-9]
    qn1 --> qn2: [0-9]
    qn2 --> qn2: [0-9]
    qn2 --> [*]: Fim
    [*] --> qo0
    qo0 --> qo1: [+-]
    qo0 --> qo2: [0-9]
    qo0 --> qo3: "."
    qo1 --> qo2: [0-9]
    qo1 --> qo3: "."
    qo2 --> qo2: [0-9]
    qo2 --> qo4: "."
    qo3 --> qo5: [0-9]
    qo4 --> qo5: [0-9]
    qo5 --> qo5: [0-9]
    qo5 --> qo6: [eE]
    qo6 --> qo7: [+-]
    qo6 --> qo8: [0-9]
    qo7 --> qo8: [0-9]
    qo8 --> qo8: [0-9]
    qo8 --> [*]: Fim
    qo5 --> [*]: Fim
    [*] --> qs0
    qs0 --> qs1: "'"
    qs1 --> qs1: caractere ≠ ' e ≠ \
    qs1 --> qs2: "\"
    qs2 --> qs1: qualquer caractere
    qs1 --> qsf: "'"
    qsf --> [*]: Fim
    [*] --> qss0
    qss0 --> qss1: '"'
    qss1 --> qss1: caractere ≠ " e ≠ \
    qss1 --> qss2: "\"
    qss2 --> qss1: qualquer caractere
    qss1 --> qssf: '"'
    qssf --> [*]: Fim
    [*] --> qop0
    qop0 --> qig1: "="
    qop0 --> qdif1: "!"
    qop0 --> qmai1: ">"
    oop0 --> qmen1: "<"
    qop0 --> qmais1: "+"
    qop0 --> qmenos1: "-"
    qop0 --> qmult1: "*"
    qop0 --> qdiv1: "/"
    qop0 --> qmod1: "%"
    qig1 --> qig2: "="
    qdif1 --> qig2: "="
    qmai1 --> qig2: "="
    qmen1 --> qig2: "="
    qdiv1 --> qdiv2: "/"
    qig2 --> [*]: Fim
    qdiv2 --> [*]: Fim
    qig1 --> [*]: Fim
    qdif1 --> [*]: Fim
    qmai1 --> [*]: Fim
    qmen1 --> [*]: Fim
    qmais1 --> [*]: Fim
    qmenos1 --> [*]: Fim
    qmult1 --> [*]: Fim
    qdiv1 --> [*]: Fim
    qmod1 --> [*]: Fim
    [*] --> qpt0
    qpt0 --> qpt1: "("
    qpt1 --> [*]: Fim
    qpt0 --> qpt1: ")"
    qpt1 --> [*]: Fim
    qpt0 --> qpt1: "{"
    qpt1 --> [*]: Fim
    qpt0 --> qpt1: "}"
    qpt1 --> [*]: Fim
    qpt0 --> qpt1: ";"
    qpt1 --> [*]: Fim
   [*] --> qst0
    qst0 --> qst1: "\""
    qst1 --> qst1: caractere ≠ "\"" && caractere ≠ "\n"
    qst1 --> qst2: "\""
    qst2 --> [*]: Fim
    [*] --> qsb0
    qsb0 --> qsb1: "/"
    qsb1 --> qsb2: "*"
    qsb2 --> qsb2: caractere ≠ "*"
    qsb2 --> qsb3: "*"
    qsb3 --> qsb3: "*"
    qsb3 --> qsb2: caractere ≠ "*"
    qsb3 --> qsbf: "/"
    qsbf --> [*]: Fim
