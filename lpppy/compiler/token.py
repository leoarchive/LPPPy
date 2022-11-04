from enum import Enum


class TokenKeys:
    programa = "programa"
    var = "var"
    caractere = "caractere"
    real = "real"
    inicio = "início"
    fim = "fim"
    conjunto = "conjunto"
    entao = "então"
    senao = "senão"
    dPeriod = ".."
    de = "de"
    se = "se"
    inteiro = "inteiro"
    leia = "leia"
    escreva = "escreva"
    rArrow = "←"
    lArrow = "→"
    colon = ":"
    rSquare = "]"
    lSquare = "["
    comma = ","
    _and = ".E."
    _not = ".NÃO."
    _or = ".OU."
    graterEq = ">="
    lessEq = "<="
    less = "<"
    grater = ">"
    NotEq = "<>"
    equal = "="
    plus = "+"
    minus = "-"
    mult = "*"
    div = "/"
    rParen = ")"
    lParen = "("
    fimse = "fim_se"
    para = "para"
    fimpara = "fim_para"
    ate = "até"
    passo = "passo"
    faca = "faça"
    mod = "%"
    exponent = "↑"
    enquanto = "enquanto"
    fimenq = "fim_enquanto"
    procedimento = "procedimento"
    null = "nulo"
    funcao = "função"
    tipo = "tipo"
    registro = "registro"
    fimreg = "fim_registro"
    logico = "lógico"
    falso = ".Falso."
    verdadeiro = ".Verdadeiro."


class TokenTypes(Enum):
    id = 1
    numb = 2
    lArrow = 3
    rArrow = 4
    programa = 5
    var = 6
    colon = 7
    dType = 8
    inicio = 9
    fim = 10
    rSquare = 11
    lSquare = 12
    dPeriod = 13
    de = 14
    comma = 15
    leia = 16
    escreva = 17
    str = 18
    logicalOps = 19
    mathOps = 20
    se = 21
    lParen = 22
    rParen = 23
    entao = 24
    fimse = 25
    senao = 26
    conjunto = 27
    para = 28
    fimpara = 29
    ate = 30
    passo = 31
    faca = 32
    exponent = 33
    enquanto = 34
    fimenq = 35
    procedimento = 36
    null = 37
    funcao = 38
    tipo = 39
    registro = 40
    fimreg = 41
    logico = 42
    falso = 43
    verdadeiro = 44


class Token:
    key = ""
    type = 0
    line = 0

    def __init__(self, key: TokenKeys, type: TokenTypes, line: int) -> None:
        self.key = key
        self.type = type
        self.line = line

    def getType(key: TokenKeys) -> TokenTypes:
        match key: 
            case TokenKeys.var:
                return TokenTypes.var
            case TokenKeys.programa:
                return TokenTypes.programa
            case TokenKeys.inicio:
                return TokenTypes.inicio
            case TokenKeys.leia:
                return TokenTypes.leia
            case TokenKeys.escreva:
                return TokenTypes.escreva
            case TokenKeys.fim:
                return TokenTypes.fim
            case TokenKeys.se:
                return TokenTypes.se
            case TokenKeys.entao:
                return TokenTypes.entao
            case TokenKeys.tipo:
                return TokenTypes.tipo
            case TokenKeys.registro:
                return TokenTypes.registro
            case TokenKeys.senao:
                return TokenTypes.senao
            case TokenKeys.fimse:
                return TokenTypes.fimse
            case TokenKeys.rArrow:
                return TokenTypes.rArrow
            case TokenKeys.lArrow:
                return TokenTypes.lArrow
            case TokenKeys.colon:
                return TokenTypes.colon
            case TokenKeys.dPeriod:
                return TokenTypes.dPeriod
            case TokenKeys.comma:
                return TokenTypes.comma
            case TokenKeys.rSquare:
                return TokenTypes.rSquare
            case TokenKeys.lSquare:
                return TokenTypes.lSquare
            case TokenKeys.rParen:
                return TokenTypes.rParen
            case TokenKeys.lParen:
                return TokenTypes.lParen
            case TokenKeys.de:
                return TokenTypes.de
            case TokenKeys.para:
                return TokenTypes.para
            case TokenKeys.fimpara:
                return TokenTypes.fimpara
            case TokenKeys.fimreg:
                return TokenTypes.fimreg
            case TokenKeys.ate:
                return TokenTypes.ate
            case TokenKeys.passo:
                return TokenTypes.passo
            case TokenKeys.enquanto:
                return TokenTypes.enquanto
            case TokenKeys.fimenq:
                return TokenTypes.fimenq
            case TokenKeys.procedimento:
                return TokenTypes.procedimento
            case TokenKeys.funcao:
                return TokenTypes.funcao
            case TokenKeys.faca:
                return TokenTypes.faca
            case TokenKeys.caractere | TokenKeys.real | TokenKeys.inteiro | TokenKeys.conjunto | TokenKeys.logico:
                return TokenTypes.dType
            case TokenKeys._and | TokenKeys._or | TokenKeys._not | TokenKeys.grater | TokenKeys.graterEq | TokenKeys.less | TokenKeys.lessEq | TokenKeys.NotEq | TokenKeys.equal:
                return TokenTypes.logicalOps
            case TokenKeys.plus | TokenKeys.minus | TokenKeys.mult | TokenKeys.div | TokenKeys.mod | TokenKeys.exponent:
                return TokenTypes.mathOps
            case _:
                return TokenTypes.id
