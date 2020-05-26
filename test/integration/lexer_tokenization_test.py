# flake8: noqa
import pytest
import pathlib
from typing import Callable
from collections import deque
from blueberry.dcg import Lexer, Token


@pytest.fixture  # type: ignore
def lexer() -> Callable[[str], Lexer]:
    def _make_lexer(source: str) -> Lexer:
        return Lexer(source)

    return _make_lexer


expected = deque([
     Token.Rule
,    Token.Operator
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.AndThen
,    Token.Rule
,    Token.End
,    Token.EOL
,    Token.Rule
,    Token.Operator
,    Token.Rule
,    Token.AndThen
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.End
,    Token.EOL
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.Operator
,    Token.OpenList
,    Token.Terminal
,    Token.CloseList
,    Token.End
,    Token.EOL
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.Operator
,    Token.OpenList
,    Token.Terminal
,    Token.CloseList
,    Token.End
,    Token.EOL
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.Operator
,    Token.OpenList
,    Token.Terminal
,    Token.CloseList
,    Token.End
,    Token.EOL
,    Token.Functor
,    Token.Open
,    Token.Constant
,    Token.Close
,    Token.Operator
,    Token.OpenList
,    Token.Terminal
,    Token.CloseList
,    Token.End
,    Token.EOL
,    Token.Rule
,    Token.Operator
,    Token.OpenList
,    Token.Terminal
,    Token.CloseList
,    Token.End
])


def test_lexer_tokenization() -> None:
    with open(f'{pathlib.Path(__file__).parent.parent}/etc/fixture.dcg') as f:
        test = Lexer(f.read())
        for token in test:
            assert token is expected.popleft()
        assert len(expected) == 0