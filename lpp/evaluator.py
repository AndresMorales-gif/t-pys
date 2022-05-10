from typing import List, Optional, cast

from lpp.ast.number import Integer
from lpp.ast.program import Program
from lpp.object.object_base import Object
from lpp.ast.node_base import ASTNode, Statement
from lpp.ast.expressions_statement import ExpressionStatement

import lpp.object.numbers as object_numbers


def evaluate(node: ASTNode) -> Optional[Object]:
  node_type = type(node)

  if node_type == Program:
    node = cast(Program, node)

    return _evaluate_statements(node.statements)
  elif node_type == ExpressionStatement:
    node = cast(ExpressionStatement, node)

    assert node.expression is not None
    return evaluate(node.expression)

  elif node_type == Integer:
    node = cast(Integer, node)

    assert node.value is not None
    return object_numbers.Integer(node.value)

  return None


def _evaluate_statements(statements: List[Statement]) -> Optional[Object]:
  result: Optional[Object] = None

  for statement in statements:
    result = evaluate(statement)

  return result
