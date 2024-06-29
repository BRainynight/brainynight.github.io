import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os 
from delegates import SimpleDelegate

PATH = "../../../content/zh-tw/notes"
from markdown_to_json import convert_md_to_json

'''
Try to use QAbstractItemModel to implement model can fit QTreeView and QTableView

- Need to implement QAbstractItemModel.index
    QAbstractTableModel is difficult to fit QTreeView
'''

class Markdown:
    attrs = ["title", "date", "categories", "tags", "description"]
    def __init__(self, d) -> None:
        self.categories = []
        self.tags = []
        self.date = "" 
        self.description = ""
        self.title = ""
        self.init(d)

    @staticmethod
    def str_to_list(val):
        if type(val) == str:
            val = [val]
        return val    

    def init(self, d: dict):
        for key, val in d.items():
            if val is None:
                val = ""

            if key == "categories":
                val = Markdown.str_to_list(val)
            elif key == "tags":
                val = Markdown.str_to_list(val)
            elif key == "date":
                val = str(val)

            setattr(self, key, val)

class MyModel(QAbstractItemModel):
    def __init__(self, data, p):
        super(MyModel, self).__init__(p)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(Markdown.attrs)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            obj = self._data[index.row()]
            attr_name = Markdown.attrs[index.column()]
            val = getattr(obj, attr_name)
            if type(val) != str:
                val = str(val)
            return val
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            obj = self._data[index.row()]
            attr_name = Markdown.attrs[index.column()]
            setattr(obj, attr_name, value)

            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False
    
    def flags(self, index):
        # Let cell content is editable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def sort(self, column, order=Qt.AscendingOrder):
        attr_name = Markdown.attrs[column]
        self.layoutAboutToBeChanged.emit()
        # Sorting the data
        print(column)
        self._data.sort(key=lambda x: getattr(x, attr_name), reverse=(order == Qt.DescendingOrder))
        self.dataChanged.emit(self.index(0, column), self.index(self.rowCount()-1, column), [Qt.EditRole])

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column, self._data[row])
        return QModelIndex()

    def parent(self, index):
        return QModelIndex()

def prepare_markdown_objs():
    files = os.listdir(PATH)
    lt = []
    for file in files:
        if not file.endswith(".md"):
            continue
        fp = os.path.join(PATH, file)
        print(fp)
        js = convert_md_to_json(fp)
        meta = js["metadata"]
        lt.append(Markdown(meta))
    return lt

app = QApplication(sys.argv)
data = prepare_markdown_objs()
model = MyModel(data, app)
print(Markdown.attrs)

table_view = QTableView()
table_view.setModel(model)
string_delegate = SimpleDelegate()
table_view.setItemDelegateForColumn(1, string_delegate)
table_view.setItemDelegateForColumn(2, string_delegate)
table_view.setItemDelegateForColumn(3, string_delegate)
w = table_view.horizontalHeader().length()+table_view.verticalHeader().width()
h = table_view.verticalHeader().length()+table_view.horizontalHeader().height()
print(table_view.horizontalHeader().height())

table_view.setFixedSize(w, h )
table_view.setSortingEnabled(True)
table_view.show()
app.exec_()
