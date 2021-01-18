import random
import time

import numpy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

from Properties import BOARD_HEIGHT, MAX_STARTING_POPULATION_COUNT_PER_ROW, SQUARE_SIZE, BOARD_WIDTH, EMPTY_CELL_STYLE


def create_default_empty_cell():
    cell = QLabel()
    cell.setMinimumWidth(SQUARE_SIZE)
    cell.setMinimumHeight(SQUARE_SIZE)
    cell.setMaximumWidth(SQUARE_SIZE)
    cell.setMaximumHeight(SQUARE_SIZE)
    cell.setStyleSheet(EMPTY_CELL_STYLE)
    return cell


def create_cells_array():
    board = []
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            cell = create_default_empty_cell()
            row.append(cell)
        board.append(row)

    return board


def cell_should_be_alive_in_next_generation(neighbours, is_cell):
    if is_cell and neighbours <= 1:
        return False
    elif is_cell and neighbours <= 3:
        return True
    elif not is_cell and neighbours == 3:
        return True
    elif is_cell and neighbours > 3:
        return False
    else:
        return False


class Algorithm(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)
    iterations = 0
    grid = None
    cells = None

    def __init__(self):
        super().__init__()
        self.cells = create_cells_array()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            if self.iterations != 0:
                new_grid = self.calculate_new_grid()
                self.signal.emit(new_grid)
                self.iterations -= 1

            time.sleep(1)

    def start_algorithm(self, iteration_input, error_label, info_label):
        if iteration_input.text() == "":
            info_label.hide()
            error_label.setText("Musisz podać ilość iteracji. Spróbuj jeszcze raz")
            error_label.show()
        elif not iteration_input.text().isnumeric():
            info_label.hide()
            error_label.setText(
                "Zła wartość wejściowa. Podana wartość musi być liczbą. Spróbuj jeszcze raz. ")
            error_label.show()
        else:
            error_label.hide()
            self.iterations = int(iteration_input.text())
            info_label.setText("Ustawiono {} iteracji.".format(self.iterations))
            info_label.show()

    def calculate_new_grid(self):
        if self.grid:
            next_gen = []
            for row in self.cells:
                next_gen_row = []
                for cell in row:
                    cell_x = self.cells.index(row)
                    cell_y = row.index(cell)

                    neighbours_count = sum(self.get_neighbours_count_for_cell(cell_x, cell_y))
                    is_cell = self.grid[cell_x][cell_y] == 1

                    if cell_should_be_alive_in_next_generation(neighbours_count, is_cell):
                        next_gen_row.append(1)
                    else:
                        next_gen_row.append(0)

                next_gen.append(next_gen_row)

            self.grid = next_gen
            return next_gen
        else:
            return self.calculate_new_random_grid()

    def get_neighbours_count_for_cell(self, x, y):
        neighbours = []

        if x > 0:
            if y > 0:
                neighbours.append(self.grid[x - 1][y - 1])
            if y < BOARD_WIDTH - 1:
                neighbours.append(self.grid[x - 1][y + 1])
            neighbours.append(self.grid[x - 1][y])

        if y > 0:
            if x < BOARD_HEIGHT - 1:
                neighbours.append(self.grid[x + 1][y - 1])
            neighbours.append(self.grid[x][y - 1])

        if x < BOARD_HEIGHT - 1:
            neighbours.append(self.grid[x + 1][y])

        if y < BOARD_WIDTH - 1:
            neighbours.append(self.grid[x][y + 1])

        if x < BOARD_HEIGHT - 1 and y < BOARD_WIDTH - 1:
            neighbours.append(self.grid[x + 1][y + 1])

        return neighbours

    def calculate_new_random_grid(self):
        new_grid = []
        for i in range(BOARD_HEIGHT):
            random_count_of_1 = numpy.random.randint(MAX_STARTING_POPULATION_COUNT_PER_ROW)
            row = []

            for j in range(random_count_of_1):
                row.append(1)

            for j in range(BOARD_WIDTH - random_count_of_1):
                row.append(0)

            random.shuffle(row)
            new_grid.append(row)

        self.grid = new_grid
        return new_grid
