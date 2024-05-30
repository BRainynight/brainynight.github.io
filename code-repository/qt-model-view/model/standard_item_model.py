import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TravelData:
    def __init__(self) -> None:
        self.name = ""
        self.group = ""
        self.org = ""
        self.startDate = ""
        self.endDate = ""
        self.reported = ""

# name: 
# group: combo box 
# org: editable text
# start date
# end date 
# reported: checkbox (delegate)

data = [
    ["Amy",  "GroupA", "orgX", "2023-01-01", "2023-01-05", False],
    ["Alex", "GroupA", "orgY", "2023-01-03", "2023-01-05", False],
    ["Sam",  "GroupB", "orgP", "2023-02-01", "2023-02-06", False],
    ["Xem",  "", "", "", "", False],
]
headers = [ "Name", "Group", "Org", "Start Date", "End Date", "Reported"]


class GroupComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(GroupComboBoxDelegate, self).__init__(parent)
        self.items = ["GroupA", "GroupB", "GroupC"]

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.items)
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value:
            idx = editor.findText(value)
            if idx >= 0:
                editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QCheckBox(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        if value is not None:
            editor.setChecked(bool(value))

    def setModelData(self, editor, model, index):
        value = True if editor.isChecked() else False
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        checkboxstyle = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkboxstyle)
        checkboxstyle.rect = option.rect
        checkboxstyle.rect.setLeft(option.rect.x() + option.rect.width() // 2 - checkbox_rect.width() // 2)
        editor.setGeometry(checkboxstyle.rect)

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        checkboxstyle = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkboxstyle)
        checkboxstyle.rect = option.rect
        checkboxstyle.rect.setLeft(option.rect.x() + option.rect.width() // 2 - checkbox_rect.width() // 2)
        
        if value:
            checkboxstyle.state = QStyle.State_On | QStyle.State_Enabled
        else:
            checkboxstyle.state = QStyle.State_Off | QStyle.State_Enabled
        
        QApplication.style().drawControl(QStyle.CE_CheckBox, checkboxstyle, painter)

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setGeometry(100, 100, 300, 300)
        
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        
        self.setLayout(layout)
        
        self.calendar.clicked.connect(self.accept)

    def selectedDate(self):
        return self.calendar.selectedDate()
    
class CalendarDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() in [3, 4]:
            self.dialog = CalendarDialog(parent)
            date_str = index.model().data(index, Qt.EditRole)
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            self.dialog.calendar.setSelectedDate(date)
            self.dialog.exec_()
            return self.dialog.calendar
        
        return super().createEditor(parent, option, index)
    
    def setEditorData(self, editor, index):
        if index.column() in [3, 4]:
            date = editor.selectedDate()
            date_str =QDate.toString(date, "yyyy-MM-dd")
            index.model().setData(index, date_str, Qt.EditRole)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        '''
        setModelData 在 cell 內容變更，並且 selected index 切換的時候被觸發
        (此例中，注意 checkbox 出現的時機)
        '''
        if index.column() in [3, 4]:
            # date = editor.selectedDate().toString("yyyy-MM-dd")
            # print("setModelData", date)
            # model.setData(index, date, Qt.EditRole)
            model.setData(index, Qt.Checked, Qt.CheckStateRole)
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() in [3, 4]:
            editor.setGeometry(option.rect)
        else:
            super().updateEditorGeometry(editor, option, index)

def set_model(model, data):
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
    model = QStandardItemModel(app)
    model = set_model(model, data)

    table_view = QTableView()
    table_view.setSortingEnabled(True)
    table_view.setModel(model)
    combobox_delegate = GroupComboBoxDelegate()
    checkbox_delegate = CheckBoxDelegate()
    calendar_delegate = CalendarDelegate()
    table_view.setItemDelegateForColumn(1, combobox_delegate)
    table_view.setItemDelegateForColumn(5, checkbox_delegate) # let checkbox center alignment
    table_view.setItemDelegateForColumn(3, calendar_delegate)
    table_view.setItemDelegateForColumn(4, calendar_delegate)
    table_view.show()
    get_travel_length(model.index(0, 3).data(), model.index(0, 4).data(),)
    sys.exit(app.exec_())
    
def get_travel_length(st, et):
    st = (QDate.fromString(st, "yyyy-MM-dd")).toPyDate()
    et = (QDate.fromString(et, "yyyy-MM-dd")).toPyDate()
    res = et - st
    print(res)




if __name__ == "__main__":
    main()
