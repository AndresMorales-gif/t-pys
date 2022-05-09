from unittest import TestCase
from typing import Any, List, Tuple, Type, cast

from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.ast.block import Block
from lpp.ast.infix import Infix
from lpp.ast.bool import Boolean
from lpp.ast.prefix import Prefix
from lpp.ast.program import Program
from lpp.ast.if_expression import If
from lpp.ast.node_base import Expression
from lpp.ast.number import Float, Integer
from lpp.ast.indentifier import Identifier
from lpp.ast.let_statement import LetStatement
from lpp.ast.return_statement import ReturnStatement
from lpp.ast.expressions_statement import ExpressionStatement


class ParserTest(TestCase):

  def _test_program_statement(self,
                              parser: Parser,
                              program: Program,
                              expect_statement_count: int = 1) -> None:
    if parser.errors:
      print(parser.errors)
    self.assertEquals(len(parser.errors), 0)
    self.assertEquals(len(program.statements), expect_statement_count)
    self.assertIsInstance(program.statements[0], ExpressionStatement)

  def _test_boolean(self, expression: Expression, expected_value: bool) -> None:
    self.assertIsInstance(expression, Boolean)
    boolean = cast(Boolean, expression)
    self.assertEquals(boolean.value, expected_value)
    self.assertEquals(boolean.token.literal, 'true' if expected_value else 'false')

  def _test_literal_expression(self,
                               expression: Expression,
                               expected_value: Any) -> None:
    value_type: Type = type(expected_value)

    if value_type == str:
      self._test_identifier(expression, expected_value)
    elif value_type == int:
      self._test_integer(expression, expected_value)
    elif value_type == float:
      self._test_float(expression, expected_value)
    elif value_type == bool:
      self._test_boolean(expression, expected_value)
    else:
      self.fail(f'Unhandled type of expression. Got={value_type}')

  def _test_float(self, expression: Expression, expected_value: float) -> None:
    self.assertIsInstance(expression, Float)
    float_number = cast(Float, expression)
    self.assertEquals(float_number.value, expected_value)
    self.assertEquals(float_number.token.literal, str(expected_value))

  def _test_identifier(self, expression: Expression, expected_value: str) -> None:
    self.assertIsInstance(expression, Identifier)
    identifier = cast(Identifier, expression)
    self.assertEquals(identifier.value, expected_value)
    self.assertEquals(identifier.token.literal, expected_value)

  def _test_integer(self, expression: Expression, expected_value: int) -> None:
    self.assertIsInstance(expression, Integer)
    integer = cast(Integer, expression)
    self.assertEquals(integer.value, expected_value)
    self.assertEquals(integer.token.literal, str(expected_value))

  def _test_infix_expression(self,
                             expression: Expression,
                             expected_left: Any,
                             expected_operator: str,
                             expected_right: Any) -> None:
    infix = cast(Infix, expression)

    assert infix.left is not None
    self._test_literal_expression(infix.left, expected_left)

    self.assertEquals(infix.operator, expected_operator)
    
    assert infix.right is not None
    self._test_literal_expression(infix.right, expected_right)

  def test_parser_program(self) -> None:
    source: str = 'let x = 5;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self.assertIsNotNone(program)
    self.assertIsInstance(program, Program)

  def test_let_statements(self) -> None:
    source: str = '''
      let x = 5;
      let y = 10;
      let foo = 20;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self.assertEqual(len(program.statements), 3)

    names: List[str] = []
    for statement in program.statements:
      self.assertEqual(statement.token_literal(), 'let')
      self.assertIsInstance(statement, LetStatement)
      assert statement.name is not None
      names.append(statement.name.value)

    expected_names: List[str] = ['x', 'y', 'foo']

    self.assertEquals(names, expected_names)

  def test_parser_error(self) -> None:
    source: str = 'let x 5;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self.assertEqual(len(parser.errors), 1)

  def test_return_statement(self) -> None:
    source: str = '''
      return 5;
      return foo;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self.assertEqual(len(program.statements), 2)

    for statement in program.statements:
      self.assertEqual(statement.token_literal(), 'return')
      self.assertIsInstance(statement, ReturnStatement)

  def test_identifier_expression(self) -> None:
    source: str = 'foobar;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self._test_program_statement(parser, program)

    expression_statement = cast(ExpressionStatement, program.statements[0])
    self._test_literal_expression(expression_statement.expression, 'foobar')

  def test_number_expression(self) -> None:
    source: str = '5; 4.3;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self._test_program_statement(parser, program, 2)

    expression_statement = cast(ExpressionStatement, program.statements[0])

    assert expression_statement.expression is not None
    self._test_literal_expression(expression_statement.expression, 5)

    expression_statement = cast(ExpressionStatement, program.statements[1])

    assert expression_statement.expression is not None
    self._test_literal_expression(expression_statement.expression, 4.3)

  def test_prefix_expression(self) -> None:
    source: str = 'not 5; -15; not true;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()
    self._test_program_statement(parser, program, 3)

    for statement, (expected_operator, expected_value) in zip(
              program.statements, [('not', 5), ('-', 15), ('not', True)]):
      statement = cast(ExpressionStatement, statement)
      self.assertIsInstance(statement.expression, Prefix)

      prefix = cast(Prefix, statement.expression)
      self.assertEquals(prefix.operator, expected_operator)

      assert prefix.right is not None
      self._test_literal_expression(prefix.right, expected_value)

  def test_infix_expression(self) -> None:
    source: str = '''
      5 + 5;
      5 - 5;
      5 * 5;
      5 / 5;
      5 > 5;
      5 < 5;
      5 == 5;
      5 != 5;
      true != false;
      true == true;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()
    self._test_program_statement(parser, program, 10)

    expected_operators_and_values: List[Tuple[Any, str, Any]] = [
      (5, '+', 5),
      (5, '-', 5),
      (5, '*', 5),
      (5, '/', 5),
      (5, '>', 5),
      (5, '<', 5),
      (5, '==', 5),
      (5, '!=', 5),
      (True, '!=', False),
      (True, '==', True),
    ] 

    for statement, (expected_left, expected_operator, expected_right) in zip(
              program.statements, expected_operators_and_values):
      statement = cast(ExpressionStatement, statement)
      assert statement.expression is not None
      self.assertIsInstance(statement.expression, Infix)
      
      self._test_infix_expression(
        statement.expression,
        expected_left,
        expected_operator,
        expected_right
      )

  def test_boolean_expression(self) -> None:
    source: str = 'true; false;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self._test_program_statement(parser, program, 2)

    expected_values: List[bool] = [True, False]
    for statement, expected_value in zip(program.statements, expected_values):
      expression_statement = cast(ExpressionStatement, statement)
      assert expression_statement.expression is not None
      self._test_literal_expression(expression_statement.expression, expected_value)

  def test_operator_precedent(self) -> None:
    test_sources: List[Tuple[str, str, int]] = [
      ('-a * b;', '((-a) * b)', 1),
      ('not -a', '(not (-a))', 1),
      ('a + b / c', '(a + (b / c))', 1),
      ('3 + 4; -5 * 5;', '(3 + 4)((-5) * 5)', 2),
      ('3 + 4 + 3 + 8 + 5;', '((((3 + 4) + 3) + 8) + 5)', 1),
      ('a * b + c;', '((a * b) + c)', 1),
      ('3 > 4 == false;', '((3 > 4) == false)', 1),
      ('3 < 4 != true;', '((3 < 4) != true)', 1),
      ('not a == b;', '((not a) == b)', 1),
      ('not a != not b; a * 8 - 5;', '((not a) != (not b))((a * 8) - 5)', 2),
      ('1 + (2 + 3) + 4;', '((1 + (2 + 3)) + 4)', 1),
      ('(a + b) * c;', '((a + b) * c)', 1),
      ('-(5 + 5);', '(-(5 + 5))', 1),
      ('not (5 < 2) == not (5 < 3 == 5 > 8);', '((not (5 < 2)) == (not ((5 < 3) == (5 > 8))))', 1),
    ]
    
    for source, expected_result, expected_statement_count in test_sources:
      lexer: Lexer = Lexer(source)
      parser: Parser = Parser(lexer)

      program: Program = parser.parse_program()
      self._test_program_statement(parser, program, expected_statement_count)
      self.assertEquals(str(program), expected_result)

  def test_if_expressions(self) -> None:
    source: str = 'if (x < y) { z }'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self._test_program_statement(parser, program)

    if_expression = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
    self.assertIsInstance(if_expression, If)
    assert if_expression.condition is not None
    self._test_infix_expression(if_expression.condition, 'x', '<', 'y')

    assert if_expression.consequence is not None
    self.assertIsInstance(if_expression.consequence, Block)
    self.assertEquals(len(if_expression.consequence.statements), 1)

    consequence_statement = cast(ExpressionStatement,
                                 if_expression.consequence.statements[0])
    assert consequence_statement.expression is not None
    self._test_identifier(consequence_statement.expression, 'z')

    self.assertIsNone(if_expression.alternative)

  def test_if_expressions_alternative(self) -> None:
    source: str = 'if (x < y) { z } else { y }'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    self._test_program_statement(parser, program)

    if_expression = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
    self.assertIsInstance(if_expression, If)
    assert if_expression.condition is not None
    self._test_infix_expression(if_expression.condition, 'x', '<', 'y')

    assert if_expression.consequence is not None
    self.assertIsInstance(if_expression.consequence, Block)
    self.assertEquals(len(if_expression.consequence.statements), 1)

    consequence_statement = cast(ExpressionStatement,
                                 if_expression.consequence.statements[0])
    assert consequence_statement.expression is not None
    self._test_identifier(consequence_statement.expression, 'z')

    assert if_expression.alternative is not None
    self.assertIsInstance(if_expression.alternative, Block)
    self.assertEquals(len(if_expression.alternative.statements), 1)

    alternative_statement = cast(ExpressionStatement,
                                 if_expression.alternative.statements[0])
    assert alternative_statement.expression is not None
    self._test_identifier(alternative_statement.expression, 'y')
