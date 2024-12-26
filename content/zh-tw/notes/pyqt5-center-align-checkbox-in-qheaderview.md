---
title: PyQt5 在 QHeaderView 加置中的 Checkbox
date: 2024-10-10 12:49:00
description: 繪製置中的 Checkbox 於 QHeaderView
categories:
  - Python
robotsdisallow: true
---
相關的Qt官方文件: https://doc.qt.io/qt-6/qheaderview.html#appearance

## QHeaderView 的外觀
QHeaderView 跟 QTableView [通常會使用同一個 model](https://doc.qt.io/qt-6/model-view-programming.html#:~:text=Some%20views%2C%20such,labels%20for%20views)，儘管 model 的 `setHeaderData` 有提供指定 `itemDataRole` 的 API，卻不是所有 `itemDataRole` 的資料都會顯示在 QHeaderView 上。

在 QHeaderView 預設的行為中，只有以下 6 種 Role 會直接影響 Header 的外觀
- [TextAlignmentRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
- [DisplayRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
- [FontRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
- [DecorationRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
- [ForegroundRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum)
- [BackgroundRole](https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum).

如果有想要畫出其他 Role data，例如 `CheckStateRole`，則需要繼承 QHeaderView 之後重新實作 `paintEvent`。

要注意的是，Header 的各 section 的外觀是透過 `paintEvent` 渲染，而不依賴 delegate。因此對 header 設置 `setItemDelegate` 是沒有用的。

下圖展示三種表格: 
- 第一種是不做任何客製化的 Table。
- 第二種讓 Header 顯示了 checkbox ，並且 Section Text 也跟著往右挪了一些，在剩下的空白中置中。
	- 注意 Section 3 只設 `CheckStateRole`但沒有設 `DisplayRole` data
	- Section 4 沒做任何 `setHeaderData`
- 第三種讓 Checkbox 和文字一起置中。

接下來，將以這三種 Table 為例，解釋該如何客製化 QHeaderView 。
## Default Header View
如同前面所說的，預設的 Header View 只會顯示幾種特定的 data role。儘管有使用 `setHeaderData` 設置 `Qt.CheckStateRole`，但沒有顯示在 Header 上。

![default_table_view](../img/pyqt5-center-align-checkbox-in-qheaderview/default_table_view.png)

## 添加 Checkbox 於 Header Section 
// reference to paint_header_checkbox.py

![add_checkbox_in_headerview](../img/pyqt5-center-align-checkbox-in-qheaderview/add_checkbox_in_headerview.png)


在 PyQt5 中，我們可以通過繼承 QHeaderView 並重寫 paintSection 方法來在表頭添加 Checkbox。主要實現步驟如下：

1. 繼承 QHeaderView 並創建自定義的 CustomHeaderView 類
2. 重新實作 paintSection，我們把原先的 paintSection 分解，並加入客製化的內容：
   - 繪製背景
   - 將原有的文字內容向右挪，保留 Checkbox 的空間
   - 在保留的空間內 (左側) 繪製 Checkbox
3. 實現 mousePressEvent 來處理 Checkbox 的點擊事件，更新 Checkbox 的狀態

經過這個步驟，Checkbox 已經顯示在 Header 上，雖然沒有 Checkbox 依然對齊左側，但文字在剩下的空間裡置中，和 Qt 預設的實作有相似的風格。
現在，我們希望 Checkbox 和文字一起置中。

## 添加 Checkbox 於 Header Section 並置中
// reference to paint_header_checkbox_center_alignment.py

![center_align_header_checkbox](../img/pyqt5-center-align-checkbox-in-qheaderview/center_align_header_checkbox.png)

要讓 Checkbox 和文字一起置中，首先需要修改 `paintSection` : 
1. Checkbox 與文字的總寬度，才能知道 Checkbox 和 text 的起始座標在哪。
	- 使用 `QStyleOptionButton` 和 `QStyle.SE_CheckBoxIndicator` 取得 Checkbox 的寬度
	- 使用 `fontMetrics().boundingRect()` 計算文字的寬度和高度
	- 更進一步的，連同間距一起計算總寬度
		- 整體寬度 = Checkbox寬度 + 文字寬度 + 間距(MARGIN)
		- 計算 section 剩餘空間，取得置中的起始位置
		```python
		widget_width = str_width + cb_width + MARGIN*3
		sec_width = self.sectionSize(logicalIndex)
		widget_margin = int((sec_width-widget_width)/2)
		```
2. 繪製置中的 Checkbox
   - 設定 Checkbox 的位置和大小
   - 和前一個例子不同，這次的 Checkbox 位置會受到 Section text 的長度而影響，而不是總是對齊左側。為了避免每次都要重新計算，`self.checkbox_locations` 用於紀錄 checkbox 的位置，以供 `mousePressEvent` 使用
   ```python
   opt = QStyleOptionButton()
   size = self.checkBoxSize()
   opt.rect = QRect(rect.left() + widget_margin, 
                    rect.top() + int((rect.height() - size) / 2),
                    size, size)
   self.checkbox_locations[logicalIndex] = opt.rect
   ```

3. 繪製置中的文字
   - 設定文字的位置，需依照 Checkbox 的寬度和間距，計算出文字的起始座標。
   ```python
   opt = QStyleOptionHeader()
   opt.rect.setLeft(rect.left() + widget_margin + cb_width + MARGIN*2)
   opt.rect.setTop(rect.top() + int((rect.height() - str_height)/2))
   ```

到這裡，`paintSection` 已經完成。

接下來需要修改 `mousePressEvent` 來處理 Checkbox 的點擊事件。
- 使用`checkbox_locations` 來判斷點擊是否在 Checkbox 範圍內
   ```python
   cb_rect = self.checkbox_locations[logicalIndex]
   pos_x = event.pos().x()
   if cb_rect.left() > pos_x or cb_rect.right() < pos_x:
       super().mousePressEvent(event)
       return
   ```

這樣的實作可以讓 Checkbox 和文字作為一體，在 section 中置中顯示，隨著滑鼠點擊更新 Checkbox 的狀態。



## 最終成果

讓 Checkbox 在 Header 和 Table Cells 都置中吧!

![image-20241226144414763](../img/pyqt5-center-align-checkbox-in-qheaderview/image-20241226144414763.png)
