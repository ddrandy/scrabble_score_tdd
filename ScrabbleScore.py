import threading
from typing import Callable
import random
import nltk

try:
    nltk.data.find("corpora/words.zip")
except LookupError:
    nltk.download("words")
from nltk.corpus import words
import curses, curses.ascii
from collections import deque

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
COUNTDOWN_TIME = 15
ROUND = 10


class ScoreCalculator(object):

    def calc(self, word: str, timeleft=COUNTDOWN_TIME):
        sum = 0
        for char in word.upper():
            if char in LETTERS:
                sum += LETTERS[char]
        return max(sum * timeleft // COUNTDOWN_TIME, 0)


class Screen:

    round_hint = "Round {}:"
    score_hint = "Current word score: {} Total score: {}"
    info_hint = "Press ESC to end game. Press ENTER to submit word. Press BACKSPACE to delete last input."
    timeout_hint = "Word input timeout on round {}"
    invalid_hint = "Invalid word entered"
    invalid_length_hint = "The length of the word does not match"
    prompt_hint = "Please enter a word of {} letters within {} seconds:"

    round_line = 0
    score_line = 1
    info_line = 2
    output_line = 4
    prompt_line = 5
    input_line = 6

    def __init__(self) -> None:
        win = self.win = curses.initscr()
        curses.reset_prog_mode()
        win.clrtobot()
        win.scrollok(False)
        win.keypad(True)
        pass

    def print_round(self, round, line=round_line):
        self._print_line(line, self.round_hint.format(round))

    def print_score(self, current_score, total_score, line=score_line):
        self._print_line(line, self.score_hint.format(current_score, total_score))

    def print_info(self, line=info_line):
        self._print_line(line, self.info_hint)

    def print_timeout(self, round, line=output_line):
        self._print_line(line, self.timeout_hint.format(round))

    def print_invalid(self, line=output_line):
        self._print_line(line, self.invalid_hint)

    def print_invalid_length(self, line=output_line):
        self._print_line(line, self.invalid_length_hint)

    def clear_line(self, line=output_line):
        self._print_line(line, "", True)

    def close(self):
        self.win.clear()
        self.win.scrollok(True)
        curses.endwin()
        curses.reset_shell_mode()

    def print_prompt(self, length, timeout, line=prompt_line):
        self._print_line(line, self.prompt_hint.format(length, timeout))

    def _print_line(self, line: int, message: str, clear_line=True):
        win = self.win
        y, x = win.getyx()
        win.move(line, 0)
        if clear_line:
            win.clrtoeol()
        win.addstr(message)
        win.move(y, x)
        win.refresh()

    def printer_input(self, word, on_enter_pressed: Callable, on_exit: Callable):
        win = self.win
        win.move(self.input_line, 0)
        while True:
            ch = win.getch()
            # clear warning info
            self.clear_line()
            # exit on press ESC
            if ch == curses.ascii.ESC or ch == curses.KEY_EXIT:
                self.clear_line(self.input_line)
                on_exit()
                break
            # read word on pressed ENTER
            elif (
                ch == curses.KEY_ENTER or ch == curses.ascii.NL or ch == curses.ascii.CR
            ):
                on_enter_pressed()
            # character pressed
            elif ch in range(ord("a"), ord("z") + 1) or ch in range(
                ord("A"), ord("Z") + 1
            ):
                word.append(str(chr(ch)))
                pass
            # delete character on press BACKSPACE
            elif (
                ch == curses.ascii.BS
                or ch == curses.KEY_BACKSPACE
                or ch == curses.ascii.DEL
            ):
                if word:
                    word.pop()
            else:
                self.print_invalid()
            # show input characters
            self._print_line(self.input_line, "".join(word))
            win.move(self.input_line, len(word))
        win.move(self.input_line, len(word))


class ScrabbleScore:
    scoreCalc = ScoreCalculator()
    word_list = words.words()
    word_set = set(words.words())
    screen = Screen()
    interrupt_call = None
    exit = False
    round = 1
    timeout = COUNTDOWN_TIME
    current_score = 0
    total_score = 0
    length = None
    word = deque()

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

        event = threading.Event()

        def interrupt_call():
            event.set()

        self.interrupt_call = interrupt_call

        def run_countdown():
            self.timeout = timeout
            interrupted = False
            while self.timeout > 0 and not interrupted:
                tick_call(self.timeout)
                interrupted = event.wait(tick)
                if not interrupted:
                    self.timeout -= tick
            if not interrupted:
                timeout_call()

        return self.new_thread(run_countdown, join=True)

    def random_letter_length(self):
        return len(random.choice(self.word_list))

    def check_spelling(self, word):
        return word.lower() in self.word_set

    def print_screen(self):
        screen = self.screen

        def tick_call(tick):
            screen.print_prompt(self.length, tick)

        def timeout_call():
            screen.print_timeout(self.round)
            self.word.clear()

        while self.round <= ROUND and not self.exit:
            screen.print_round(self.round)
            screen.print_score(self.current_score, self.total_score)
            screen.print_info()
            self.length = self.random_letter_length()
            self.countdown(COUNTDOWN_TIME, 1, tick_call, timeout_call)
            self.round += 1
        screen.close()

    def read_input(self):
        def on_enter_pressed():
            word = "".join(self.word)
            isValid = len(word) == self.length and self.check_spelling(word)
            if isValid:
                self.current_score = self.scoreCalc.calc(word, self.timeout)
                self.total_score += self.current_score
                if self.interrupt_call:
                    self.interrupt_call()
                self.word.clear()
            elif len(word) != self.length:
                self.screen.print_invalid_length()
            else:
                self.screen.print_invalid()
            return isValid

        def on_exit():
            self.exit = True
            if self.interrupt_call:
                self.interrupt_call()
            pass

        self.screen.printer_input(self.word, on_enter_pressed, on_exit)

    def new_thread(
        self, target=None, daemon=True, join=False, join_timeout=None, start=True
    ):
        thread = threading.Thread(target=target)
        thread.daemon = daemon
        if start:
            thread.start()
        if join:
            thread.join(join_timeout)

    def main(self):
        self.new_thread(self.read_input, start=True)
        self.new_thread(self.print_screen, join=True, start=True)

        # print total score after player quits the game
        print("\rTotal score: {}".format(self.total_score))
        pass


if __name__ == "__main__":
    ScrabbleScore().main()
