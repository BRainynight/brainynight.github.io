from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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

ind = model.index(0, 0)
role = Qt.CheckStateRole
print("Get data for CheckStateRole", model.data(ind, role))
print("Is same to call checkState() on item", model.item(0,0).checkState())

model.setData(ind, Qt.Unchecked, role)
print("After setCheckState", model.data(ind, role))
model.item(0,0).setCheckState( Qt.Checked)
print("Item also has equivalent function setCheckState, it can also modify data", model.item(0,0).checkState())

model.setData(ind, Qt.Unchecked, )

