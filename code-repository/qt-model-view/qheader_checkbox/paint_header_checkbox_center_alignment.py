import sys
from PyQt5.QtWidgets import (
    QApplication, QTableView, QHeaderView, QStyle, QStyleOptionHeader, QVBoxLayout, QWidget, 
    QHeaderView, QStyleOptionButton, QHeaderView, QStyleOptionHeader, QStyle )
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPalette
from PyQt5.QtCore import Qt, QRect

MARGIN = 4

class CustomHeaderView(QHeaderView):
    def __init__(self, horizental=True,parent=None):
        super().__init__(horizental, parent)
        self.checkbox_locations = dict()

    def paintSection(self, painter, rect, logicalIndex):
        self.draw_background(painter, rect, logicalIndex)
        self.paint_center_alignment_checkbox_label(painter, rect, logicalIndex)

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

    
    def paint_center_alignment_checkbox_label(self, painter, rect, logicalIndex ):
        str_width, str_height = self.get_header_lebel_size(logicalIndex)
        checkboxstyle = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkboxstyle)
        cb_width = checkbox_rect.width()
        widget_width = str_width + cb_width + MARGIN*3
        sec_width = self.sectionSize(logicalIndex)
        widget_margin = int( (sec_width-widget_width)/2)
        ## checkbox 
        opt = QStyleOptionButton()
        size = self.checkBoxSize()
        opt.rect = QRect( rect.left() + widget_margin,  rect.top() + int((rect.height() - size) / 2,), size, size)
        self.checkbox_locations[logicalIndex] = opt.rect
        value = self.model().headerData(logicalIndex, Qt.Horizontal, Qt.CheckStateRole)
        if value:
            opt.state = QStyle.State_On | QStyle.State_Enabled
        else:
            opt.state = QStyle.State_Off | QStyle.State_Enabled
        self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, opt, painter)

        ## text 
        opt = QStyleOptionHeader()
        opt.rect = rect 
        opt.rect.setLeft(rect.left() + widget_margin + cb_width + MARGIN*2)
        opt.rect.setTop(rect.top() + int(  (rect.height() - str_height)/2 ))
        text = self.model().headerData(logicalIndex, Qt.Horizontal, Qt.DisplayRole)
        if text is None:
            ss = ""
        else:
            ss = str(text)
        opt.text = ss
        self.style().drawControl(QStyle.CE_HeaderLabel, opt, painter)
    

    
    def get_header_lebel_size(self, logicalIndex):
        # get the header width: https://stackoverflow.com/questions/52857397/how-to-know-header-text-width-in-qstyle
        opt = QStyleOptionHeader()
        ss = str(self.model().headerData(logicalIndex, Qt.Horizontal, Qt.DisplayRole))
        w = self.fontMetrics().boundingRect(ss).width()
        h =  self.fontMetrics().boundingRect(ss).height()
        return w, h


    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == -1:
            super().mousePressEvent(event)
            return

        logicalIndex = self.logicalIndexAt(event.pos().x() )
        cb_rect = self.checkbox_locations[logicalIndex]
        pos_x = event.pos().x()
        if cb_rect.left() > pos_x or cb_rect.right() < pos_x:
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

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('QHeaderView: Center Align Checkbox')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())
