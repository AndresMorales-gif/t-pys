from typing import Optional

from lpp.token import Token
from lpp.ast.node_base import Expression, Statement


class ExpressionStatement(Statement):

  def __init__(self, token: Token, expression: Optional[Expression] = None) -> None:
    super().__init__(token)
    self.expression = expression

  def __str__(self) -> str:
    return str(self.expression)
