---
title: QStyle draw functions 範例
date: 2024-07-23 22:55:00
description: "透過一個簡單的範例，展示 drawPrimitive 畫出來的元件，以及 SubElement 在實際案例的作用。"
categories:
  - Default
---

這個範例將展示 
1. 畫出部分 Primitive Element ，了解他們個別長什麼樣子: `PE_IndicatorArrowUp`, `PE_IndicatorItemViewItemCheck`, `PE_IndicatorCheckBox`, `PE_IndicatorRadioButton`, `PE_IndicatorArrowRight`, `PE_IndicatorProgressChunk`, `PE_FrameMenu`。
2. 如何使用 SubElement 與 `subElementRect`

![show_PE_element_and_how_to_use_subelementrect](../img/qstyle-example-for-draw-functions/show_PE_element_and_how_to_use_subelementrect.png)

## Primitive Element

這裡使用最簡單的 `QStyleOption`，讓每個 element 都套用相同的設定。事實上有些 element 需要搭配特定的 option，在 [drawPrimitive](https://doc.qt.io/qt-6/qstyle.html#drawPrimitive) 裡面有表格說明。

```python
for i, pe in enumerate(styles_name):
    name = pe
    pe = eval("QStyle."+pe)

    # use the most general option. which option should be used for each item are 
    # written in https://doc.qt.io/qt-6/qstyle.html#drawPrimitive
    option = QStyleOption()
    option.initFrom(self)
    option.rect = QRect(10, 10+20*i, 20, 20)
    self.style().drawPrimitive(pe, option, painter,)
    painter.drawText(40, 10+20*(i+1),  name)

```



## Control Element 與 SubElement

模仿 [Styles and Style Aware Widgets](https://doc.qt.io/qt-6/style-reference.html#styling-java-check-boxes:~:text=The%20QCheckBox%20paints%20itself%20in%20QWidget%3A%3ApaintEvent()%20with%20style%20option%20opt%20and%20QStylePainter%20p.%20The%20QStylePainter%20class%20is%20a%20convenience%20class%20to%20draw%20style%20elements.%20Most%20notably%2C%20it%20wraps%20the%20methods%20in%20QStyle%20used%20for%20painting.%20The%20QCheckBox%20draws%20itself%20as%20follows%3A) 的一段範例，畫出 checkbox 與 checkbox label。需要注意的地方是

1. `btn_opt` 原本的 `rect` 很重要，有初始位置的概念在，會影響 `subElementRect` 算出來的結果。
2. `subElementRect(QStyle.SE_CheckBoxContents, ...)` 並沒有包含 text 的空間，原本算出來的 `rect` 寬度只有 `1`，需要手動算文字寬度加上去，才能完整顯示文字。目前不清楚對 QCommonStyle 而言，調整文字寬度的地方在哪。

```python
def draw_ce(self, ):
    painter = QPainter(self)
    # A QCheckBox, draws a PE_IndicatorCheckBox, a CE_CheckBoxLabel and a PE_FrameFocusRect.

    btn_opt = QStyleOptionButton()
    btn_opt.rect = QRect(10, 180, 20, 20)

    subopt = QStyleOptionButton()
    subopt.rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, btn_opt, self)
    print(subopt.rect)
    self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, subopt, painter, self)

    # Draw the checkbox label
    subopt = QStyleOptionButton(btn_opt)
    subopt.text = "This is label for checkbox"

    font_metrics = QFontMetrics(subopt.fontMetrics)
    text_width = font_metrics.width(subopt.text)

    subopt.rect = self.style().subElementRect(QStyle.SE_CheckBoxContents, btn_opt, self)
    print("Before set text width", subopt.rect)
    subopt.rect.setWidth(subopt.rect.width() + text_width)

    print("After set text width", subopt.rect)
    self.style().drawControl(QStyle.CE_CheckBoxLabel, subopt, painter, self)

```

## 完整程式

```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def draw_pe(self, ):
        painter = QPainter(self)
        
        styles_name = ( "PE_IndicatorArrowUp", "PE_IndicatorItemViewItemCheck", "PE_IndicatorCheckBox", 
                        "PE_IndicatorRadioButton", "PE_IndicatorArrowRight", "PE_IndicatorProgressChunk",
                        "PE_FrameMenu"
                       )
        for i, pe in enumerate(styles_name):
            name = pe
            pe = eval("QStyle."+pe)
            
            # use the most general option. which option should be used for each item are 
            # written in https://doc.qt.io/qt-6/qstyle.html#drawPrimitive
            option = QStyleOption()
            option.initFrom(self)
            option.rect = QRect(10, 10+20*i, 20, 20)
            self.style().drawPrimitive(pe, option, painter,)
            painter.drawText(40, 10+20*(i+1),  name)

    def draw_ce(self, ):
        painter = QPainter(self)
        # A QCheckBox, draws a PE_IndicatorCheckBox, a CE_CheckBoxLabel and a PE_FrameFocusRect.

        btn_opt = QStyleOptionButton()
        btn_opt.rect = QRect(10, 180, 20, 20)
        
        subopt = QStyleOptionButton()
        subopt.rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, btn_opt, self)
        print(subopt.rect)
        self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, subopt, painter, self)

        # Draw the checkbox label
        subopt = QStyleOptionButton(btn_opt)
        subopt.text = "This is label for checkbox"

        font_metrics = QFontMetrics(subopt.fontMetrics)
        text_width = font_metrics.width(subopt.text)

        subopt.rect = self.style().subElementRect(QStyle.SE_CheckBoxContents, btn_opt, self)
        print("Before set text width", subopt.rect)
        subopt.rect.setWidth(subopt.rect.width() + text_width)
        
        print("After set text width", subopt.rect)
        self.style().drawControl(QStyle.CE_CheckBoxLabel, subopt, painter, self)
        

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_pe()
        self.draw_ce()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PE_FrameFocusRect Example')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    ex = App()
    ex.show()
    sys.exit(app.exec_())
```