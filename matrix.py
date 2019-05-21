import numpy as np


EMPTY_GROUP = [None, None, None,
               None, None, None,
               None, None, None]
EMPTY_MATRIX = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]]
EASY_SAMPLE_MATRIX = [
    [7   , None, None, None, None, None, None, None, 3   ],
    [None, 6   , 4   , None, None, None, 9   , 8   , None],
    [None, 9   , None, 7   , None, 3   , None, 1   , None],
    [None, None, 9   , 3   , None, 4   , 6   , None, None],
    [None, None, None, None, 9   , None, None, None, None],
    [None, None, 7   , 6   , None, 2   , 1   , None, None],
    [None, 8   , None, 4   , None, 7   , None, 3   , None],
    [None, 1   , 3   , None, None, None, 7   , 6   , None],
    [6   , None, None, None, None, None, None, None, 4   ]]
MEDIUM_SAMPLE_MATRIX = [
    [None, 8   , None, 6   , None, 2   , None, 7   , None],
    [None, None, 2   , None, 1   , None, 3   , None, None],
    [None, None, None, 3   , None, 8   , None, None, None],
    [7   , None, 3   , None, 6   , None, 1   , None, 9   ],
    [None, None, None, None, None, None, None, None, None],
    [6   , None, 1   , None, 5   , None, 8   , None, 7   ],
    [None, None, None, 4   , None, 5   , None, None, None],
    [None, None, 6   , None, 3   , None, 7   , None, None],
    [None, 3   , None, 2   , None, 6   , None, 9   , None]]
HARD_SAMPLE_MATRIX = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, 4   , None, None, 6   , None, None, 8   ],
    [None, None, None, None, 5   , 4   , None, 2   , 9   ],
    [4   , None, 5   , None, None, 9   , None, 6   , None],
    [None, None, 3   , None, None, None, 8   , None, None],
    [None, 2   , None, 8   , None, None, 9   , None, 3   ],
    [8   , 9   , None, 7   , 3   , None, None, None, None],
    [6   , None, None, 4   , None, None, 2   , None, None],
    [None, None, None, None, None, None, None, None, None]]
COMPLETE_SET = set([1, 2, 3, 4, 5, 6, 7, 8, 9])


class NumberSpace:
    def __init__(self):
        self.possibilities = COMPLETE_SET

    def add_possibility(self, possibility):
        self.possibilities.add(possibility)
    
    def rm_possibility(self, possibility):
        self.possibilities.discard(possibility)


class CellGroup(NumberSpace):
    def __init__(self, size=9):
        NumberSpace.__init__(self)
        self.size = size
        self.cells = []
    
    def add_cell(self, cell):
        self.cells.append(cell)
        if cell.value is not None:
            self.rm_possibility(cell.value)

    def refresh_possibilities(self):
        for cell in self.cells:
            self.rm_possibility(cell.value)

    def get_values(self):
        return set([cell.value for cell in self.cells if cell.value is not None])


class Cell(NumberSpace):
    def __init__(self,
        value,
        row,
        column,
        box):
        NumberSpace.__init__(self)
        self.value = value
        self.row = row
        self.column = column
        self.box = box
        self.is_solved = True if value is not None else False
    
    def __str__(self):
        return 
    
    def set_value(self, value):
        self.value = value
        self.possibilities = set([])
        self.is_solved = True

    
class Row(CellGroup):
    def __init__(self, row_number):
        CellGroup.__init__(self)
        self.row_number = row_number


class Column(CellGroup):
    def __init__(self, column_number):
        CellGroup.__init__(self)
        self.column_number = column_number


class Box(CellGroup):
    def __init__(self, box_number):
        CellGroup.__init__(self)
        self.box_number = box_number
        self.rows = [Row(0), Row(1), Row(2)]
        self.columns = [Column(0), Column(1), Column(2)]


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
        self.values = values
        self.cells = []
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.columns = [Column(0), Column(1), Column(2), Column(3), Column(4), Column(5), Column(6), Column(7), Column(8)]
        self.rows = [Row(0), Row(1), Row(2), Row(3), Row(4), Row(5), Row(6), Row(7), Row(8)]
        self.boxes = [Box(0), Box(1), Box(2), Box(3), Box(4), Box(5), Box(6), Box(7), Box(8)]
        self._1 = 0
        self._2 = 0
        self._3 = 0
        self._4 = 0
        self._5 = 0
        self._6 = 0
        self._7 = 0
        self._8 = 0
        self._9 = 0
        for row_num, row in enumerate(self.values):
            for column_num, value in enumerate(row):
                box_num = ((row_num // 3) * 2 + (column_num // 3))
                this_cell = Cell(value=value,
                                 row=self.rows[row_num], 
                                 column=self.columns[column_num], 
                                 box=self.boxes[box_num])
                self.cells.append(this_cell)
                self.rows[row_num].add_cell(this_cell)
                self.columns[column_num].add_cell(this_cell)
                self.boxes[box_num].add_cell(this_cell)
                if this_cell.value == 1:
                    self._1 += 1
                elif this_cell.value == 2:
                    self._2 += 1
                elif this_cell.value == 3:
                    self._3 += 1
                elif this_cell.value == 4:
                    self._4 += 1
                elif this_cell.value == 5:
                    self._5 += 1
                elif this_cell.value == 6:
                    self._6 += 1
                elif this_cell.value == 7:
                    self._7 += 1
                elif this_cell.value == 8:
                    self._8 += 1
                elif this_cell.value == 9:
                    self._9 += 1
        self.solved = False
        self.stuck = False
    
    def get_row(self, row_number):
        return [cell.value for cell in self.cells if cell.row == row_number]

    def get_column(self, column_number):
        return [cell.value for cell in self.cells if cell.column == column_number]
    
    def get_box(self, box_number):
        return [cell.value for cell in self.cells if cell.box == box_number]

    def check_number(self, number_to_check):
        instances = len([cell.value for cell in self.cells if cell.value == number_to_check])
        if instances == 9:
            self.numbers.pop(self.numbers.index(number_to_check))
            return 9
        else:
            return instances
    
    def get_missing(self, list_of_numbers):
        return [number for number in self.numbers if number not in list_of_numbers]

    def __str__(self):
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
            
    def is_solved(self):
        if not self.numbers:
            self.solved = True
            return True
        else:
            return False

    # def 

    def update_possibilities(self, cell):
        # TODO update all possibilities
        return None

    def fill_in_answers(self):
        # TODO fill in answers after possibilities have been updated
        return None

    def solve(self):
        while not self.solved and not self.stuck:
            break # TODO actually solve it
