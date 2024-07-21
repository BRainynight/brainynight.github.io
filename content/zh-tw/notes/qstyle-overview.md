---
title: QStyle Overview
date: 2024-07-21 09:12:00
description: "研讀 QStyle 的閱讀筆記，介紹三種 style elements 與 SubControl、SubElement。"
categories:
  - Default
---
> 本篇是 [Styles and Style Aware Widgets](https://doc.qt.io/qt-6/style-reference.html) 的閱讀筆記

Qt 中，Style 指的是那些繼承 QStyle 的類別，QStyle 自身是抽象類。Qt 內建就有多個 styles 供選擇，某些 styles 只能在特定平台上使用。自定義的 styles 需透過 [`create()`](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QStyleFactory.html#PySide6.QtWidgets.QStyleFactory.create "PySide6.QtWidgets.QStyleFactory.create") 創建、透過 [`setStyle()`](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QApplication.html#PySide6.QtWidgets.QApplication.setStyle "PySide6.QtWidgets.QApplication.setStyle") 設置。

Qt 內建的 widget 所需的繪圖環節，幾乎都由 style 執行。當所有的繪圖細節都封裝於 QStyle，就可以確保各元件之間繪製效果的一致性。例如: 陰影效果在各元件之間一致、highlight color 統一 .... 等等。

QStyle 負責繪製  graphical elements，一個 element 可能是一個 widget (eg. push button) 或是 style elements (一部分的 widget，例如: push button bevel, windows frame ...)。
QStyle 透過 draw functions 繪製 graphical elements，這些 draw function 基本上有相似的 argument: 
- enum value: 指定畫哪一個 "graphical element"
- [QStyleOption](https://doc.qt.io/qt-6/qstyleoption.html) : 如何、在哪畫這個 element (有關這個 elemnt 的設定)
- [QPainter](https://doc.qt.io/qt-6/qpainter.html) : 用來畫 element 
- [QWidget](https://doc.qt.io/qt-6/qwidget.html) : 這個繪畫在什麼物件上。
## Style Elements

> A style element is a graphical part of a GUI. A widget consists of a hierarchy (or tree) of style elements.

一個 widget 是由多個 style elements 組成。以下圖來說，Push Button 由三個部分組成
- Focus Frame 
- Label 
- Button Bevel 
而 Button Bevel 又由多個元素組成
- Bevel Frame 
- .... 

![pushbuttontree](https://doc.qt.io/qt-6/images/conceptualpushbuttontree.png)

Widget 可以只呼叫 style 一次，直接丟一個最 high level 的元素 (ex. `CE_PushButton`)，讓細節實作在 `QStyle` 裡面。
```cpp
void QPushButton::paintEvent(QPaintEvent *)
{
    QStylePainter p(this);
    QStyleOptionButton option;
    initStyleOption(&option);
    p.drawControl(QStyle::CE_PushButton, option);
}
```

也可以直接在自己的 `paintEvent` 裡面，逐一呼叫 `style` 把元素一個個畫出來，如 `QTabWidget` 就是直接在自己的 function 畫 `PE_FrameTabBarBase`, `PE_FrameTabBarBase`。
```cpp
void QTabWidget::paintEvent(QPaintEvent *)
{
    Q_D(QTabWidget);
    if (documentMode()) {
        QStylePainter p(this, tabBar());
        if (QWidget *w = cornerWidget(Qt::TopLeftCorner)) {
            QStyleOptionTabBarBase opt;
            QTabBarPrivate::initStyleBaseOption(&opt, tabBar(), w->size());
            opt.rect.moveLeft(w->x() + opt.rect.x());
            opt.rect.moveTop(w->y() + opt.rect.y());
            p.drawPrimitive(QStyle::PE_FrameTabBarBase, opt);
        }
        if (QWidget *w = cornerWidget(Qt::TopRightCorner)) {
            QStyleOptionTabBarBase opt;
            QTabBarPrivate::initStyleBaseOption(&opt, tabBar(), w->size());
            opt.rect.moveLeft(w->x() + opt.rect.x());
            opt.rect.moveTop(w->y() + opt.rect.y());
            p.drawPrimitive(QStyle::PE_FrameTabBarBase, opt);
        }
        return;
    }
    QStylePainter p(this);

    QStyleOptionTabWidgetFrame opt;
    initStyleOption(&opt);
    opt.rect = d->panelRect;
    p.drawPrimitive(QStyle::PE_FrameTabWidget, opt);
}

```

Style elements 總共有三種: 

| Enums                                                                        | Prefix | Draw functions          |
| ---------------------------------------------------------------------------- | ------ | ----------------------- |
| [PrimitiveElement](https://doc.qt.io/qt-6/qstyle.html#PrimitiveElement-enum) | `PE_`  | `QStyle::drawPrimitive` |
| [ControlElement](https://doc.qt.io/qt-6/qstyle.html#ControlElement-enum)     | `CE_`  | `QStyle::drawControl` |
| [ComplexControl](https://doc.qt.io/qt-6/qstyle.html#ComplexControl-enum)     | `CC_`  | `QStyle::drawComplexControl` |

### Primitive Elements
Primitive Elements: 作為裝飾的被動元件，不會跟 User 互動。
### Control Elements
負責某種與 User 互動的工作。它可以是一個完整的 widget 如 Push Button。也可以是 widget 的一部分，像 scroll bar slider。
- 當 Control element 是由多個 element 組合而成時，這些 elements 怎麼畫、放在哪、bounding rectangle 大小，通常放在 `style` 裡面計算與決定。
### Complex Control Elements
這種物件由多個 control elements 組成。他們的行為受 cursor 位置與按鍵影響，以 scroll bars 為例，User 可以用滑鼠移動 slider，也可以按 line up 與 line down 按鈕。Complex control elements 通常透過 control & primitive elemnts 組成需要的子控制元件。
## 其他 QStyle 裡的 Enum 
[Other QStyle Tasks](https://doc.qt.io/qt-6/style-reference.html#other-qstyle-tasks)
QStyle 裡有一些 enum，他們不代表實體的 element，但與 element 有關連。任務像是
- 用來取得 element 需要的 bounding rectangle
- 取得元件與 frame 之間的 Margin Size (`PM_ButtonMargin`)

這裡提到三種 enum: 

| Enum Name                                                          | Prefix | Related QStyle Function  | Related Function Description        | Related Graphical Elements |
| ------------------------------------------------------------------ | ------ | ------------------------ | ----------------------------------- | -------------------------- |
| [SubElement](https://doc.qt.io/qt-6/qstyle.html#SubElement-enum)   | `SE_`  | `QStyle::subElementRect` | 回傳該 `subElement` 的面積大小，以 `QRect` 表示 | Primitive Elements         |
| [SubControl](https://doc.qt.io/qt-6/qstyle.html#SubControl-enum)   | `SC_`  | `QStyle::subControlRect` | 回傳該 `subControl` 的面積大小，以 `QRect` 表示 | Control Elements           |
| [PixelMetric](https://doc.qt.io/qt-6/qstyle.html#PixelMetric-enum) | `PM_`  | `QStyle::pixelMetric`    | 回傳 Offset, Margin 等距離，單位是 Pixel     |                            |

SubElement, SubControl 都不是 graphical elements，不能用於 `draw` 開頭的幾個 draw functions。PixelMetric 更不是，底下的名稱都是與距離相關的。

接下來以 `SubControl` 為例，透過 Qt source code 觀察該怎麼用。`SubElement` 的用法也相似，只是 `SubElement` 和 control 無關。

### QStyle::SubControl
- [enum SubControl](https://doc.qt.io/qt-6/qstyle.html#SubControl-enum)
SubControl 這個 enum 內的東西不代表 GUI element，它們更像是 "flag"。
有些 SubControl 會有對應的 control element，例如 `SC_SCrollBarSlider` 之於 `CE_ScrollBarSlider`。

常見的用法
1. 確認 option 的 flags 包含這個 flag，如有就可以進行對應的繪製。例如: 看到 `SC_SCrollBarSlider` 就畫 `CE_ScrollBarSlider`。
2. 使用 function `subControlRect(...)` 取得這個 SubControl item 的 rectangle 大小，設給 `option.rect`。option 在繪製時是必須的輸入內容，SubControl 影響繪製的效果(大小)，而不直接參與繪製。

> You cannot use the style to draw a sub control; the style will only calculate the bounding rectangle in which the sub control should be drawn. 

以下  `SC_ScrollBarSubLine` 舉例
### Example: `drawComplexControl`
在 [`QCommonStyle::drawComplexControl`](https://codebrowser.dev/qt5/qtbase/src/widgets/styles/qcommonstyle.cpp.html#3318) 當中，`SC_ScrollBarSubLine` 的作用
1. 先確認 `QStyleOptionSlider->subControls` 裡面有無 `SC_ScrollBarSubLine` (如同確認有無這個 flag) 
2. 若有，透過 function `subControlRect` 取得 rectangle，並指給 `newScrollbar.rect`
3. 最後，繪製的部分是 `drawControl(CE_ScrollBarSubLine, &newScrollbar, p, widget)`，用到的是 control element `CE_ScrollBarSubLine`，而非SubControl `SC_ScrollBarSubLine`! 

```cpp
if (const QStyleOptionSlider *scrollbar = qstyleoption_cast<const QStyleOptionSlider *>(opt)) {
	// Make a copy here and reset it for each primitive.
	QStyleOptionSlider newScrollbar = *scrollbar;
	State saveFlags = scrollbar->state;
	// 1. check flag has SC_ScrollBarSubLine
	if (scrollbar->subControls & SC_ScrollBarSubLine) {
		newScrollbar.state = saveFlags;
		// 2. get rect and assign to option (QStyleOptionSlider)
		newScrollbar.rect = proxy()->subControlRect(cc, &newScrollbar, SC_ScrollBarSubLine, widget);
		if (newScrollbar.rect.isValid()) {
			if (!(scrollbar->activeSubControls & SC_ScrollBarSubLine))
				newScrollbar.state &= ~(State_Sunken | State_MouseOver);
			// 3. draw GUI element through CE_ScrollBarSubLine
			proxy()->drawControl(CE_ScrollBarSubLine, &newScrollbar, p, widget);
		}
	}
```

