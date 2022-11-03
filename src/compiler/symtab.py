#
# This file is part of the LPPPy distribution (https://github.com/leozamboni/LPPPy).
# Copyright (c) 2022 Leonardo Z. N.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from compiler.token import Token, TokenTypes


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
