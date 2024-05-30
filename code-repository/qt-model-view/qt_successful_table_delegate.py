import math
import sys
from PyQt5.QtCore import Qt, QRect, QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QApplication, QCheckBox, QStyledItemDelegate, QStyle, QStyleOptionButton, QTableView, QHeaderView, QStyleFactory)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import pyqtSignal,  QSize, Qt
from PyQt5.QtGui import QPainter, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QStyle, QTableWidget,
        QStyledItemDelegate, QTableWidgetItem, QTableView, QWidget, QCheckBox,
        QVBoxLayout, QHBoxLayout, QStyleFactory)
__all__ = [ 
    "MyTableWidget"
]

# class MyTableWidget(QWidget):
class MyTableWidget(QTableWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.model = MyModel(self)
        self.view = MyTreeView(self)
        self.view.setModel(self.model)

        v = QVBoxLayout(self)
        v.addWidget(self.view)
        self.setLayout(v)
        # self.view.add_checkbox_widgets()
        
        self.delegate = CheckBoxDelegate(self.view)
        self.view.setItemDelegate(self.delegate)


def create_checkbox(parent):
    w = QWidget(parent)
    l = QHBoxLayout(parent)
    l.setAlignment(Qt.AlignCenter)
    cb = QCheckBox(w)
    cb.setStyle(QStyleFactory.create('windows'))
    cb.setStyle(QStyleFactory.create('fusion'))
    print(cb.style().objectName() )
    print( QStyleFactory.keys())

    l.addWidget(cb)
    w.setLayout(l)
    return w

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
        value = 1 if editor.isChecked() else 0
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


class MyTreeView(QTableView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)

    def add_checkbox_widgets(self, ):
        for row in range(self.model().rowCount()):
            for col in range(self.model().columnCount()):
                w = create_checkbox(self)
                ind = self.model().index(row, col)
                self.setIndexWidget(ind, w)





class MyModel(QStandardItemModel  ):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.init_value()

    def init_value(self, ):
        for i in range(5):
            lt = []
            for j in range(3):
                obj = QStandardItem("")
                obj.setData(False, Qt.CheckStateRole)
                obj.setCheckable(False)
                lt.append(obj)  
            self.appendRow(lt)





if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setStyle('macintosh')
    
    widget = MyTableWidget()
    widget.show()
    

    sys.exit(app.exec_())