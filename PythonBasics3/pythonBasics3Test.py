import unittest
import pythonBasics3


class TestPythonBasicsOne(unittest.TestCase):

    # Test case for starts_with_non_number
    def test_starts_with_non_number(self):
        self.assertEqual(pythonBasics3.starts_with_non_number("Once upon a time, I was 18"), True)

        self.assertEqual(pythonBasics3.starts_with_non_number("5 weekdays each week"), False)

        self.assertEqual(pythonBasics3.starts_with_non_number("-5 is what I got on my quiz"), True)

        self.assertEqual(pythonBasics3.starts_with_non_number(" 1 more meal left in the fridge"), True)

        self.assertEqual(pythonBasics3.starts_with_non_number("# is used to comment a line in Python"), True)

        self.assertEqual(pythonBasics3.starts_with_non_number("1 more bag of chips left"), False)

        self.assertEqual(pythonBasics3.starts_with_non_number("Bench pressed 225 pounds"), True)

        self.assertEqual(pythonBasics3.starts_with_non_number("Ran a 100 meeter dash"), True)

    # Test case for multiple_words
    def test_multiple_words(self):
        self.assertEqual(pythonBasics3.multiple_words("That's 10/10"), True)

        self.assertEqual(pythonBasics3.multiple_words(" "), False)

        self.assertEqual(pythonBasics3.multiple_words("Different\twhitespace"), False)

        self.assertEqual(pythonBasics3.multiple_words("It's-all-one-word"), False)

        self.assertEqual(pythonBasics3.multiple_words(" one-sided? "), False)


if __name__ == '__main__':
    unittest.main(verbosity=1)
