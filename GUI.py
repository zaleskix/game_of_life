from functools import partial

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QInputDialog, QLineEdit, QStyle

from Algorithm import CELLS_ARRAY, Algorithm, calculate_new_random_grid
from Properties import EMPTY_CELL_STYLE, BOARD_HEIGHT, BOARD_WIDTH, UI_ELEMENT_HEIGHT, TITLE_TEXT_STYLE, GAME_NAME, \
    AUTHOR, \
    AUTHOR_TEXT_STYLE, FULL_CELL_STYLE, BUTTON_WIDTH, BOTTOM_LABEL_TEXT_STYLE, ERROR_LABEL_TEXT_STYLE, \
    INFO_LABEL_TEXT_STYLE


class GUI(QWidget):
    main_vertical_layout = None
    error_label = None
    info_label = None
    algorithm = Algorithm()

    def __init__(self):
        super().__init__()
        self.new_thread = QThread()
        self.create_main_GUI()
        self.create_async_watcher()
        self.setLayout(self.main_vertical_layout)
        self.setWindowTitle('Review')

    def create_async_watcher(self):
        self.new_thread.started.connect(self.algorithm.run)  # Init worker run() at startup (optional)
        self.algorithm.signal.connect(self.update_existing_grid)  # Connect your signals/slots
        self.algorithm.moveToThread(self.new_thread)  # Move the Worker object to the Thread object
        self.new_thread.start()

    def create_main_GUI(self):
        # głowny layout programu
        self.main_vertical_layout = QVBoxLayout(self)
        self.error_label = self.add_error_label()
        self.info_label = self.add_info_label()

        self.main_vertical_layout.setSpacing(0)
        self.main_vertical_layout.addStretch()
        self.main_vertical_layout.widget()

        self.add_credentials_header_to_GUI()
        self.add_grid_to_GUI()

        self.main_vertical_layout.addWidget(self.error_label)
        self.main_vertical_layout.addWidget(self.info_label)
        self.create_bottom_controls()

    def create_bottom_controls(self):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignCenter)

        row2 = QHBoxLayout()
        row2.setAlignment(Qt.AlignCenter)

        name_label = QLabel(self)
        name_label.setText('Liczba iteracji:')
        name_label.setFixedHeight(UI_ELEMENT_HEIGHT)
        name_label.setStyleSheet(BOTTOM_LABEL_TEXT_STYLE)
        name_label.setFixedWidth(150)

        input = QLineEdit(self)
        input.setFixedWidth(100)
        input.setFixedHeight(40)

        start_button = QPushButton("Start simulation")
        start_button.setFixedHeight(UI_ELEMENT_HEIGHT)
        start_button.setFixedWidth(BUTTON_WIDTH)
        start_button.clicked.connect(partial(self.algorithm.start_algorithm, input, self.error_label, self.info_label))

        row.setSpacing(25)
        row2.setSpacing(25)
        row.setContentsMargins(50,0,50,0)
        row2.setContentsMargins(50,0,50,0)

        row.addWidget(name_label)
        row.addWidget(input)

        row2.addWidget(start_button)

        self.main_vertical_layout.addLayout(row)
        self.main_vertical_layout.addLayout(row2)
        self.main_vertical_layout.addWidget(QLabel())

    def clear_grid(self):
        for row in CELLS_ARRAY:
            for cell in row:
                cell.setStyleSheet(EMPTY_CELL_STYLE)

    def update_existing_grid(self, new_grid):
        self.clear_grid()
        if self.algorithm.iterations != 0:
            self.info_label.setText("Iteracje pozostałe do końca {}".format(self.algorithm.iterations))
        else:
            self.info_label.setText("Algorytm zakończył działanie. \nMożesz ustawić nową liczbe iteracji i rozpoczać od nowa")

        self.info_label.show()
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if new_grid[i][j] == 1:
                    CELLS_ARRAY[i][j].setStyleSheet(FULL_CELL_STYLE)

    def add_error_label(self):
        h_layout = QHBoxLayout()
        h_layout.setSpacing(50)

        error_label = QLabel()
        error_label.setStyleSheet(ERROR_LABEL_TEXT_STYLE)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.hide()
        error_label.setText("")
        return error_label

    def add_info_label(self):
        h_layout = QHBoxLayout()
        h_layout.setSpacing(50)

        error_label = QLabel()
        error_label.setStyleSheet(INFO_LABEL_TEXT_STYLE)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.hide()
        error_label.setText("")
        return error_label

    def add_grid_to_GUI(self):
        for x in range(BOARD_HEIGHT):
            row = QHBoxLayout()
            row.setSpacing(0)
            for y in range(BOARD_WIDTH):
                row.addWidget(CELLS_ARRAY[x][y])

            self.main_vertical_layout.addLayout(row)
        self.main_vertical_layout.addWidget(QLabel())

    def add_credentials_header_to_GUI(self):
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

        self.main_vertical_layout.addLayout(title_h_layout)
        self.main_vertical_layout.addLayout(author_h_layout)
        self.main_vertical_layout.addWidget(QLabel())