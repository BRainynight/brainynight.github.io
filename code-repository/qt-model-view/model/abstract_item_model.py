import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import delegates  

'''
Abstract item model: can calculate duration from TravelData.

'''

def convert_to_datetime(s: str):
    if s =="":
        return datetime(2024, 1, 1)
    return datetime.strptime(s, '%Y-%m-%d').date()

class TravelData:
    attrs = ["name", "group", "org", "startDate", "endDate", "reported"]
    
    def __init__(self, n, g, o, sd, ed, r) -> None:
        self.name = n
        self.group = g
        self.org = o
        self.startDate = sd
        self.endDate = ed
        self.reported = r
    
    
    def get_duration(self, ):
        return convert_to_datetime(self.endDate) - convert_to_datetime(self.startDate)

class MyModel(QAbstractTableModel):
    def __init__(self, data, p):
        super(MyModel, self).__init__(p)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(TravelData.attrs)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            obj = self._data[index.row()]
            attr_name = TravelData.attrs[index.column()]
            val = getattr(obj, attr_name)
            # print(index, attr_name, val, role)
            return val
        return None
    

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            obj = self._data[index.row()]
            attr_name = TravelData.attrs[index.column()]
            setattr(obj, attr_name, value)

            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False
    
    def flags(self, index):
        # Let cell content is editable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


def generate_objs():
    data = [ 
        ["Amy",  "GroupA", "orgX", "2023-01-01", "2023-01-05", False],
        ["Alex", "GroupA", "orgY", "2023-01-03", "2023-01-05", False],
        ["Sam",  "GroupB", "orgP", "2023-02-01", "2023-02-06", False],
        ["Xem",  "", "", "", "", False],
    ]
    return [ TravelData(*d) for d in data ] 

def main():
    app = QApplication(sys.argv)
    data = generate_objs()
    model = MyModel(data, app)

    table_view = QTableView()
    table_view.setSortingEnabled(True)
    table_view.setModel(model)
    string_delegate = delegates.SimpleDelegate()
    combobox_delegate = delegates.GroupComboBoxDelegate()
    checkbox_delegate = delegates.CheckBoxDelegate()
    calendar_delegate = delegates.CalendarDelegate()
    table_view.setItemDelegateForColumn(0, string_delegate)
    table_view.setItemDelegateForColumn(1, combobox_delegate)
    table_view.setItemDelegateForColumn(5, checkbox_delegate) # let checkbox center alignment
    table_view.setItemDelegateForColumn(3, calendar_delegate)
    table_view.setItemDelegateForColumn(4, calendar_delegate)
    table_view.show()
    app.exec_()
    # sys.exit(app.exec_())

    for d in data:
        # get duration is really easy and doesn't relate to index value.
        print(d.name, d.get_duration())

main()



