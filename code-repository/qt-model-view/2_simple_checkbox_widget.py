import sys
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

'''
Show checkbox in QTableView by add QCheckBox.
No setting on model.
'''

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        self.model = QStandardItemModel(3, 4) 
        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                # Method 2: Add checkbox directly
                cb = QCheckBox(self)
                self.tableView.setIndexWidget(index, cb)

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QTableView with QCheckBox')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())
