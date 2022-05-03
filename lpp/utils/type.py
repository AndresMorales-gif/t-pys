from enum import Enum, auto, unique


@unique
class TokenType(Enum):
  ASSIGN = auto()
  COMMA = auto()
  EOF = auto()
  FUNCTION = auto()
  IDENT = auto()
  ILLEGAL = auto()
  STR = auto()
  INT = auto()
  FLOAT = auto()
  LBRACE = auto()
  LET = auto()
  LPAREN = auto()
  PLUS = auto()
  RBRACE = auto()
  RPAREN = auto()
  SEMICOLON = auto()
