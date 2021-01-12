from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QInputDialog, QLineEdit

from Algorithm import calculate_new_random_grid, CELLS_ARRAY
from Properties import EMPTY_CELL_STYLE, BOARD_HEIGHT, BOARD_WIDTH, BUTTON_HEIGHT, TITLE_TEXT_STYLE, GAME_NAME, AUTHOR, \
    AUTHOR_TEXT_STYLE, FULL_CELL_STYLE


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        # głowny layout programu
        main_vertical_layout = QVBoxLayout(self)
        main_vertical_layout.setSpacing(0)
        main_vertical_layout.addStretch()
        main_vertical_layout.widget()

        self.add_credentials_header_to_GUI(main_vertical_layout)
        self.add_grid_to_GUI(main_vertical_layout)
        self.add_input(main_vertical_layout)
        self.add_control_buttons(main_vertical_layout)

        self.setLayout(main_vertical_layout)
        self.setWindowTitle('Review')

    def add_input(self, main_vertical_layout):
        row = QHBoxLayout()
        row.addStretch()

        name_label = QLabel(self)
        name_label.setFixedWidth(200)
        name_label.setText('Liczba iteracji:')

        input = QLineEdit(self)
        input.setFixedWidth(100)

        row.setSpacing(100)
        row.setContentsMargins(100,0,100,0)

        row.addWidget(name_label)
        row.addWidget(input)

        main_vertical_layout.addLayout(row)
        main_vertical_layout.addWidget(QLabel())

    def clear_grid(self):
        for row in CELLS_ARRAY:
            for cell in row:
                cell.setStyleSheet(EMPTY_CELL_STYLE)

    def generate_new_random_grid(self):
        grid = calculate_new_random_grid()
        self.clear_grid()

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if grid[i][j] == 1:
                    CELLS_ARRAY[i][j].setStyleSheet(FULL_CELL_STYLE)

    def add_control_buttons(self, main_vertical_layout):
        h_layout = QHBoxLayout()
        h_layout.setSpacing(50)
        load_starting_points = QPushButton("Load random starting points")
        load_starting_points.setMinimumHeight(BUTTON_HEIGHT)
        load_starting_points.setMaximumHeight(BUTTON_HEIGHT)
        load_starting_points.clicked.connect(partial(self.generate_new_random_grid))
        h_layout.addWidget(load_starting_points)

        start_button = QPushButton("Start simulation")
        start_button.setMinimumHeight(BUTTON_HEIGHT)
        start_button.setMaximumHeight(BUTTON_HEIGHT)
        h_layout.addWidget(start_button)

        main_vertical_layout.addLayout(h_layout)

    def add_grid_to_GUI(self, board):
        for x in range(BOARD_HEIGHT):
            row = QHBoxLayout()
            row.setSpacing(0)
            for y in range(BOARD_WIDTH):
                row.addWidget(CELLS_ARRAY[x][y])

            board.addLayout(row)
        board.addWidget(QLabel())

    def add_credentials_header_to_GUI(self, vertical_layout):
        title_h_layout = QHBoxLayout()
        title_h_layout.setAlignment(Qt.AlignCenter)
        title_label = QLabel(GAME_NAME)
        title_label.setStyleSheet(TITLE_TEXT_STYLE)
        title_h_layout.addWidget(title_label)

        author_h_layout = QHBoxLayout()
        author_h_layout.setAlignment(Qt.AlignCenter)
        author_label = QLabel("by " + AUTHOR)
        author_label.setStyleSheet(AUTHOR_TEXT_STYLE)
        author_h_layout.addWidget(author_label)

        vertical_layout.addLayout(title_h_layout)
        vertical_layout.addLayout(author_h_layout)
        vertical_layout.addWidget(QLabel())
