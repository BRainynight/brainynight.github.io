import sys
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.table_view = QTableView()
        self.model = QStandardItemModel(3, 4)
        self.init_model_data()        
        
        self.table_view.setModel(self.model)
        self.set_header() # should add header model after set model of table, otherwise header model will be overritten.

        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)
        self.setWindowTitle('QTableView Example')
        self.resize(400, 300)
    
    def init_model_data(self, ):
        # Populate the model with data
        for row in range(3):
            for column in range(4):
                item = QStandardItem(f'Item {row+1}, {column+1}')
                self.model.setItem(row, column, item)

    def set_header(self, ):
        self.header_model = QStandardItemModel(1, 4)
        h = self.table_view.horizontalHeader()
        h.setModel(self.header_model)
        print(self.header_model.rowCount(), self.header_model.columnCount())
        for row in range(self.header_model.rowCount()):
            for column in range(self.header_model.columnCount()):
                if column != 2:
                    continue
                index = self.header_model.index(row, column)
                cb = QCheckBox(self)
                h.setIndexWidget(index, cb)
                a = h.indexWidget(index)
                print(row, column, a) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = MainWidget()
    example.show()
    sys.exit(app.exec_())
