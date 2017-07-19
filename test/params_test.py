import unittest
from catalearn.local_params import get_local_vars

class LocalVarsTest(unittest.TestCase):

    def test_print(self):
        a = 1
        b = get_local_vars('print(a)', 1)
        self.assertEqual(a, b['a'])

if __name__ == '__main__':
    unittest.main()