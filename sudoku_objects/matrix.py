#! /usr/bin/env python3
"""
This class simply defines the sudoku matrix as a component of it's constituent parts.
"""
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
from sudoku_objects.base import VERBOSE

from sudoku_objects.cell import Cell
from sudoku_objects.box import Box
from sudoku_objects.row import Row
from sudoku_objects.column import Column

from sudoku_objects.exceptions import DuplicationError


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
    def __init__(self, values, verbose=VERBOSE):
        """
        Description
        -----------
        Initializes the Matrix object. A list of 9 lists of 9 values representing a sudoku
        Matrix. The only required argument is `values` wich is that list of lists described above.
        """
        self.values = values
        self.verbose = verbose
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
            if row_col == 'row':
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
                        raise DuplicationError("STOP! You have duplicates, see above!!!")
                    else:
                        solved_values.add(cell.value)
        for column in self.columns:
            solved_values = set()
            for index, cell in enumerate(column.cells):
                if cell.value:
                    if cell.value in solved_values:
                        print(f"We have a duplicate in column:{column.column_number}; cell:{index}")
                        print(column)
                        raise DuplicationError("STOP! You have duplicates, see above!!!")
                    else:
                        solved_values.add(cell.value)
        for box in self.boxes:
            solved_values = set()
            for index, cell in enumerate(box.cells):
                if cell.value:
                    if cell.value in solved_values:
                        print(f"We have a duplicate in box:{box.box_number}; cell:{index}")
                        print(box)
                        raise DuplicationError("STOP! You have duplicates, see above!!!")
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
        try:
            while not self.solved and not self.stuck:
                if self.verbose:
                    print(f"Iteration: {iteration}")
                    print(f"Pre-Processing State:\n{self.__str__()}")
                    print(f"Pre-Processing Possibilities:\n{self.__poss__()}")
                self.update_possibilities()
                self.fill_in_answers()
                self.update_remaining_numbers()
                self.is_solved()
                self.quality_check()
                if self.verbose:
                    print(f"Post-Processing State:\n{self.__str__()}")
                    print(f"Post-Processing Possibilities:\n{self.__poss__()}")
                iteration += 1
            if self.verbose:
                if self.solved:
                    print(f"Solved:\n{self.__str__()}")
                elif self.stuck:
                    print(f"Stuck:\n{self.__str__()}")
                else:
                    print(f"???:\n{self.__str__()}")
        except DuplicationError as e:
            print(e)
