import random

import numpy
from PyQt5.QtWidgets import QLabel

from Properties import BOARD_HEIGHT, MAX_STARTING_POPULATION_COUNT_PER_ROW, SQUARE_SIZE, BOARD_WIDTH, EMPTY_CELL_STYLE


def calculate_new_random_grid():
    grid = []
    for i in range(BOARD_HEIGHT):
        random_count_of_1 = numpy.random.randint(MAX_STARTING_POPULATION_COUNT_PER_ROW)
        row = []

        for j in range(random_count_of_1):
            row.append(1)

        for j in range(BOARD_WIDTH - random_count_of_1):
            row.append(0)

        random.shuffle(row)
        grid.append(row)

    return grid


def create_cells_array():
    board = []
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            cell = QLabel()
            cell.setMinimumWidth(SQUARE_SIZE)
            cell.setMinimumHeight(SQUARE_SIZE)
            cell.setMaximumWidth(SQUARE_SIZE)
            cell.setMaximumHeight(SQUARE_SIZE)
            cell.setStyleSheet(EMPTY_CELL_STYLE)
            row.append(cell)
        board.append(row)

    return board


CELLS_ARRAY = create_cells_array()
