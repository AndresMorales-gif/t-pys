from typing import List
from unittest import TestCase

from lpp.lexer import Lexer
from lpp.token import Token
from lpp.utils.type import TokenType


class LexerTest(TestCase):

  def test_ilegal(self) -> None:
    source: str = '¡¿@'
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(len(source)):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.ILLEGAL, '¡'),
        Token(TokenType.ILLEGAL, '¿'),
        Token(TokenType.ILLEGAL, '@')
    ]

    self.assertEquals(tokens, expected_tokens)

  def test_one_character_operator(self) -> None:
    source: str = '=+'
    lexer: Lexer = Lexer(source)
    tokens: List[Token] = []
    for i in range(len(source)):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.ASSIGN, '='),
        Token(TokenType.PLUS, '+')
    ]

    self.assertEquals(tokens, expected_tokens)

  def test_eof(self) -> None:
    source: str = '+'
    lexer: Lexer = Lexer(source)
    tokens: List[Token] = []
    for i in range(len(source) + 1):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.PLUS, '+'),
        Token(TokenType.EOF, '')
    ]

    self.assertEquals(tokens, expected_tokens)

  def test_delimiters(self) -> None:
    source = '(){},;'
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(len(source)):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.LPAREN, '('),
        Token(TokenType.RPAREN, ')'),
        Token(TokenType.LBRACE, '{'),
        Token(TokenType.RBRACE, '}'),
        Token(TokenType.COMMA, ','),
        Token(TokenType.SEMICOLON, ';'),
    ]

    self.assertEquals(tokens, expected_tokens)

  def test_assignment(self) -> None:
    source: str = 'let five = 5;'
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(5):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.LET, 'let'),
        Token(TokenType.IDENT, 'five'),
        Token(TokenType.ASSIGN, '='),
        Token(TokenType.INT, '5'),
        Token(TokenType.SEMICOLON, ';'),
    ]
    self.assertEquals(tokens, expected_tokens)

  def test_assignment_str(self) -> None:
    source: str = 'let str_five = \'five\';'
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(5):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.LET, 'let'),
        Token(TokenType.IDENT, 'str_five'),
        Token(TokenType.ASSIGN, '='),
        Token(TokenType.STR, '\'five\''),
        Token(TokenType.SEMICOLON, ';'),
    ]
    self.assertEquals(tokens, expected_tokens)

  def test_function_declaration(self) -> None:
    source: str = '''
      let sum = def(x, y) {
        x + y;
      };
    '''
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(16):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.LET, 'let'),
        Token(TokenType.IDENT, 'sum'),
        Token(TokenType.ASSIGN, '='),
        Token(TokenType.FUNCTION, 'def'),
        Token(TokenType.LPAREN, '('),
        Token(TokenType.IDENT, 'x'),
        Token(TokenType.COMMA, ','),
        Token(TokenType.IDENT, 'y'),
        Token(TokenType.RPAREN, ')'),
        Token(TokenType.LBRACE, '{'),
        Token(TokenType.IDENT, 'x'),
        Token(TokenType.PLUS, '+'),
        Token(TokenType.IDENT, 'y'),
        Token(TokenType.SEMICOLON, ';'),
        Token(TokenType.RBRACE, '}'),
        Token(TokenType.SEMICOLON, ';')
    ]
    self.assertEquals(tokens, expected_tokens)

  def test_fuction_call(self) -> None:
    source: str = 'let result = sum(two, three);'
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(10):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.LET, 'let'),
        Token(TokenType.IDENT, 'result'),
        Token(TokenType.ASSIGN, '='),
        Token(TokenType.IDENT, 'sum'),
        Token(TokenType.LPAREN, '('),
        Token(TokenType.IDENT, 'two'),
        Token(TokenType.COMMA, ','),
        Token(TokenType.IDENT, 'three'),
        Token(TokenType.RPAREN, ')'),
        Token(TokenType.SEMICOLON, ';'),
    ]
    self.assertEquals(tokens, expected_tokens)

  def test_control_statement(self) -> None:
    source: str = '''
      if (5 < 10) {
        return true;
      } else {
        return false;
      }
    '''
    lexer: Lexer = Lexer(source)

    tokens: List[Token] = []
    for i in range(17):
        tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
        Token(TokenType.IF, 'if'),
        Token(TokenType.LPAREN, '('),
        Token(TokenType.INT, '5'),
        Token(TokenType.LT, '<'),
        Token(TokenType.INT, '10'),
        Token(TokenType.RPAREN, ')'),
        Token(TokenType.LBRACE, '{'),
        Token(TokenType.RETURN, 'return'),
        Token(TokenType.TRUE, 'true'),
        Token(TokenType.SEMICOLON, ';'),
        Token(TokenType.RBRACE, '}'),
        Token(TokenType.ELSE, 'else'),
        Token(TokenType.LBRACE, '{'),
        Token(TokenType.RETURN, 'return'),
        Token(TokenType.FALSE, 'false'),
        Token(TokenType.SEMICOLON, ';'),
        Token(TokenType.RBRACE, '}')
    ]
    self.assertEquals(tokens, expected_tokens)