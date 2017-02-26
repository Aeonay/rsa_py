'''Tests for the rsa_functions module'''

import unittest
from rsa_py import rsa_functions

class RSAFunctionsTestCase(unittest.TestCase):
    '''Tests for rsa_functions.py'''

    def test_primality_test(self):
        '''Is 9973 a prime? (it is)'''
        # Need to assert a prime above the top 1000
        self.assertTrue(rsa_functions.primality_test(9973, 5))

if __name__ == '__main__':
    unittest.main()
