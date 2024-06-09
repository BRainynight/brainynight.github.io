from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

class SimpleDelegate(QStyledItemDelegate):
    '''
    Don't like original text disappear when double click the cell.
    '''
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)