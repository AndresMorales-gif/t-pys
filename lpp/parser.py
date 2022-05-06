from enum import IntEnum
from typing import Callable, Dict, List, Optional

from lpp.utils.type import (
    Precedence,
    TokenType,
)
from lpp.lexer import Lexer
from lpp.token import Token
from lpp.ast.program import Program
from lpp.ast.indentifier import Identifier
from lpp.ast.let_statement import LetStatement
from lpp.ast.node_base import Statement, Expression
from lpp.ast.return_statement import ReturnStatement
from lpp.ast.expressions_statement import ExpressionStatement


PrefixParseFn = Callable[[], Optional[Expression]]
InfixParseFn = Callable[[Expression], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFns = Dict[TokenType, InfixParseFn]


class Parser:

  def __init__(self, lexer: Lexer) -> None:
    self._lexer = lexer
    self._errors: List[str] = []
    self._current_token: Optional[Token] = None
    self._peek_token: Optional[Token] = None

    self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
    self._infix_parse_fns: InfixParseFns = self._register_infix_fns()
    self._advance_token()
    self._advance_token()

  @property
  def errors(self) -> List[str]:
    return self._errors

  def _advance_token(self):
    self._current_token = self._peek_token
    self._peek_token = self._lexer.next_token()

  def _expected_token(self, token_type: TokenType) -> bool:
    assert self._peek_token is not None
    if self._peek_token.token_type == token_type:
      self._advance_token()
      return True
    self._expected_token_error(token_type)
    return False

  def _expected_token_error(self, token_type: TokenType) -> None:
    assert self._peek_token is not None
    self.errors.append(
        f'expected {token_type} but got {self._peek_token.token_type}')

  def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
    assert self._current_token is not None
    try:
      prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
    except KeyError as e:
      return None

    left_expression = prefix_parse_fn()
    return left_expression

  def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
    assert self._current_token is not None
    expression_statement = ExpressionStatement(token=self._current_token)

    expression_statement.expression = self._parse_expression(Precedence.LOWEST)

    assert self._peek_token is not None
    if self._peek_token.token_type == TokenType.SEMICOLON:
      self._advance_token()
    return expression_statement

  def _parser_identifier(self) -> Identifier:
    assert self._current_token is not None
    return Identifier(
      token=self._current_token,
      value=self._current_token.literal
    )

  def _parse_let_statement(self) -> Optional[LetStatement]:
    assert self._current_token is not None
    let_statement = LetStatement(token=self._current_token)

    if not self._expected_token(TokenType.IDENT):
      return None

    let_statement.name = self._parser_identifier()

    if not self._expected_token(TokenType.ASSIGN):
      return None

    # TODO finished parser expressions
    while self._current_token.token_type != TokenType.SEMICOLON:
      self._advance_token()

    return let_statement

  def _parse_return_statement(self) -> Optional[ReturnStatement]:
    assert self._current_token is not None
    return_statement = ReturnStatement(token=self._current_token)

    self._advance_token()

    # TODO finished parser expressions
    while self._current_token.token_type != TokenType.SEMICOLON:
      self._advance_token()

    return return_statement

  def parse_program(self) -> Program:
    program: Program = Program([])

    assert self._current_token is not None
    while self._current_token.token_type != TokenType.EOF:
      statement = self._parse_statement()
      if statement is not None:
        program.statements.append(statement)
      self._advance_token()

    return program

  def _parse_statement(self) -> Optional[Statement]:
    assert self._current_token is not None
    if self._current_token.token_type == TokenType.LET:
      return self._parse_let_statement()
    if self._current_token.token_type == TokenType.RETURN:
      return self._parse_return_statement()
    return self._parse_expression_statement()

  def _register_infix_fns(self) -> InfixParseFns:
    return {}

  def _register_prefix_fns(self) -> PrefixParseFns:
    return {
      TokenType.IDENT: self._parser_identifier,
    }
