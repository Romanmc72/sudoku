#!/usr/bin/env python3
"""
This class defines the two dimensions 3x3 cell box inside of a larger sudoku matrix.
"""
from sudoku_objects.base import _CellGroup
from sudoku_objects.row import Row
from sudoku_objects.column import Column
from sudoku_objects.cell import Cell


class Box(_CellGroup):
    """
    Description
    -----------
    This object represents a box of 3x3 cells
    contained within asudoku matrix of 9x9 cells or 3x3 boxes.
    This is a 2 dimensional object with height and width of 3.
    """
    def __init__(self, box_number):
        _CellGroup.__init__(self, number=box_number, ndim=2)
        self.box_number = box_number
        self.rows = [Row(0), Row(1), Row(2)]
        self.columns = [Column(0), Column(1), Column(2)]
        self.slices = []

    def __str__(self):
        my_str = []
        line_break = '+---+---+---+'
        nl = '\n|'
        my_str.append(line_break + nl)
        for cell_number in range(len(self.cells)):
            my_str.append(f" {self.cells[cell_number].value if self.cells[cell_number].value is not None else ' '} |")
            if cell_number in [2, 5]:
                my_str.append('\n' + line_break + nl)
        my_str.append('\n' + line_break)
        return ''.join(my_str)

    def __poss__(self):
        """
        This method iterates over the cells in a box and prints those
        cells out as a bigger matrix of those 9 cells containing
        either the possibilities left within the cell or if it is
        solved printing the solution in the center.

        Possibilities are positioned like so:
        +-------+
        | 1 2 3 |
        | 4 5 6 |
        | 7 8 9 |
        +-------+
        in a matrix of 9 similar cells.
        """

        my_str = []
        line_break = "+-------+-------+-------+"
        nl = "\n|"
        my_str.append(line_break + nl)

        # Running through the 3 rows in a box
        for iteration in range(3):

            # Go through each cell in the current row of the box
            for cell in self.rows[iteration].cells:

                # If this cell is solved, don't bother with
                # the possibilities, fill the actual solved
                # value in, inside of the middle
                if cell.is_solved:

                    # iteration #1 is the center when iterating from [0, 3)
                    # which is where we want to print the solved value
                    # if it is a solved cell
                    if iteration != 1:

                        # So if it's not the center of a solved cell, print the blank line
                        my_str.append('       |')

                    # This is the center of the cell
                    else:

                        # Otherwise it is the center and fill it in with the value
                        my_str.append(f'   {cell.value}   |')

                # This cell is not solved
                else:

                    # Only give me:
                    # 1, 2, or 3 on the 1st row for this cell
                    # 4, 5, or 6 for the 2nd row foir this cell
                    # 7, 8, or 9 for the 3rd row of the cell
                    #
                    # sets the ranges at [1-4), [4-7), and [7-10)
                    for possibility in range((iteration * 3) + 1, ((iteration + 1) * 3) + 1):

                        # If this value is a possibility in the cell,
                        # add it to the string for this representation of the row
                        # otherwise leave as blank
                        my_str.append(f' {possibility if possibility in cell.possibilities else " "}')
                    my_str.append(' |')
            if iteration != 2:

                # If it's not the end, start the next row
                my_str.append(nl)
            else:

                # If it is the end, just add a newline
                my_str.append('\n')
        return ''.join(my_str)

    def rm_possibility(self, possibility: int) -> None:
        """
        Description
        -----------
        This function removes a possibility from the box.
        Once a number within the box is solved, the possibility
        is removed so that no other cells may contain its value.

        Params
        ------
        :possibility: int
        The possibility to be removed from the box

        Return
        ------
        None
        """
        self.possibilities.discard(possibility)
        [row.rm_possibility(possibility) for row in self.rows]
        [column.rm_possibility(possibility) for column in self.columns]

    def add_cell(self, cell: Cell) -> None:
        """
        Description
        -----------
        This function appends cells to the box so
        that it contains a set 9 cells each arranged
        in miniature rows and columns.

        It assumes that cells are added
        in order from left to right, top to bottom.

        Params
        ------
        :cell: Cell
        A cell object that contains either the number
        or the set of possibilities for that cell to contain.

        Return
        ------
        None
        """
        self.cells.append(cell)
        cell_num = len(self.cells) - 1
        col_num = cell_num % 3
        row_num = cell_num // 3
        self.columns[col_num].add_cell(cell)
        self.rows[row_num].add_cell(cell)

    def get_row(self, row_number: int) -> set:
        """
        Description
        -----------
        This function returns the values
        present within a row of this box.

        Params
        ------
        :row_number: int
        The row whose values you are interested in.

        Return
        ------
        set
        The values present in the box row
        """
        return {cell.value for cell in self.rows[row_number].cells if cell.value}

    def get_column(self, column_number: int) -> set:
        """
        Description
        -----------
        This function returns the values
        present within a column of this box.

        Params
        ------
        :column_number: int
        The column whose values you are interested in.

        Return
        ------
        set
        The values present in the box column
        """
        return {cell.value for cell in self.columns[column_number].cells if cell.value}

    def get_row_possibilities(self, row_number: int) -> set:
        """
        Description
        -----------
        This function returns the possibilities
        remaining in this box's row.

        Params
        ------
        :row_number: int
        The row whose possibilities you are interested in.

        Return
        ------
        set
        The set of possibilities
        """
        possibilities = set()
        [possibilities.union(cell.possibilities) for cell in self.rows[row_number].cells if cell.possibilities]
        return possibilities

    def get_column_possibilities(self, column_number: int) -> set:
        """
        Description
        -----------
        This function returns the possibilities
        remaining in this box's column.

        Params
        ------
        :column_number: int
        The column whose possibilities you are interested in.

        Return
        ------
        set
        The set of possibilities
        """
        possibilities = set()
        [possibilities.union(cell.possibilities) for cell in self.columns[column_number].cells if cell.possibilities]
        return possibilities
