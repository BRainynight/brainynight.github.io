import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MultiList(QComboBox):
    itemChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(MultiList, self).__init__(parent)
        self.setEditable(True)

        self.displayText = ""
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.slotUpdateText()

        self.model.itemChanged.connect(self.slotUpdate)

    def addItem(self, text):
        row = self.model.rowCount()
        item = QStandardItem()
        item.setText(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model.setItem(row, 0, item)

    def addItems(self, texts):
        for text in texts:
            self.addItem(text)

    def getCheckedItems(self):
        checkedItems = []
        for i in range(self.model.rowCount()):
            if self.model.item(i, 0).checkState() == Qt.Checked:
                checkedItems.append(self.model.item(i, 0).text())
        return checkedItems

    def setCheckedItems(self, items):
        for item in items:
            index = self.findText(item)
            if index != -1:
                self.model.item(index).setData(Qt.Checked, Qt.CheckStateRole)
        self.slotUpdate()

    @pyqtSlot()
    def slotUpdateText(self):
        self.lineEdit().setText(self.displayText)

    @pyqtSlot()
    def slotUpdate(self):
        self.displayText = ""
        for i in range(self.model.rowCount()):
            if self.model.item(i, 0).checkState() == Qt.Checked:
                self.displayText += self.model.item(i, 0).text() + "; "
        QTimer.singleShot(0, self.slotUpdateText)

def main():
    app = QApplication(sys.argv)
    multiList = MultiList()

    multiList.addItems(["One", "Two", "Three", "Four"])
    multiList.setCheckedItems(["One", "Two"])

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Select items:"))
    layout.addWidget(multiList, 1)

    widget = QWidget()
    widget.setWindowTitle("MultiList example")
    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
