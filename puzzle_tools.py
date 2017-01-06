"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque

# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    Example not feasible due to the requirement of
    instantiation of large amount of variables
    """

    # dictionary of string representation of the puzzle configurations that has
    # been seen
    seen_config = {}

    p_node = PuzzleNode(puzzle)

    def _find_sol(puzzle_node):
        """
        @type puzzle_node: PuzzleNode
        @rtype: PuzzleNode
        """
        # if the puzzle configuration is already seen then we ignore it
        if str(puzzle_node.puzzle) in seen_config:
            return None

        # when puzzle solved, return the node
        elif puzzle_node.puzzle.is_solved():
            return puzzle_node

        # if fail_function is true, add the configuration to seen_config
        elif puzzle_node.puzzle.fail_fast():
            seen_config[str(puzzle_node.puzzle)] = True
            return None

        else:
            # save the configuration as already seen
            seen_config[str(puzzle_node.puzzle)] = True

            # set the puzzle_node's children into the puzzle's extensions
            # with puzzle_node as the parent

            children = [PuzzleNode(i, parent=puzzle_node) for i in
                        puzzle_node.puzzle.extensions()]

            for i in children:
                # return path if it reaches towards a solution
                path = _find_sol(i)
                if path:
                    return path

    return _one_path(_find_sol(p_node))


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    Example not feasible due to the requirement of
    instantiation of large amount of variables
    """
    a = PuzzleNode(puzzle)

    # a set of puzzles that has already been seen
    has_seen = set()

    # a list to act as a queue
    pending = deque([a])

    while len(pending) != 0:

        # keep track of visited nodes
        visited = pending.popleft()
        # check if puzzle is solved
        if visited.puzzle.is_solved():
            return _one_path(visited)

        elif visited.puzzle.fail_fast():
            return None

        else:
            # check if the puzzle configuration has already been seen
            if str(visited.puzzle) not in has_seen:
                has_seen.add(str(visited.puzzle))

                # set the puzzle_node's children into the puzzle's extensions
                # with puzzle_node as the parent
                children = [PuzzleNode(i, parent=visited) for i in
                            visited.puzzle.extensions()]
                visited.children = children

                for i in children:
                    pending.append(i)


def _one_path(p_node):
    """
    Helper function for the Search Functions
    Clears out the paths that does not lead to the proper solution and returns
    a p_node with only 1 children where p_node is the proper final solution
    of the puzzle

    @type p_node: PuzzleNode
    @rtype: PuzzleNode
    """

    if not p_node.parent:
        return p_node
    else:

        # makes the parent of p_node have p_node as its only child
        p_node.parent.children = [p_node]

        # recursively call one_path on the parent of p_node until we reach
        # the root
        return _one_path(p_node.parent)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type
         self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other.

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1 == pn2
        True
        >>> pn1 == pn3
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
