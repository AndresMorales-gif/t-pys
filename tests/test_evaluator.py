from unittest import TestCase
from typing import List, Tuple, cast

from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.evaluator import evaluate
from lpp.ast.program import Program
from lpp.object.numbers import Integer
from lpp.object.object_base import Object


class EvaluatorTest(TestCase):

  def _evaluate_tests(self, source: str) -> Object:
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    program: Program = parser.parse_program()

    evaluated = evaluate(program)

    assert evaluated is not None
    return evaluated

  def _test_integer_object(self, value: Object, expected: int) -> None:
    self.assertIsInstance(value, Integer)
    value = cast(Integer, value)
    self.assertEquals(value.value, expected)

  def test_integer_evaluation(self) -> None:
    tests: List[Tuple[str, int]] = [
        ('5', 5),
        ('10', 10)
    ]

    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_integer_object(evaluated, expected)
