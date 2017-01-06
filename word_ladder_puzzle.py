from puzzle import Puzzle

class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> w1 = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> w2 = WordLadderPuzzle('same', 'came', {'same', 'came', 'case'})
        >>> w3 = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> w1 == w2
        False
        >>> w1 == w3
        True
        """
        return (type(self) == type(other) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return string representation of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> print(w)
        same -> case
        """
        return "{} -> {}".format(self._from_word, self._to_word)

    def __repr__(self):
        """
        Represent WordLadderPuzzle self as a string that can be evaluated to
        produce an equivalent WordLadderPuzzle.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> w
        WordLadderPuzzle(same -> case)
        """
        return "WordLadderPuzzle({} -> {})".format(self._from_word,
                                                   self._to_word)

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> w.is_solved()
        False
        >>> w = WordLadderPuzzle('came', 'case', {'same', 'came', 'case'})
        >>> w.is_solved()
        False
        >>> w = WordLadderPuzzle('case', 'case', {'same', 'came', 'case'})
        >>> w.is_solved()
        True
        """
        return self._from_word == self._to_word

    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w = WordLadderPuzzle('same', 'case', {'same', 'came', 'case'})
        >>> l1 = list(w.extensions())
        >>> l2 = list(w.extensions())
        >>> len(l1) == len(l2)
        True
        >>> all([s in l2 for s in l1])
        True
        >>> all([s in l1 for s in l2])
        True
        """
        ext_list = []
        legal, illegal = 0, 1

        # iterate through words in set until desired length is reached
        for word in self._word_set:
            if len(word) != len(self._from_word):
                pass
            else:
                # current word has desired length
                j = legal
                # iterate through characters of word until equivalence is false
                for i in range(len(word)):
                    if word[i] == self._from_word[i]:
                        pass
                    else:
                        # equivalence of current letter is false
                        j += illegal

                # append word to list if condition is met
                if j == illegal:
                    ext_list.append(WordLadderPuzzle(word,
                                                     self._to_word,
                                                     self._word_set))

        return ext_list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import depth_first_solve, \
        breadth_first_solve
    from time import time
    with open("words.txt", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
