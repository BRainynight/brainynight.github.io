import sys
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

class CustomizeCheckBox(QWidget):
    def __init__(self, parent, ftor ):
        super().__init__(parent)
        l = QHBoxLayout(self)
        self.cb = QCheckBox(self)
        l.addWidget(self.cb)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0) # You must set margins, otherwise checkbox style is strange.
        self.setLayout(l)
        self.cb.stateChanged.connect(ftor)

class CheckBoxTableModel(QStandardItemModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role in [ Qt.CheckStateRole, Qt.UserRole]:
            if index.row() == 0:
                self.setItemData(index, {Qt.CheckStateRole:value}) # Don't set to CheckStateRole!! it causes problem!!
            else:
                self.setItemData(index, {Qt.UserRole:value})
            # self.dataChanged.emit(index, index, [Qt.CheckStateRole]) # No need to emit again!
            return True
        return False

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model.dataChanged.connect(self.on_item_changed)

    def initUI(self):
        layout = QVBoxLayout(self)
        self.tableView = QTableView(self)
        self.model = CheckBoxTableModel(3, 4) 
        self.tableView.setModel(self.model)

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                callback = self.getCheckBoxHandler(index)
                w = CustomizeCheckBox(self, callback)
                self.tableView.setIndexWidget(index, w)

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QTableView with QCheckBox')
        self.show()
    
    def on_item_changed(self, item):
        val  = self.model.data(item, Qt.UserRole)
        print("Current data is,", val)
       
    def getCheckBoxHandler(self, index):
        def handler(state):
            self.model.setData(index, state , Qt.UserRole)
        return handler


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())
