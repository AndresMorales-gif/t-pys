from typing import Dict, NamedTuple

from lpp.utils.const import KEIWORDS
from lpp.utils.type import TokenType


class Token(NamedTuple):
  token_type: TokenType
  literal: str

  def __str__(self) -> str:
    return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
  return KEIWORDS.get(literal, TokenType.IDENT)