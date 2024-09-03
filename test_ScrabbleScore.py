import unittest
from ScrabbleScore import LETTERS

class ScrabbleScoreTestCase(unittest.TestCase):
    
    # letters dictionary unit test
    def test_letters(self):
        self.assertEqual(26, len(LETTERS))
        

if __name__ == "__main__":
    unittest.main()