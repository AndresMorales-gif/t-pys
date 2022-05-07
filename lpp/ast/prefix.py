from typing import Optional

from lpp.token import Token
from lpp.ast.node_base import Expression
from lpp.utils.type import TokenType


class Prefix(Expression):

  def __init__(self, token: Token, operator: str, right: Optional[Expression] = None) -> None:
    super().__init__(token)
    self.operator = operator
    self.right = right

  def __str__(self) -> str:
    space = '' if self.token.token_type != TokenType.NEGATION else ' '
    return f'({self.operator}{space}{str(self.right)})'
