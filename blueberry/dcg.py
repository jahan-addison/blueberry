import re
from enum import Enum
from typing import Dict, Optional
from mypy_extensions import TypedDict


class Token(int, Enum):
    label: Optional[str]

    def __new__(cls, value: int, label: Optional[str] = None) -> 'Token':
        obj: Token = int.__new__(cls, value)  # type: ignore
        obj._value_ = value,
        obj.label = label
        return obj

    Constant = (0, None)
    Rule = (1, None)
    Functor = (2, None)
    Open = (3, '(')
    Close = (4, ')')
    OpenList = (5, '[')
    CloseList = (6, ']')
    HeadTailSeparator = (7, '|')
    AndThen = (8, ',')
    Operator = (9, '-->')
    EOL = (10, None)
    End = (11, '.')
    Terminal = (12, None)
    Unknown = (13, None)


class yylex_t(TypedDict, total=False):
    """The TypedDict for a `yylex` data type. """
    token: Token
    data: Optional[str]  # The `yytext` data


class Lexer:
    """ LL(1) Definite Clause Grammar Lexer """
    def __init__(self, source: str):
        self._symbol_table: Dict[str, str] = {}
        self.yylex: yylex_t = {
            'token': Token.Unknown,
            'data': None
        }
        self._source = source
        self._pointer = 0
        self._at: str
        self._rule = False
        self._terminals = False

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

    def __next__(self) -> Token:
        token: Optional[Token] = None
        if not self.pointer:
            raise StopIteration('Lexer Iterator out of bounds')

        self._at = self._source[self._pointer - 1]

        self._skip_whitespace_and_comments()
        self._reset()
        for name, lexeme in Token.__members__.items():
            if lexeme.label == self.pointer:
                if lexeme == Token.OpenList:
                    self._terminals = True
                if lexeme == Token.CloseList:
                    self._terminals = False
                self._set_token(lexeme, self.pointer)
                self._inc()
                return lexeme

        term = self._read_term()

        token = token or self._eol_token(term)

        if term == '-->':
            self._rule = True
            self._set_token(Token.Operator, term)
            return Token.Operator

        if re.match('[A-Za-z0-9_]+', term):
            peek = self._peek_next()
            if self._at == '(':
                self._set_token(Token.Constant, term)
                return Token.Constant
            if self._terminals:
                self._set_token(Token.Terminal, term)
                return Token.Terminal
            if self.pointer == '(':
                self._set_token(Token.Functor, term)
                return Token.Functor
            if self._rule or peek == '-->' or peek == ',':
                self._set_token(Token.Rule, term)
                return Token.Rule
            self._set_token(Token.Constant, term)
            return Token.Constant

        return token or Token.Unknown

    def _inc(self) -> None:
        """Increment the pointer, similar to pointer arithmetic."""
        self._pointer += 1

    def _dec(self) -> None:
        """Decrement the pointer, similar to pointer arithmetic."""
        self._pointer -= 1

    def _read_term(self) -> str:
        """Read next term.
        Read the next term from the source string, skipping all comments.
        """
        term: str = ''
        self._skip_whitespace_and_comments()
        if self.pointer == '\r':
            self._inc()
            return '\r\n'
        elif self.pointer == '\n':
            return '\n'
        elif self.pointer == '.':
            return '.'
        elif self.pointer == ',':
            return ','
        while self.pointer and not re.match(r'[,\t\r\n\{\}\[\]\(\)\. ]', self.pointer):
            term += self.pointer
            self._inc()
        return term

    def _eol_token(self, term: str) -> Optional[Token]:
        """Tokenize EOL sequences. """
        if term[:2] == '\r\n':
            self._inc()
            self._inc()
            self._rule = False
            self._set_token(Token.EOL, '\r\n')
            return Token.EOL
        elif term[0] == '\n':
            self._inc()
            self._rule = False
            self._set_token(Token.EOL, '\n')
            return Token.EOL
        return None

    def _reset(self) -> None:
        """Reset scanner data. """
        self.yylex = {
            'token': Token.Unknown,
            'data': None
        }

    def _set_token(self, token: Token, term: str) -> None:
        """Set last token and scanner data. """
        self._last = token
        self.yylex = {
            'token': token,
            'data': term
        }

    def _peek_next(self) -> str:
        """Peek one term.
        Peek ahead one term to infer lexical sequence.
        """
        term: str = ''
        self._skip_whitespace_and_comments()
        index: int = self._pointer
        size: int = len(self._source)
        while index < size and not re.match(r'[,\t\r\n\{\}\[\]\(\)\. ]', self._source[index]):
            term += self._source[index]
            index += 1

        return term

    def _skip_whitespace_and_comments(self) -> None:
        """Skip whitespace.
        Skips all whitespace and comments recursively until the beginning
        of the next term.
        """
        if re.match('[\t ]', self.pointer):
            self._inc()
            self._skip_whitespace_and_comments()
        if self.pointer == '%':
            self._skip_to_next_line()
            self._skip_whitespace_and_comments()

    def _skip_to_next_line(self) -> None:
        """ Skips until sequences of EOL. """
        skip = True
        while skip:
            if not self.pointer:
                skip = False
                break
            self._inc()
            if self.pointer == '\n' \
                    or self.pointer == '\r':
                skip = False


class Parser:
    def rule(self) -> None:
        pass

    def head(self) -> None:
        pass

    def body(self) -> None:
        pass


lexer = Lexer(r""" sentence --> pronoun(subject), verb_phrase. % a comment
 verb_phrase --> verb, pronoun(object).
 pronoun(subject) --> [he].
 pronoun(subject) --> [she, ze, they].""")

# for test in lexer:
#     print(test)
#     print('yylex:', lexer.yylex)
