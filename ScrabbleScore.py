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
        for char in word:
            if char in LETTERS:
                sum += LETTERS[char]
        return sum
