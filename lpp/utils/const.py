from typing import Dict

from lpp.utils.type import TokenType


TOKENS: Dict[str, TokenType] = {
  '=': TokenType.ASSIGN,
  '+': TokenType.PLUS,
  '': TokenType.EOF,
  '(': TokenType.LPAREN,
  ')': TokenType.RPAREN,
  '{': TokenType.LBRACE,
  '}': TokenType.RBRACE,
  ',': TokenType.COMMA,
  ';': TokenType.SEMICOLON
}

KEIWORDS: Dict[str, TokenType] = {
  'let': TokenType.LET
}