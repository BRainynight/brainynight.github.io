import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import delegates  
data = [
    ["Amy",  "GroupA", "orgX", "2023-01-01", "2023-01-05", False],
    ["Alex", "GroupA", "orgY", "2023-01-03", "2023-01-05", False],
    ["Sam",  "GroupB", "orgP", "2023-02-01", "2023-02-06", False],
    ["Xem",  "", "", "", "", False],
]
headers = [ "Name", "Group", "Org", "Start Date", "End Date", "Reported"]
    
def get_travel_length(st, et):
    st = (QDate.fromString(st, "yyyy-MM-dd")).toPyDate()
    et = (QDate.fromString(et, "yyyy-MM-dd")).toPyDate()
    res = et - st
    print(res)


def set_model(app, data):
    model = QStandardItemModel(app)
    for row in data:
        lt = []
        for i, val in enumerate(row):
            it = QStandardItem(val)
            if i == 5:
                it.setCheckable(True)
            lt.append(it)
        model.appendRow(lt)
    return model

def main():
    app = QApplication(sys.argv)    
    model = set_model(app, data)

    table_view = QTableView()
    table_view.setSortingEnabled(True)
    table_view.setModel(model)
    combobox_delegate = delegates.GroupComboBoxDelegate()
    checkbox_delegate = delegates.CheckBoxDelegate()
    calendar_delegate = delegates.CalendarDelegate()
    table_view.setItemDelegateForColumn(1, combobox_delegate)
    table_view.setItemDelegateForColumn(5, checkbox_delegate) # let checkbox center alignment
    table_view.setItemDelegateForColumn(3, calendar_delegate)
    table_view.setItemDelegateForColumn(4, calendar_delegate)
    table_view.show()
    get_travel_length(model.index(0, 3).data(), model.index(0, 4).data(),)
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
