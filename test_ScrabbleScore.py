import unittest
from ScrabbleScore import LETTERS
from ScrabbleScore import ScoreCalculator


class ScrabbleScoreTestCase(unittest.TestCase):

    val_1 = list("AEIOULNRST")
    val_2 = list("DG")
    val_3 = list("BCMP")
    val_4 = list("FHVWY")
    val_5 = ["K"]
    val_8 = list("JX")
    val_10 = list("QZ")

    scoreCalc = ScoreCalculator()

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

if __name__ == "__main__":
    unittest.main()
