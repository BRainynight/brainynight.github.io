---
title: QStandardItemModel 的優勢
date: 2024-05-23 23:05:00
description: 為何要使用 QStandardItemModel，而不繼承 QAbstractItemModel?
categories:
  - Python
---

`QStandardItemModel` 繼承 [QAbstractItemModel](https://doc.qt.io/qt-6/qabstractitemmodel.html) ，如果想 implement 一個 Model，繼承 `QStandardItemModel` 會方便很多。

接下來會以一個簡單的例子說明，過於簡單的資料結構繼承 `QAbstractItemModel` 可能有哪些困擾。
## Quick Example
假設手上的資料是 一個 2 rows x 3 columns Table，表格內容都是 True/False
### 使用 `QAbstractItemModel` 
繼承 `QAbstractItemModel` 需要實作以下內容
1. 提供儲存的資料結構: 以一個 2D list 儲存
2. 由於儲存的結構是自己提供的，有些 function 要重新設計，而有些本就是 pure virtual function
	- `setData()`,  `data()`: 存在哪、怎麼拿。
	- `rowCount()`,  `columnCount()`: 同上，因為資料結構是自己的，數量也要自己算。

```python
class MyModel(QAbstractTableModel):
    def __init__(self, data):
        super(MyModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False
```

### 使用 `QStandardItemModel`
直接使用 Model，透過創建 `QStandardItem` 放資料進去。
- `setCheckState(Qt.CheckState)` 相當於 `setData(Qt.CheckState, Qt.CheckStateRole`)，

```python
model = QStandardItemModel()
for i in range(2):
	row = []
	for _ in range(3):
		it = QStandardItem("")
		# Checked: True, Unchecked: False
		status = Qt.Checked if i==0 else Qt.Unchecked
		it.setCheckState(status)
		row.append(it)
	model.appendRow(row)
```

提取、重設資料也很簡單，不必實作 getter 跟 setter。

在 `QAbstractItemModel` 當中，data 的 setter 跟 getter 都有一個參數 `role`。role 會影響資料存到哪裡、從哪提資料，如果 setter 跟 getter 給的 role 不同，就會拿不到想要的內容。
對 model 設資料的 API 如下，需要給定 index 跟 role。
```python
setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole): bool	
data(const QModelIndex &index, int role = Qt::DisplayRole): QVariant
```

而 QStandardItemModel 提供 API `item` 可以拿到 `QStandardItem`。在 `QStandardItem` 上又可以直接呼叫 `setCheckState`設值 -- 相當於對 model 以 `setData(index, checkState, Qt.CheckStateRole)`，可讀性更好，也更直觀。

下面的範例說明怎麼透過 model 和 item 設值與取值，要做到這些都不需要實作 function 就能辦到。

```python
ind = model.index(0, 0)
role = Qt.CheckStateRole
print("Get data for CheckStateRole", model.data(ind, role))
print("Is same to call checkState() on item", model.item(0,0).checkState())

model.setData(ind, Qt.Unchecked, role)
print("After setCheckState", model.data(ind, role))
model.item(0,0).setCheckState( Qt.Checked)
print("Item also has equivalent function setCheckState, it can also modify data", model.item(0,0).checkState())

```
## 總結
`QStandardItemModel` 提供實用的介面，相當於對每一「格」的資料再封裝。
在為 `QListView`/`QTableView`/`QTreeView` 做搭配的 model 時，一個簡單的方法判斷是否該採用
- 資料的型態是簡單的 string, boolean 這種 build-in type 嗎? 是的話，`QStandardItemModel` 夠用。
- 如果資料本身存在 customize class 裡面，本來就要實作 model 的 `data`/`setData` ，針對不同的 role 呼叫 class 不同的 function 給資料、存資料，就可以檢視 `QAbstractItemModel` 是否更好用。

---