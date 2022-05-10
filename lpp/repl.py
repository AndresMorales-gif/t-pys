from typing import List

from lpp.token import Token
from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.ast.program import Program
from lpp.utils.type import TokenType


EOF_TOKEN: Token = Token(TokenType.EOF, '')


def _print_parse_errors(errors: List[str]) -> None:
  for error in errors:
    print(error)

def start_repl() -> None:
  while (source := input('>> ')) != 'exit()':
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    program: Program = parser.parse_program()

    if len(parser.errors) > 0:
      _print_parse_errors(parser.errors)
      continue

    print(program)