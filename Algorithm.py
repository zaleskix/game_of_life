import random
import time
import numpy
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore

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

class Algorithm(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)
    iterations = 0
    grid = None

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            if self.iterations != 0:
                new_grid = self.calculate_new_grid()
                self.signal.emit(new_grid)
                self.iterations -= 1

            time.sleep(1)

    def calculate_new_grid(self):
        #TODO: opracowac czesc logiczna algorytmu
        return calculate_new_random_grid()

    def start_algorithm(self, input, error_label, info_label):
        if input.text() == "":
            info_label.hide()
            error_label.setText("Musisz podać ilość iteracji. Spróbuj jeszcze raz")
            error_label.show()
        elif not input.text().isnumeric():
            info_label.hide()
            error_label.setText(
                "Zła wartość wejściowa. Podana wartość musi być liczbą. Spróbuj jeszcze raz. ")
            error_label.show()
        else:
            error_label.hide()
            self.iterations = int(input.text())
            info_label.setText("Ustawiono {} iteracji.".format(self.iterations))
            info_label.show()
