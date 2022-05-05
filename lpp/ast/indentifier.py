from lpp.ast.node_base import Expression
from lpp.token import Token


class Identifier(Expression):

  def __init__(self, token: Token, value: str) -> None:
    super().__init__(token)
    self.value = value

  def __str__(self) -> str:
    return self.value
