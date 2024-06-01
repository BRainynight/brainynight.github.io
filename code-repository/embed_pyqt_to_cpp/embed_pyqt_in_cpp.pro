QT += core widgets

CONFIG += c++11
LOC  = YOUR_PYTHONQT_ROOT

# Include the .prf files
include($$LOC/build/common.prf)
include($$LOC/build/PythonQt.prf)
include($$LOC/build/PythonQt_QtAll.prf)

# Specify the source files
SOURCES += main.cpp

# Include directories (optional, if not specified in .prf files)
# INCLUDEPATH += /usr/include/qt5 /usr/include/qt5/QtCore /usr/include/qt5/QtWidgets $$LOC/pythonqt

# Library directories (optional, if not specified in .prf files)
LIBS += -L/usr/lib/x86_64-linux-gnu -L$$LOC/lib

QMAKE_RPATHDIR += $$LOC/lib
TARGET = gui