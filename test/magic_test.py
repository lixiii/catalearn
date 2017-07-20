import catalearn
import unittest
import sys

class MagicTest(unittest.TestCase):

    def test_print(self):
        connector = catalearn.ServerConnector('user1', 'local')
        connector.CATALEARN_URL = 'localhost'
        a = 1
        catalearn.magic.run_in_cloud('print(a)', connector, sys._getframe(0).f_locals)

    def test_create_var(self):
        connector = catalearn.ServerConnector('user1', 'local')
        connector.CATALEARN_URL = 'localhost'
        env = catalearn.magic.run_in_cloud('b = 2', connector, sys._getframe(0).f_locals)
        assert env['b'] == 2

    def test_import(self):
        connector = catalearn.ServerConnector('user1', 'local')
        connector.CATALEARN_URL = 'localhost'
        import numpy as np
        env = catalearn.magic.run_in_cloud('c = np.array([1,2,3])', connector, sys._getframe(0).f_locals)
        assert np.array_equal(env['c'], np.array([1,2,3]))

if __name__ == '__main__':
    unittest.main()