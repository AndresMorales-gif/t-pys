from typing import List, Optional, Type, cast

from lpp.ast.block import Block
from lpp.ast.infix import Infix
from lpp.ast.bool import Boolean
from lpp.ast.prefix import Prefix
from lpp.ast.program import Program
from lpp.ast.if_expression import If
from lpp.ast.number import Float, Integer
from lpp.ast.node_base import ASTNode, Statement
from lpp.ast.return_statement import ReturnStatement
from lpp.object.object_base import Object, ObjectType
from lpp.ast.expressions_statement import ExpressionStatement

import lpp.object.null as object_null
import lpp.object.bool as object_bool
import lpp.object.string as object_string
import lpp.object.return_object as object_return
import lpp.object.numbers as object_numbers


TRUE = object_bool.Boolean(True)
FALSE = object_bool.Boolean(False)
NULL = object_null.Null()


def evaluate(node: ASTNode) -> Optional[Object]:
  node_type: Type = type(node)

  if node_type == Program:
    node = cast(Program, node)

    return _evaluate_program(node)
  elif node_type == ExpressionStatement:
    node = cast(ExpressionStatement, node)

    assert node.expression is not None
    return evaluate(node.expression)

  elif node_type == Integer:
    node = cast(Integer, node)

    assert node.value is not None
    return object_numbers.Integer(node.value)

  elif node_type == Float:
    node = cast(Float, node)

    assert node.value is not None
    return object_numbers.Float(node.value)

  elif node_type == Boolean:
    node = cast(Boolean, node)

    assert node.value is not None
    return _to_boolean_object(node.value)

  elif node_type == Prefix:
    node = cast(Prefix, node)

    assert node.right is not None
    right = evaluate(node.right)
    assert right is not None
    return _evaluate_prefix_expression(node.operator, right)

  elif node_type == Infix:
    node = cast(Infix, node)

    assert node.right is not None and node.left is not None
    left = evaluate(node.left)
    right = evaluate(node.right)
    assert right is not None and left is not None
    return _evaluate_infix_expression(node.operator, left, right)

  elif node_type == Block:
    node = cast(Block, node)

    return _evaluate_block_statements(node)
  elif node_type == If:
    node = cast(If, node)

    return _evaluate_if_expression(node)

  elif node_type == ReturnStatement:
    node = cast(ReturnStatement, node)

    assert node.return_value is not None
    value = evaluate(node.return_value)
    
    assert value is not None
    return object_return.Return(value)

  return None


def _evaluate_if_expression(if_expression: If) -> Optional[Object]:
  assert if_expression is not None
  condition = evaluate(if_expression.condition)

  assert condition is not None
  if _is_truthy(condition):
    assert if_expression.consequence is not None
    return evaluate(if_expression.consequence)
  elif if_expression.alternative is not None:
    return evaluate(if_expression.alternative)
  else:
    return NULL


def _evaluate_block_statements(block: Block) -> Optional[Object]:
  result: Optional[Object] = None

  for statement in block.statements:
    result = evaluate(statement)

    if result is not None and result.type() == ObjectType.RETURN:
      return result

  return result

def _evaluate_program(program: Program) -> Optional[Object]:
  result: Optional[Object] = None
  for statement in program.statements:
    result = evaluate(statement)

    if type(result) == object_return.Return:
      result = cast(object_return.Return, result)
      return result.value
  return result


def _evaluate_statements(statements: List[Statement]) -> Optional[Object]:
  result: Optional[Object] = None

  for statement in statements:
    result = evaluate(statement)

  return result


def _is_truthy(obj: Object) -> bool:
  if obj is NULL:
    return False
  if obj is TRUE:
    return True
  if obj is FALSE:
    return False
  if obj.type() == ObjectType.INTEGER:
    obj = cast(object_numbers.Integer, obj)
    if obj.value == 0:
      return False
  if obj.type() == ObjectType.FLOAT:
    obj = cast(object_numbers.Float, obj)
    if obj.value == 0:
      return False
  if obj.type() == ObjectType.STRING:
    obj = cast(object_string.String, obj)
    if obj.value == '':
      return False
  return True


def _to_boolean_object(value: bool) -> object_bool.Boolean:
  return TRUE if value else FALSE


def _evaluate_bang_operator_expression(right: Object) -> Object:
  if right is TRUE:
    return FALSE
  if right is FALSE:
    return TRUE
  if right is NULL:
    return TRUE

  return FALSE


def _evaluate_infix_expression(operator: str,
                               left: Object,
                               right: Object) -> Object:
  if left.type() == ObjectType.INTEGER or left.type() == ObjectType.FLOAT:
    if right.type() == ObjectType.INTEGER or right.type() == ObjectType.FLOAT:
      return _evaluate_number_infix_expression(operator, left, right)
  if operator == '==':
    return _to_boolean_object(left is right)
  if operator == '!=':
    return _to_boolean_object(left is not right)
  if operator == 'and':
    return _to_boolean_object(left is TRUE and right is TRUE)
  if operator == 'or':
    return _to_boolean_object(left is TRUE or right is TRUE)

  return NULL


def _evaluate_minus_operator_expression(right: Object) -> Object:
  if type(right) == object_numbers.Integer:
    right = cast(object_numbers.Integer, right)
    return object_numbers.Integer(-right.value)
  if type(right) == object_numbers.Float:
    right = cast(object_numbers.Float, right)
    return object_numbers.Float(-right.value)
  return NULL


def _evaluate_number_infix_expression(operator: str,
                                      left: Object,
                                      right: Object) -> Object:
  left_value = cast(object_numbers.Integer, left).value \
      if left.type() == ObjectType.INTEGER \
      else cast(object_numbers.Float, left).value

  right_value = cast(object_numbers.Integer, right).value \
      if right.type() == ObjectType.INTEGER \
      else cast(object_numbers.Float, right).value

  result = None

  if operator == '+':
    result = left_value + right_value
  if operator == '-':
    result = left_value - right_value
  if operator == '/':
    result = left_value / right_value
  if operator == '*':
    result = left_value * right_value
  if operator == '^':
    result = left_value ** right_value

  if result:
    if type(result) == float and result.is_integer():
      result = int(result)
    return object_numbers.Integer(result) if type(result) == int \
        else object_numbers.Float(result)

  if operator == '<':
    return _to_boolean_object(left_value < right_value)
  if operator == '<=':
    return _to_boolean_object(left_value <= right_value)
  if operator == '>':
    return _to_boolean_object(left_value > right_value)
  if operator == '>=':
    return _to_boolean_object(left_value >= right_value)
  if operator == '==':
    return _to_boolean_object(left_value == right_value)
  if operator == '!=':
    return _to_boolean_object(left_value != right_value)

  return NULL


def _evaluate_prefix_expression(operator: str, right: Object) -> Object:
  if operator == 'not':
    return _evaluate_bang_operator_expression(right)
  elif operator == '-':
    return _evaluate_minus_operator_expression(right)
  else:
    return NULL
