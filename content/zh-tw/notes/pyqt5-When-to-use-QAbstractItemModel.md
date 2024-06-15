---
title: 使用 QAbstractItemModel 的時機
date: 2024-05-23 23:05:00
description: 當資料結構較為複雜、是一個自己實作的物件時，考慮使用 QAbstractItemModel
categories:
  - Python
---

在這個範例中，資料是一個「出差核銷系統」，每一筆資料包含

- 出差人
- Group (小組)
- Organization (大組)
- 起始日
- 結束日
- 已呈報

事後，我們需要根據每一筆資料計算些資訊，例如: 差旅長度。並且預期這個系統有延伸的可能，也續會增加「報帳金額」、「日均花費金額」.... 



## QStandardItemModel

使用 `QStandardItemModel`，資料有如 2D excel 表格，優點是 Model 不需要實作。缺點是計算相關資料 (如差旅長度) 時，資料的關聯性差，需要透過 row (同一筆資料)、column (起始日、結束日) 找到需要的資料。

```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import delegates  
data = [
    ["Amy",  "GroupA", "orgX", "2023-01-01", "2023-01-05", False],
    ["Alex", "GroupA", "orgY", "2023-01-03", "2023-01-05", False],
    ["Sam",  "GroupB", "orgP", "2023-02-01", "2023-02-06", False],
    ["Xem",  "", "", "", "", False],
]
headers = [ "Name", "Group", "Org", "Start Date", "End Date", "Reported"]

def set_model(app, data):
    model = QStandardItemModel(app)
    for row in data:
        lt = []
        for i, val in enumerate(row):
            it = QStandardItem(val)
            if i == 5: # Reported
                it.setCheckable(True)
            lt.append(it)
        model.appendRow(lt)
    return model

def get_duration(st, et):
    st = (QDate.fromString(st, "yyyy-MM-dd")).toPyDate()
    et = (QDate.fromString(et, "yyyy-MM-dd")).toPyDate()
    res = et - st
    print(res)
```

## 不使用 QStandardItemModel

如果已經確定顯示的方法只有 Table 或 List，可以使用 `QAbstractTableModel`，相較於 base class `QAbstractItemModel`，它多實作了 `index`, `parent`，只需要實作  `rowCount`, `columnCount` 之類的方法。使用 `QAbstractItemModel` 則具有面對 `QTreeView` 的彈性，但連 `index` 都需要自己實作。

本例使用  `QAbstractTableModel` 。缺點是需要自己處理放資料的地方、並實作 `rowCount`, `columnCount` 之類的方法。本例用一個 list 儲存 objects。

優點是每一筆資料直接對應一個物件，事後在算差旅天數的時候，可以直接對物件呼叫 `get_duration` 直接取得 -- 把相關的資料跟工具封裝在一起。如果有一些不需要顯示在 GUI 上，卻與物件有關連的資料，也可以直接記載物件上。

```py
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def convert_to_datetime(s: str):
    if s =="":
        return datetime(2024, 1, 1)
    return datetime.strptime(s, '%Y-%m-%d').date()

class TravelData:
    attrs = ["name", "group", "org", "startDate", "endDate", "reported"]
    def __init__(self, n, g, o, sd, ed, r) -> None:
        self.name = n
        self.group = g
        self.org = o
        self.startDate = sd
        self.endDate = ed
        self.reported = r
    
    def get_duration(self, ):
        return convert_to_datetime(self.endDate) - convert_to_datetime(self.startDate)

class MyModel(QAbstractTableModel):
    def __init__(self, data, p):
        super(MyModel, self).__init__(p)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(TravelData.attrs)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            obj = self._data[index.row()]
            attr_name = TravelData.attrs[index.column()]
            val = getattr(obj, attr_name)
            return val
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            obj = self._data[index.row()]
            attr_name = TravelData.attrs[index.column()]
            setattr(obj, attr_name, value)
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False
    
    def flags(self, index): # Let cell content is editable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
```





