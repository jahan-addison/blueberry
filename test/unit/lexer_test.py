import pytest
from os import linesep
from typing import List, Callable
from blueberry.dcg import Lexer, Token

f1_t = Callable[[str], Lexer]
f2_t = List[str]


@pytest.fixture  # type: ignore
def lexer() -> Callable[[str], Lexer]:

    def _make_lexer(source: str) -> Lexer:
        return Lexer(source)

    return _make_lexer


@pytest.fixture  # type: ignore
def whitespace() -> List[str]:
    return [
        '''    pronoun(subject) --> [she].''',
        '''  pronoun(object) --> [him].''',
        '''
            pronoun(object) --> [her].''',
        '''    verb --> [likes].\nconj --> [and, or]. '''
    ]


def test_skip_whitespace_comments(lexer: f1_t, whitespace: f2_t) -> None:
    test = lexer(whitespace[0])
    test._skip_whitespace_and_comments()
    assert test.pointer == 'p'
    test = lexer(whitespace[1])
    test._skip_whitespace_and_comments()
    assert test.pointer == 'p'
    test = lexer(whitespace[3])
    test._skip_whitespace_and_comments()
    test._pointer += len(linesep)
    assert test.pointer == 'e'


def test_read_term(lexer: f1_t) -> None:
    test = lexer(' verb --> v,r. ')
    term1 = test._read_term()
    term2 = test._read_term()
    term3 = test._read_term()
    assert term1 == 'verb'
    assert term2 == '-->'
    assert term3 == 'v'


def test_get_token(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    assert next(test) == Token.Rule
    assert next(test) == Token.Operator
    assert next(test) == Token.OpenList
    assert next(test) == Token.Terminal
    assert next(test) == Token.CloseList
    assert next(test) == Token.End


def test_inc(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    test._pointer = 3
    test._inc()
    assert test._pointer == 4


def test_dec(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    test._pointer = 3
    test._dec()
    assert test._pointer == 2


def test_reset(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    default = {
        'token': Token.Unknown,
        'data': 'nil'
    }
    test.yylex = {
        'token': Token.Operator,
        'data': '-->'
    }
    test._reset()
    assert test.yylex['token'] == list(default.values())[0]
    assert test.yylex['data'] == list(default.values())[1]


def test_set_token(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    test._set_token(Token.Rule, 'verb')
    result = {
        'token': Token.Rule,
        'data': 'verb'
    }
    assert test.yylex['token'] == list(result.values())[0]
    assert test.yylex['data'] == list(result.values())[1]
    assert test._last == Token.Rule


def test_skip_to_next_line(lexer: f1_t, whitespace: f2_t) -> None:
    test = lexer(whitespace[3])
    test._skip_to_next_line()
    test._pointer += len(linesep)
    assert test.pointer == 'c'


def test_peek_next(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    test._pointer = 4
    peek = test._peek_next()
    assert peek == '-->'


def test_eol_token(lexer: f1_t) -> None:
    test = lexer('verb --> [likes].')
    test._pointer = 0
    assert test._eol_token('\r\n') is Token.EOL
    assert test._eol_token('\n') is Token.EOL
