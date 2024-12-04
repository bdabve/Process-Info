#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import psutil
from datetime import datetime


class ProcessManager:
    """Manage system processes and interact with process-related data."""

    def __init__(self):
        self.params = ['pid', 'name', 'status', 'username', 'exe']

    def get_all_processes(self):
        """
        Retrieve a list of all processes with attributes defined in self.params.

        :return: List of tuples representing processes with (pid, name, status, username, exe).
        """
        # ps = [p.info for p in psutil.process_iter(attrs=self.params)]
        return [
            (p.info['pid'], p.info['name'], p.info['status'], p.info['username'], p.info['exe'])
            for p in psutil.process_iter(attrs=['pid', 'name', 'status', 'username', 'exe'])
        ]

    def get_process_by_name(self, name: str):
        """
        Retrieve processes matching a specific name.

        :param name: The name (or part of it) of the process to search for.
        :return: List of tuples representing processes or an empty list if none found.
        """
        ps = [p.info for p in psutil.process_iter(attrs=self.params) if name in p.info['name']]
        if len(ps) == 0:
            return False
        else:
            rows = [(p['pid'], p['name'], p['status'], p['username'], p['exe']) for p in ps]
        return rows

    def get_process_by_user(self, username: str):
        """
        Retrieve processes owned by a specific user.

        :param username: The username of the process owner.
        :return: List of tuples representing processes or an empty list if none found.
        """
        return [
            (p['pid'], p['name'], p['status'], p['username'], p['exe'])
            for p in psutil.process_iter(attrs=self.params)
            if username.lower() == p['username'].lower()
        ]

    def get_process_details(self, pid: int):
        """
        Retrieve detailed information for a process by its PID.

        :param pid: The process ID (PID) to retrieve details for.
        :return: Dictionary of process details or "Permission Error" if access is denied.
        """
        try:
            process = psutil.Process(pid)
            # if process.net_connections()
            return {
                'PID': pid,
                'Created': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M'),
                'Parent': process.ppid(),
                'Name': process.name(),
                'Executable': process.exe(),
                'CMDLine': '\n'.join(process.cmdline()),
                'Status': process.status(),
                'CWD': process.cwd(),
                'Owner': process.username(),
                'CPU Percent': process.cpu_percent(),
                'Connections': 'Yes' if process.net_connections() else 'No',
            }
        except psutil.AccessDenied:
            return "Permission Error"


def get_column_value(table: QtWidgets.QTableWidget, column: int) -> str:
    """
    Get the value from a specific column of the selected row in a QTableWidget.

    :param table: The QTableWidget instance.
    :param column: The column index to retrieve the value from.
    :return: The value as a string.
    """
    row = table.currentRow()
    return table.item(row, column).text()


def display_table_records(table: QtWidgets.QTableWidget, rows: list, headers: list):
    """
    Populate a QTableWidget with rows and headers.

    :param table: The QTableWidget instance.
    :param rows: A list of rows where each row is a list or tuple of values.
    :param headers: A list of column headers.
    """
    table.clear()
    table.setColumnCount(len(headers))
    table.setRowCount(len(rows))
    table.setHorizontalHeaderLabels(headers)

    for row_idx, row_data in enumerate(rows):
        for col_idx, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(value))
            table.setItem(row_idx, col_idx, item)


def populate_comboBox(combobox: QtWidgets.QComboBox, items: list):
    """
    Populate a QComboBox with a list of items.

    :param combobox: The QComboBox instance.
    :param items: A list of strings to populate the combobox.
    """
    combobox.blockSignals(True)
    combobox.clear()
    combobox.addItems(items)
    combobox.blockSignals(False)


if __name__ == '__main__':
    pm = ProcessManager()
    # print(pm.get_all_processes())
    # print(pm.get_process_details(1))
    # print(pm.get_process_by_name('python'))
    # print(pm.get_process_details(pid=28472,))
