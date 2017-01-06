from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with marker indicating pegs,
        spaces, and unused and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = list()
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid1.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "#", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = list()
        >>> grid2.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid2.append(["*", ".", "*", "*", "*", ".", "."])
        >>> grid2.append([".", "*", "*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "#", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid2.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid2.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gps1 == gps2
        False
        >>> grid3 = list()
        >>> grid3.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid3.append(["*", ".", "*", "*", "*", ".", "."])
        >>> grid3.append([".", "*", "*", "*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "#", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid3.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid3.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gps2 == gps3
        True
        """
        return type(self) == type(other) and self._marker == other._marker

    # noinspection PyGlobalUndefined
    def __str__(self):
        """
        Return string representation of GridPegSolitairePuzzle self.

        >>> grid = list()
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "#", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gps)
         .  .  *  *  *  .  .
         .  .  *  *  *  .  .
         *  *  *  *  *  *  *
         *  *  *  #  *  *  *
         *  *  *  *  *  *  *
         .  .  *  *  *  .  .
         .  .  *  *  *  .  .
        """
        global z
        string = ""
        for i in self._marker:
            for z in range(len(i) - 1):
                string += " " + i[z] + " "
            string += " " + i[z] + "\n"
        return string[:-1].rstrip()

    def __repr__(self):
        """
        Represent GridPegSolitairePuzzle self as a string that can be evaluated
        to produce an equivalent GridPegSolitairePuzzle.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = list()
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "#", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*", "*", "*"])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gps
        GridPegSolitairePuzzle([['.', '.', '*', '*', '*', '.', '.'], \
['.', '.', '*', '*', '*', '.', '.'], \
['*', '*', '*', '*', '*', '*', '*'], \
['*', '*', '*', '#', '*', '*', '*'], \
['*', '*', '*', '*', '*', '*', '*'], \
['.', '.', '*', '*', '*', '.', '.'], ['.', '.', '*', '*', '*', '.', '.']])
        """
        return "GridPegSolitairePuzzle({})".format(self._marker)

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = list()
        >>> grid1.append([".", ".", ".", "*", ".", ".", "."])
        >>> gps1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> gps1.is_solved()
        True
        >>> grid2 = list()
        >>> grid2.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gps2.is_solved()
        False
        """
        return len(self._pegs_coordinates()) == 1

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid1 = list()
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> grid1.append([".", ".", "*", "*", "*", ".", "."])
        >>> gps = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> l1 = list(gps.extensions())
        >>> l2 = list(gps.extensions())
        >>> len(l1) == len(l2)
        True
        >>> all([s in l2 for s in l1])
        True
        >>> all([s in l1 for s in l2])
        True
        """
        # introducing variables for the convenience
        ext_list = []
        directions = ["up", "down", "left", "right"]
        peg_coordinates = self._pegs_coordinates()
        # loops over coordinates/directions and makes the appropriate swaps
        for i in peg_coordinates:
            for j in directions:
                legal_extension = self._jump(j, i)
                # returns list of tuples with new coordinates of the extensions
                if legal_extension:
                    ext_list.append(GridPegSolitairePuzzle(legal_extension,
                                                           self._marker_set))
        return ext_list

    def _jump(self, direction, peg_coordinates):

        x = peg_coordinates[0]
        y = peg_coordinates[1]
        # looping over every sub-list to copy the marker list
        marker_copy = [i[:] for i in self._marker]
        # checking whether peg coordinates refer to a peg
        if marker_copy[x][y] != "*":
            return None
        # checking if the target coordinate refers to a valid cell in the board
        elif (direction == "up" and x-2 >= 0 and marker_copy[x-1][y] == "*" and
              marker_copy[x-2][y] == "."):
            # check if target coordinate refers to empty and if jumping over peg
            marker_copy[x-2][y], marker_copy[x-1][y] = "*", "."
            # swap empty with peg and vice versa, and peg jumped over w/ empty
            marker_copy[x][y] = "."
        elif (direction == "down" and x+2 <= len(self._marker)-1 and
              marker_copy[x+1][y] == "*" and marker_copy[x+2][y] == "."):
            marker_copy[x+2][y], marker_copy[x+1][y] = "*", "."
            marker_copy[x][y] = "."
        elif (direction == "left" and y-2 >= 0 and
              marker_copy[x][y-1] == "*" and marker_copy[x][y-2] == "."):
            marker_copy[x][y-2], marker_copy[x][y-1] = "*", "."
            marker_copy[x][y] = "."
        elif (direction == "right" and y+2 <= len(self._marker[0])-1 and
              marker_copy[x][y+1] == "*" and marker_copy[x][y+2] == "."):
            marker_copy[x][y+2], marker_copy[x][y+1] = "*", "."
            marker_copy[x][y] = "."
        else:
            return None

        return marker_copy

    def _pegs_coordinates(self):

        peg_coordinates = []
        # loop over marker/sub-list of marker to check if index refers to a peg
        for i in range(len(self._marker)):
            for j in range(len(self._marker[i])):
                if self._marker[i][j] == "*":
                    # creating a list of tuples with the coordinates of the pegs
                    peg_coordinates.append((i, j))
        return peg_coordinates

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
