from typing import List

from lpp.token import Token
from lpp.ast.node_base import Statement


class Block(Statement):

  def __init__(self,
               token: Token,
               statements: List[Statement]) -> None:
    super().__init__(token)
    self.statements = statements

  def __str__(self) -> str:
    out: List[str] = [str(statement) for statement in self.statements]
    return '{'+''.join(out)+'}'
