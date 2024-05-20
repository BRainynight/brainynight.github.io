import sys
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def init_model(self, ):
        self.model = QStandardItemModel(3, 4) 
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                it = QStandardItem()
                it.setCheckState(Qt.Checked if (i%2+j%2)==0 else Qt.Unchecked)
                it.setCheckable(True)
                self.model.setItem(i, j, it)

    def initUI(self):
        layout = QVBoxLayout(self)
        self.init_model()
        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                # Method 2: Add checkbox directly, it will not cause starange layout.
                # cb = QCheckBox(self)
                # self.tableView.setIndexWidget(index, cb)

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QTableView with QCheckBox')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())
