LETTERS = {
    x: y
    for key, y in {
        "AEIOULNRST": 1,
        "DG": 2,
        "BCMP": 3,
        "FHVWY": 4,
        "K": 5,
        "JX": 8,
        "QZ": 10,
    }.items()
    for x in key
}


class ScoreCalculator(object):

    def calc(self, word: str):
        sum = 0
        for char in word.upper():
            if char in LETTERS:
                sum += LETTERS[char]
        return sum


class ScrabbleScore:
    scoreCalc = ScoreCalculator()

    def run(self):
        word = input("Please enter a word:")
        if not self.isAlphaOnly(word):
            print("Please enter alphabet only.")
        else:
            score = self.scoreCalc.calc(word)
            print(f'Score of "{word}" is: {score}')
