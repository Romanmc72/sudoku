#!/usr/bin/env python3
"""
This class defines the one dimensional eith 9-cell
matrix column or 3-cell box column contained in a
sudoku puzzle
"""
from sudoku_objects.base import _CellGroup


class Column(_CellGroup):
    """
    Description
    -----------
    This object represents a column of 9 cells
    contained in a matrix of 9 columns. This is
    a 1 dimensional object with a height of 9.
    """
    def __init__(self, column_number):
        _CellGroup.__init__(self, number=column_number)
        self.column_number = column_number

    def __str__(self) -> str:
        my_str = []
        line_break = "+---+\n"
        my_str.append(line_break)
        for cell in self.cells:
            my_str.append(f"| {cell.value if cell.value is not None else ' '} |\n{line_break}")
        return ''.join(my_str)

    def __poss__(self) -> str:
        return
