from enum import Enum, IntEnum, auto, unique


@unique
class TokenType(Enum):
  AND = auto()
  ASSIGN = auto()
  COMMA = auto()
  DECR = auto()
  DIFF = auto()
  DIVISION = auto()
  ELSE = auto()
  EOF = auto()
  EQUALS = auto()
  FALSE = auto()
  FLOAT = auto()
  FUNCTION = auto()
  GT = auto()
  GT_OR_EQUALS = auto()
  IDENT = auto()
  IF = auto()
  ILLEGAL = auto()
  INCR = auto()
  INT = auto()
  LBRACE = auto()
  LET = auto()
  LPAREN = auto()
  LT = auto()
  LT_OR_EQUALS = auto()
  MINUS = auto()
  MOD = auto()
  MULTIPLICATION = auto()
  NEGATION = auto()
  OR = auto()
  PLUS = auto()
  POWER = auto()
  RBRACE = auto()
  RETURN = auto()
  RPAREN = auto()
  SEMICOLON = auto()
  STR = auto()
  TRUE = auto()


class Precedence(IntEnum):
  LOWEST = 1
  EQUALS = 2
  LESSGREATER = 3
  SUM = 4
  PRODUCT = 5
  POWER = 6
  PREFIX = 7
  CALL = 8
