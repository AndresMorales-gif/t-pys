from ctypes.wintypes import FLOAT
from re import match
from typing import Dict

from lpp.token import Token, lookup_token_type
from lpp.utils.const import TOKENS
from lpp.utils.type import TokenType


class Lexer:

  def __init__(self, source: str) -> None:
    self._source: str = source
    self._character: str = ''
    self._read_position: int = 0
    self._position: int = 0
    self._read_character()

  def _is_initial_token(self, character: str) -> bool:
    return bool(match(r'^[=<>!+-]$', character))

  def _is_letter(self, character: str) -> bool:
    return bool(match(r'^[a-záéíóúA-ZÁÉÍÓÚ0-9\_]$', character))

  def _is_letter_initial(self, character: str) -> bool:
    return bool(match(r'^[a-zA-Z\_]$', character))

  def _is_number(self, character: str) -> bool:
    return bool(match(r'^\d$', character))

  def _is_str(self, character: str) -> bool:
    return bool(match(r'^\'$', character))

  def _next_charaacter(self) -> str:
    if self._read_position >= len(self._source):
      return ''
    else:
      return self._source[self._read_position]

  def next_token(self) -> Token:
    self._skip_whitespaces()
    try:
      if self._is_initial_token(self._character):
        character_token = f'{self._character}{self._next_charaacter()}'
        if len(character_token) == 2 and character_token in TOKENS:
          self._read_character()
          self._character = character_token
      if self._character in TOKENS:
        token = Token(TOKENS[self._character], self._character)
      elif self._is_letter_initial(self._character):
        literal = self._read_identifier()
        token_type = lookup_token_type(literal)
        return Token(token_type, literal)
      elif self._is_number(self._character):
        number = self._read_number()
        return Token(TokenType.FLOAT if number.get("is_float") else TokenType.INT, number.get("number"))
      elif self._is_str(self._character):
        literal = self._read_str()
        return Token(TokenType.STR, literal)
      else:
        token = Token(TokenType.ILLEGAL, self._character)
      self._read_character()
      return token
    except Exception as e:
      value, = e.args
      return Token(TokenType.ILLEGAL, value)

  def _read_character(self) -> None:
    self._character = self._next_charaacter()

    self._position = self._read_position
    self._read_position += 1

  def _read_identifier(self) -> str:
    initial_position = self._position

    while self._is_letter(self._character):
      self._read_character()

    return self._source[initial_position: self._position]

  def _read_number(self) -> Dict[str, str | bool]:
    initial_position = self._position
    is_float = False
    is_error = False

    while self._is_number(self._character):
      self._read_character()
      if match(r'^,$', self._character):
        if is_float:
          is_error = True
        self._read_character()
        is_float = True
    if is_error:
      raise Exception(self._source[initial_position: self._position])
    return {"number": self._source[initial_position: self._position], "is_float": is_float}

  def _read_str(self) -> str:
    initial_position = self._position
    self._read_character()
    while not self._is_str(self._character):
      if match(r'^$', self._character):
        raise Exception(self._source[initial_position: self._position])
      self._read_character()
    self._read_character()
    return self._source[initial_position: self._position]

  def _skip_whitespaces(self) -> None:
    while match(r'^\s$', self._character):
      self._read_character()
