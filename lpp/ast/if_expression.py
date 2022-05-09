from typing import Optional

from lpp.token import Token
from lpp.ast.block import Block
from lpp.ast.node_base import Expression


class If(Expression):
  
  def __init__(self, 
               token: Token,
               condition: Optional[Expression] = None,
               consequence: Optional[Block] = None,
               alternative: Optional[Block] = None) -> None:
    super().__init__(token)
    self.condition = condition
    self.consequence = consequence
    self.alternative = alternative

  def __str__(self) -> str:
    out: str = f'if {str(self.condition)} {str(self.consequence)}'
    if self.alternative:
      out += f'else {str(self.alternative)}'
    return out