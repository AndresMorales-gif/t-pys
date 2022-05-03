from typing import Dict

from lpp.token import TokenType


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