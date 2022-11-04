from lpppy.compiler.error import Error, ErrorTypes
from lpppy.compiler.token import Token, TokenTypes, TokenKeys


class Lexer:
    stdin: str = ""
    index: int = 0
    line: int = 1

    keyWords: TokenKeys = [
        TokenKeys.programa,
        TokenKeys.var,
        TokenKeys.leia,
        TokenKeys.escreva,
        TokenKeys.caractere,
        TokenKeys.real,
        TokenKeys.inicio,
        TokenKeys.fim,
        TokenKeys.conjunto,
        TokenKeys.dPeriod,
        TokenKeys.de,
        TokenKeys.se,
        TokenKeys.inteiro,
        TokenKeys.entao,
        TokenKeys.graterEq,
        TokenKeys.lessEq,
        TokenKeys.NotEq,
        TokenKeys.fimse,
        TokenKeys.senao,
        TokenKeys._and,
        TokenKeys._not,
        TokenKeys._or,
        TokenKeys.grater,
        TokenKeys.less,
        TokenKeys.equal,
        TokenKeys.para,
        TokenKeys.fimpara,
        TokenKeys.ate,
        TokenKeys.passo,
        TokenKeys.faca,
        TokenKeys.enquanto,
        TokenKeys.fimenq,
        TokenKeys.procedimento,
        TokenKeys.null,
        TokenKeys.funcao,
        TokenKeys.tipo,
        TokenKeys.registro,
        TokenKeys.fimreg,
        TokenKeys.logico,
        TokenKeys.falso,
        TokenKeys.verdadeiro,
    ]
    keyChars: TokenKeys = [
        TokenKeys.mod,
        TokenKeys.minus,
        TokenKeys.plus,
        TokenKeys.mult,
        TokenKeys.div,
        TokenKeys.rArrow,
        TokenKeys.lArrow,
        TokenKeys.rParen,
        TokenKeys.lParen,
        TokenKeys.colon,
        TokenKeys.rSquare,
        TokenKeys.comma,
        TokenKeys.lSquare,
        TokenKeys.exponent,
    ]
    chars: list[str] = ["\n"]

    def __init__(self, stdin: str) -> None:
        self.stdin = stdin

    def lex_dotwords(self) -> Token:
        start = self.index
        self.index += 1

        while self.stdin[self.index] != ".":
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        self.index += 1
        key = self.stdin[start : self.index]
        token = self.lex_keyword(key)
        if token:
            return token
        return Token(key, TokenTypes.id, self.line)

    def lex_string(self) -> Token:
        start = self.index
        self.index += 1

        while self.stdin[self.index] != '"':
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        self.index += 1

        key = self.stdin[start : self.index]
        return Token(key, TokenTypes.str, self.line)

    def lex_alpha(self) -> Token:
        start = self.index
        while (
            self.isAlphaOrOP(self.stdin[self.index])
            or self.stdin[self.index].isnumeric()
        ):
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        key = self.stdin[start : self.index]
        token = self.lex_keyword(key)
        if token:
            return token
        return Token(key, TokenTypes.id, self.line)

    def lex_number(self) -> Token:
        start = self.index
        while len(self.stdin) > self.index and (
            self.stdin[self.index].isnumeric()
            or (
                self.stdin[self.index] == "." and self.stdin[self.index + 1].isnumeric()
            )
        ):
            self.index += 1

        key = self.stdin[start : self.index]
        return Token(key, TokenTypes.numb, self.line)

    def lex_keyword(self, key: str) -> Token:
        for keyWord in self.keyWords:
            if key == keyWord:
                return Token(key, Token.getType(key), self.line)

    def lex_keychar(self, key: str) -> Token:
        for keyChar in self.keyChars:
            if key == keyChar[0]:
                self.index += 1
                return Token(key, Token.getType(key), self.line)

    def lex_chars(self, key: str) -> Token:
        for char in self.chars:
            if key == char:
                if key == "\n":
                    self.line += 1
                    break

    def isAlphaOrOP(self, key: str) -> bool:
        return key.isalpha() or key == "=" or key == "<" or key == ">" or key == "_"

    def lex(self) -> Token:
        if len(self.stdin) <= self.index:
            Error(
                ErrorTypes.lexer_unexpected_token, {"key": "eof", "line": self.line}
            )

        key = self.stdin[self.index]

        if key == ".":
            token = self.lex_dotwords()
            if token.key == TokenKeys.falso:
                token = Token("0", TokenTypes.numb, self.line)
            elif token.key == TokenKeys.verdadeiro:
                token = Token("1", TokenTypes.numb, self.line)

            if token:
                return token

        if key == '"':
            token = self.lex_string()
            if token:
                return token

        if self.isAlphaOrOP(key):
            token = self.lex_alpha()
            if token.key == TokenKeys.null:
                token = Token("0", TokenTypes.numb, self.line)
            if token:
                return token

        if key.isnumeric():
            token = self.lex_number()
            if token:
                return token

        token = self.lex_keychar(key)
        if token:
            return token

        token = self.lex_chars(key)
        if token:
            return token

        self.index += 1
        return self.lex()
