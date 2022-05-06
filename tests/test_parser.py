from unittest import TestCase
from typing import Any, List, Type, cast

from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.ast.program import Program
from lpp.ast.node_base import Expression
from lpp.ast.indentifier import Identifier
from lpp.ast.let_statement import LetStatement
from lpp.ast.return_statement import ReturnStatement
from lpp.ast.expressions_statement import ExpressionStatement


class ParserTest(TestCase):

  def _test_program_statement(self,
                              parser: Parser,
                              program: Program,
                              expect_statement_count: int = 1) -> None:
    self.assertEquals(len(parser.errors), 0)
    self.assertEquals(len(program.statements), expect_statement_count)
    self.assertIsInstance(program.statements[0], ExpressionStatement)

  def _test_literal_expression(self,
                               expression: Expression,
                               expected_value: Any) -> None:
    value_type: Type = type(expected_value)

    if value_type == str:
      self._test_identifier(expression, expected_value)
    else:
      self.fail(f'Unhandled type of expression. Got={value_type}')

  def _test_identifier(self, expression: Expression, expected_value: str) -> None:
    self.assertIsInstance(expression, Identifier)
    identifier = cast(Identifier, expression)
    self.assertEquals(identifier.value, expected_value)
    self.assertEquals(identifier.token.literal, expected_value)

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
