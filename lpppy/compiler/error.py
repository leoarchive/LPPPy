import sys
from enum import Enum
from lpppy.compiler.token import Token


class ErrorTypes(Enum):
    lexer_unexpected_token = 1
    parser_unexpected_token = 2
    code_internal_error_not_implemented_yet = 3


class Error:
    def __init__(self, type: ErrorTypes, token: Token) -> None:
        if not token:
            exit(1)
        print(
            f"{self.getMsg(type)} '{token.key}' na linha {token.line};\nSinta-se livre para reportar ou tirar dúvidas em https://github.com/leozamboni/LPPPy/issues.\n",
            file=sys.stderr,
        )
        exit(1)

    def getMsg(self, type: ErrorTypes) -> str:
        match type:
            case ErrorTypes.lexer_unexpected_token:
                return "LEXER: token inesperado"
            case ErrorTypes.parser_unexpected_token:
                return "PARSER: token inesperado"
            case ErrorTypes.code_internal_error_not_implemented_yet:
                return "CODE(erro interno): funcionalidade ainda não implementada"
