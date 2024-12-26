import sys
from PyQt5.QtWidgets import (
    QApplication, QTableView, QHeaderView, QStyle, QCheckBox,
    QVBoxLayout, QWidget, QHBoxLayout, QStyleOptionButton, QStyleOptionHeader
)
from PyQt5.QtGui import QStandardItemModel, QPalette
from PyQt5.QtCore import Qt, QRect

MARGIN = 4

class CustomHeaderView(QHeaderView):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.checkbox_locations = dict()
        self.setStretchLastSection(True)

    def paintSection(self, painter, rect, logicalIndex):
        self.draw_background(painter, rect, logicalIndex)
        self.paint_center_alignment_checkbox_label(painter, rect, logicalIndex)

    def draw_background(self, painter, rect, logicalIndex):
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

    def checkBoxSize(self):
        checkboxstyle = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkboxstyle)
        return checkbox_rect.width()

    def get_header_lebel_size(self, logicalIndex):
        text = str(self.model().headerData(logicalIndex, Qt.Horizontal, Qt.DisplayRole))
        w = self.fontMetrics().boundingRect(text).width()
        h = self.fontMetrics().boundingRect(text).height()
        return w, h

    def paint_center_alignment_checkbox_label(self, painter, rect, logicalIndex):
        str_width, str_height = self.get_header_lebel_size(logicalIndex)
        cb_width = self.checkBoxSize()
        widget_width = str_width + cb_width + MARGIN * 3
        sec_width = self.sectionSize(logicalIndex)
        widget_margin = int((sec_width - widget_width) / 2)

        # Draw checkbox
        opt = QStyleOptionButton()
        size = self.checkBoxSize()
        opt.rect = QRect(
            rect.left() + widget_margin,
            rect.top() + int((rect.height() - size) / 2),
            size, size
        )
        self.checkbox_locations[logicalIndex] = opt.rect
        
        value = self.model().headerData(logicalIndex, Qt.Horizontal, Qt.CheckStateRole)
        if value == Qt.PartiallyChecked:
            opt.state = QStyle.State_NoChange | QStyle.State_Enabled
        else:
            opt.state = QStyle.State_On | QStyle.State_Enabled if value == Qt.Checked else QStyle.State_Off | QStyle.State_Enabled
        self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, opt, painter)

        # Draw text
        opt = QStyleOptionHeader()
        opt.rect = rect
        opt.rect.setLeft(rect.left() + widget_margin + cb_width + MARGIN * 2)
        opt.rect.setTop(rect.top() + int((rect.height() - str_height) / 2))
        text = self.model().headerData(logicalIndex, Qt.Horizontal, Qt.DisplayRole)
        opt.text = str(text) if text is not None else ""
        self.style().drawControl(QStyle.CE_HeaderLabel, opt, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index != -1:
            cb_rect = self.checkbox_locations.get(index)
            if cb_rect and cb_rect.contains(event.pos()):
                current_state = self.model().headerData(index, self.orientation(), Qt.CheckStateRole)
                new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
                self.model().setHeaderData(index, self.orientation(), new_state, Qt.CheckStateRole)
                # Update all checkboxes in the column
                self.parent().parent().update_column_checkboxes(index, new_state)
                return
        super().mousePressEvent(event)

class CustomizeCheckBox(QWidget):
    def __init__(self, parent=None, callback=None, row=None, column=None):
        super().__init__(parent)
        self.row = row
        self.column = column
        layout = QHBoxLayout(self)
        self.cb = QCheckBox(self)
        layout.addWidget(self.cb)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        if callback:
            self.cb.stateChanged.connect(lambda state: callback(state, self.row, self.column))

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.model = QStandardItemModel(3, 2)
        
        headers = ["Column A", "Column B"]
        for col in range(2):
            self.model.setHeaderData(col, Qt.Horizontal, headers[col], Qt.DisplayRole)
            self.model.setHeaderData(col, Qt.Horizontal, Qt.Unchecked, Qt.CheckStateRole)

        self.tableView = QTableView(self)
        self.header = CustomHeaderView(Qt.Horizontal)
        self.tableView.setHorizontalHeader(self.header)
        self.tableView.setModel(self.model)

        # Add checkboxes to cells
        for row in range(3):
            for col in range(2):
                index = self.model.index(row, col)
                w = CustomizeCheckBox(self.tableView, self.on_cell_checkbox_changed, row, col)
                self.tableView.setIndexWidget(index, w)

        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Centered Checkboxes Table')
        self.show()

    def on_cell_checkbox_changed(self, state, row, column):
        # Update header checkbox state
        self.update_header_checkbox_state(column)

    def update_header_checkbox_state(self, column):
        checked_count = 0
        total_count = self.model.rowCount()
        
        # Count checked checkboxes in current column
        for row in range(total_count):
            widget = self.tableView.indexWidget(self.model.index(row, column))
            if widget.cb.isChecked():
                checked_count += 1
        
        # Set header checkbox state based on checked count
        if checked_count == 0:
            header_state = Qt.Unchecked
        elif checked_count == total_count:
            header_state = Qt.Checked
        else:
            header_state = Qt.PartiallyChecked
            
        self.model.setHeaderData(column, Qt.Horizontal, header_state, Qt.CheckStateRole)

    def update_column_checkboxes(self, column, state):
        # Update all checkbox states in the column
        for row in range(self.model.rowCount()):
            widget = self.tableView.indexWidget(self.model.index(row, column))
            widget.cb.setChecked(state == Qt.Checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableWidget()
    sys.exit(app.exec_())