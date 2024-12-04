#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from headers.h_interface import Ui_MainWindow
import config
from utils import ProcessManager, display_table_records, populate_comboBox


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up UI font and icons
        self.font = QtGui.QFont()
        self.font.setFamily("Technology")
        config.interface_icons(self)

        # Instantiate ProcessManager
        self.process_manager = ProcessManager()

        # Display username
        username = self.get_current_user()
        self.ui.buttonUsername.setText(username)

        # Connect UI elements to callbacks
        self.ui.processTableWidget.itemDoubleClicked.connect(self.process_details)
        self.ui.lineEditSearch.returnPressed.connect(self.search_process)
        self.ui.processByUser.currentIndexChanged.connect(self.process_by_user)

        # Configure and hide dock widget
        self.ui.dockWidget.setTitleBarWidget(QtWidgets.QWidget())
        self.ui.dockWidget.close()

        # Initialize application
        self.goto_process_page()
        self.showMaximized()

    @staticmethod
    def get_current_user():
        """Retrieve the current system username."""
        import psutil
        return psutil.users()[0].name

    def pagebuttons_stats(self):
        """Update page button states based on the current page."""
        current_page = self.ui.containerStackedWidget.currentIndex()
        self.ui.buttonProcess.setChecked(current_page == 0)
        self.ui.buttonService.setChecked(current_page == 1)

    def update_count_label(self, rows):
        """Update the process count label."""
        self.ui.labelProcessCount.setText(f"Total Process ({len(rows)})")

    def goto_process_page(self):
        """Switch to the process page and display all processes."""
        users = ['All'] + list({process[3] for process in self.process_manager.get_all_processes() if process[3]})
        populate_comboBox(self.ui.processByUser, users)
        self.all_process()

    def display_process(self, rows):
        """Display processes in the table widget."""
        headers = ['PID', 'NAME', 'STATUS', 'USER', 'EXECUTABLE']
        display_table_records(self.ui.processTableWidget, rows, headers)
        self.update_count_label(rows)
        self.pagebuttons_stats()

    def all_process(self):
        """Display all processes."""
        processes = self.process_manager.get_all_processes()
        self.display_process(processes)

    def search_process(self):
        """Search and display processes by name."""
        p_name = self.ui.lineEditSearch.text()
        processes = self.process_manager.get_process_by_name(p_name)
        if processes:
            self.display_process(processes)
        else:
            self.ui.labelError.setText(f"No process with name '{p_name}'")

    def process_by_user(self):
        """Filter processes by the selected user."""
        username = self.ui.processByUser.currentText()
        processes = self.process_manager.get_process_by_user(username) if username != 'All' else self.process_manager.get_all_processes()
        if processes:
            self.display_process(processes)
        else:
            self.ui.labelError.setText(f"No processes owned by '{username}'")

    def process_details(self):
        """Show details for a selected process."""
        self.ui.labelError.clear()
        try:
            pid = int(self.get_selected_pid())
            details = self.process_manager.get_process_details(pid)

            if details == "Permission Error":
                self.ui.labelError.setText("You must have root permissions.")
                self.ui.dockWidget.close()
                return

            self.clear_details_form(self.ui.formLayout)
            for count, (key, value) in enumerate(details.items(), start=1):
                key_label = self.create_label(self.ui.scrollAreaWidgetContents, f"key_{key}")
                value_label = self.create_label(self.ui.scrollAreaWidgetContents, f"value_{count}")
                key_label.setText(key)
                value_label.setText(str(value))
                self.ui.formLayout.setWidget(count, QtWidgets.QFormLayout.LabelRole, key_label)
                self.ui.formLayout.setWidget(count, QtWidgets.QFormLayout.FieldRole, value_label)

            self.ui.dockWidget.show()
        except ValueError:
            self.ui.labelError.setText("Invalid PID selected.")

    def handle_process(self, action):
        """Handle process actions (terminate, suspend, resume)."""
        print(f"Handle Process: {action}")

    def get_selected_pid(self):
        """Retrieve the PID of the selected row in the table."""
        return self.ui.processTableWidget.item(self.ui.processTableWidget.currentRow(), 0).text()

    @staticmethod
    def create_label(parent, label_name):
        """Create a styled QLabel."""
        label = QtWidgets.QLabel(parent)
        label.setObjectName(label_name)
        label.setFont(QtGui.QFont("Monaco", 12))
        label.setWordWrap(True)
        label.setStyleSheet(
            "border: 1px solid rgb(64, 66, 72); border-top:none; border-left: none; border-right: none"
        )
        return label

    @staticmethod
    def clear_details_form(form_layout):
        """Clear all widgets from a QFormLayout."""
        while form_layout.count():
            item = form_layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())
