import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# modify from qt website example

class CustomizeCheckBox(QWidget):
    def __init__(self, parent, ftor ):
        super().__init__(parent)
        l = QHBoxLayout(self)
        self.cb = QCheckBox(self)
        l.addWidget(self.cb)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0) 
        self.setLayout(l)
        self.cb.stateChanged.connect(ftor)
    
    def set_check_state(self, s):
        self.cb.setCheckState(s)

class CheckBoxTableModel(QStandardItemModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role in [ Qt.CheckStateRole, Qt.UserRole]:
            self.setItemData(index, {Qt.UserRole:value})
            return True
        return False

class BasedTableView(QTableView):
    def __init__(self, p ):
        super().__init__(p)
    
    def model_item_data_changed(self, item):
        if item.index().row() == 0:
            for i in range(1, self.model().rowCount()):
                value = item.data(Qt.UserRole)
                ind = self.model().index(i, item.index().column())
                self.indexWidget(ind).set_check_state(value)

    def init(self, model):
        self.setModel(model)
        self.model().itemChanged.connect(self.model_item_data_changed)
        for row in range(self.model().rowCount()):
            for column in range(self.model().columnCount()):
                index = self.model().index(row, column)
                callback = self.getCheckBoxHandler(index)
                w = CustomizeCheckBox(self, callback)
                self.setIndexWidget(index, w)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setFocusPolicy(Qt.NoFocus)        
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

    def getCheckBoxHandler(self, index):
        def handler(state):
            self.model().setData(index, state , Qt.UserRole)
        return handler
    
class FloatHeaderTableView(BasedTableView):
    def __init__(self, p):
        super().__init__(p)
        self.floating_header_row = BasedTableView(self)
        self.delegate = Delegate(self.floating_header_row)
        self.floating_header_row.setItemDelegate(self.delegate)
        self.setAlternatingRowColors(True)

        self.floating_header_row.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.floating_header_row.verticalScrollBar().setValue)
        
        self.floating_header_row.horizontalScrollBar().valueChanged.connect(self.horizontalScrollBar().setValue)
        self.horizontalScrollBar().valueChanged.connect(self.floating_header_row.horizontalScrollBar().setValue)
        

    def init(self, model):
        super().init(model)
        self.floating_header_row.init(model)
        
        self.viewport().stackUnder(self.floating_header_row)
        self.floating_header_row.setSelectionModel(self.selectionModel())
        for row in range(1, self.model().rowCount()):
            self.floating_header_row.setRowHidden(row, True)

        self.floating_header_row.setRowHeight(0, self.rowHeight(0))

        self.floating_header_row.horizontalHeader().setFixedHeight(self.horizontalHeader().height())
        self.floating_header_row.verticalHeader().setFixedHeight(self.verticalHeader().width())

        self.floating_header_row.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.floating_header_row.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.floating_header_row.show()

        self.updateFrozenTableGeometry()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateFrozenTableGeometry()

    def updateFrozenTableGeometry(self):
        # x y w h 
        # frameWidth: outline width of frame 


        self.floating_header_row.setGeometry(self.frameWidth(), 
                                             self.frameWidth(), 
                                             self.viewport().width() , 
                                             self.rowHeight(0)
                                            ) 

class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if (index.row()==0):
            opt = QStyleOptionHeader()
            opt.rect = option.rect
            opt.state = QStyle.State_Enabled
            QApplication.style().drawControl(QStyle.CE_Header, opt, painter)


    
class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model.dataChanged.connect(self.on_item_changed)

    def initUI(self):
        layout = QVBoxLayout(self)
        self.model = CheckBoxTableModel(10, 5)
        # self.tableView = BasedTableView(self)
        self.tableView = FloatHeaderTableView(self)
        self.tableView.init(self.model) 


        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QTableView with QCheckBox')
        self.show()
    
    def on_item_changed(self, item):
        val  = self.model.data(item, Qt.UserRole)
        print("Current data is,", val)
       



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    pattle = mainWin.palette()
    base_brush = pattle.base()
    alter_brush = pattle.alternateBase()
    pattle.setBrush(QPalette.Base, alter_brush)
    pattle.setBrush(QPalette.AlternateBase, base_brush)
    mainWin.setPalette(pattle)

    sys.exit(app.exec_())
