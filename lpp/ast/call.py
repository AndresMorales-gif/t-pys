from typing import List

from lpp.token import Token
from lpp.ast.node_base import Expression


class Call(Expression):

  def __init__(self,
               token: Token,
               function: Expression,
               arguments: List[Expression] = []) -> None:
    super().__init__(token)
    self.function = function
    self.arguments = arguments

  def __str__(self) -> str:
    arg_list: List[str] = [str(argument) for argument in self.arguments]
    args = ', '.join(arg_list)
    return f'{str(self.function)}({args})'
