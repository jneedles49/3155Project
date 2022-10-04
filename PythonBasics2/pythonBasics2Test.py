import unittest
import pythonBasics2


class TestPythonBasicsTwo(unittest.TestCase):
    def test_count_threes(self):
        self.assertEqual(pythonBasics2.count_threes('033'), 11.0)
        self.assertEqual(pythonBasics2.count_threes('9369'), 3123.0)
        self.assertEqual(pythonBasics2.count_threes('999'), 333.0)
        self.assertEqual(pythonBasics2.count_threes('30669636'), 10223212.0)

    def test_longest_consecutive_repeating_char(self):
        # Default cases
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('aaa'), 'a')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('abba'), 'b')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('caaddda'), 'd')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('aaaffftttt'), 't')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('aaababbacccca'), 'c')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('ddabab'), 'd')
        self.assertEqual(pythonBasics2.longest_consecutive_repeating_char('caac'), 'a')
        # Multiple outputs
        self.assertEqual(set(pythonBasics2.longest_consecutive_repeating_char('caacc')), {'a'})
        self.assertEqual(set(pythonBasics2.longest_consecutive_repeating_char('bbbaaaceeef')), {'b'})
        self.assertEqual(set(pythonBasics2.longest_consecutive_repeating_char('abcddefgghij')), {'d'})
        self.assertEqual(set(pythonBasics2.longest_consecutive_repeating_char('aabbbccddddefggghhhh')), {'d'})

    def test_is_palindrome(self):
        self.assertEqual(pythonBasics2.is_palindrome("Hello"), False)
        self.assertEqual(pythonBasics2.is_palindrome("civic"), True)
        self.assertEqual(pythonBasics2.is_palindrome("Civic"), True)
        self.assertEqual(pythonBasics2.is_palindrome("Racecar"), True)
        self.assertEqual(pythonBasics2.is_palindrome("Dont nod"), True)
        self.assertEqual(pythonBasics2.is_palindrome("was it a cat I saw"), True)
        self.assertEqual(pythonBasics2.is_palindrome("It was not a cat"), False)


if __name__ == '__main__':
    unittest.main(verbosity=1)
