# Blueberry 💎 [![Build Status](https://travis-ci.org/jahan-addison/blueberry.svg?branch=master)](https://travis-ci.org/jahan-addison/blueberry)

#### This is a Definite Clause Grammar Python 3, and C++17 parser generator.

## Details

Definitive clause grammars provide a natural way to design languages by means of a grammar f-algebra. They facilitate production and rules that each carry and chain their own endofunctor similar to monadic composition.

This is incredibly useful in natural language design, because it enables a more intuitive, hands-on system to parse and generate productions.

And, more importantly:

> The definite clauses of a DCG can be considered a set of axioms where the validity of a sentence, and the fact that it has a certain parse tree can be considered theorems that follow from these axioms. This has the advantage of making it so that recognition and parsing of expressions in a language becomes a general matter of proving statements, such as statements in a logic programming language.


## Examples

```prolog
as --> [].
as --> [a], as.
```

```prolog
tree_nodes(nil) --> [].
tree_nodes(node(Name, Left, Right)) -->
        tree_nodes(Left),
        [Name],
        tree_nodes(Right).
```

```prolog
sentence --> pronoun(subject), verb_phrase.
 verb_phrase --> verb, pronoun(object).
 pronoun(subject) --> [he].
 pronoun(subject) --> [she].
 pronoun(object) --> [him].
 pronoun(object) --> [her].
 verb --> [likes].
```

The above grammar allows sentences like "he likes her" and "he likes him", but not "her likes he" and "him likes him".

We can additionally query the grammars for all possible combinations.

## Usage

The end-goal is a provided cli tool to code-generate parser generators for C++17 and python 3 based on a provided dcg grammar. The generated code will be able to query a language and combinations just as Prolog clauses, in their own algebraic implementation detail.

## What's Left

* ☑ DCG Lexer
* ☑ DCG Parser
* 🔧 DCG Transformer and (lazy) evaluation
* 🔧 C++17 algebra
* 🔧 Code generation

### Development

Install dependencies with poetry.

Run `poetry install`.

During development, run `make start` to start and run the program, and `make test` to run the test suite.