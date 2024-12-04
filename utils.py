#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import psutil


def get_column_value(table: QtWidgets.QTableWidget, column: int) -> str:
    """
    Get column text form a selected row table
    :table: table name from wich getting values
    :column: column number
    :return: string value in the given column and table
    """
    row = table.currentRow()                # current selected row
    value = table.item(row, column).text()
    return value


def display_table_records(table, rows, headers):
    table.clear()
    table.setColumnCount(len(headers))
    table.setRowCount(len(rows))       # required set row count for the tableWidget
    table_row = 0                           # table Row
    for row in rows:
        # we are inside a tuple of records
        for column, r in enumerate(row):
            # index, item_text
            item = QtWidgets.QTableWidgetItem(str(r))                     # required; item must be QTableWidgetItem
            table.setItem(table_row, column, item)         # add item to the table
            # if column in right_column:
                # item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)   # align credit field left
        table_row += 1
    # horizontal headers labels
    table.setHorizontalHeaderLabels(headers)


def get_process_details(pid):
    from datetime import datetime
    try:
        process = psutil.Process(pid)
        details = {
            'PID': pid,
            'Parent': process.ppid(),
            'Name': process.name(),
            'Executable': process.exe(),
            'CMDLine': '\n'.join(process.cmdline()),
            'Created': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M'),
            'Status': process.status(),
            'CWD': process.cwd(),
            'Username': process.username(),
            'CPU_Percent': process.cpu_percent(),
            'Connections': 'Yes' if process.net_connections() and len(process.net_connections()) > 0 else 'No',
        }
    except psutil.AccessDenied:
        # # TODO: display password dialog
        return "Permission Error"
    else:
        return details


def populate_comboBox(combobox: QtWidgets.QComboBox, items: list):
    """
    Populate comboBox
    :combobox: comboboxWidget to populate (client_cart | product in call diaog)
    :items: items to add to the combobox
    """
    combobox.blockSignals(True)
    combobox.clear()
    combobox.addItems(items)
    combobox.blockSignals(False)


def get_all_process():
    """
    Get All Process
    """
    params = ['pid', 'name', 'status', 'username', 'exe']
    ps = [p.info for p in psutil.process_iter(attrs=params)]
    rows = [(p['pid'], p['name'], p['status'], p['username'], p['exe']) for p in ps]
    return rows


def get_process_by_name(p_name):
    """
    Search a process by name
    :p_name: the process name
    :return: rows if process found else return False
    """
    params = ['pid', 'name', 'status', 'username', 'exe']
    ps = [p.info for p in psutil.process_iter(attrs=params) if p_name in p.info['name']]
    if len(ps) == 0:
        return False
    else:
        rows = [(p['pid'], p['name'], p['status'], p['username'], p['exe']) for p in ps]
        return rows


def get_process_by_user(username):
    """
    Get user by specific user
    :username: username owner of procss
    """
    params = ['pid', 'name', 'status', 'username', 'exe']
    ps = [p.info for p in psutil.process_iter(attrs=params) if username in p.info['username']]
    rows = [(p['pid'], p['name'], p['status'], p['username'], p['exe']) for p in ps]
    return rows
