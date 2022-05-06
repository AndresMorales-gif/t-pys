from typing import Optional

from lpp.token import Token
from lpp.ast.node_base import Expression


class Infix(Expression):
  
  def __init__(self, token: Token, 
              left: Expression, 
              operator: str, 
              right: Optional[Expression] = None) -> None:
    super().__init__(token)
    self.left = left
    self.operator = operator
    self.right = right

  def __str__(self) -> str:
    return f'{str(self.left)} {self.operator} {str(self.right)}'
