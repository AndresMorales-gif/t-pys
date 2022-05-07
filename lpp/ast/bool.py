from contextvars import Token
from typing import Optional
from lpp.ast.node_base import Expression


class Boolean(Expression):

  def __init__(self, token: Token, value: Optional[bool] = None) -> None:
    super().__init__(token)
    self.value = value

  def __str__(self) -> str:
    return self.token_literal()