---
title: Qt Souce Code 研讀-PE_FrameFocusRect, QFusionStyle 與 QPushButton
date: 2024-06-27 21:51:00
description: 嘗試繪製 PE_FrameFocusRect 時的 Qt source code 探索。
categories:
  - Python
---

為了深入了解 Primitive Elements, Control Elements 這些 GUI element 實作上會怎麼使用。

我嘗試從一個實作下手 -- 從 `QStyle::PrimitiveElement` 裡挑選了一個元素出來，在 custom widget 畫出這個效果。

這次選中 `PE_FrameFocusRect` 。

### PE_FrameFocusRect
首先需要知道元素 `PE_FrameFocusRect` 是什麼。見下圖，藍色的框就是 `PE_FrameFocusRect` 的效果。

![PE_FrameFocusRect](../img/qt-read-source-code-about-frame-focus-rect/PE_FrameFocusRect.jpg)

根據[官方的例子](https://doc.qt.io/qt-6/qstyle.html#developing-style-aware-custom-widgets)，彷彿直接呼叫 `drawPrimitive` 就完成了。為了驗證，我實作了一個 `CustomPushButton`，希望在 Focus 時畫上`PE_FrameFocusRect`。

結果下面這段 code 沒有造成任何變化
```python
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
            option = QStyleOptionFocusRect()
            option.initFrom(self)
            option.rect = QRect(0, 0, 100, 100)
            option.backgroundColor = self.palette().highlight().color()
            self.style().drawPrimitive(QStyle.PE_FrameFocusRect, option, painter,)
            painter.restore()
```

探究原因，根據[文章 "Qt 绘制 PE_FrameFocusRect"](https://segmentfault.com/a/1190000040259127)敘述到，有些效果出現與否，跟當前的主題有關。

以 `QPushButton` 來說，在 Windows 上我有兩個主題可以用 : `Fusion` 和
`Windows`。其中，`Windows` 在點 button 時會有 `PE_FrameFocusRect`，而 `Fusion` 卻不會。

![compare-windows-and-fusion-styles](../img/qt-read-source-code-about-frame-focus-rect/compare-windows-and-fusion-styles.jpg)

在設置顏色、並把主題設成 `Windows` 之後，效果生效了。代表 `paintEvent` 的 code 還是有生效的。
```python
app = QApplication(sys.argv)
app.setStyle('Windows')
```

剩下的問題是

- 為何在 Fusion 主題下 `drawPrimitive` 沒有作用? 
- Highlight color 是藍色 `#308cc6`，為何顯示出來是橘紅色? 

### QFusionStyle::drawPrimitive
以下片段節錄於 `qfusionstyle.cpp`。
```cpp
void QFusionStyle::drawPrimitive(PrimitiveElement elem,
                                 const QStyleOption *option,
                                 QPainter *painter, const QWidget *widget) const
{
case PE_FrameFocusRect:
        if (const QStyleOptionFocusRect *fropt = qstyleoption_cast<const QStyleOptionFocusRect *>(option)) {
            //### check for d->alt_down
            if (!(fropt->state & State_KeyboardFocusChange))
                return;
            QRect rect = option->rect;

            painter->save();
            painter->setRenderHint(QPainter::Antialiasing, true);
            painter->translate(0.5, 0.5);
            QColor fillcolor = highlightedOutline;
            fillcolor.setAlpha(80);
            painter->setPen(fillcolor.darker(120));
            fillcolor.setAlpha(30);
            QLinearGradient gradient(rect.topLeft(), rect.bottomLeft());
            gradient.setColorAt(0, fillcolor.lighter(160));
            gradient.setColorAt(1, fillcolor);
            painter->setBrush(gradient);
            painter->drawRoundedRect(option->rect.adjusted(0, 0, -1, -1), 1, 1);
            painter->restore();
        }
        break;
}
```

這段 code 做了兩件事: 
1. 判斷 `state` 是否包含 `State_KeyboardFocusChange`，若不包含直接返回，不會畫任何東西。
2. color 使用的是來自 QFusionStyle 的色盤 (`highlightedOutline` 是前面設的變數，取自這裡代表在 custom widget 怎麼設都不會影響結果。)

回頭驗證，會發現
1. option.state 是不包含 `State_KeyboardFocusChange` 的，因此 `QFusionStyle::drawPrimitive` 會直接返回，不會畫東西。 
	```python
	# option is QStyleOptionFocusRect
	print(bool(option.state & QStyle.State_KeyboardFocusChange))
	```
2. 即使手動設置 state，讓它也有 `State_KeyboardFocusChange` 的 flag，因為前面提到顏色透過 `highlightedOutline` 拿到的，紅色的效果不會影響到 FocusRect，和 `Windows` 主題不一樣! 
	```python
	option.state |= QStyle.State_KeyboardFocusChange
	```
	![FocusRect_and_State_KeyboardFocusChange](../img/qt-read-source-code-about-frame-focus-rect/FocusRect_and_State_KeyboardFocusChange.jpg)

至此，這個實驗算是成功在 custom widget 上畫出 `PE_FrameFocusRect` 的效果了。但經由前面的探索可以看到，雖然都是 PushButton，不同主題下顯現的元素卻不一樣。`Windows` 有 `PE_FrameFocusRect`，而 `Fusion` 預設下是沒有的。

### QWindowsStyle::drawPrimitive

關於顏色的問題 `QWindowsStyle` 會取用到 `QStyleOptionFocusRect::backgroundColor`，因此設置是有效的。只不過在畫 `PE_FrameFocusRect` 時，它對 Color 又做了 XOR 運算。以本例的 highlight color 來說，運算完的顏色是 `#cf7339` (橘紅色)。

```cpp
void QWindowsStyle::drawPrimitive(PrimitiveElement pe, const QStyleOption *opt, QPainter *p,
                                  const QWidget *w) const
{
    ......
	case PE_FrameFocusRect:
        if (const QStyleOptionFocusRect *fropt = qstyleoption_cast<const QStyleOptionFocusRect *>(opt)) {
            //### check for d->alt_down
            if (!(fropt->state & State_KeyboardFocusChange) && !proxy()->styleHint(SH_UnderlineShortcut, opt))
                return;
            QRect r = opt->rect;
            p->save();
            p->setBackgroundMode(Qt::TransparentMode);
            QColor bg_col = fropt->backgroundColor;
            if (!bg_col.isValid())
                bg_col = p->background().color();
            // Create an "XOR" color.
            QColor patternCol((bg_col.red() ^ 0xff) & 0xff,
                              (bg_col.green() ^ 0xff) & 0xff,
                              (bg_col.blue() ^ 0xff) & 0xff);
            p->setBrush(QBrush(patternCol, Qt::Dense4Pattern));
            p->setBrushOrigin(r.topLeft());
            p->setPen(Qt::NoPen);
            p->drawRect(r.left(), r.top(), r.width(), 1);    // Top
            p->drawRect(r.left(), r.bottom(), r.width(), 1); // Bottom
            p->drawRect(r.left(), r.top(), 1, r.height());   // Left
            p->drawRect(r.right(), r.top(), 1, r.height());  // Right
            p->restore();
        }
        break;
	......
}
```

### QFusionStyle::drawControl 
PushButton 屬於 [control element](https://doc.qt.io/qt-6/qstyle.html#ControlElement-enum)，在 enum 的敘述中有一段: 
> QStyle::CE_PushButton: A QPushButton, draws CE_PushButtonBevel, CE_PushButtonLabel and PE_FrameFocusRect.

`CE_PushButton` 基本上是由三個元素組成: 
- `CE_PushButtonBevel`
- `CE_PushButtonLabel`
- `PE_FrameFocusRect` 

探究 `QFusionStyle::drawControl` 關於 `CE_PushButton` 繪製的片段卻會看到，只有畫 `CE_PushButtonBevel` 和 `CE_PushButtonLabel`。

```cpp
void QFusionStyle::drawControl(ControlElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget) const
{
......
case CE_PushButton:
	if (const QStyleOptionButton *btn = qstyleoption_cast<const QStyleOptionButton *>(option)) {
		proxy()->drawControl(CE_PushButtonBevel, btn, painter, widget);
		QStyleOptionButton subopt = *btn;
		subopt.rect = subElementRect(SE_PushButtonContents, btn, widget);
		proxy()->drawControl(CE_PushButtonLabel, &subopt, painter, widget);
	}
	break;
 ......
}
```

而  `QWindowsstyle::drawControl` 在關於繪製 `CE_PushButton` 的片段，用到 ` QCommonStyle::drawControl`。這裡的就很明確，分別畫了兩個 control 元素 `CE_PushButtonBevel` 與 `CE_PushButtonLabel`，和一個 Primitive 元素  `PE_FrameFocusRect` 。

```cpp
void QCommonStyle::drawControl(ControlElement element, const QStyleOption *opt, QPainter *p, const QWidget *widget) const
{
......
case CE_PushButton:
	if (const QStyleOptionButton *btn = qstyleoption_cast<const QStyleOptionButton *>(opt)) {
		proxy()->drawControl(CE_PushButtonBevel, btn, p, widget);
		QStyleOptionButton subopt = *btn;
		subopt.rect = subElementRect(SE_PushButtonContents, btn, widget);
		proxy()->drawControl(CE_PushButtonLabel, &subopt, p, widget);
		if (btn->state & State_HasFocus) {
			QStyleOptionFocusRect fropt;
			fropt.QStyleOption::operator=(*btn);
			fropt.rect = subElementRect(SE_PushButtonFocusRect, btn, widget);
			proxy()->drawPrimitive(PE_FrameFocusRect, &fropt, p, widget);
		}
	}
	break;
......
}
```

這就是為何同是 Push Button，在不同的主題會出現的元素不同。
## Example Code 
以下是本篇實驗所使用的完整內容：
```python 
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
    app.setStyle('Windows')
    ex = App()
    ex.show()
    sys.exit(app.exec_())
```
