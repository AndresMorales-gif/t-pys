from lpp.lexer import Lexer
from lpp.token import Token
from lpp.utils.type import TokenType


EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
  while (source := input('>> ')) != 'exit()':
    lexer: Lexer = Lexer(source)

    while (token := lexer.next_token()) != EOF_TOKEN:
      print(token)
