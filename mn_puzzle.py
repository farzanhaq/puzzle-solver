from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like 15-puzzle, which may be solved, unsolved, or unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a '*'
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> grid1 = list()
        >>> grid1.append(['*', '1', '2'])
        >>> grid1.append(['3', '4', '5'])
        >>> grid2 = list()
        >>> grid2.append(['*', '1', '2'])
        >>> grid2.append(['3', '4', '5'])
        >>> mn1 = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> mn2 = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> mn1 == mn2
        True
        """
        return (type(self) == type(other) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    # noinspection PyGlobalUndefined
    def __str__(self):
        """
        Return string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str
        >>> grid1 = list()
        >>> grid1.append(['*', '1', '2'])
        >>> grid1.append(['3', '4', '5'])
        >>> grid2 = list()
        >>> grid2.append(['*', '1', '2'])
        >>> grid2.append(['3', '4', '5'])
        >>> mn1 = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> print(mn1)
        ---------
         *  1  2
         3  4  5
        ---------
        """
        global z
        string = '-' * 9 + '\n'
        for i in self.from_grid:
            for z in range(len(i) - 1):
                string += ' ' + i[z] + ' '
            string += ' ' + i[z + 1] + '\n'
        string += '-' * 9
        return string

    def __repr__(self):
        """
        Represent MNPuzzle self as a string that can be evaluated to produce an
        equivalent MNPuzzle.

        @type self: MNPuzzle
        @rtype: str

        >>> grid1 = list()
        >>> grid1.append(['*', '1', '2'])
        >>> grid1.append(['3', '4', '5'])
        >>> grid2 = list()
        >>> grid2.append(['*', '1', '2'])
        >>> grid2.append(['3', '4', '5'])
        >>> mn = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> mn
        MNPuzzle[['*', '1', '2'], ['3', '4', '5']]
        """
        return 'MNPuzzle{}'.format([(self.from_grid[i]) for i in range(self.n)])

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool

        >>> grid1 = list()
        >>> grid1.append(['*', '1', '2'])
        >>> grid1.append(['3', '4', '5'])
        >>> grid2 = list()
        >>> grid2.append(['*', '1', '2'])
        >>> grid2.append(['3', '4', '5'])
        >>> mn1 = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> mn1.is_solved()
        True
        >>> grid3 = list()
        >>> grid2.append(['1', '2', '3'])
        >>> grid2.append(['*', '4', '5'])
        >>> mn2 = MNPuzzle(tuple(grid1), (tuple(grid3)))
        >>> mn2.is_solved()
        False
        """
        return self.from_grid == self.to_grid

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> grid1 = list()
        >>> grid1.append(['*', '1', '2'])
        >>> grid1.append(['3', '4', '5'])
        >>> grid2 = list()
        >>> grid2.append(['1', '2', '3'])
        >>> grid2.append(['4', '5', '*'])
        >>> mn = MNPuzzle(tuple(grid1), (tuple(grid2)))
        >>> l1 = list(mn.extensions())
        >>> l2 = list(mn.extensions())
        >>> len(l1) == len(l2)
        True
        >>> all([mn in l2 for mn in l1])
        True
        >>> all([mn in l1 for mn in l2])
        True
        """
        # introducing variables for the convenience
        ext_list = []
        directions = ['up', 'down', 'left', 'right']
        # looping over the directions to enable the appropriate swap and create
        # legal extensions
        for i in directions:
            legal_extension = self._swap(i)
            if legal_extension:
                # returning a list of tuples of list as the new extension
                ext_list.append(MNPuzzle(legal_extension, self.to_grid))
        return ext_list

    def _empty_tile(self):
        counter = 0
        # looping over from grid tuple and lists in from grid to check for empty
        # space and returning the coordinates of it
        for i in self.from_grid:
            for j in i:
                if j == '*':
                    return counter, i.index(j)
            counter += 1
        return None

    def _swap(self, direction):
        # introducing variables for convenience
        empty_coordinate = self._empty_tile()
        x = empty_coordinate[0]
        y = empty_coordinate[1]
        # looping over from grid to create a list of tuples with coordinates
        coordinates = [list(i) for i in list(self.from_grid)]
        # checking whether empty coordinate is on the edge of the board and
        # swapping coordinate values with appropriate neighbour tile values
        if direction == 'up' and x != 0:
            coordinates[x][y], coordinates[x - 1][y] = coordinates[x - 1][y],\
                                                       coordinates[x][y]
        elif direction == 'down' and x != self.n - 1:
            coordinates[x][y], coordinates[x + 1][y] = coordinates[x + 1][y],\
                                                       coordinates[x][y]
        elif direction == 'left' and y != 0:
            coordinates[x][y], coordinates[x][y - 1] = coordinates[x][y - 1],\
                                                       coordinates[x][y]
        elif direction == 'right' and y != self.m - 1:
            coordinates[x][y], coordinates[x][y + 1] = coordinates[x][y + 1],\
                                                       coordinates[x][y]
        else:
            return None

        return tuple([tuple(i) for i in coordinates])

if __name__ == '__main__':
    import doctest

    doctest.testmod()
    target_grid = (('1', '2', '3'), ('4', '5', '*'))
    start_grid = (('*', '2', '3'), ('1', '4', '5'))
    from puzzle_tools import depth_first_solve, \
        breadth_first_solve
    from time import time

    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print('BFS solved: \n\n{} \n\nin {} seconds'.format(
        solution, end - start))

    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print('DFS solved: \n\n{} \n\nin {} seconds'.format(
        solution, end - start))
