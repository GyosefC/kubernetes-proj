import unittest
import questions
from python_katas.utils import unittest_runner


class TestSumOfElements(unittest.TestCase):

    def test_empty_list(self):
        lst = []
        self.assertEqual(questions.sum_of_element(lst), 0)

    def test_integers_list(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(questions.sum_of_element(lst), 15)

    def test_negative_numbers(self):
        lst = [1, -6, 7, 0, 99]
        self.assertEqual(questions.sum_of_element(lst), 101)

    def test_all_zeros(self):
        lst = [0] * 50000
        self.assertEqual(questions.sum_of_element(lst), 0)


class TestVerbing(unittest.TestCase):

    def test_short_word(self):
        self.assertEqual(questions.versing('run'), 'runing')

    def test_long_word(self):
        self.assertEqual(questions.versing('python'), 'pythoning')

    def test_short_word_ending_with_ing(self):
        self.assertEqual(questions.versing('sing'), 'singly')

    def test_long_word_ending_with_ing(self):
        self.assertEqual(questions.versing('coding'), 'codingly')


class TestWordsConcatenation(unittest.TestCase):

    def test_list(self):
        lst = ["take", "me", "home"]
        self.assertEqual(questions.words_concatenation(lst), 'take me home', 'Should be "take me home"')

    def test_long_list(self):
        lst = ["take", "me", "home", "country", "road"]
        self.assertEqual(questions.words_concatenation(lst), 'take me home country road', 'Should be "take me home country road"')


class TestReverseWordsConcatenation(unittest.TestCase):

    def test_sample(self):
        # your code here
        pass


class TestIsUniqueString(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestListDiff(unittest.TestCase):

    def test_sample(self):
        # your code here
        pass


class TestPrimeNumber(unittest.TestCase):

    def test_sample(self):
        # your code here
        pass


class TestPalindromeNum(unittest.TestCase):
    """
    1 Katas
    """


class TestPairMatch(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestBadAverage(unittest.TestCase):

    def test_sample(self):
        # your code here
        pass


class TestBestStudent(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestPrintDictAsTable(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestMergeDicts(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestSevenBoom(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestCaesarCipher(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


class TestSumOfDigits(unittest.TestCase):
    def test_sample(self):
        # your code here
        pass


if __name__ == '__main__':
    import inspect
    import sys

    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
