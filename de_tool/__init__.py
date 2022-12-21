from typing import List

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

def create_app() -> QApplication:
    """Returns the QApplication."""
    app = QApplication(sys.argv)
    return app

class MainWindow(QMainWindow):
    """Class for the main window if this app"""

    def __init__(self) -> None:
        super().__init__()

        self.set_title_of_the_window("Data entry tool")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.window_layout = self.get_main_layout()

        # adding objects to the layout
        # the browser
        self.browser = QWebEngineView()
        self.window_layout.addWidget(self.browser)
        self.central_widget.setLayout(self.window_layout)
        self.browser.load(QUrl("https://www.sreality.cz/detail/prodej/byt/3+1/praha-zizkov-milicova/3946825548"))

        # add the table widget
        self.table = QTableWidget()
        self.window_layout.addWidget(self.table)

        # creating the button layout
        self.button_layout = QHBoxLayout()
        
        # next button
        self.next_cell_button = QPushButton("Next cell")

        # previous button
        self.previous_cell_button = QPushButton("Previous cell")

        # refresh table button
        self.refresh_table_button = QPushButton("Refresh table")

        # adding buttons to the horizontal button group layout
        self.button_layout.addWidget(self.next_cell_button)
        self.button_layout.addWidget(self.previous_cell_button)
        self.button_layout.addWidget(self.refresh_table_button)

        # adding the button group to the main layout
        self.window_layout.addLayout(self.button_layout)
        self.window_layout.setStretchFactor(self.browser,8)
        self.window_layout.setStretchFactor(self.table,2)
        self.window_layout.setStretchFactor(self.button_layout,0)

        

    def set_title_of_the_window(self, window_title: str) -> None:
        """Sets the title of a window"""
        self.setWindowTitle(window_title)

    def get_main_layout(self) -> QVBoxLayout:
        """Returns the layout object"""
        return QVBoxLayout()


if __name__ == "__main__":
    
    app = create_app()

    window = MainWindow()
    window.show()

    app.exec()