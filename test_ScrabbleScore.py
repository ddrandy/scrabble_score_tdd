import unittest
from unittest import mock
from ScrabbleScore import LETTERS
from ScrabbleScore import ScrabbleScore, ScoreCalculator


class ScrabbleScoreTestCase(unittest.TestCase):

    val_1 = list("AEIOULNRST")
    val_2 = list("DG")
    val_3 = list("BCMP")
    val_4 = list("FHVWY")
    val_5 = ["K"]
    val_8 = list("JX")
    val_10 = list("QZ")

    scoreCalc = ScoreCalculator()
    scrabble = ScrabbleScore()

    # letters dictionary unit test
    def test_letters(self):
        self.assertEqual(26, len(LETTERS))

    def test_letter_key(self):
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
        self.check_letter_value(self.val_1, 1)
        self.check_letter_value(self.val_2, 2)
        self.check_letter_value(self.val_3, 3)
        self.check_letter_value(self.val_4, 4)
        self.check_letter_value(self.val_5, 5)
        self.check_letter_value(self.val_8, 8)
        self.check_letter_value(self.val_10, 10)

    def check_letter_value(self, list: list, val: int):
        for char in list:
            self.assertEqual(val, LETTERS[char])

    # scrabble score addition unit test
    def test_score_addition(self):
        self.assertEqual(14, self.scoreCalc.calc("CABBAGE"))

    def test_calc_upper_and_lower_case(self):
        self.assertEqual(8, self.scoreCalc.calc("tomato"))
        self.assertEqual(8, self.scoreCalc.calc("Tomato"))
        self.assertEqual(14, self.scoreCalc.calc("CaBbAgE"))

    @mock.patch("ScrabbleScore.print", create=True)
    @mock.patch("ScrabbleScore.input", create=True)
    def test_user_input(self, mocked_input, mocked_print):
        # invalid input with number
        mocked_input.side_effect = ["ab0"]
        self.scrabble.run()
        self.assertEqual("Please enter alphabet only.", mocked_print.call_args.args[0])

        # invalid input with symbols
        mocked_input.side_effect = ["#$%"]
        self.scrabble.run()
        self.assertEqual("Please enter alphabet only.", mocked_print.call_args.args[0])

        # legal input
        mocked_input.side_effect = ["cabbage"]
        self.scrabble.run()
        self.assertEqual('Score of "cabbage" is: 14', mocked_print.call_args.args[0])

    def test_countdown_timer(self):
        tick_called = 0
        timeout_called = 0

        def tick(tick):
            nonlocal tick_called
            # print("tick {}".format(tick))
            tick_called += 1

        def timeout():
            nonlocal timeout_called
            # print("timeout")
            timeout_called += 1

        timer_thread = self.scrabble.countdown(
            0.05, 0.01, tick_call=tick, timeout_call=timeout
        )
        timer_thread.join()
        self.assertEqual(5, tick_called)
        self.assertEqual(1, timeout_called)

    def test_countdown_score(self):
        self.assertEqual(8, self.scoreCalc.calc("tomato"))
        self.assertEqual(5, self.scoreCalc.calc("tomato", 10))
        self.assertEqual(0, self.scoreCalc.calc("cabbage", 0))

    def test_word_length_generation(self):
        for _ in range(10000):
            length = self.scrabble.random_letter_length()
            self.assertIn(length, range(1, 13))

    def test_word_spelling(self):
        self.assertTrue(self.scrabble.check_spelling("apple"))
        self.assertTrue(self.scrabble.check_spelling("Cabbage"))
        self.assertFalse(self.scrabble.check_spelling("aple"))
        self.assertFalse(self.scrabble.check_spelling("oranga"))


if __name__ == "__main__":
    unittest.main()
