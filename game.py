from time import sleep

from colorama import init
from termcolor import colored

from papers_please.inspector import Inspector
from papers_please.data_constructor import DataStarterPack
from papers_please.input_utils import input_int, user_input, confirm


class Game(object):
    """Gaming process."""

    def __init__(self):
        self.ins = None
        self.failures = 0

    def __enter__(self):
        self.init_game()
        return self

    def __exit__(self, err_type, err, err_traceback):
        self.stop()

    def init_game(self):
        """Assign game properties."""
        self.ins = Inspector()
        self.failures = 3  # the game stops after 3 mismatches
        init()  # colorama method-helper for termcolor proper operations on Win

    def start(self):
        """Start the game."""
        ins = self.ins
        day_number = 1
        mistakes = {
            3: 'first',
            2: 'second',
            1: 'last'
        }

        while self.failures:
            # You already can quit after the first game day.
            if day_number > 1:
                wanna_rest = confirm(
                    'Are you wanna get a rest', default_no=True
                )
                if wanna_rest:
                    break

            print(f'Day №{day_number}\n')
            entrants_value = input_int(
                'How many entrants you can serve', default=5, show_default=False
            )

            # Following operations of while loop are unreachable
            # if entrants_value = 0.
            if entrants_value:
                data = DataStarterPack(entrants_value)

                bulletin = data.create_bulletin()
                print('=================')
                print(bulletin)
                print('=================\n')

                ins.receive_bulletin(bulletin)
                entrants = data.create_papers()

                for entrant in entrants:
                    color = 'red'  # default color of decision representation

                    # Following operations of for loop are unreachable if
                    # you have 3 mistakes.
                    if not self.failures:
                        continue

                    user_input('Next')  # splitter between entrants
                    print('-----------------')
                    for document, contents in entrant.items():
                        print('DOCUMENT:', document.replace('_', ' '))
                        print(contents)
                        print('-----------------')

                    answer, decision = ins.inspect(entrant)
                    your_answer = confirm(
                        '\nLet the entrant in', default_yes=True
                    )
                    if your_answer != answer:  # mismatching handler
                        print(
                            f"\nIt's your {mistakes.get(self.failures)} mistake!"
                        )
                        self.failures -= 1

                    # Change color to green if entrant is allowed.
                    if answer:
                        color = 'green'
                    print(colored(f'\n{decision}\n', color))

                ins.clear()  # clear inspector's cache
                day_number += 1

            sleep(2)

        # Following representation is unreachable
        # if you wanna quit (get a rest).
        if not self.failures:
            print("You're fired!")

    def stop(self):
        """Stop the game."""
        self.ins = None


def main():
    """Initialize the game."""
    with Game() as game:
        game.start()


if __name__ == '__main__':
    main()
