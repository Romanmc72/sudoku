# TODO use the CLI to solve one or many sudoku puzzles
# TODO add web scraping tool for online sudoku puzzles from a URL or something
# TODO create a NLD_JSON parsing method to solve puzzles submitted as JSON
# TODO create a CSV parsing method to solve puzzles submitted as CSV
# TODO createa a STDIN parsing method to solve puzzles submitted through STDIN
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
    where the next line is the next matrix.

    e.g. Null matrix (in JSON document, entire matrix must be on same line. Represented here in prettyjson for readability)
    {"sample_puzzle":
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
    dest='input',
    formatter_class=RawTextHelpFormatter)
parser.add_argument(
    '--format',
    help="""\
        Use this input parameter to describe the input format of your input parameter.

        Must be one of <HTTP|CSV|JSON|STDIN>

        HTTP
        - Not functioning yet.

        CSV
        - for comma separated values, must be comma separated. One puzzle per CSV file.

        JSON
        - For newline delimited JSON, each puzzle is on its own line with the name as the key and the puzzle as a value.
        - Each puzzle value is a collection of the rows in the puzzle with row number top to bottom as keys [0-8] with the values of the cells
          within the row as keys [0-8] and values or either the number of the empty string "" for blanks.
        - See above for examples, can process multiple examples per newline delimited json file.

        STDIN
        - Pipe output from the terminal into the argument parser and specify this value to pick that up""",
    dest='format',
    formatter_class=RawTextHelpFormatter)

if __name__ == '__main__':
    print("# TODO Make this work")
