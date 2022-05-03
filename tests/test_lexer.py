from typing import List
from unittest import TestCase

from lpp.lexer import Lexer
from lpp.token import Token, TokenType


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