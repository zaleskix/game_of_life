import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

from GUI import GUI

if __name__ == '__main__':
    windowExample = GUI()
    windowExample.show()
    sys.exit(app.exec())
