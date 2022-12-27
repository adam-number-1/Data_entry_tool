from __future__ import annotations

from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QToolBar, QAction, QLabel, 
    QStatusBar, QDialog, QTableWidgetItem, QTabWidget, QShortcut
    )
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

from de_tool.decs import empty_check
from de_tool.db_model import Apartment, session

def create_app() -> QApplication:
    """Returns the QApplication."""
    app = QApplication(sys.argv)
    return app

class ObjectTable(QTableWidget):

    attributes = ["id", "district", "street", "shape", "link"]

    def __init__(self) -> None:
        super().__init__()
        self.INGORE_AUTO_COMMIT = False
        self.object_list = []

    def add_list(self, list) -> None:
        """Assign list of SQLAlchemy mapped objects to the table widget"""
        self.object_list = list
        

    @classmethod
    def create_table_from_obj_list(cls, list_: List[Apartment]) -> ObjectTable:
        """Class method that allows creation of a table directly from the list of objects"""
        table = cls()
        table.object_list = list_
        
        return table

    def draw_table(self) -> None:
        """Draws the table"""
        self.INGORE_AUTO_COMMIT = True
        self.clearContents()
        
        if self.object_list:
            self.setRowCount(len(self.object_list))
            self.setColumnCount(len(self.attributes))

            row = 0
            for obj in self.object_list:
                col = 0
                for attr in self.attributes:
                    
                    
                    self.setItem(row,col,QTableWidgetItem(str(obj.get(attr))))
                    
                    col +=1
                row+=1

        self.INGORE_AUTO_COMMIT = False
    
    
    def delete_row(self, row_number :int) -> None:
        """Removes an item from the list and changes the table accordingly"""
        obj_to_delete = None
        try:
            obj_to_delete = self.object_list[row_number]
        except:
            pass

        if not obj_to_delete:
            return

        session.delete(obj_to_delete)
        self.object_list = self.object_list[:row_number] + self.object_list[row_number+1:]
        self.removeRow(row_number)

    def blacklist_ad(self, obj_index: int):
        link_to_blacklist = None
        try:
            link_to_blacklist = self.object_list[obj_index].link
        except:
            pass

        if link_to_blacklist:
            session.execute(f"INSERT INTO sales_blacklist (link) VALUES ('{link_to_blacklist}') ON DUPLICATE KEY UPDATE link = link;")

    def cell_changed_at(self, row:int, column:int):
        self.object_list[row].set(self.attributes[column], self.item(row,column).text())
        session.commit()

    def update_object_list(self):

        if not self.object_list:
            return

        for n, obj in enumerate(self.object_list):
            for m, attr in enumerate(self.attributes):
                
                new_value = self.item(n,m).text()
                new_value = None if new_value == "None" else new_value

                if attr == "id":
                    obj.set(attr, int(new_value))
                else:
                    obj.set(attr, new_value)


    def get_ad_link(self) -> str:
        obj_index = self.currentRow()
        return self.object_list[obj_index].link

    def get_ad_street(self) -> str:
        obj_index = self.currentRow()
        return self.object_list[obj_index].street

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


class TabWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
  
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWebEngineView()
        self.tab2 = QWebEngineView()
  
        # Add tabs
        self.tabs.addTab(self.tab1, "Listing")
        self.tabs.addTab(self.tab2, "Map")
  
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    """Class for the main window if this app"""

    def __init__(self) -> None:
        super().__init__()

        self.auto_commit = False

        self.set_title_of_the_window("Data entry tool")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.window_layout = self.get_main_layout()

        # adding objects to the layout
        # the browser
        self.browser = TabWidget()
        self.window_layout.addWidget(self.browser)
        self.central_widget.setLayout(self.window_layout)


        # add the table widget
        self.table = ObjectTable.create_table_from_obj_list(Apartment.get_objects())
        self.table.draw_table()
        self.table.cellChanged.connect(self.isChanged)
        self.window_layout.addWidget(self.table)

        # creating the button layout
        self.button_layout = QHBoxLayout()
        
        # open add button
        self.open_ad_button = QPushButton("Open ad")
        self.open_ad_button.clicked.connect(self.open_ad_button_clicked)       

        # next button
        self.commit_button = QPushButton("Commit changes")
        self.commit_button.clicked.connect(self.commit_button_clicked)

        # next button
        self.black_list_button = QPushButton("Black list row")
        self.black_list_button.clicked.connect(self.black_list_button_clicked)

        # previous button
        self.remove_button = QPushButton("Remove row")
        self.remove_button.clicked.connect(self.remove_clicked)

        # refresh table button
        self.refresh_table_button = QPushButton("Refresh table")
        self.refresh_table_button.clicked.connect(self.refresh_button_clicked)

        # adding buttons to the horizontal button group layout
        self.button_layout.addWidget(self.open_ad_button)
        self.button_layout.addWidget(self.commit_button)
        self.button_layout.addWidget(self.black_list_button)
        self.button_layout.addWidget(self.remove_button)
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
        self.auto_commit_action = QAction("Auto-commit", self)
        self.auto_commit_action.setStatusTip("Toggle to commit changes everytime a row is exited.")
        self.auto_commit_action.setCheckable(True)
        self.auto_commit_action.changed.connect(self.toggle_auto_commit)
        self.toolbar.addAction(self.auto_commit_action)

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

        # adding a shortcut to open the browser
        self.browser_short = QShortcut(QKeySequence("Alt+O"), self)
        self.browser_short.activated.connect(self.open_ad_button_clicked)

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

    # button slot methods

    def open_ad_button_clicked(self, *args):

        ad_to_open = None
        ad_street = None
        try:
            ad_to_open = self.table.get_ad_link()
            ad_street = self.table.get_ad_street()
        except:
            pass

        self.browser.tab1.load(QUrl(ad_to_open))
        self.browser.tab2.load(QUrl(f"https://www.google.cz/maps/place/{ad_street},+Praha"))

    def commit_button_clicked(self, clicked: bool):
        # i need to update all the objects in the list first and then i can commit
        self.table.update_object_list()
        session.commit()

    def black_list_button_clicked(self, clicked: bool):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.table.blacklist_ad(selected_row)
        self.table.delete_row(selected_row)
        


    def remove_clicked(self, clicked: bool):
        selected_row = self.table.currentRow()
        print(selected_row)
        if selected_row == -1:
            return
        self.table.delete_row(selected_row)

    def refresh_button_clicked(self, clicked: bool):
        new_list = Apartment.get_objects()
        self.table.add_list(new_list)
        self.table.draw_table()

    # auto-commit-action toggled
    def toggle_auto_commit(self):
        self.auto_commit = self.auto_commit_action.isChecked()

    def isChanged(self, row, column):
        if self.table.INGORE_AUTO_COMMIT or (not self.auto_commit) or (not self.table.object_list):
            return

        print(row,column)
        self.table.cell_changed_at(row,column)
        session.commit()

if __name__ == "__main__":
    
    app = create_app()

    window = MainWindow()
    window.showMaximized()

    app.exec()