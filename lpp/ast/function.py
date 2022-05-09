from typing import List, Optional

from lpp.token import Token
from lpp.ast.block import Block
from lpp.ast.node_base import Expression
from lpp.ast.indentifier import Identifier


class Function(Expression):

  def __init__(self, token: Token,
               parameters: List[Identifier] = [],
               body: Optional[Block] = None) -> None:
    super().__init__(token)
    self.parameters = parameters
    self.body = body

  def __str__(self) -> str:
    param_list: List[str] = [str(parameter) for parameter in self.parameters]
    params: str = ', '.join(param_list)
    return f'{self.token_literal()}({params}) {str(self.body)}'
