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
  LOGIC = 2
  EQUALS = 3
  LESSGREATER = 4
  SUM = 5
  PRODUCT = 6
  POWER = 7
  PREFIX = 8
  CALL = 9
