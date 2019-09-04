# TODO use the CLI to solve one or many sudoku puzzles
# TODO add web scraping tool for online sudoku puzzles from a URL or something
# 
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    description="""\
    Description
    -----------
    Use this program to solve various sudoku puzzles. Input a local CSV/JOSN file, a URL,
    or input from stdin that this program will interpret and solve printing to the terminal on
    either a successful completion or if the program is stuck.

    CSV Input
    ---------
    A CSV must come in the form of 9 comma separated lines of values where the unknown
    ones are left blank. find an example in `/sudoku/samples.csv`

    Only one matrix is allowed per CSV

    e.g. (Null matrix)
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,
    ,,,,,,,,


    JSON Input
    ----------
    A JSON document can contain multiple matricies, and they must come as newline delimited JSON
    where the next line is the next matrix. A matrix must be of the form:
    
    (Null matrix, in JSON document, matrix must be on same line. Represented here for readability)
    {
        "0": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "1": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "2": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "3": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "4": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "5": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "6": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "7": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""},
        "8": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""}
    }

    # TODO Design this
    # URL Input
    # ---------
    # You can expect this module to parse HTML input insode of which there exists data of the form:
    # 
    # <tr><td>value = 1</td></tr>
    """,
    formatter_class=RawTextHelpFormatter)
parser.add_argument(
    '--input',
    help="""\
    This is the inupt parameter, the default value is `test` which will run the `Matrix.solve()` method on the samples.py
    matricies and print the results to the terminal. Otherwise specify a file location on your local filesystem or a URL which will point
    to one or many sudoku puzzles.
    
    Try `--input ./my_csv_file.csv` or
        `--input ./my_json_file.json` or
        `--input https://some.sudokuwebsite.com/puzzle/?difficuly=2`""",
    formatter_class=RawTextHelpFormatter)