import unittest
from unittest import mock
from ScrabbleScore import LETTERS
from ScrabbleScore import ScrabbleScore, ScoreCalculator


class LettersTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """SetUp for Letters tests."""
        self.val_1 = list("AEIOULNRST")
        self.val_2 = list("DG")
        self.val_3 = list("BCMP")
        self.val_4 = list("FHVWY")
        self.val_5 = ["K"]
        self.val_8 = list("JX")
        self.val_10 = list("QZ")

    # letters dictionary unit test
    def test_letters(self):
        """Test letters dict length."""
        self.assertEqual(26, len(LETTERS))

    def test_letter_key(self):
        """Test character key."""
        for char in self.val_1:
            self.assertIn(char, LETTERS)
        for char in self.val_2:
            self.assertIn(char, LETTERS)
        for char in self.val_3:
            self.assertIn(char, LETTERS)
        for char in self.val_4:
            self.assertIn(char, LETTERS)
        for char in self.val_5:
            self.assertIn(char, LETTERS)
        for char in self.val_8:
            self.assertIn(char, LETTERS)
        for char in self.val_10:
            self.assertIn(char, LETTERS)

    def test_letter_value(self):
        """Test letter values."""
        self.check_letter_value(self.val_1, 1)
        self.check_letter_value(self.val_2, 2)
        self.check_letter_value(self.val_3, 3)
        self.check_letter_value(self.val_4, 4)
        self.check_letter_value(self.val_5, 5)
        self.check_letter_value(self.val_8, 8)
        self.check_letter_value(self.val_10, 10)

    def check_letter_value(self, list: list, val: int):
        """Internal function."""
        for char in list:
            self.assertEqual(val, LETTERS[char])


class ScoreCalculatorTestCase(unittest.TestCase):

    def setUp(self):
        """Setup for ScoreCalculator tests."""
        self.calculator = ScoreCalculator()

    def test_score_calculation(self):
        """Test the score calculation for a word."""
        self.assertEqual(self.calculator.calc("cabbage"), 14)
        self.assertNotEqual(self.calculator.calc("scrabble", timeleft=10), 14)

    def test_score_case_insensitivity(self):
        """Test score calculation is case insensitive."""
        self.assertEqual(
            self.calculator.calc("Scrabble"), self.calculator.calc("scrabble")
        )

    def test_empty_word(self):
        """Test calculation for an empty word."""
        self.assertEqual(self.calculator.calc(""), 0)

    def test_non_alphabetic_characters(self):
        """Test score calculation for non-alphabetic input."""
        self.assertEqual(self.calculator.calc("1234"), 0)
        self.assertEqual(self.calculator.calc("!@#$"), 0)
        self.assertEqual(
            self.calculator.calc("hello123"), 8
        )  # Only letters should count

    def test_extremely_long_word(self):
        """Test calculation for a long word."""
        long_word = "a" * 1000  # Word with 1000 'a' characters
        self.assertEqual(self.calculator.calc(long_word), 1000)

    def test_mixed_case_input(self):
        """Test mixed-case input produces the same score."""
        self.assertEqual(
            self.calculator.calc("ScRaBbLe"), self.calculator.calc("scrabble")
        )

    def test_repeated_characters(self):
        """Test calculation for words with repeated characters."""
        self.assertEqual(self.calculator.calc("aaaa"), 4)

    def test_timing_edge_cases(self):
        """Test timing edge cases."""
        self.assertEqual(self.calculator.calc("scrabble", timeleft=0), 0)
        self.assertEqual(self.calculator.calc("scrabble", timeleft=-5), 0)


class ScrabbleScoreTestCase(unittest.TestCase):

    def setUp(self):
        """Setup for ScrabbleScore game tests"""
        self.game = ScrabbleScore()

    def test_check_spelling(self):
        """Test word validation against the dictionary."""
        self.assertTrue(self.game.check_spelling("apple"))
        self.assertFalse(self.game.check_spelling("xyzabc"))
        self.assertFalse(
            self.game.check_spelling("")
        )  # Empty string is not a valid word

    def test_random_letter_length(self):
        """Test random letter length generation."""
        length = self.game.random_letter_length()
        self.assertIsInstance(length, int)
        self.assertGreater(length, 0)
        # self.assertLessEqual(length, 15)

    def test_game_exit_condition(self):
        """Test the game exit condition logic."""
        self.game.exit = True
        self.assertTrue(self.game.exit)

    @mock.patch("ScrabbleScore.print", create=True)
    @mock.patch("ScrabbleScore.input", create=True)
    def test_user_input(self, mocked_input, mocked_print):
        """Test user input with mocked inputs."""
        # invalid input with number
        mocked_input.side_effect = ["ab0"]
        self.game.run()
        self.assertEqual("Please enter alphabet only.", mocked_print.call_args.args[0])

        # invalid input with symbols
        mocked_input.side_effect = ["#$%"]
        self.game.run()
        self.assertEqual("Please enter alphabet only.", mocked_print.call_args.args[0])

        # legal input
        mocked_input.side_effect = ["cabbage"]
        self.game.run()
        self.assertEqual('Score of "cabbage" is: 14', mocked_print.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
