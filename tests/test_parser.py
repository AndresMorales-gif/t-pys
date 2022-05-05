from typing import List
from unittest import TestCase

from lpp.ast.let_statement import LetStatement
from lpp.ast.program import Program
from lpp.ast.return_statement import ReturnStatement
from lpp.parser import Parser
from lpp.lexer import Lexer


class ParserTest(TestCase):

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
