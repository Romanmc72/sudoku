# sudoku
This code exists to solve sudoku puzzles.

The module matrix.py contains a class for your typical sudoku matrix and subclasses for various parts of that matrix including rows, columns, boxes, and cells. A sudoku matrix can be created by calling:
```
import matrix as M

my_matrix = M.Matrix(values)
```
where `values` is a list of 9 lists each containing integers from 1-9 or `None` where there is no known value.

example:
```
values = [
    [7   , None, None, None, None, None, None, None, 3   ],
    [None, 6   , 4   , None, None, None, 9   , 8   , None],
    [None, 9   , None, 7   , None, 3   , None, 1   , None],
    [None, None, 9   , 3   , None, 4   , 6   , None, None],
    [None, None, None, None, 9   , None, None, None, None],
    [None, None, 7   , 6   , None, 2   , 1   , None, None],
    [None, 8   , None, 4   , None, 7   , None, 3   , None],
    [None, 1   , 3   , None, None, None, 7   , 6   , None],
    [6   , None, None, None, None, None, None, None, 4   ]]
```
You can print the matrix using `print(my_matrix)` and it will be output to the terminal.

simply call `my_matrix.solve()` and the algorithm will run until either the sudoku puzzle is solved or the algorithm is stuck. Either way it will print the finished (or partially finished) matrix prefixed with either `Solved:` or `Stuck:`

If the algorithm is stuck you can manually add in a value by identifying the cell via it's location relative to the first cell in the matrix, or in it's row, column or box and using the `set_value()` method. The cells, rows, columns, and boxes are stored in those attributes and can be accessed via their indecies from 0-8. 0 is the first cell in the row|column|box and 8 is the last one going left to right top to bottom. If you want to call it by the cells attribute, those range from 0-80 in the same order.

example:
```
my_matrix.rows[0].cells[1].set_value(5)
```

If you use the `set_value()` method, the other possibilities in the surrounding cells will be automatically updated as well.

If you provide the assistance and call `solve()` again, the algorithm should finish the job or get stuck again. Ideally it can solve any sudoku withou assistance, but we're not there yet. (but close!)
