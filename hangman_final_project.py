__author__ = 'Nitzan Papini'
"""
HANGMAN GAME!
-------------
This is the final project in this course. It is a Hangman game.

First of all, the player enters a path for a .txt file 
containing english words, separated by one whitespace.
Secondly, the player enters a natural number thus pointing to a word
within the file.

The rules of the game itself are fairly simple -
the player guesses a letter which s/he thinks is in the word, and
the program checks the guess and reacts accordingly.

The goal? Guess the right letters before you run out of tries, And win the game!

GOOD LUCK!
"""

import os

# Art for the game's opening.
HANGMAN_ASCII_ART = "  _    _                                         \n" \
                    " | |  | |                                        \n" \
                    " | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  \n" \
                    " |  __  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ \n" \
                    " | |  | | (_| | | | | (_| | | | | | | (_| | | | |\n" \
                    " |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|\n" \
                    "                      __/ |                      \n" \
                    "                     |___/ "
# Maximum number of tries:
MAX_TRIES = 6
# Photos of all of the hanged man's statuses.
HANGMAN_PHOTOS = {
    0: r"""
x-------x
    """,
    1: r"""
x-------x
|
|
|
|
|
    """,
    2: r"""
x-------x
|       |
|       0
|
|
|
    """,
    3: r"""
x-------x
|       |
|       0
|       |
|
|
    """,
    4: r"""
x-------x
|       |
|       0
|      /|\ 
|
|
    """,
    5: r"""
x-------x
|       |
|       0
|      /|\ 
|      /
|
    """,
    6: r"""
x-------x
|       |
|       0
|      /|\ 
|      / \ 
|
    """,
}


def main():
    """
    Runs program.
    :return: None
    :rtype: None
    """
    opening_screen()
    # Receive a valid file path and a valid index for a word,
    # then pick a secret word and run the game.
    path = validate_file_path()
    index = validate_index()
    secret_word = choose_word(path, index)
    print("Let's begin playing!!!\n")
    print(hangman(secret_word))


def opening_screen():
    """
    This function prints out the opening screen of the Hangman Game!
    :return: None
    :rtype: None
    """
    print(HANGMAN_ASCII_ART, '\n', MAX_TRIES, '\n\n')


def hangman(the_secret_word):
    """
    This function handles the game itself.
    :param the_secret_word: as received from file by the main() function.
    Guessing it is the goal of the player.
    :type the_secret_word: str
    :return: WIN or LOSE
    :rtype: str
    """
    old_letters_guessed = []
    num_of_tries = 0
    print_hangman_status(0)
    # Continue to play until valid but wrong inputs exceed maximum
    # number of tries, or player has won the game.
    while num_of_tries < MAX_TRIES:
        show_hidden_word(the_secret_word, old_letters_guessed)
        # Read until we get a valid guess.
        while True:
            letter_guessed = input("Guess a letter, will'ya? ").lower()
            if try_update_letter_guessed(letter_guessed, old_letters_guessed):
                break

        if letter_guessed not in the_secret_word:
            # Wrong guess.
            num_of_tries += 1
            print(':(')
            print_hangman_status(num_of_tries)
            continue

        # If the player has guessed the word, he has won the game!
        if check_win(the_secret_word, old_letters_guessed):
            return 'WIN'
    # If player guessed wrong 6 times, he has lost the game!
    return 'LOSE'


def validate_index():
    """
    This function makes sure the player enters a valid index for file.
    Valid index must be a natural number.
    :return: index of word in given file.
    :rtype: int
    """
    index = input("Guess a number pointing to"
                  " secret word within file: ")
    while not index.isdigit() or int(index) <= 0:
        index = input("The number must be a natural"
                      " number. Try again: ")
    return int(index)


def validate_file_path():
    """
        This function makes sure the player enters a valid path of file.
        Valid path must exist, be readable, and be a text file.
        :return: path of file.
        :rtype: str
        """
    while True:
        file_path = input("Please enter a text file path containing the"
                          " words for guessing:\n")
        if not os.path.exists(file_path):
            print("Path entered does not exist.")
        elif not os.access(file_path, os.R_OK):
            print("The file you chose is not readable.")
        elif os.path.splitext(file_path.lower())[1] != '.txt':
            print("The file you choose must be a text file and"
                  " its path must end with '.txt'.")
        else:
            break

    return file_path


def print_hangman_status(failed_tries):
    """
    This function prints out the hanged man's current
    status according to the amount of tries the player has wasted.
    :param failed_tries: number of tries
    :type failed_tries: int
    :return: None
    :rtype: None
    """
    print(HANGMAN_PHOTOS[failed_tries])


def show_hidden_word(the_secret_word, letters_already_guessed):
    """
    This function shows the part of the secret
    word that the player has already guessed.
    :param the_secret_word: The full secret word.
    :param letters_already_guessed: Letters that the player
    has already guessed.
    :type the_secret_word: str
    :type letters_already_guessed: list
    :return: shown_word
    :rtype: str
    """

    shown_word = ''
    for letter in the_secret_word:
        if letter in letters_already_guessed:
            shown_word += letter + ' '
        else:
            shown_word += '_ '
    print(shown_word)
    return shown_word


def choose_word(file_path, index):
    """
    This function returns the secret word based on the index received.
    :param file_path: the path of the file containing all the words
    :param index: an index that points to the secret word in the file.
    :type file_path: str
    :type index: int
    :return: The secret word based on the index of it in the file.
    :rtype: str
    """
    with open(file_path, "r") as words_file:
        # Create a list containing all the words from the file.
        list_of_words = []
        for line in words_file:
            list_of_words += line.split()
        # Remove any duplicates from list.
        list_of_words = list(dict.fromkeys(list_of_words))
    # Find word at given index to be the secret word
    # (assuming index starts at 1):
    index = (index - 1) % len(list_of_words)
    the_secret_word = list_of_words[index]
    return the_secret_word


def check_valid_input(letter_guessed, letters_already_guessed):
    """
    Returns True if letter_guessed is indeed an english letter,
    one letter long and has not been tried before.
    :param letter_guessed: Letter guessed received by player
    :param letters_already_guessed: list of all the valid letter that
    has already been tried
    :type letter_guessed: str
    :type letters_already_guessed: list
    :return: Whether letter_guessed is a valid input
    :rtype: bool
    """
    return (len(letter_guessed) == 1 and
            letter_guessed.isalpha() and
            letter_guessed not in letters_already_guessed)


def try_update_letter_guessed(letter_guessed, letters_already_guessed):
    """
    Returns 'True' if 'letter_guessed' is indeed an english letter,
    one letter long and has not been tried before.
    :param letter_guessed: Letter guessed received by player
    :param letters_already_guessed: list of all the valid letter that
    has already been tried
    :type letter_guessed: str
    :type letters_already_guessed: list
    :return: Whether letter_guessed is a valid input
    :rtype: bool
    """
    if check_valid_input(letter_guessed, letters_already_guessed):
        letters_already_guessed.append(letter_guessed)
        letters_already_guessed.sort()
        return True
    print('X')
    print(' -> '.join(letters_already_guessed))
    return False


def check_win(the_secret_word, letters_already_guessed):
    """
    This function checks if the player has won the game.
    :param the_secret_word:
    :param letters_already_guessed: All the letters the player has
    already guessed.
    :type the_secret_word: str
    :type letters_already_guessed: list
    :return: True if ALL letters of the secret word are also in
    the letters_already_guessed list.
    :rtype: bool
    """
    return set(the_secret_word) <= set(letters_already_guessed)


if __name__ == '__main__':
    main()
