from __future__ import annotations

from typing import List

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QToolBar, QAction, QLabel, 
    QStatusBar, QDialog, QTableWidgetItem
    )
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

def create_app() -> QApplication:
    """Returns the QApplication."""
    app = QApplication(sys.argv)
    return app

class ObjectTable(QTableWidget):

    def __init__(self) -> None:
        super().__init__()
        self.object_list = []

    def add_list(self, list) -> None:
        """Assign list of SQLAlchemy mapped objects to the table widget"""
        self.object_list = list
        self.setCurrentCell(0,0)

    @classmethod
    def create_table_from_obj_list(cls, list) -> ObjectTable:
        """Class method that allows creation of a table directly from the list of objects"""
        table = cls()
        table.object_list = list
        table.setCurrentCell(0,0)
        return table

    def draw_table(self) -> None:
        """Draws the table"""
        self.clearContents()

        row = 0
        for obj in self.object_list:
            col = 0
            for attr in obj.attr:
                self.setItem(row,col,QTableWidgetItem(text=attr))
                col +=1
            row+=1
        
    def delete_row(self, row_number :int) -> None:
        """Removes an item from the list and changes the table accordingly"""
        self.object_list = self.object_list[:row_number] + self.object_list[row_number+1:]
        self.removeRow(row_number)

    def next_cell(self) -> None:
        """Selects the next cell"""
        
        if self.currentColumn() == self.columnCount():
            if self.currentRow() == self.rowCount():
                return
            else:
                self.setCurrentCell(self.currentRow()+1,0)
                # commit if autocommit
        else:
            self.setCurrentCell(self.currentRow(),self.currentColumn()+1)
        
    def next_cell(self) -> None:
        """Selects the previous cell"""
        
        if self.currentColumn() == 0:
            if self.currentRow() == 0:
                return
            else:
                self.setCurrentCell(self.currentRow()-1,self.columnCount())
                # commit if autocommit
        else:
            self.setCurrentCell(self.currentRow(),self.currentColumn()-1)

    # need a method to move the pointer on deletion


class LogDialog(QDialog):
    """CLass for the log window widget"""
    def __init__(self):
        super().__init__()

        # layout of the log window
        self.win_layout = QVBoxLayout()

        # log text label
        log_text = "Log does not exist"
        with open("de_tool\log.txt", "r", encoding="utf-8") as log:
            log_text = log.read()
            log_text = log_text if log_text else "LOG IS EMPTY"

        self.log_label = QLabel(log_text)
        self.log_label.setWordWrap(True)

        self.win_layout.addWidget(self.log_label)

        self.setLayout(self.win_layout)


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
        self.browser.load(QUrl("https://www.google.cz/maps/@50.0785044,14.4403464,14z"))

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

        # adding toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # adding commit actions to toolbar
        self.commit_all_action = QAction("Commit changes", self)
        self.commit_all_action.setStatusTip("Commit all changes.")
        self.toolbar.addAction(self.commit_all_action)

        self.auto_commit_action = QAction("Auto-commit", self)
        self.auto_commit_action.setStatusTip("Toggle to commit changes everytime a row is exited.")
        self.auto_commit_action.setCheckable(True)
        self.toolbar.addAction(self.auto_commit_action)

        # separator
        self.toolbar.addSeparator()

        # discard arction
        self.discard_action = QAction("Discard entry", self)
        self.discard_action.setStatusTip("Deletes an entry from the database.")
        self.toolbar.addAction(self.discard_action)

        self.black_list_action = QAction("Black list entry", self)
        self.black_list_action.setStatusTip("Moves an entry in a black list.")
        self.toolbar.addAction(self.black_list_action)     

        # adding a menu
        # adding show log actions
        self.menu = self.menuBar()
        self.logs_menu = self.menu.addMenu("Logs")
        self.show_log_action = QAction("Show log", self)
        self.show_log_action.setStatusTip("Shows the txt file with the commits.")
        
        # adding slots to blog actions
        self.show_log_action.triggered.connect(self.open_log)
        self.logs_menu.addAction(self.show_log_action)

        # adding purge log action
        self.purge_log_action = QAction("Purge log", self)
        self.purge_log_action.setStatusTip("Clears out the log txt file")
        self.purge_log_action.triggered.connect(self.purge_log)
        self.logs_menu.addAction(self.purge_log_action)

        # setting status bar 
        self.setStatusBar(QStatusBar(self))

    def open_log(self) -> None:
            dlg = LogDialog()
            dlg.exec()

    def purge_log(self) -> None:
            with open("de_tool\log.txt", "w+", encoding="utf-8") as log:
                log.write("")
            

    def set_title_of_the_window(self, window_title: str) -> None:
        """Sets the title of a window"""
        self.setWindowTitle(window_title)

    def get_main_layout(self) -> QVBoxLayout:
        """Returns the layout object"""
        return QVBoxLayout()


if __name__ == "__main__":
    
    app = create_app()

    window = MainWindow()
    window.showMaximized()

    app.exec()