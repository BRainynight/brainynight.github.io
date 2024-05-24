---
title: Qt Model View Framework
date: 2024-05-23 22:00:00
description: Model View Framework 的介紹，這跟 MVC 有何不同?
categories:
  - Python
---

## Model-View-Controller
MVC (model-view-controller) 是一種 design pattern，圖為 First Head Design Pattern 的範例。傳統的 MVC 架構如下
- Model: 掌管業務邏輯，會是這個架構中唯一與 Database 交互的 component. 
- View: 透過 Controller 得到 Model 的資料，呈現在 UI 上。
- Controller: 轉換 User Input 成 Model 應該採取的動作，讓 Model 採取動作、並拿新的資料更新 View。
![First Head-MVC](https://www.oreilly.com/api/v2/epubs/9780596516680/files/httpatomoreillycomsourceoreillyimages2242349.png.jpg)

## Model/View Framework
QT 簡化了這三者的關係，當 View 跟 Controller 結合，就成為 Model/View architecture。這種架構更簡單，且依然切分 Data / UI ，甚至得以讓同一個 Model 直接搭配不同的 View，無須改變底層資料結構。

而為了彈性的處理 User Input，QT 導入了 [*delegate*](https://doc.qt.io/qt-6/qitemdelegate.html) 的概念。在 QT 當中，delegate 負責處理編輯 (edit) 跟渲染 (render)，透過 customize delegate，更可以改變渲染的外觀，與存資料到 Model 的型式。

## Models 
所有的 item models 都繼承  [QAbstractItemModel](https://doc.qt.io/qt-6/qabstractitemmodel.html) ，資料本身不一定要存在 model class，可以是外部的 database ，或其他自定義的 class。

要客製化 model，建議從  [QAbstractListModel](https://doc.qt.io/qt-6/qabstractlistmodel.html),  [QAbstractTableModel](https://doc.qt.io/qt-6/qabstracttablemodel.html) 甚至 [QStandardItemModel](https://doc.qt.io/qt-6/qstandarditemmodel.html) 開始，他們提供更多 default implementation。Qt 還提供 [QFileSystemModel](https://doc.qt.io/qt-6/qfilesystemmodel.html), 和 SQL 系列的 model，這裡不贅述。

## Views
所有的 view 都繼承於抽象類 [QAbstractItemView](https://doc.qt.io/qt-6/qabstractitemview.html)，三種主要的: 
- [QListView](https://doc.qt.io/qt-6/qlistview.html)
- [QTableView](https://doc.qt.io/qt-6/qtableview.html)
- [QTreeView](https://doc.qt.io/qt-6/qtreeview.html)

事實上，[QColumnView](https://doc.qt.io/qt-6/qcolumnview.html), [QHeaderView](https://doc.qt.io/qt-6/qheaderview.html) 也是繼承自 `QAbstractItemView`。但改變 header 的需求較少，同樣不贅述。

### Delegate 
- 官方文件: [QStyledItemDelegate Class](https://doc.qt.io/qt-6/qstyleditemdelegate.html#subclassing-qstyleditemdelegate)
- 官方範例[Star Delegate Example](https://doc.qt.io/qt-6/qtwidgets-itemviews-stardelegate-example.html):  C++ 範例，
	- PyQT5 的版本可以看: [PyQT5  Delegate Example](https://github.com/baoboa/pyqt5/blob/master/examples/itemviews/stardelegate.py)。

當遇到沒辦法透過 Standard Delegate (QStyledItemDelegate) 呈現的 Data Type 就需要自己定義 Delegate。
- 和渲染相關的:
	- `paint` 改變渲染的方式
	- `sizeHint` 決定呈現的 item 大小
- 和編輯相關的: 可在 tableview 放自訂的 QWidget Editor，跟這些 function 有關
	- `createEditor`: 回傳要放在表格裡，讓 User 編輯資料的 widget
	- `setEditorData`: 提供 editor 資料
	- `setModelData`: 對 model 更新資料
	在一般的情況下，delegate 不需要客製化，這塊稍後再提。
## Convenience Classes
除了以上基本的 Model View，QT 還提供了其他的 class，這些 class 預先 implement 了一些 function，讓使用者不必手把手實作抽象類的 function。
### Widget
如果用途非常簡單，不需要自己控制 model，可以考慮使用 [QListWidget](https://doc.qt.io/qt-6/qlistwidget.html), [QTreeWidget](https://doc.qt.io/qt-6/qtreewidget.html)與 [QTableWidget](https://doc.qt.io/qt-6/qtablewidget.html)。
- 優點: 已經套好 model/view，直接套用就有成品。
- 缺點: 不能隨意替換 model，對 view 的控制權比較差。

## Reference 

- 官方文件: [model/view framework](https://doc.qt.io/qtforpython-5/overviews/model-view-programming.html#model-view-programming) 
