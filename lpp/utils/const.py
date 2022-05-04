from typing import Dict

from lpp.utils.type import TokenType


TOKENS: Dict[str, TokenType] = {
    '=': TokenType.ASSIGN,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLICATION,
    '/': TokenType.DIVISION,
    '^': TokenType.POWER,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    '<': TokenType.LT,
    '>': TokenType.GT,
    '': TokenType.EOF
}

KEIWORDS: Dict[str, TokenType] = {
    'def': TokenType.FUNCTION,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'if': TokenType.IF,
    'let': TokenType.LET,
    'mod': TokenType.MOD,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE
}
