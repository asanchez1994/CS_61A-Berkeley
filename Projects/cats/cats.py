

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    count = 0

    for elem in paragraphs:
        if select(elem) == True:
            count +=1
            if count == k + 1:
                return elem
    return ""

    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2


    def helper(string):

        # prepare string for comparison with topics
        lower_string = string.lower()
        new_string = remove_punctuation(lower_string) 
        final_string = new_string.split(" ")

        # check each element for a match
        for elem in topic:
            for x in final_string:
                if x == elem:
                    return True
        return False

    return helper
        
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3

    misses = 0 
    if len(typed_words) > len(reference_words):
        misses = len(typed_words) - len(reference_words)
    percent = 0.0
    
    if len(typed_words) == 0:
        return 0.0
    
    for words1, words2 in zip(typed_words, reference_words):
        if words1 != words2:
            misses += 1

    percent = 100 * ((len(typed_words) - misses)/len(typed_words))
    if percent < 0.0:
        return 0.0

    return percent

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(list(typed))/ 5) * (60 / elapsed) 
    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    diff_list =[]
    min_diff = 0 

    # Check for exact match
    for elem in valid_words:
        if elem == user_word:
            return user_word

        # Calculate minimum difference 
        diff_list.append(diff_function(user_word, elem, limit))
        min_diff = min(diff_list)
    
    # Find word with minimum distance
    if min_diff <= limit: 
        for elem in valid_words:
            if diff_function(user_word, elem, limit) == min_diff:
                return elem
    else:
        return user_word

    # END PROBLEM 5


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6

    def helper(changes=0, index=0):

        # Do not exceed limit
        if changes > limit:
            return limit + 1

        # Bases cases
        if len(start) == index or len(goal) == index:
            return changes + abs(len(start) - len(goal))

        # Recursive calls 
        elif start[index] == goal[index]:
            return helper(changes, index+1)
        else:
            return helper(changes+1, index+1)
            
    return helper()

    # END PROBLEM 6


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def helper(start, goal, answer):

        if answer > limit:
            return limit + 1

        if min(len(goal), len(start)) == 0:
            return answer + max(len(goal), len(start))
        else:
            if start[0] == goal[0]:
                return helper(start[1:], goal[1:], answer)
            else:
                add_diff = helper(start, goal[1:], answer + 1) 
                sub_diff = helper(start[1:], goal, answer + 1) 
                reverse_diff = helper(start[1:], goal[1:], answer + 1)

                return min(add_diff, sub_diff, reverse_diff)

    return helper(start, goal, 0)

def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    
    # BEGIN PROBLEM 8

    counter = 0
    for elem in typed:
        if elem == prompt[counter]:
            counter += 1
        else:
            break

    progress_ratio = counter / len(prompt)

    send({'id': id, 'progress': progress_ratio})
    return progress_ratio

    # END PROBLEM 8

def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9

    # Declare list of list to populate 
    metalist = []

    # Generate times for each word per player
    for i in range(len(times_per_player)):
        metalist.append([])
        for j in range(len(times_per_player[i]) - 1):
            metalist[i].append(times_per_player[i][j+1] - times_per_player[i][j])
        
    # Use constructor to encapsulate list of lists and word list 
    return game(words, metalist)

    "** YOUR CODE HERE ***"
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    # BEGIN PROBLEM 10

    # Generate list of lists to return
    metalist = []
    for _ in players:
        metalist.append([])
        
    # Loop through all words
    for word in words:
        fastest_time = 100000
        fastest_player = "dummy"

        # For each word, check each player's performance
        for player in players:
            # Remember player who got the best score 
            if time(game, player, word) < fastest_time:
                fastest_time = time(game, player, word)
                fastest_player = player

        # Add word to list of player who scored best 
        metalist[fastest_player].append(word_at(game, word))

    return metalist

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
