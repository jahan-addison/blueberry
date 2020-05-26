
import pytest
from typing import List, Callable
from collections import deque, OrderedDict
from blueberry.dcg import Token, Parser, DCGParserError

f1_t = Callable[[str], Parser]
f3_t = List[str]


@pytest.fixture  # type: ignore
def parser() -> f1_t:
    def _get_parser(source: str) -> Parser:
        return Parser(source)

    return _get_parser


@pytest.fixture  # type: ignore
def code() -> List[str]:
    return [
        '''    pronoun(subject) --> [she].''',
        '''  pronoun(object) --> [him].''',
        '''
            pronoun(object) --> [her].''',
        '''    verb --> [likes].''',
        '''as --> [].''',
        '''np --> det,n.''',
        '''vp --> v,np.''',
        '''vp --> v.''',
        '''kp --> verb(V), noun_phrase(NP).'''
    ]


def test_take(parser: f1_t, code: f3_t) -> None:
    test = parser(code[0])
    test.take(Token.Functor)
    with pytest.raises(DCGParserError):
        test.take(Token.Close)
    test = parser(code[0])
    # should not error:
    test.take([Token.Rule, Token.Functor])
    test.take(Token.Open)
    test.take(Token.Constant)
    test.take([Token.Close])


def test_error(parser: f1_t, code: f3_t) -> None:
    test = parser(code[0])
    with pytest.raises(DCGParserError):
        test.error('Functor', Token.Operator)


def test_rule(parser: f1_t, code: f3_t) -> None:
    test = parser(code[2])
    test.rule()
    expected = OrderedDict([('pronoun object', deque(['her']))])
    assert test.rules == expected
    test = parser(code[3])
    test.rule()
    expected = OrderedDict([('verb', deque(['likes']))])
    assert test.rules == expected


def test_body(parser: f1_t, code: f3_t) -> None:
    test = parser(code[4])
    test.lexer._pointer = 3
    next(test.lexer)
    assert test.body() == deque([])  # empty terminal list
    test = parser(code[5])
    test.lexer._pointer = 3
    next(test.lexer)
    assert test.body() == deque(['det', 'n'])  # rule set, non-terminal
    test = parser(code[1])
    test.lexer._pointer = 17
    next(test.lexer)
    assert test.body() == deque(['him'])  # terminal list
    test = parser(code[8])
    test.lexer._pointer = 3
    next(test.lexer)
    assert test.body() == deque(['verb', 'V', deque(['noun_phrase', 'NP'])])  # functor


def test_parse(parser: f1_t, code: f3_t) -> None:
    test = parser('''np --> det,n.\nvp --> v,np.''')
    test.parse()
    assert test.rules == OrderedDict([('np', deque(['det', 'n'])), ('vp', deque(['v', 'np']))])
