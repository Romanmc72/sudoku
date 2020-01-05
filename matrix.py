#! /usr/bin/env python3
# TODO count instances of each possibility within a CellGroup and where
#       there exist only one instance of said possibility within that group, then: 
#           instance.set_value(possibility)
# 
# TODO use box slices to further remove possibilities from other CellGroups
# TODO implement clearer controls around rows/columns/boxes and periphery elements
#       essentially not relying on the order, but on the logic behind how sets 
#       are organized within sudoku
# TODO use the X-wing/Triple/Double/Quad techniques to ID and reduce possibilities
#
# if exists:
# ++===+===+===++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   ||
# ++===+===+===++
# || 1 | 2 | 3 ||
# ++---+---+---++
# || 4 | 5 |   || Where 6 and 9 must exist ...
# ++---+---+---++
# || 7 | 8 |   || in one of these 2 spaces...
# ++===+===+===++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   ||
# ++===+===+===++
#
# then 6 & 9 necessarily CANNOT exist in the third column of box 1 above
# or box 3 below
#
# There also exists scenarios with doubles/triples/x-wing patterns that eliminate more possibilities
#
# X-wing:
# ++===+===+===++
# ||   |   |   ||
# ++---+---+---++
# ||2,6|   |2,6|| <- 2 & 6 are the possibilities here
# ++---+---+---++
# ||   |   |   ||
# ++===+===+===++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   || 
# ++---+---+---++
# ||   |   |   || 
# ++===+===+===++
# ||2,6|   |2,6|| <- and here
# ++---+---+---++
# ||   |   |   ||
# ++---+---+---++
# ||   |   |   ||
# ++===+===+===++
#
# Therefore the values 2 and 6 cannot exist in any other cells in 
# those columns (1 & 3), those rows (2 & 7), or those boxes (1 & 3)
# 
# import numpy as np
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
            return f"""\
+-------+
|       |
|   {self.value}   |
|       |
+-------+"""
        else:
            return f"""\
+-------+
| {1 if 1 in self.possibilities else ' '} {2 if 2 in self.possibilities else ' '} {3 if 3 in self.possibilities else ' '} |
| {4 if 4 in self.possibilities else ' '} {5 if 5 in self.possibilities else ' '} {6 if 6 in self.possibilities else ' '} |
| {7 if 7 in self.possibilities else ' '} {8 if 8 in self.possibilities else ' '} {9 if 9 in self.possibilities else ' '} |
+-------+"""

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


class CellGroup(_NumberSpace):
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
    
    def add_cell(self, cell: Cell) -> None:
        """
        Description
        -----------
        This method adds a cell to a particular group,
        and if that cell is solved it removes the
        value of that cell from the remaining possibilities.

        Params
        ------
        :cell: Cell
        The Cell object to be added tot this group.

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
        return str(dict([(index, cell.value) for index, cell in enumerate(self.cells)]))
    
    def __dict__(self):
        return dict([(index, cell.value) for index, cell in enumerate(self.cells)])
    
    def __poss__(self):
        pass



class Row(CellGroup):
    """
    Description
    -----------
    This object represents a row of 9 cells
    contained in a matrix of 9 rows. This is
    a 1 dimensional object with a width of 9.
    """
    def __init__(self, row_number):
        CellGroup.__init__(self, number=row_number)
        self.row_number = row_number

    def __str__(self):
        my_str = []
        line_break = ''.join(["+---" for i in range(len(self.cells))] + ["+"] )
        my_str.append(line_break + '\n|')
        for cell in self.cells:
            my_str.append(f""" {cell.value if cell.value is not None else ' '} |""")
        my_str.append('\n' + line_break)
        return ''.join(my_str)
    
    def __poss__(self):
        my_str = []
        line_break = ''.join(["+-------" for i in range(len(self.cells))] + ["+"] )
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



class Column(CellGroup):
    """
    Description
    -----------
    This object represents a column of 9 cells
    contained in a matrix of 9 columns. This is
    a 1 dimensional object with a height of 9.
    """
    def __init__(self, column_number):
        CellGroup.__init__(self, number=column_number)
        self.column_number = column_number
 
    def __str__(self):
        my_str = []
        line_break = "+---+\n"
        my_str.append(line_break)
        for cell in self.cells:
            my_str.append(f"| {cell.value if cell.value is not None else ' '} |\n{line_break}")
        return ''.join(my_str)


class Box(CellGroup):
    """
    Description
    -----------
    This object represents a box of 3x3 cells
    contained within asudoku matrix of 9x9 cells or 3x3 boxes.
    This is a 2 dimensional object with height and width of 3.
    """
    def __init__(self, box_number):
        CellGroup.__init__(self, number=box_number, ndim=2)
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


class Matrix:
    """
    pass in a list of 9 lists that are each 9 long
    and contains `None` for unknown values, but
    integers for known values

    here is an empty one:
    [[None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None, None]]    
    """
    def __init__(self, values):
        """
        Description
        -----------
        Initializes the Matrix object. A list of 9 lists of 9 values representing a sudoku
        Matrix. The only required argument is `values` wich is that list of lists described above.
        """
        self.values = values
        self.cells = []
        self.numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.columns = [Column(0), Column(1), Column(2), Column(3), Column(4), Column(5), Column(6), Column(7), Column(8)]
        self.rows = [Row(0), Row(1), Row(2), Row(3), Row(4), Row(5), Row(6), Row(7), Row(8)]
        self.boxes = [Box(0), Box(1), Box(2), Box(3), Box(4), Box(5), Box(6), Box(7), Box(8)]
        for row_num, row in enumerate(self.values):
            for column_num, value in enumerate(row):
                box_num = ((row_num // 3) * 3 + (column_num // 3))
                this_cell = Cell(value=value,
                                 row=self.rows[row_num], 
                                 column=self.columns[column_num], 
                                 box=self.boxes[box_num])
                self.cells.append(this_cell)
                self.rows[row_num].add_cell(this_cell)
                self.columns[column_num].add_cell(this_cell)
                self.boxes[box_num].add_cell(this_cell)
        self.finds = 0
        self.solved = False
        self.stuck = False

    def __str__(self) -> str:
        """
        This method will print out the sudoku puzzle as 
        interpreted by the matrix class object. The printed 
        puzzle will go to the terminal and will be boxed like so:

        ++===+===+===++===+===+ ...
        || 1 | 2 | 3 || 4 |   :   
        ++---+---+---+---+ ...
        || 4 | 5 | 6 ||   :
        ++---+---+---++ ...
        || 7 | 8 |   :
        ++===+===+ ...
        || 2 |   :
        ++---+ ...
        """
        my_str = []
        row_break = "++---+---+---++---+---+---++---+---+---++"
        box_break = "++===+===+===++===+===+===++===+===+===++"
        my_str.append(box_break + '\n')
        for row in self.rows:
            my_str.append('||')
            for cell_number in range(len(row.cells)):
                my_str.append(f""" {row.cells[cell_number].value if row.cells[cell_number].value is not None else ' '} |""")
                if cell_number in [2, 5, 8]:
                    my_str.append('|')
            my_str.append('\n')
            if row.row_number in [2, 5, 8]:
                my_str.append(box_break + '\n')
            else:
                my_str.append(row_break + '\n')
        return ''.join(my_str)

    def __poss__(self) -> str:
        """Returns a :str: representation of all of the possibilities remaining or the actual values filled in"""
        all__poss__ = []
        for each_row in self.rows:

            # Uses the __poss__() attribute for the row, and strips
            # off the last row of characters so that they can be
            # seamlessly stacked. The last row does get the separator
            # appended back to it in the `return`.
            all__poss__.append(each_row.__poss__()[0:-73])

        return ''.join(all__poss__ + ['+-------' for i in range(9)] + ['+'] + ['\n', '\n'])

    def get_row(self, row_number: int) -> set:
        """Returns the set of values contained in the specified row number"""
        return {cell.value for cell in self.rows[row_number].cells if cell.value}

    def get_column(self, column_number: int) -> set:
        """Returns the set of values contained in the specified column number"""
        return {cell.value for cell in self.columns[column_number].cells if cell.value}

    def get_box(self, box_number: int) -> set:
        """Returns the set of values contained in the specified box number"""
        return {cell.value for cell in self.boxes[box_number].cells if cell.value}

    def check_number(self, number_to_check: int) -> tuple:
        """
        Description
        -----------
        This function checks to see how many of a particular number
        remain to be solved for in the matrix. As soon as there are
        9 instances of a number the number is considered solved and
        will no longer be check for when solving the remaining cells.
        
        Params
        ------
        :number_to_check: int
        The number (from 1-9) that this function will look through the
        matrix to see how many instances of the provided number exist.

        Return
        ------
        tuple
        (number_to_check, instances)
        this returns the number you are looking for and how many
        times it appears in the matrix.
        """
        instances = len([cell.value for cell in self.cells if cell.value == number_to_check])
        if instances == 9:
            self.numbers.discard(number_to_check)
            [cell.rm_possibility(number_to_check) for cell in self.cells]
            [row.rm_possibility(number_to_check) for row in self.rows]
            [column.rm_possibility(number_to_check) for column in self.columns]
            [box.rm_possibility(number_to_check) for box in self.boxes]
            return (number_to_check, 9)
        else:
            return (number_to_check, instances)
    
    def update_remaining_numbers(self):
        copy_of_numbers = self.numbers.copy()
        for number in copy_of_numbers:
            self.check_number(number)

    def is_solved(self):
        if not self.numbers:
            self.solved = True
            return True
        else:
            self.solved = False
            return False

    def get_box_slice(self, box_number: int, group_number: int, row_col='row') -> set:
        """
        Description
        -----------

        Params
        ------
        :box_number: int
        The box number within the matrix

        :group_number: int
        The row or column number within the box that we are getting slices from.

        :row_col: str
        Either 'row' or 'col' if we are looking in the rows
        or columns of the box indicated.

        Return
        ------
        set
        The set of values that this box will slice
        """
        possibilities_in_the_rest_of_the_group = set()
        if row_col == 'row':
            possibilities_in_this_group = self.boxes[box_number].get_row_possibilities(group_number)
            for row_num in range(3):
                if row_num != group_number:
                    possibilities_in_the_rest_of_the_group.union(self.boxes[box_number].get_row_possibilities(row_num))
        elif row_col == 'col':
            possibilities_in_this_group = self.boxes[box_number].get_column_possibilities(group_number)
            for col_num in range(3):
                if col_num != group_number:
                    possibilities_in_the_rest_of_the_group.union(self.boxes[box_number].get_column_possibilities(col_num))
        else:
            raise ValueError(f"You passed in: `{row_col}``, but we were expecting either `row` or `col`.")
        return possibilities_in_this_group.difference(possibilities_in_the_rest_of_the_group)

    
    def slice_bad_possibilities(self, values_to_slice: set, box_number: int, group_number: int, row_col='row') -> None:
        """
        Description
        -----------
        This function removes bad possibilities from adjacent boxes.

        Params
        ------
        :values_to_slice: set
        The values to be removed from adjacent boxes.

        :box_number: int
        The box number within the matrix

        :group_number: int
        The row or column number within the box that we are getting slices from.

        :row_col: str
        Either 'row' or 'col' if we are looking in the rows
        or columns of the box indicated.

        Return
        ------
        The number of possibilities successfully removed from
        cells who previously contained bad slices.
        """
        values_removed = 0
        for each_value in values_to_slice:
            if row_col =='row':
                group_to_slice = self.boxes[box_number].rows[group_number].cells[0].row 
            elif row_col == 'col':
                group_to_slice = self.boxes[box_number].columns[group_number].cells[0].column 
            else:
                raise ValueError(f"You passed in: `{row_col}``, but we were expecting either `row` or `col`.")
            for cell in group_to_slice.cells:
                if cell.box.box_number != box_number:
                    values_removed += 1 if cell.rm_possibility(each_value) > 0 else 0
        return values_removed
    
    def update_possibilities(self) -> None:
        """
        Description
        -----------
        This method updates the possibilities for all of the cells in the matrix.
        First it scans the individual cells and the neighboring possibilities.
        Then it looks to see if there are any box slices that would further
        eliminate the possibilities for a given set of cell.

        Params
        ------
        None

        Return
        ------
        None
        """ 
        for cell in self.cells:
            cell.refresh_possibilities()
        while self.finds != 0:
            self.finds = 0
            for box_num in range(9):
                for row_num in range(3):
                    other_args = {"box_number": box_num, "group_number": row_num, "row_col": 'row'}
                    self.finds += self.slice_bad_possibilities(values_to_slice=self.get_box_slice(**other_args), **other_args)
                for col_num in range(3):
                    other_args = {"box_number": box_num, "group_number": col_num, "row_col": 'col'}
                    self.finds += self.slice_bad_possibilities(values_to_slice=self.get_box_slice(**other_args), **other_args)

    def fill_in_answers(self):
        self.finds = 0
        for row in self.rows:
            self.finds += row.scan_instances()
        for column in self.columns:
            self.finds += column.scan_instances()
        for box in self.boxes:
            self.finds += box.scan_instances()
        if self.finds == 0:
            self.stuck = True

    def quality_check(self) -> None:
        """
        Description
        -----------
        This step checks to see that there are duplicated
        results in any of the rows, columns, or boxes. If
        there are it'll halt execution and raise an error.

        Params
        ------
        None

        Return
        ------
        None
        """
        for row in self.rows:
            solved_values = set()
            for index, cell in enumerate(row.cells):
                if cell.value:
                    if cell.value in solved_values:
                        print(f"We have a duplicate in row:{row.row_number}; cell:{index}")
                        print(row)
                        self.stuck = True
                    else:
                        solved_values.add(cell.value)
        for column in self.columns:
            solved_values = set()
            for index, cell in enumerate(column.cells):
                if cell.value:
                    if cell.value in solved_values:
                        print(f"We have a duplicate in column:{column.column_number}; cell:{index}")
                        print(column)
                        self.stuck = True
                    else:
                        solved_values.add(cell.value)
        for box in self.boxes:
            solved_values = set()
            for index, cell in enumerate(box.cells):
                if cell.value:
                    if cell.value in solved_values:
                        print(f"We have a duplicate in box:{box.box_number}; cell:{index}")
                        print(box)
                        self.stuck = True
                    else:
                        solved_values.add(cell.value)

    def solve(self, verbose: bool = True):
        """
        Description
        -----------
        This is the method that actually solves the puzzle.
        It first scans the puzzle's currentt state to update
        the possibilities based on neighboring cells, then
        fills in logically each cell that must be a particular
        value, finally updating the remaining possibilities
        and repeating upntil the puzzle is either solved or stuck.

        Whether or not the verbosity is set,
        the final state of stuck or solved is printed.

        Params
        ------
        :verbose: bool = True
        Whether or not to print the iteration #
        and the state of the puzzle with each iteration.

        Return
        ------
        None
        """
        iteration = 0
        self.stuck = False
        while not self.solved and not self.stuck:
            print(f"Iteration: {iteration}")
            print(f"Pre-Processing State:\n{self.__str__()}")
            print(f"Pre-Processing Possibilities:\n{self.__poss__()}")
            self.update_possibilities()
            self.fill_in_answers()
            self.update_remaining_numbers()
            self.is_solved()
            self.quality_check()
            print(f"Post-Processing State:\n{self.__str__()}")
            print(f"Post-Processing Possibilities:\n{self.__poss__()}")
            iteration += 1
        if self.solved:
            print(f"Solved:\n{self.__str__()}")
        elif self.stuck:
            print(f"Stuck:\n{self.__str__()}")
        else:
            print(f"???:\n{self.__str__()}")
