---
title: PythonQt 讓 Python 的 QT Application 嵌入於 C++
date: 2024-06-01 05:30:00
description: 研究 PythonQt 模組
categories:
  - Python

---


## Install PyQt5
```bash
sudo apt install qtbase5-dev
sudo apt install libqt5widgets5
sudo apt install libqt5widgets5
sudo apt install libqt5gui5
sudo apt install qtbase5-private-dev

# web engine related.
sudo apt install qtwebengine5-dev qtwebengine5-dev-tools libqt5webengine5 libqt5webenginewidgets5

```
## Install PythonQt
我的環境是 WSL

1. git clone PythonQt

    ```bash
    git clone https://github.com/MeVisLab/pythonqt.git
    ```
2. 參考 [Building](https://mevislab.github.io/pythonqt/Building.html) 頁面 Linux 的環節

    ```bash 
    cd $PythonQtRoot
    qmake
    make all 
    ```

### [fatal error: 'private/qmetaobjectbuilderp.h'](https://stackoverflow.com/questions/65924650/how-to-build-pythonqt-in-ubutnu)
安裝 `qtbase5-private-dev`
```bash
sudo apt install qtbase5-private-dev
```

## Compile The First App
PythonQt 提供了 `pro` 檔案於 `$PYTHONQT_ROOT/build`底下，這種檔案用於 qmake，如果想使用 cmake 則需另外轉換。

下面的範例導入了 core 跟 widgets 兩個模組，如果有用到其他模組，像是 [`QWebEngineView `](https://doc.qt.io/qt-6/qwebengineview.html)，就繼續往後加。加的關鍵字可以看 QT 網站上，會寫這個元件的 qmake 要寫什麼，以 `QWebEngineView` 來說就是 `QT += webenginewidgets` (search: qmake)

```cmake
QT += core widgets # 如果有用到其他 module 加在這裡

CONFIG += c++11
LOC  = ABS/PATH/TO/PYTHONQT

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

# 不想把 lib 放在 LD_LIBRARY_PATH 要設 RPATH，QMAKE_RPATHDIR 是讓 qmake 在生成 command 時設 rpath 的 info
QMAKE_RPATHDIR += $$LOC/lib

# 執行檔名稱
TARGET = gui
```

## 官方範例

- Source code 在: [PythonQt/examples](https://github.com/MeVisLab/pythonqt/blob/master/examples/)，但範例在 `$PYTHONQT_ROOT/lib` 底下! 

- 執行範例的時候，記得把 Lib 加入 `LD_LIBRARY_PATH`

    ```bash
    export LD_LIBRARY_PATH=$PYTHONQT_ROOT/lib
    ```

- For example:

    `PyLauncher` 是其中一個範例，功能是會執行傳入的 py 檔，如果檔案無效會發出警告。

    下面讓 `PyLauncher` 執行另一個 example 的 py 檔: 

    ```bash
    cd $PYTHONQT_ROOT/lib
    ./PyLauncher ../examples/PyGuiExample/example.py
    ```

    