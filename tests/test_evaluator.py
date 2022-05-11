from unittest import TestCase
from typing import Any, List, Tuple, cast

from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.object.error import Error
from lpp.object.bool import Boolean
from lpp.ast.program import Program
from lpp.evaluator import NULL, evaluate
from lpp.object.object_base import Object
from lpp.object.numbers import Integer, Float


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

  def _test_boolean_object(self, value: Object, expected: int) -> None:
    self.assertIsInstance(value, Boolean)
    value = cast(Boolean, value)
    self.assertEquals(value.value, expected)

  def _test_float_object(self, value: Object, expected: float) -> None:
    self.assertIsInstance(value, Float)
    value = cast(Float, value)
    self.assertEquals(value.value, expected)

  def _test_null_object(self, value: Object) -> None:
    self.assertEquals(value, NULL)

  def test_integer_evaluation(self) -> None:
    tests: List[Tuple[str, int]] = [
        ('5', 5),
        ('10', 10),
        ('-5', -5),
        ('-10', -10),
        ('-10 + 5', -5),
        ('5 + 5', 10),
        ('(5 + (5 * 8)) ^ 2', 2025),
        ('5 - 10', -5),
        ('2 * 2 * 2 * 2', 16),
        ('2 * 5 - 3', 7),
        ('2 ^ 3', 8),
        ('50 / 2', 25),
        ('2 * (5 - 3)', 4),
        ('(2 + 7) / 3', 3),
        ('50 / 2 * 2 + 10', 60)
    ]

    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_integer_object(evaluated, expected)

  def test_float_evaluation(self) -> None:
    tests: List[Tuple[str, float]] = [
        ('2.1', 2.1),
        ('8.4', 8.4),
        ('-3.2', -3.2),
        ('2.5 * 3', 7.5),
        ('5 / 2', 2.5),
        ('5 + 3.2', 8.2),
        ('12 / 10', 1.2),
        ('2 * (35 / 4)', 17.5),
    ]

    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_float_object(evaluated, expected)

  def test_boolean_evaluation(self) -> None:
    tests: List[Tuple[str, int]] = [
        ('true', True),
        ('false', False)
    ]

    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_boolean_object(evaluated, expected)

  def test_bang_operator(self) -> None:
    tests: List[Tuple[str, int]] = [
        ('not true', False),
        ('not false', True),
        ('not not true', True),
        ('not not false', False),
        ('not 5', False),
        ('not not 5', True),
        ('not false == true', True),
        ('false != true', True),
        ('not 5 == true', False),
        ('not 5 == not not 2', False),
        ('(5 > 2) == not true', False),
        ('not (5 < 7)', False),
        ('5 <= 8', True),
        ('7 >= 9', False),
        ('2 >= 2', True),
        ('2 > 2', False),
        ('3 <= 3', True),
        ('3 < 3', False),
        ('-3 < 3', True),
        ('-3 < 3 and 4 < 10', True),
        ('not (-3 < 3) and 4 < 10', False),
        ('-3 < 3 or not (4 < 10)', True),
        ('-3 > 3 or not (4 < 10)', False)
    ]

    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_boolean_object(evaluated, expected)

  def test_if_else_evaluation(self) -> None:
    tests: List[Tuple[str, Any]] = [
        ('if (true) { 10; }', 10),
        ('if (false) { 10; }', None),
        ('if (1) { 10; }', 10),
        ('if (1 < 2) { 10; }', 10),
        ('if (1 > 2) { 10; }', None),
        ('if (0) { 10; } else { 20; }', 20),
        ('if (0.0) { 10; } else { 20; }', 20),
        ('if (1 < 2 and 5 < 8) { 10; } else { 20; }', 10),
        ('if (1 > 2 and 5 < 8) { 10; } else { 20; }', 20),
        ('if (1 > 2 or 5 < 8) { 10; } else { 20; }', 10),
    ]
    for source, expected in tests:
      evaluated = self._evaluate_tests(source)

      if type(expected) == int:
        self._test_integer_object(evaluated, expected)
      else:
        self._test_null_object(evaluated)

  def test_return_evaluation(self) -> None:
    tests: List[Tuple[str, Any]] = [
        ('return 10;', 10),
        ('return 10; 9;', 10),
        ('return 2 * 5; 9;', 10),
        ('9; return 3 * 6; 9;', 18),
        ('''
            if (10 > 1) {
              if (20 > 10) {
                return 1;
              }
              return 0;
            }
        ''', 1),
    ]
    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self._test_integer_object(evaluated, expected)

  def test_error_handling(self) -> None:
    tests: List[Tuple[str, str]] = [
        ('5 + true;', 'Type mismatch: INTEGER + BOOLEAN'),
        ('5 + true; 9;', 'Type mismatch: INTEGER + BOOLEAN'),
        ('-true;', 'Unknown operator: -BOOLEAN'),
        ('true + false;', 'Unknown operator: BOOLEAN + BOOLEAN'),
        ('5; true - false; 10;', 'Unknown operator: BOOLEAN - BOOLEAN'),
        ('''
          if (10 > 7) {
            return true + false;
          }
        ''', 'Unknown operator: BOOLEAN + BOOLEAN'),
        ('''
          if (10 > 1) {
            if (true) {
              return true * false;
            }
            return 1;
          }
        ''', 'Unknown operator: BOOLEAN * BOOLEAN'),
        ('''
          if (5 < 2) {
            return 1;
          } else {
            return true / false;
          }
        ''', 'Unknown operator: BOOLEAN / BOOLEAN')
    ]
    for source, expected in tests:
      evaluated = self._evaluate_tests(source)
      self.assertIsInstance(evaluated, Error)

      evaluated = cast(Error, evaluated)
      self.assertEquals(evaluated.message, expected)
      