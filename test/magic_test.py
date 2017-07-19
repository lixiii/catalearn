import catalearn
import unittest
import sys

class MagicTest(unittest.TestCase):

    def test_print(self):
        connector = catalearn.ServerConnector('user1', 'local')
        connector.CATALEARN_URL = 'localhost'
        a = 1
        catalearn.magic.run_in_cloud('print(a)', connector)

    def test_create_var(self):
        bomba = 'bomba'
        connector = catalearn.ServerConnector('user1', 'local')
        connector.CATALEARN_URL = 'localhost'
        env = catalearn.magic.run_in_cloud('b = 2', connector)
        print('b is ' + str(env['b']))

if __name__ == '__main__':
    unittest.main()