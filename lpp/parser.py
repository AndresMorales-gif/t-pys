from typing import Callable, Dict, List, Optional

from lpp.utils.type import (
    Precedence,
    TokenType,
)
from lpp.lexer import Lexer
from lpp.token import Token
from lpp.ast.block import Block
from lpp.ast.infix import Infix
from lpp.ast.bool import Boolean
from lpp.ast.prefix import Prefix
from lpp.ast.program import Program
from lpp.ast.if_expression import If
from lpp.ast.number import Float, Integer
from lpp.utils.const import PRECEDENCES
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

  def _current_precedence(self) -> Precedence:
    assert self._current_token is not None
    try:
      return PRECEDENCES[self._current_token.token_type]
    except KeyError:
      return Precedence.LOWEST

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

  def _parse_block(self) -> Block:
    assert self._current_token is not None
    block_statement = Block(token=self._current_token, statements=[])
    self._advance_token()

    while not self._current_token.token_type == TokenType.RBRACE \
            and not self._current_token.token_type == TokenType.EOF:
      statement = self._parse_statement()
      if statement:
        block_statement.statements.append(statement)
      self._advance_token()
    
    return block_statement

  def _parser_boolean(self) -> Boolean:
    assert self._current_token is not None
    return Boolean(token=self._current_token,
                   value=self._current_token.token_type == TokenType.TRUE)

  def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
    assert self._current_token is not None
    try:
      prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
    except KeyError:
      message = f'no function found to parse {self._current_token.literal}'
      self.errors.append(message)
      return None

    left_expression = prefix_parse_fn()
    assert self._peek_token is not None
    while not self._peek_token.token_type == TokenType.SEMICOLON and \
            precedence < self._peek_precedence():
      try:
        infix_parse_fn = self._infix_parse_fns[self._peek_token.token_type]
        self._advance_token()

        assert left_expression is not None
        left_expression = infix_parse_fn(left_expression)
      except KeyError:
        return left_expression
    return left_expression

  def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
    assert self._current_token is not None
    expression_statement = ExpressionStatement(token=self._current_token)

    expression_statement.expression = self._parse_expression(Precedence.LOWEST)

    assert self._peek_token is not None
    if self._peek_token.token_type == TokenType.SEMICOLON:
      self._advance_token()
    return expression_statement

  def _parser_float(self) -> Optional[Float]:
    assert self._current_token is not None
    float_number = Float(token=self._current_token)
    try:
      float_number.value = float(self._current_token.literal)
    except ValueError:
      self.errors.append(
          f'Could not parse {self._current_token.literal} as integer'
      )
      return None
    return float_number

  def _parse_grouped_expression(self) -> Optional[Expression]:
    self._advance_token()
    expression = self._parse_expression(Precedence.LOWEST)
    if not self._expected_token(TokenType.RPAREN):
      return None
    return expression

  def _parser_integer(self) -> Optional[Integer]:
    assert self._current_token is not None
    integer = Integer(token=self._current_token)
    try:
      integer.value = int(self._current_token.literal)
    except ValueError:
      self.errors.append(
          f'Could not parse {self._current_token.literal} as integer'
      )
      return None
    return integer

  def _parser_identifier(self) -> Identifier:
    assert self._current_token is not None
    return Identifier(
        token=self._current_token,
        value=self._current_token.literal
    )

  def _parse_if_expression(self) -> Optional[If]:
    assert self._current_token is not None
    if_expression = If(token=self._current_token)

    if not self._expected_token(TokenType.LPAREN):
      return None
    
    self._advance_token()
    if_expression.condition = self._parse_expression(Precedence.LOWEST)

    if not self._expected_token(TokenType.RPAREN):
      return None
    
    if not self._expected_token(TokenType.LBRACE):
      return None
    
    if_expression.consequence = self._parse_block()
    
    if self._peek_token.token_type == TokenType.ELSE:
      self._advance_token()
           
      if not self._expected_token(TokenType.LBRACE):
        return None
      
      if_expression.alternative = self._parse_block()
    return if_expression

  def _parse_infix_expression(self, left: Expression) -> Infix:
    assert self._current_token is not None
    infix = Infix(token=self._current_token,
                  left=left,
                  operator=self._current_token.literal)
    precedence = self._current_precedence()

    self._advance_token()

    infix.right = self._parse_expression(precedence)

    return infix

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

  def _parse_prefix_expression(self) -> Prefix:
    assert self._current_token is not None
    prefix_expression = Prefix(
        token=self._current_token,
        operator=self._current_token.literal
    )
    self._advance_token()

    prefix_expression.right = self._parse_expression(Precedence.PREFIX)
    return prefix_expression

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

  def _peek_precedence(self) -> Precedence:
    assert self._peek_token is not None
    try:
      return PRECEDENCES[self._peek_token.token_type]
    except KeyError:
      return Precedence.LOWEST

  def _register_infix_fns(self) -> InfixParseFns:
    return {
        TokenType.PLUS: self._parse_infix_expression,
        TokenType.MINUS: self._parse_infix_expression,
        TokenType.DIVISION: self._parse_infix_expression,
        TokenType.MULTIPLICATION: self._parse_infix_expression,
        TokenType.POWER: self._parse_infix_expression,
        TokenType.EQUALS: self._parse_infix_expression,
        TokenType.DIFF: self._parse_infix_expression,
        TokenType.LT: self._parse_infix_expression,
        TokenType.LT_OR_EQUALS: self._parse_infix_expression,
        TokenType.GT: self._parse_infix_expression,
        TokenType.GT_OR_EQUALS: self._parse_infix_expression,
    }

  def _register_prefix_fns(self) -> PrefixParseFns:
    return {
        TokenType.TRUE: self._parser_boolean,
        TokenType.FALSE: self._parser_boolean,
        TokenType.IDENT: self._parser_identifier,
        TokenType.LPAREN: self._parse_grouped_expression,
        TokenType.INT: self._parser_integer,
        TokenType.FLOAT: self._parser_float,
        TokenType.NEGATION: self._parse_prefix_expression,
        TokenType.MINUS: self._parse_prefix_expression,
        TokenType.IF: self._parse_if_expression,
    }
