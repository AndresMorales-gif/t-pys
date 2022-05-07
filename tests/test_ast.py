from unittest import TestCase
from lpp.ast.expressions_statement import ExpressionStatement
from lpp.ast.number import Integer

from lpp.token import Token
from lpp.ast.program import Program
from lpp.utils.type import TokenType
from lpp.ast.let_statement import LetStatement
from lpp.ast.return_statement import ReturnStatement
from lpp.ast.indentifier import Identifier


class ASTTest(TestCase):

  def test_let_statement(self) -> None:
    source: str = 'let my_let = other_let;'
    program: Program = Program(statements=[
        LetStatement(
            token=Token(TokenType.LET, literal='let'),
            name=Identifier(
                token=Token(TokenType.IDENT, literal='my_let'),
                value='my_let'
            ),
            value=Identifier(
                token=Token(TokenType.IDENT, literal='other_let'),
                value='other_let'
            )
        )
    ])

    program_str = str(program)

    self.assertEqual(program_str, source)

  def test_return_statement(self) -> None:
    source: str = 'return 5;'
    program: Program = Program(statements=[
        ReturnStatement(
            token=Token(TokenType.RETURN, literal='return'),
            return_value=Identifier(
                token=Token(TokenType.INT, literal='5'),
                value='5'
            )
        )
    ])

    program_str = str(program)

    self.assertEqual(program_str, source)

  def test_integer_statement(self) -> None:
    source: str = '5'
    program: Program = Program(statements=[
        ExpressionStatement(
            token=Token(TokenType.RETURN, literal='return'),
            expression=Integer(
                token=Token(TokenType.INT, literal='5'),
                value=5
            )
        )
    ])

    program_str = str(program)

    self.assertEqual(program_str, source)
