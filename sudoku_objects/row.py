#!/usr/bin/env python3
"""
This class defines the one dimensional horizontal 9-cell
row contained either within a full matrix or a smaller
3-cell row contained within a box.
"""
from sudoku_objects.base import _CellGroup


class Row(_CellGroup):
    """
    Description
    -----------
    This object represents a row of 9 cells
    contained in a matrix of 9 rows. This is
    a 1 dimensional object with a width of 9.
    """
    def __init__(self, row_number):
        _CellGroup.__init__(self, number=row_number)
        self.row_number = row_number

    def __str__(self):
        my_str = []
        line_break = ''.join(["+---" for i in range(len(self.cells))] + ["+"])
        my_str.append(line_break + '\n|')
        for cell in self.cells:
            my_str.append(f""" {cell.value if cell.value is not None else ' '} |""")
        my_str.append('\n' + line_break)
        return ''.join(my_str)

    def __poss__(self):
        my_str = []
        line_break = ''.join(["+-------" for i in range(len(self.cells))] + ["+"])
        my_str.append(line_break + '\n|')
        for iteration in range(3):
            for cell in self.cells:
                if cell.is_solved:
                    if iteration != 1:
                        my_str.append('       |')
                    else:
                        my_str.append(f'   {cell.value}   |')
                else:
                    for possibility in range((iteration * 3) + 1, ((iteration + 1) * 3) + 1):
                        my_str.append(f' {possibility if possibility in cell.possibilities else " "}')
                    my_str.append(' |')
            if iteration != 2:
                my_str.append('\n|')
            else:
                my_str.append('\n')
        my_str.append(line_break)
        return ''.join(my_str)
