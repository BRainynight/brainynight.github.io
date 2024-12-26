import sys
from PyQt5.QtWidgets import (
    QApplication, QTableView, QHeaderView, QStyle, QStyleOptionHeader, QVBoxLayout, QWidget, 
    QHeaderView, QStyleOptionButton, QHeaderView, QStyleOptionHeader, QStyle )

from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QPainter, QPalette
from PyQt5.QtCore import Qt, QRect

# d->model->headerData(logicalIndex, d->orientation, Qt::DecorationRole);

MARGIN = 4
class CustomHeaderView(QHeaderView):
    def __init__(self, horizental=True,parent=None):
        super().__init__(horizental, parent)

    def paintSection(self, painter, rect, logicalIndex):
        self.draw_background(painter, rect, logicalIndex)
        self.paint_original_section_but_shift_right(painter, rect, logicalIndex)
        self.paint_the_checkbox(painter, rect, logicalIndex)

    def draw_background(self, painter, rect, logicalIndex ):
        painter.save()
        opt = QStyleOptionHeader()
        opt.rect = rect
        model = self.model()
        background = model.headerData(logicalIndex, self.orientation(), Qt.BackgroundRole)
        if background:
            opt.palette.setBrush(QPalette.Button, background)
            opt.palette.setBrush(QPalette.Window, background)
            painter.setBrushOrigin(opt.rect.topLeft())
        self.style().drawControl(QStyle.CE_Header, opt, painter, self)
        painter.restore()
    
    def checkBoxAreaWidth(self, ):
        return self.checkBoxSize() + 2 * MARGIN; 

    def checkBoxSize(self, ):
        checkboxstyle = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkboxstyle)
        return checkbox_rect.width()

    def paint_original_section_but_shift_right(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect.adjusted(self.checkBoxAreaWidth(), 0, 0, 0), logicalIndex)
        painter.restore()

    def paint_the_checkbox(self, painter, rect, logicalIndex, ):      
        opt = QStyleOptionButton()
        size = self.checkBoxSize()
        opt.rect = QRect(rect.left() + MARGIN, rect.top() + int((rect.height() - size) / 2,), size, size)
        value = self.model().headerData(logicalIndex, Qt.Horizontal, Qt.CheckStateRole)
        if value:
            opt.state = QStyle.State_On | QStyle.State_Enabled
        else:
            opt.state = QStyle.State_Off | QStyle.State_Enabled
        self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, opt, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == -1:
            super().mousePressEvent(event)
            return

        logicalIndex = self.logicalIndexAt(event.pos().x() )
        sec_pos = self.sectionPosition(logicalIndex)
        if event.pos().x() > sec_pos +self.checkBoxAreaWidth():
            super().mousePressEvent(event)
            return

        current_state = self.model().headerData(index, self.orientation(), Qt.CheckStateRole)
        new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
        self.model().setHeaderData(index, self.orientation(), new_state, Qt.CheckStateRole)
    
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

        self.model.setHeaderData(0, Qt.Horizontal, True, Qt.CheckStateRole)
        self.model.setHeaderData(0, Qt.Horizontal, "1111", Qt.DisplayRole)
        self.model.setHeaderData(1, Qt.Horizontal, False, Qt.CheckStateRole)
        self.model.setHeaderData(1, Qt.Horizontal, "222", Qt.DisplayRole)
        self.model.setHeaderData(2, Qt.Horizontal, True, Qt.CheckStateRole)

    def initUI(self):
        layout = QVBoxLayout(self)
        self.init_model()
        self.tableView = QTableView(self)

        self.header = CustomHeaderView()
        self.tableView.setHorizontalHeader(self.header)
        self.tableView.setModel(self.model)

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)


        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QHeaderView: Add Checkbox in Header')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())
