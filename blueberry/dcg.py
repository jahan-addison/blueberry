from enum import Enum
from typing import Dict, Optional


class Tokens(int, Enum):
    label: Optional[str]

    def __new__(cls, value: int, label: Optional[str] = None) -> 'Tokens':
        obj: Tokens = int.__new__(cls, value)  # type: ignore
        obj._value_ = value,
        obj.label = label
        return obj

    Constant = (0, None)
    Rule = (1, None)
    Open = (2, '(')
    Close = (3, ')')
    OpenList = (4, '[')
    CloseList = (5, ']')
    HeadTailSeparator = (6, '|')
    AndThen = (7, ',')
    EOL = (8, '\n')
    End = (9, None)


class Lexer:
    """ LL(0) Definite Clause Grammar Lexer """
    def __init__(self, source: str):
        self._pointer = 0
        self._source = source
        self._symbol_table: Dict[str, str] = {}
        pass

    @property
    def pointer(self) -> str:
        """Pointer of current location in scanner. """
        try:
            return self._source[self._pointer]
        except IndexError:
            return ''

    @property
    def symbols(self) -> Dict[str, str]:
        """The symbol table. """
        return self._symbol_table

    def __iter__(self: 'Lexer') -> 'Lexer':
        """Iterator instance. """
        return self

    def rules(self) -> None:
        pass

    def char(self) -> None:
        pass

    def head(self) -> None:
        pass

    def body(self) -> None:
        pass
