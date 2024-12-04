#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 30-November-2024
# desc          :
# ----------------------------------------------------------------------------


import psutil
from PyQt5 import QtWidgets, QtGui
from headers.h_interface import Ui_MainWindow
import config
import utils


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configuration for FONT and ICONS
        self.font = QtGui.QFont()
        self.font.setFamily("Technology")

        # icons and callback functions
        config.interface_icons(self)

        username = psutil.users()[0].name
        self.ui.buttonUsername.setText(username)

        # CALLBACK FUNCTIONS
        self.ui.processTableWidget.itemDoubleClicked.connect(self.process_details)
        self.ui.lineEditSearch.returnPressed.connect(self.search_process)
        self.ui.processByUser.currentIndexChanged.connect(self.process_by_user)

        # dockWidget
        self.ui.dockWidget.setTitleBarWidget(QtWidgets.QWidget())   # hide the dockTitleWidget
        self.ui.dockWidget.close()

        # init
        self.goto_process_page()
        self.showMaximized()

    def pagebuttons_stats(self):
        """
        This function to change page button state from checked to unchecked
        [0] == Process Page
        """
        self.ui.buttonProcess.setChecked(self.ui.containerStackedWidget.currentIndex() == 0)
        self.ui.buttonService.setChecked(self.ui.containerStackedWidget.currentIndex() == 1)

    def update_count_label(self, rows):
        self.ui.labelProcessCount.setText(f"Total Process ( {len(rows)} )")

    def goto_process_page(self):
        """
        Go to process page
            - Populate comboBox
            - display all process
        """
        users = list(set(ps.username() for ps in psutil.process_iter()))
        users.insert(0, 'All')
        utils.populate_comboBox(self.ui.processByUser, users)
        self.all_process()

    def display_process(self, rows):
        """
        DISPLAY PROCESS IN THE TABLE WIDGET
        this function called when processButton is clicked
        """
        # display result in table and update count label
        headers = ['PID', 'NAME', 'STATUS', 'USER', 'EXECUTABLE']
        utils.display_table_records(self.ui.processTableWidget, rows, headers)
        self.update_count_label(rows)
        self.pagebuttons_stats()

    def all_process(self):
        """
        Display all process
        """
        rows = utils.get_all_process()
        self.display_process(rows)

    def search_process(self):
        """
        Search for a process by name
        """
        p_name = self.ui.lineEditSearch.text()
        rows = utils.get_process_by_name(p_name)
        if rows:
            self.display_process(rows)
        else:
            self.ui.labelError.setText(f"No process with name {p_name}")

    def process_by_user(self):
        """
        Get all process owned by a specific user
        """
        username = self.ui.processByUser.currentText()      # get username from QComboBox
        rows = utils.get_process_by_user(username)
        if rows:
            self.display_process(rows)
        else:
            self.ui.labelError.setText(f"No process owned by ({username})")

    # ====> DETAILS PAGE <====
    def create_label(self, parent, label_name):
        """
        Create Label
        :parent: the parent of the label
        :label_name: label object name
        """
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        label = QtWidgets.QLabel(parent)
        label.setObjectName(label_name)
        label.setFont(font)
        label.setWordWrap(True)
        label.setStyleSheet('border: 1px solid rgb(64, 66, 72); border-top:none; border-left: none; border-right: none')
        return label

    def clear_details_form(self, formLayout: QtWidgets.QFormLayout):
        """
        Clear the formLayout
        :framLayout: the frame name
        """
        layout = formLayout.layout()            # get the layout of the frame
        if layout:
            while layout.count() > 0:               # check if the layout has items
                item = layout.takeAt(0)         # Remove the first item
                widget = item.widget()          # get the widget associated with the item
                if widget:
                    widget.deleteLater()        # Delete the widget to free memory
                else:
                    layout.removeItem(item)     # Remove non-widget items like spacers

    def process_details(self):
        """
        PROCESS DETAILS FOR PID
        this function called when table item is double clicked
        """
        self.ui.labelError.setText('')      # clear label error

        self.pid = int(utils.get_column_value(self.ui.processTableWidget, 0))    # get pid from tableWidget
        details = utils.get_process_details(self.pid)                            # get pid details from utils

        if details == 'Permission Error':
            # Must Be Root
            self.ui.labelError.setText("You don't have permission ( You Must Be Root )")
            self.ui.dockWidget.close()
        elif isinstance(details, dict):
            # Clear the form layout
            self.clear_details_form(self.ui.formLayout)

            count = 1
            for key, value in details.items():
                key_label = self.create_label(self.ui.scrollAreaWidgetContents, f"self.ui.key_label_{key}")
                key_label.setText(f"{key}")

                value_label = self.create_label(self.ui.scrollAreaWidgetContents, f"value_label_{count}")
                value_label.setText(f"{value}")

                self.ui.formLayout.setWidget(count, QtWidgets.QFormLayout.LabelRole, key_label)
                self.ui.formLayout.setWidget(count, QtWidgets.QFormLayout.FieldRole, value_label)

                count += 1

            # Open details card
            self.ui.dockWidget.show()

    def handle_process(self, todo):
        """
        This function handle
        Terminating process; Susppend process, Resume process
        todo: terminate, suspend, resume
        """
        print(f'Handle Process: {self.pid} ({todo})')


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    dialog = Interface()
    dialog.show()
    sys.exit(app.exec_())
