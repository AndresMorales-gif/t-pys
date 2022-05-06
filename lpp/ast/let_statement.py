from typing import Optional
from lpp.ast.indentifier import Identifier
from lpp.ast.node_base import Expression, Statement
from lpp.token import Token


class LetStatement(Statement):

  def __init__(self,
               token: Token,
               name: Optional[Identifier] = None,
               value: Optional[Expression] = None) -> None:
    super().__init__(token)
    self.name = name
    self.value = value

  def __str__(self) -> str:
    return f'{super().token_literal()} {str(self.name)} = {str(self.value)};'
