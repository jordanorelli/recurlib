#!/usr/bin/env python
import unittest
import time
from recurly.verification import digest_data, generate_signature, verify_params

class VerificationTest(unittest.TestCase):
    def setUp(self):
        self.origin_time = 1312806801
        self.test_sig = 'fb5194a51aa97996cdb995a89064764c5c1bfd93-1312806801'
        self.private_key = '0123456789abcdef0123456789abcdef'

    def test_recurly(self):
        """ Python port of Recurly's unit tests for the same library. """
        self.assertEqual(digest_data([[], {}, '', None]), '[]')
        self.assertEqual(digest_data(
            {'a': [1, 2, 3], 'b': {'c': '123', 'd': '456'}}),
            '[a:[1,2,3],b:[c:123,d:456]]'
        )
        self.assertEqual(digest_data({'a': 1, 'c': 3, 'b': 2}),
                         '[a:1,b:2,c:3]')
        self.assertEqual(digest_data({'1': 4, '2': 5, '3': 6}), '[4,5,6]')
        self.assertEqual(digest_data({'syntaxchars': ' \\ [ ] : , '}),
                                     '[syntaxchars: \\\\ \[ \] \: \, ]')

    def test_proper_signature(self):
        args = {'a': 'foo', 'b': 'bar'}
        sig = generate_signature('update', args, self.private_key,
                                 self.origin_time)
        self.assertEqual(sig, self.test_sig)

    def test_valid_signature(self):
        _time = time.time
        time.time = lambda: self.origin_time + 60
        args = {'a': 'foo', 'b': 'bar', 'signature': self.test_sig}
        self.assertTrue(verify_params('update', args, self.private_key))
        time.time = _time

    def test_digest(self):
        self.assertEqual(digest_data(''), '')
        self.assertEqual(digest_data(None), None)
        self.assertEqual(digest_data([]), None)
        self.assertEqual(digest_data({}), None)
        self.assertEqual(digest_data(1), 1)

if __name__ == '__main__':
    unittest.main()
