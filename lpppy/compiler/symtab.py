from lpppy.compiler.token import Token, TokenTypes


class Symtab:
    symbols = []
    dtypes = []

    def push(self, token: Token, dtype: TokenTypes) -> None:
        self.symbols.append(
            {
                "token": token,
                "dtype": dtype,
            }
        )

    def getType(self, key: str) -> TokenTypes:
        for sym in self.symbols:
            if sym["token"].key == key:
                return sym["dtype"]

    def pushDType(self, token: str) -> None:
        self.dtypes.append(token)

    def checkDType(self, key: str) -> bool:
        for token in self.dtypes:
            if token.key == key:
                return True
        return False
