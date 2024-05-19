---
title: PyQt5 讓 QTableView 顯示置中的 CheckBox
date: 2024-05-18 12:30:00
description: 讓 QTableView 顯示置中的 CheckBox
categories:
  - Python
---
## 讓 Checkbox 置中
TableVeiw 預設的 checkbox 沒辦法置中，解決方法有兩類
1. 使用 Delegate 
2. 透過 setItemWidget 設 Layout，加 checkbox 元件

## Example


```python
import sys
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex 
from PyQt5.QtGui import QStandardItemModel

class CustomizeCheckBox(QWidget):
    def __init__(self, parent, ftor ):
        super().__init__(parent)
        l = QHBoxLayout(self)
        self.cb = QCheckBox(self)
        l.addWidget(self.cb)
        l.setAlignment(Qt.AlignCenter)
        # You must set margins, otherwise checkbox style is strange.
        l.setContentsMargins(0, 0, 0, 0)                
        # m = l.contentsMargins()
        # print(m.left(), m.right(), m.top(), m.bottom(), )
        self.setLayout(l)
        self.cb.stateChanged.connect(ftor)

    def get_checkbox(self, ):
        return self.cb

class CheckBoxTableModel(QStandardItemModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)
        self._rows = rows
        self._columns = columns
        self._data = [[False for _ in range(columns)] for _ in range(rows)]

    def rowCount(self, parent=QModelIndex()):
        return self._rows

    def columnCount(self, parent=QModelIndex()):
        return self._columns

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return ""
        if role == Qt.UserRole:
            return self._data[index.row()][index.column()]
        return None

    def setData(self, index, value, role=Qt.EditRole):

        '''
        setData set value to customize data struct when role is checkStateRole,
        avoid data Qt.CheckStateRole modified in itemData. 
        It should be None, otherwise, checkbox will be shown.
        '''
        if index.isValid() and role == Qt.CheckStateRole:
            self._data[index.row()][index.column()] = value
            data = {Qt.DisplayRole: "", Qt.EditRole:"", Qt.UserRole:value}
            print(data)
            self.setItemData(index, data)
            
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return False
    
    # def flags(self, index):
    #     return Qt.ItemIsEditable | Qt.ItemIsEnabled


class CheckBoxTableView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model.dataChanged.connect(self.on_item_changed)
    def initUI(self):
        layout = QVBoxLayout(self)

        self.tableView = QTableView(self)
        self.model = CheckBoxTableModel(3, 4) 
        self.tableView.setModel(self.model)

        for row in range(3):
            for column in range(4):
                index = self.model.index(row, column)
                # Method 1
                ftor = self.getCheckBoxHandler(index)
                w = CustomizeCheckBox(self, ftor)
                self.tableView.setIndexWidget(index, w)
                # Method 2: Add checkbox directly, it will not cause starange layout.
                # cb = QCheckBox(self)
                # self.tableView.setIndexWidget(index, cb)


        layout.addWidget(self.tableView)
        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QTableView with QCheckBox')
        self.show()
    
    def on_item_changed(self, item):
        if type(item) == QModelIndex:
            # val  = self.model.data(item, Qt.CheckStateRole)
            val  = self.model.data(item, Qt.UserRole)
        else:
            val = self.model.data(item.index(), Qt.CheckStateRole)
        print("Current data is,", val)
       
    def getCheckBoxHandler(self, index):
        def handler(state):
            self.model.setData(index, state , Qt.CheckStateRole)

        return handler


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = CheckBoxTableView()
    sys.exit(app.exec_())


```