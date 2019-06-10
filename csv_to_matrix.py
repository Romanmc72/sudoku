# By Roman Czerwinski
#
# This module will contain functions to read CSV files and convert them into objects that can be 
# read by the Matrix class and solved as sudoku puzzles.
# Input
#  'file_name.csv'
# Output
# list of 9 lists of 9 elements
# [[...],[...],[...],[...],...]
# TODO find illegal character set for directory enumeration
import csv
import re

import matrix as m

def csv_to_matrix(file_name: str) -> object:
    """
    :param file_name: str
    a csv file name whose contents are 9 rows of comma separated integers
    or blank spaces
    :return: object
    a matrix.Matrix object
    """
    matrix_object = []
    csv_rdr = csv.reader(open(file_name, 'r'))
    for line in csv_rdr:
       matrix_object.append([None if element == '' else int(element) for element in line])
    return m.Matrix(matrix_object)

def regexp_files_in_dir(location_expression: str) -> list:
    """
    :param location_expression: str
    input a filepath with regex expressions in any portion to
    allow the program to scan directories for files matching the specified 
    pattern(s)
    :return: list
    list of strings for the file paths matching your expression
    """
    separated_path = re.split('/', location_expression)
    file_expression = separated_path[-1]
    directory_expressions = separated_path[:-1:]
    # recursively loop through the directories and find matching files
    #
    for index, expression in enumerate(directory_expressions):
        [element for element in os.listdir('/'.join(directory_expressions[0:index + 1]) if re.match(expression, element)]

# {a: {b: c: {d: {f: {g: x}}, e: {f: {g: x}}}}}
# [dira, dirb, dirc, dird, dirf, dirg, filex]
# [dira, dirb, dirc, dire, dirf, dirg, filex]