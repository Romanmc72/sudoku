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
# import numpy as np

COMPLETE_SET = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
NULL_SET = set([])


def list_of_zeroes(set_of_values):
    return [0 for value in set_of_values]
      

class NumberSpace:
    def __init__(self):
        self.possibilities = COMPLETE_SET.copy()

    def add_possibility(self, possibility):
        self.possibilities.add(possibility)
    
    def rm_possibility(self, possibility):
        self.possibilities.discard(possibility)


class CellGroup(NumberSpace):
    def __init__(self):
        NumberSpace.__init__(self)
        self.cells = []
    
    def add_cell(self, cell):
        self.cells.append(cell)
        if cell.value is not None:
            self.rm_possibility(cell.value)
        self.refresh_possibilities()

    def refresh_possibilities(self):
        self.possibilities = COMPLETE_SET.difference(self.get_values())

    def get_values(self):
        return set([cell.value for cell in self.cells if cell.value is not None])

    def scan_instances(self):
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



class Cell(NumberSpace):
    def __init__(self, value, row, column, box):
        NumberSpace.__init__(self)
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
    
    def __str__(self):
        return str(self.value)

    def __dict__(self):
        return {"row": self.row.row_number,
                "column": self.column.column_number,
                "box": self.box.box_number,
                "value": self.value}
    
    def set_value(self, value):
        self.value = value
        self.possibilities = NULL_SET.copy()
        self.is_solved = True
    
    def refresh_possibilities(self):
        if not self.is_solved:
            self.possibilities = self.row.possibilities.intersection(
                self.column.possibilities.intersection(
                    self.box.possibilities))
            if len(self.possibilities) == 1:
                self.set_value(self.possibilities.pop())
        else:
            self.possibilities = NULL_SET.copy()
    
class Row(CellGroup):
    def __init__(self, row_number):
        CellGroup.__init__(self)
        self.row_number = row_number

    def __str__(self):
        my_str = []
        line_break = ''.join(["+---" for i in range(len(self.cells))] + ["+"] )
        my_str.append(line_break + '\n|')
        for cell in self.cells:
            my_str.append(f""" {cell.value if cell.value is not None else ' '} |""")
        my_str.append('\n' + line_break)
        return ''.join(my_str)


class Column(CellGroup):
    def __init__(self, column_number):
        CellGroup.__init__(self)
        self.column_number = column_number
 
    def __str__(self):
        my_str = []
        line_break = "+---+\n"
        my_str.append(line_break)
        for cell in self.cells:
            my_str.append(f"| {cell.value if cell.value is not None else ' '} |\n{line_break}")
        return ''.join(my_str)


class Box(CellGroup):
    def __init__(self, box_number):
        CellGroup.__init__(self)
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

    def rm_possibility(self, possibility):
        self.possibilities.discard(possibility)
        [row.rm_possibility(possibility) for row in self.rows]
        [column.rm_possibility(possibility) for column in self.columns]
    
    def add_cell(self, cell):
        self.cells.append(cell)
        cell_num = len(self.cells) - 1
        col_num = cell_num % 3
        row_num = cell_num // 3
        self.columns[col_num].add_cell(cell)
        self.rows[row_num].add_cell(cell)


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
            return (number_to_check, 9)
        else:
            return (number_to_check, instances)
    
    def update_remaining_numbers(self):
        for number in self.numbers:
            self.check_number(number)

    def is_solved(self):
        if not self.numbers:
            self.solved = True
            return True
        else:
            return False

    def update_possibilities(self):
        for cell in self.cells:
            cell.refresh_possibilities()

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

    def solve(self):
        self.stuck = False
        while not self.solved and not self.stuck:
            self.update_possibilities()
            self.fill_in_answers()
            self.update_remaining_numbers()
            self.is_solved()
        if self.solved:
            print(f"Solved:\n{self.__str__()}")
        elif self.stuck:
            print(f"Stuck:\n{self.__str__()}")
        else:
            print(f"???:\n{self.__str__()}")