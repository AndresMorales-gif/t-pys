from typing import Optional

from lpp.token import Token
from lpp.ast.node_base import Expression


class Integer(Expression):

  def __init__(self, token: Token, value: Optional[int] = None) -> None:
    super().__init__(token)
    self.value = value

  def __str__(self) -> str:
    return str(self.value)


class Float(Expression):

  def __init__(self, token: Token, value: Optional[float] = None) -> None:
    super().__init__(token)
    self.value = value

  def __str__(self) -> str:
    return str(self.value)
