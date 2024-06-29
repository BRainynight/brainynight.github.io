import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CustomButton(QPushButton):
    def __init__(self, title, parent=None):
        super(CustomButton, self).__init__(title, parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.hasFocus():
            painter = QPainter(self)
            painter.save()

            pen = QPen(QColor('red'))
            painter.setPen(pen)

            option = QStyleOptionFocusRect()
            option.initFrom(self)
            option.rect = QRect(0, 0, 100, 100)
            option.backgroundColor = self.palette().highlight().color()

            # State_KeyboardFocusChange is necessary in style "Fusion" for element PE_FrameFocusRect 
            # option.state |= QStyle.State_KeyboardFocusChange
            print(bool(option.state & QStyle.State_KeyboardFocusChange))
            self.style().drawPrimitive(QStyle.PE_FrameFocusRect, option, painter,)
            painter.restore()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        line_edit = QLineEdit("Focus on me and see the frame!")
        layout.addWidget(line_edit)

        self.button = CustomButton('Click Me')
        self.button.setFixedSize(100, 50)
        layout.addWidget(self.button)

        self.setLayout(layout)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PE_FrameFocusRect Example')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('Windows')
    ex = App()
    ex.show()
    sys.exit(app.exec_())