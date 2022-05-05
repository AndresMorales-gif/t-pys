from typing import List, Optional
from lpp.ast.indentifier import Identifier
from lpp.ast.let_statement import LetStatement
from lpp.ast.return_statement import ReturnStatement

from lpp.lexer import Lexer
from lpp.token import Token
from lpp.ast.program import Program
from lpp.utils.type import TokenType
from lpp.ast.node_base import Statement


class Parser:

  def __init__(self, lexer: Lexer) -> None:
    self._lexer = lexer
    self._errors: List[str] = []
    self._current_token: Optional[Token] = None
    self._peek_token: Optional[Token] = None

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

  def _parse_let_statement(self) -> Optional[LetStatement]:
    assert self._current_token is not None
    let_statement = LetStatement(token=self._current_token)

    if not self._expected_token(TokenType.IDENT):
      return None

    let_statement.name = Identifier(
        token=self._current_token, value=self._current_token.literal)

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
    return None
