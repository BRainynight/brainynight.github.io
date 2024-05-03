---
title: Python 相對匯入與絕對匯入
description: 關於相對匯入與絕對匯入的優缺點，以及如何迅速解決絕對匯入模組在移動後，需要被匯入時的解決辦法。
date: 2022-06-05 11:11:40
categories: Python
aliases:
- /posts/2022-06-05-python-import
- /posts/2022-06-05-python-import.html
---

這篇的重點依然在於「相對引用與絕對引用」，但在這之間，先來看一些有關 import 的觀念。

## [概念](https://docs.python.org/3/reference/import.html#packages)

不管它是用 C語言、Python 或其他什麼方式來實作，Python 只有一種型態的模組物件(module object)，所有的 Module 都是這種型態(type)。管理這些 module ，提供他們名稱層級架構的就是 Package。

我們可以把 Package 就想像成一個檔案系統管理檔案的樣子，但它又不完全等價於檔案系統，因為 package 與 module 們不一定需要來自檔案系統。以檔案系統作為類比，是因為 package 如檔案系統一般有分層架構。所有的 package 本質上都是 module，但不是所有的 module 都是 package ，這是一個充分非必要條件。

Package 可以視為是一種特殊的 module ，更仔細的說：**任何包含有 `__path__` 屬性的 module 會被認為是一個 package**。

> All packages are modules, but not all module are packages. Packages Are a special kind of module; specifically, any module that contains a `__path__` attribute is considered a package.

Python定義了兩種的 package，regular package 和 namespace package

| [Regular package](https://docs.python.org/3/reference/import.html#packages) | Namespace packages                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 不一定非得有 `__init__.py`  才能是 package，但是只要有這個檔案，在 import 到該 package 時，一定會先執行  `__init__.py` 再去執行其他動作。 | 由多個 [portions (直接翻譯：部份)](https://docs.python.org/3/glossary.html#term-portion)構成的，每個 portion 都貢獻一個子模組(subpackage)給父模組(parent package)。Portion  可分佈在檔案系統中不同的地方，資料夾、網路、甚至是 zip file 反正必須是 Python 可以搜尋到的地方。 |

## [Import Search](https://docs.python.org/3/reference/import.html#searching)

當試圖載入模型時，首先會被檢查的地方是 `sys.modules`，這個字典會將**已經載入的模組名稱**(module name) mapping 到已經加載的 module 實例。

### Module Cache

`sys.modules` 是可寫的，但是要很小心、隨意改寫很容易有錯，**總之不要動它**。隨意地刪除 key 有可能不會破壞關聯的 Module (因為其他 module 可能保留對它的reference)。但是，他會使字典的映射功能無效﹔使用該 key 找 module 時找不到，引發 [`ModuleNotFoundError`](https://docs.python.org/zh-tw/3/library/exceptions.html#ModuleNotFoundError)

來實際操作看看：

```python
import sys 
print(sys.modules) # 超多東西
print(sys.modules["typing"]) # 挑其中的 typing 出來看
# <module 'typing' from 'C:\\path\\to\\user\\anaconda3\\lib\\typing.py'>
type(sys.modules["typing"])
# module
```

`sys.modules` 是一個字典，紀錄著 modeul name : module instance 這樣一組一組的訊息，是匯入模組時第一個搜尋的地方。

### Finders and Loader

若指定的 module name 在 `sys.modules` 中找不到，會調用 Python 的 import 協議 (protocol)，以尋找並加載此 module 。這個協議包含兩個部分: [finders](https://docs.python.org/3/glossary.html#term-finder)  [loaders](https://docs.python.org/3/glossary.html#term-loader)，但將不細講。只要滿足協議，我們甚至可以透過網址(URL)匯入模組。

Python 有它預設的 finder，預設的搜索路徑為`sys.path`，其中包含了這三種位置 ([The Module Search Path](https://docs.python.org/3/tutorial/modules.html#the-module-search-path))

1. 被執行腳本的所在資料夾
2. [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) (一堆資料夾名稱，是 PYTHONPATH 是機器自身的環境變數之一)
3. 一些預設的地方，像是 site-packages 資料夾 ([`site`](https://docs.python.org/3/library/site.html#module-site)模組在管理)

## 相對與絕對匯入的比較

Python 社群對於這兩種匯入的制定在這裡: [PEP328 Imports: Multi-Line and Absolute/Relative](https://www.python.org/dev/peps/pep-0328/#rationale-for-absolute-imports)

|      | 絕對匯入                                                     | 相對匯入                                                     |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 優點 | 使用上簡易、直覺                                             | 移動檔案時修改較為方便                                       |
| 缺點 | 在檔案系統中移動時，需要尋訪檔案中所有 import 的地方，修改層級關係 | 該檔案無法作為腳本執行，必須由其他腳本檔案先 import 該 module 後執行。 |



## 絕對位置匯入(Absolute Import)

前面提到，Import Search 時會嘗試再 `sys.modules` 所列的路徑中嘗試尋找要被匯入的模組。而對於一些我們自創的、沒有被記載於 `sys.modules` 的模組而言，絕對匯入(absolute import)是指，被引入的 package 使用的是從 root folder 到該 package/module 之間的完整路徑。

```python
import foo
```

像這樣的用法，在 Python 2.4 之前，並沒有明確的說 import 所指的位置應該是 top-level 或是其他 module insider。為了解決這個歧異(ambiguity) 從 Python 2.5 開始，這種 `import foo` 的寫法，被稱為「 **absolute import**」。它代表這個 `foo` 必定是可以透過 `sys.path` 取得的 module 或 package，這稱為絕對匯入。

> To resolve the ambiguity, it is proposed that `foo` will always be a module or package reachable from `sys.path`. This is called an absolute import.

根據 [PEP 328](https://www.python.org/dev/peps/pep-0328/#rationale-for-absolute-imports)，從 python 2.5開始，所有直接`import xxx` 語法，都會是 top-level module : 與 `__main__` 同級(資料夾)的 module。

絕對導入的優點是清楚、架構易懂，但也有著問題：重命名層次結構中 high-level 的 package 時、或是將一個 package 移至另一個 package 時，要去修改所有的程式碼，需要付出較高的代價。

一個簡單粗暴，但就軟體架構規劃未必是好事的作法是，在移動 package 時將「要被 import 的 package」的層級，用 

```python
sys.path.append("path/to/pkg's/parent")
```

強制把該 package 加到被搜索行列（ `sys.path`）裡面。



## 相對匯入 (Relative Import)

當 import package 時 package 前面有 `.` 就是相對匯入。

> A single leading dot indicates a relative import, starting with the current package. Two or more leading dots give a relative import to the parent(s) of the current package, one level per dot after the first. Here’s a sample package layout. 
>
> Relative imports use a module’s __name__ attribute to determine that module’s position in the package hierarchy. If the module’s name does not contain any package information (e.g. it is set to ‘__main__’) then relative imports are resolved as if the module were a top level module, regardless of where the module is actually located on the file system.

或許我們可以用 tree 來看待這個 import 的過程，在資料結構 tree 當中，同層節點之間是不相連的，每個節點只與父輩與子代相連。要走訪同輩的節點，也需要先走到上一層，再往訪問道目標的同輩節點。相對匯入中的第一個點，不但是告訴電腦「當前的模式是相對匯入!」，也是點出這個樹的根結點 (root) 是「這個檔案的上一層」。有點像是找族譜，兄弟之間是二代血親，當哥哥要計算與弟弟之間是幾等親時，必須先溯源到父親 (一個 dot )，再往下找到弟弟。所以說，相對引入裡面「一個 dot 表示當前位置」可以看做「知道當前的父輩之位置，可以從該父輩往下找到要找到的檔案名稱」

在最標準的起手式`import .pkgName` ，相對路徑的**起點**就是寫這行的**檔案的所在位置**而非 root file 。

- 一個點表示當前包的位置開始引入
- 兩個點表示上級
- 三個點表示上上級

以此類推，舉例說明

```python
package/
    __init__.py
    subpackage1/
        __init__.py # here!
        moduleX.py # here! 
        moduleY.py
    subpackage2/
        __init__.py
        moduleZ.py
    moduleA.py
```

不管在 `subpackage1/moduleX.py` 或 `subpackage1/__init__.py` 中，下面的導入都是有效的(因為他們同級)。

```python
from .moduleY import spam
from .moduleY import spam as ham
from . import moduleY
from ..subpackage1 import moduleY
from ..subpackage2.moduleZ import eggs
from ..moduleA import foo
```

- 絕對匯入可以用

  ```python
  import XXX.YYY
  from XXX import YYY
  ```

- 但相對匯入只能用 `from XXX import YYY`  這種語法。

  ```python
  from .moduleY import spam
  ```

  另一種寫法是禁止的 

  ```python
  import .moduleY # 禁止!!!!!!
  ```

  這是因為寫 `import XXX.YYY.ZZZ` 之後，去除 keyword `import`，`XXX.YYY.ZZZ` 是可使用的(usable)。但是去除 `import` 後`.moduleY` 是一個不可使用的表達方式。

  

### 相對匯入的原則 ([Rationale for Relative Imports](https://www.python.org/dev/peps/pep-0328/#id9))

隨著絕對匯入的作法敲定，出現了一個問題﹔是否該允許相對匯入的存在。相對匯入最大的優點在於：重新編排大型 package 架構時，不需要一個個編輯子模組。此外，沒有相對引入的話在 package 內部的模組無法輕易的 import 自己。也就是說，相鄰的兩個檔案卻需要大老遠從 root 拉路徑過來  import，這種繞遠路的行為十足弔詭。

### 相對匯入的缺點

然而，使用相對路徑還是有些須注意的地方：

1. 使用了相對路徑的檔案沒辦法直接執行(不能作為 `__main__`)
2. 由於相對路徑變得要計算套件之間的上下層關係來決定 import，**因此 top level 不能低於被匯入的套件**。需要在 import 套件中最高層的位置的**再上一層**，建立呼叫這一整套 package 的 .py 作為直接執行的檔案（他就是 `__main__`）。

某些程度上這種作為變得十足麻煩，想測試套件還需要往上爬一層創立另一個檔案再來 import …. ，甚至有些專案會把相對路徑跟絕對路徑都寫出來：

```python
try: 
    from .where import package 
except:
    from where.package import * 
```

我曾經在 stackoverflow 看到一則討論在說為何用了相對路徑的 python 檔不能執行？這很麻煩。而某位網友說：「使用相對路徑的檔案你應該視為『套件』而非『腳本 (script) 』」。

或許正因為這個原因，比起嫌相對路徑比絕對路徑麻煩，更應該把相對路徑跟絕對路徑本來當作是在不同的場合所使用的…. 這樣的思路來思考吧。

## Reference 

- [理解Python的 relative 和 absolute import](https://carsonwah.github.io/15213187969322.html)