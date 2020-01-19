#!/usr/bin/env python3
"""
This classe defines what attributes a single cell holds
"""
from textwrap import dedent

from sudoku_objects.base import _NumberSpace
from sudoku_objects.base import NULL_SET


class Cell(_NumberSpace):
    """
    Description
    -----------
    This represents an individual cell that exists
    within a matrix of 81 cells. This cell not only
    exists in a mtrix, but also in a box, row, and
    column each containing another group of cells.
    """
    def __init__(self, value, row, column, box):
        _NumberSpace.__init__(self)
        self.value = value
        self.row = row
        self.column = column
        self.box = box
        self.is_solved = True if value is not None else False
        if self.is_solved:
            self.row.rm_possibility(self.value)
            self.column.rm_possibility(self.value)
            self.box.rm_possibility(self.value)
            self.possibilities = NULL_SET.copy()

    def __str__(self) -> str:
        return str(self.value)

    def __poss__(self) -> str:
        """
        Description
        -----------
        This returns either the list of possibilities
        left to solve for a particular cell, or the
        solved value centered within the cell.
        """
        if self.is_solved:
            return dedent(f"""\
                +-------+
                |       |
                |   {self.value}   |
                |       |
                +-------+""")
        else:
            return dedent(f"""\
                +-------+
                | {1 if 1 in self.possibilities else ' '} {2 if 2 in self.possibilities else ' '} {3 if 3 in self.possibilities else ' '} |
                | {4 if 4 in self.possibilities else ' '} {5 if 5 in self.possibilities else ' '} {6 if 6 in self.possibilities else ' '} |
                | {7 if 7 in self.possibilities else ' '} {8 if 8 in self.possibilities else ' '} {9 if 9 in self.possibilities else ' '} |
                +-------+""")

    def __dict__(self):
        return {
            "row": self.row.row_number,
            "column": self.column.column_number,
            "box": self.box.box_number,
            "value": self.value,
            "possibilities": self.possibilities
        }

    def set_value(self, value):
        self.value = value
        self.possibilities = NULL_SET.copy()
        self.is_solved = True
        for cell in self.row.cells:
            cell.rm_possibility(value)
        for cell in self.column.cells:
            cell.rm_possibility(value)
        for cell in self.box.cells:
            cell.rm_possibility(value)

    def refresh_possibilities(self):
        if not self.is_solved:
            self.possibilities = self.row.possibilities.intersection(
                self.column.possibilities.intersection(
                    self.box.possibilities))
            if len(self.possibilities) == 1:
                self.set_value(self.possibilities.pop())
        else:
            self.possibilities = NULL_SET.copy()
