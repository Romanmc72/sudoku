#!/usr/bin/env python3
"""
This file contains matricies of varying
levels of difficulty and creates matrix
objects from them for easy testing
"""
from sudoku_objects.matrix import Matrix

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
    [None, None, None, None, None, None, None, None, None]
]
EASY_SAMPLE_MATRIX = [
    [7, None, None, None, None, None, None, None, 3],
    [None, 6, 4, None, None, None, 9, 8, None],
    [None, 9, None, 7, None, 3, None, 1, None],
    [None, None, 9, 3, None, 4, 6, None, None],
    [None, None, None, None, 9, None, None, None, None],
    [None, None, 7, 6, None, 2, 1, None, None],
    [None, 8, None, 4, None, 7, None, 3, None],
    [None, 1, 3, None, None, None, 7, 6, None],
    [6, None, None, None, None, None, None, None, 4]
]
MEDIUM_SAMPLE_MATRIX = [
    [None, 8, None, 6, None, 2, None, 7, None],
    [None, None, 2, None, 1, None, 3, None, None],
    [None, None, None, 3, None, 8, None, None, None],
    [7, None, 3, None, 6, None, 1, None, 9],
    [None, None, None, None, None, None, None, None, None],
    [6, None, 1, None, 5, None, 8, None, 7],
    [None, None, None, 4, None, 5, None, None, None],
    [None, None, 6, None, 3, None, 7, None, None],
    [None, 3, None, 2, None, 6, None, 9, None]
]
HARD_SAMPLE_MATRIX = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, 4, None, None, 6, None, None, 8],
    [None, None, None, None, 5, 4, None, 2, 9],
    [4, None, 5, None, None, 9, None, 6, None],
    [None, None, 3, None, None, None, 8, None, None],
    [None, 2, None, 8, None, None, 9, None, 3],
    [8, 9, None, 7, 3, None, None, None, None],
    [6, None, None, 4, None, None, 2, None, None],
    [None, None, None, None, None, None, None, None, None]
]

EZ = Matrix(EASY_SAMPLE_MATRIX)
MD = Matrix(MEDIUM_SAMPLE_MATRIX)
HD = Matrix(HARD_SAMPLE_MATRIX)
