#!/usr/bin/env python3
"""
These are base classes, functions and
objects shared by other objects in this module.

None of them are individually all too useful, but when
combined with other objects form the basis on whic this
program solves sudoku puzzles.
"""

VERBOSE = True
COMPLETE_SET = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
NULL_SET = set([])


def list_of_zeroes(set_of_values: list) -> list:
    """
    Description
    -----------
    This funciton takes a list, and returns a
    list of zeros that matches the length of
    the list provided.

    Params
    ------
    :set_of_values: list
    Any list whose length will be used to
    generate a list of zeros.

    Return
    ------
    list
    A list of zeros.
    """
    return [0 for value in set_of_values]


class _NumberSpace:
    """
    Description
    -----------
    This represents a numberspace that can contain possibilities.
    Any object that can contain possibilities inherits attributes from this class.
    """
    def __init__(self):
        self.possibilities = COMPLETE_SET.copy()

    def add_possibility(self, possibility):
        self.possibilities.add(possibility)

    def rm_possibility(self, possibility: int) -> int:
        """
        Description
        -----------
        This method discards a possibility from a set of possibilities.
        If the value was present it will return the value removed,
        otherwise it will return 0.

        Params
        ------
        :possibility: int
        The possibility to be removed
        from the set of possibilities

        Return
        ------
        The possibility being removed
        (if one is removed) otherwise 0 if none are effected.
        """
        if possibility in self.possibilities:
            removing = possibility
        else:
            removing = 0
        self.possibilities.discard(possibility)
        return removing


class _CellGroup(_NumberSpace):
    """
    Description
    -----------
    This is the base class of attributes and
    methods used by various other classes of
    either 1 or 2 dimensions (rows, columns, boxes).

    Params
    ------
    :number: int
    This is the number of this cell group within
    the context of other similar cell groups in
    the matrix.

    :ndim: int = 1
    This is the number of dimensions for this cell group.
    """
    def __init__(self, number: int, ndim: int = 1):
        _NumberSpace.__init__(self)
        self.number = number
        self.ndim = ndim
        self.cells = []

    def add_cell(self, cell: object) -> None:
        """
        Description
        -----------
        This method adds a cell to a particular group,
        and if that cell is solved it removes the
        value of that cell from the remaining possibilities.

        Params
        ------
        :cell: Cell object
        The Cell object to be added to this group.

        Return
        ------
        None
        """
        self.cells.append(cell)
        if cell.value is not None:
            self.rm_possibility(cell.value)
        self.refresh_possibilities()

    def refresh_possibilities(self):
        self.possibilities = COMPLETE_SET.difference(self.get_values())

    def get_values(self):
        return {cell.value for cell in self.cells if cell.value}

    def scan_instances(self):
        """
        Description
        -----------
        If there are any cells who only have one possible
        value to set, or if those cells are the only cell
        eligible for that value, then those cells are
        assigned to the value they are eligible for.

        Params
        ------
        None

        Return
        ------
        int
        This function returns the number of values that are
        solved when the cells of this cell group are scanned.
        """
        self.refresh_possibilities()
        instance_counter = dict(zip(self.possibilities,
                                    list_of_zeroes(self.possibilities)))
        for possibility in self.possibilities:
            for cell in self.cells:
                if possibility in cell.possibilities:
                    instance_counter[possibility] += 1
        values_to_set = [value for value in instance_counter.keys() if instance_counter[value] == 1]
        cells_solved = len(values_to_set)
        for value in values_to_set:
            for cell in self.cells:
                if value in cell.possibilities:
                    cell.set_value(value)
        return cells_solved

    def __str__(self):
        pass

    def __dict__(self):
        return dict([(index, cell.value) for index, cell in enumerate(self.cells)])

    def __poss__(self):
        pass
