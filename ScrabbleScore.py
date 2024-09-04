import time
import threading
from typing import Callable
import random
import nltk

try:
    nltk.data.find("corpora/words.zip")
except LookupError:
    nltk.download("words")
from nltk.corpus import words

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
    word_list = set(words.words())

    def run(self):
        word = input("Please enter a word:")
        if not word.isalpha():
            print("Please enter alphabet only.")
        else:
            score = self.scoreCalc.calc(word)
            print(f'Score of "{word}" is: {score}')

    def countdown(
        self,
        timeout,
        tick=1,
        tick_call: Callable[[int], None] = None,
        timeout_call: Callable[[], None] = None,
    ) -> threading.Thread:
        def run_countdown():
            nonlocal timeout
            while timeout > 0:
                tick_call(timeout)
                time.sleep(tick)
                timeout -= tick
            timeout_call()

        countdown_thread = threading.Thread(target=run_countdown)
        countdown_thread.daemon = True
        countdown_thread.start()
        return countdown_thread

    def random_letter_length(self):
        return random.randint(1, 12)

    def check_spelling(self, word):
        return word.lower() in self.word_list
