import unittest
from arithmeticLexer import arithmeticLexer
from arithmeticListener import arithmeticListener
from arithmeticParser import arithmeticParser, ParseTreeWalker
import antlr4

from dsl_listener import evaluate_line


class MyTestCase(unittest.TestCase):
    def test_return_const(self):
        line = 'return 2'
        assert evaluate_line(line).result == 2

    def test_assign(self):
        line = 'a = 2'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 2

    def test_plus(self):
        line = 'a = 1 + 1'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 2

    def test_mulitple_plus(self):
        line = 'a = 1 + 1 + 1 + 1'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 4

    def test_minus(self):
        line = 'a = 3 - 1'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 2

    def test_multiple_minus(self):
        line = 'a = 3 - 1 - 1'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 1

    def test_mix_plus_minus(self):
        line = 'a = 3 + 1 - 1 + 2 - 1'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 4

    def test_parans(self):
        line = 'a = (1 + 1) + (1 + 1)'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 4

    def test_multi_line(self):
        line = """a = 2
        return a
        """
        dsl = evaluate_line(line)


if __name__ == '__main__':
    unittest.main()
