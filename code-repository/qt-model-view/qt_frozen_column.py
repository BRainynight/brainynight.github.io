import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView, QHeaderView, QAbstractItemView, QAbstractSlider, QVBoxLayout, QWidget, QScrollBar

# example from qt website

class FreezeTableWidget(QTableView):
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.frozenTableView = QTableView(self)

        self.init()

        # Let column1 also scroll down
        # Use 2 tableview, frozenTableView is the fixed column.
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

    def init(self):
        self.frozenTableView.setModel(self.model())
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.viewport().stackUnder(self.frozenTableView)

        self.frozenTableView.setStyleSheet("QTableView { border: none;"
                                           "background-color: #8EDE21;"
                                           "selection-background-color: #999}")
        self.frozenTableView.setSelectionModel(self.selectionModel())
        for col in range(1, self.model().columnCount()):
            self.frozenTableView.setColumnHidden(col, True)

        self.frozenTableView.setColumnWidth(0, self.columnWidth(0))

        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()

        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == 0:
            self.frozenTableView.setColumnWidth(0, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction, modifiers):
        current = super().moveCursor(cursorAction, modifiers)
        print("moveCursor")

        if cursorAction == QAbstractItemView.MoveLeft and current.column() > 0 and \
           self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(0):
            newValue = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() - \
                       self.frozenTableView.columnWidth(0)
            self.horizontalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        print("scrollTo")
        if index.column() > 0:
            super().scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        print("updateFrozenTableGeometry")
        print(self.verticalHeader().width(), self.frameWidth())
        print(self.frameWidth(), )
        print(self.columnWidth(0))
        print(self.viewport().height(), self.horizontalHeader().height())

        self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                         self.frameWidth(), self.columnWidth(0),
                                         self.viewport().height() + self.horizontalHeader().height())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Sample data for demonstration purposes
    from PyQt5.QtGui import QStandardItemModel, QStandardItem
    model = QStandardItemModel(10, 5)
    for row in range(10):
        for column in range(5):
            item = QStandardItem(f"Item {row},{column}")
            model.setItem(row, column, item)

    freezeTableWidget = FreezeTableWidget(model)
    freezeTableWidget.show()
    sys.exit(app.exec_())
