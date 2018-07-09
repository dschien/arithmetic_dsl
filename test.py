import pandas as pd
import unittest

from dsl_listener import evaluate_line, DSL, evaluate_lines


class MyTestCase(unittest.TestCase):
    def test_return_const(self):
        line = 'return 2'
        assert evaluate_line(line).result == 2

    def test_assign(self):
        line = 'a = 2'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 2

    def test_var_ref(self):
        line = 'a = 2 * b'
        d = DSL()
        d.variables['b'] = 3
        dsl = evaluate_line(line, d)
        assert dsl.variables['a'] == 6

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

    def test_prod(self):
        line = 'a = 3 * 2'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 6

    def test_div(self):
        line = 'a = 6 / 2'
        dsl = evaluate_line(line)
        assert dsl.variables['a'] == 3

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
        dsl = evaluate_lines(line)
        assert dsl.result == 2

    def test_multi_line_variables(self):
        line = """a = 2
        a = a * 2
        return a
        """
        dsl = evaluate_lines(line)
        assert dsl.result == 4

    def test_pandas(self):
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)

        line = 'a = 2 * b'
        d = DSL()
        d.variables['b'] = df
        dsl = evaluate_line(line, d)

        from pandas.util.testing import assert_frame_equal

        d = {'col1': [2, 4], 'col2': [6, 8]}
        df_new = pd.DataFrame(data=d)

        assert_frame_equal(dsl.variables['a'], df_new)


if __name__ == '__main__':
    unittest.main()
