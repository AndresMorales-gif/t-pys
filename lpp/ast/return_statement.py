from typing import Optional

from lpp.token import Token
from lpp.ast.node_base import Expression, Statement


class ReturnStatement(Statement):

  def __init__(self,
               token: Token,
               return_value: Optional[Expression] = None) -> None:
    super().__init__(token)
    self.return_value = return_value

  def __str__(self) -> str:
    return f'{super().token_literal()} {str(self.return_value)};'
