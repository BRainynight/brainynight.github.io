---
title: Python 日誌模組 Logging (1) 建立一個基礎 logger 模板!
date: 2022-01-20 23:11:51
categories: Python
description: 提供一個快速使用 logger 的 code snippet
aliases:
- /posts/2022-01-20-python-logger-quick
---

在開發 Python 專案時，是否經歷過一種狀況：在測試的時候需要不斷輸出一些資訊以便觀察狀態，但在正式上線之後又不須要這些東西輸入。有可能是不想給使用者看到，也有可能是不斷 print out 會造成某些阻塞。
當開發版與上線版之間在切換時，最樸實無華的作法就是打開程式，一行行的把 Print 註解掉，但這顯然非常的沒有效率。

<!--more-->

Python 的原生套件中有一個名為 `logging` 的模組，在一些較為正式的模組套件包中都不難看到它的蹤影。

本篇文章接下來的內容大多是閱讀 Python 官方文件後的快速整理，希望能將 logging 模組簡單的介紹並上手！細部的設定會放在下一篇文章。建議使用電腦觀看，透過左邊的目錄快速切換！

## 日誌等級的基本認知

預設的 logging 訊息等級一共有五個，其中 **logging 的日誌等級預設是 WARNING(30)** ，因此在預設的情況下，數值小於30的日誌等級不會輸出。

| 等級     | 數值 |
| -------- | ---- |
| DEBUG    | 10   |
| INFO     | 20   |
| WARNING  | 30   |
| ERROR    | 40   |
| CRITICAL | 50   |

## 單一模組：使用 logging 即可

### 直接使用

不設定 handler，也不設定`basicConfig` ，預設是輸出到終端機上(terminal/stdout)。如前面所說，logging 的日誌等級預設是 `WARNING(30)`。因此低於 WARNING 的 INFO 沒有被輸出在 terminal。

```python
import logging
logging.warning('Watch out!')  
logging.info('I told you so') 
```

```
WARNING:root:Watch out!
```

### 寫入日誌檔案 

多數的情況需要儲存、以供事後查看這些紀錄檔案，例如訓練深度學習模型的時候，或是執行一個長時間運行的系統的時候。

```python
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

如此一來將不會有任何輸出，但查看當前的執行目錄會發現 `example.log` 這個檔案裡有寫入日誌訊息。由於`basicConfig` 函式中，設置了等級為 DEBUG等級 (10)，因此三行訊息都有被包含進去。

```
# example.log 內部的長相
DEBUG:root:This message should go to the log file
INFO:root:So should this
WARNING:root:And this, too
```

如果重複執行上面的程式，日誌會不斷的加在`example.log`當前內容的後面，想要每次都直接刷新日誌檔案而不是接續(append)，需要加上參數 `filemode=w` 。

```python
logging.basicConfig(filename='example.log',filemode='w',  level=logging.DEBUG)
```

## 多重模組：使用 logger 

多數情況我們所要面臨的狀況並沒有那麼簡單，專案是具有架構層級的模組，每個檔案都各自使用 logging 險得雜亂無章。後面會仔細介紹設定，這裡先簡單的提供了一個 function 可以直接調用。

它將創建一個 logger，將輸出導向 terminal (stdout)、並自動儲存日誌到檔案。但以下幾點需要注意：

1. 不使用層級：直接使用 `get_logger()`，返回的 logger 不會有層級。`rootName` 參數可自由選擇是否更改，但 child 請設為空

   ```python
   logger = get_logger(rootName="__main__", childName="")
   ```

2. 根據程式的 package 層級自動設定：要把 `childName=__name__`在子程式中打上去！

   ```python
   logger = get_logger(rootName="__main__", childName=__name__)
   ```

3. 自定義層級：同時覆蓋 rootName, child 自己寫層級架構。

   ```python
   get_logger(rootName="parent", childName="child1.child2")
   ```

除了 `rootName` 與 `childName` 兩個參數是會影響到 logger 層級的，其他都是有關 log file 的參數：

- `fileName`：可自訂 log file 的名稱
- `timeFalg`：是否要再檔名後面自動添加當前的時間戳，如此能使 log file 不被覆蓋，因為函式中預設的寫入行為是覆寫(`w`)。
- `log_dir`：log file 所儲存的資料夾，預設會在當前的目錄下創建一個名為 `logs` 的資料夾，並將紀錄都存在裡面。

如果有不只一個 python 檔在跑，且彼此沒有上下層級關係，記得覆寫 rootName，不要讓兩個 logger 同名，否則當其中一份程式碼中跑到新增訊息，輸入的訊息會讓兩個程式的 logger 都接收到，影響到彼此的 output。

```python
import logging, sys, os

def get_logger(rootName="__main__", childName="", fileName="record", timeFlag=True, log_dir="logs"):
    logName = rootName if not childName else  rootName+"."+childName
    print("Your Log name is : ", logName)
    logger = logging.getLogger(logName) 
    logger.setLevel(logging.DEBUG)
    if timeFlag:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%m%d_%H%M%S")
        fileName+="_"+dt_string
        
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    
    fileName = os.path.join(log_dir, fileName)

    if not childName: # 只能在最頂層加，如果每一層都這樣加，每一個 child logger 也會都 print 一行
        # file handler
        fh = logging.FileHandler(fileName+".log",mode='w', encoding='utf-8-sig')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler() # sys.stdout
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        # formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # put filehandler into logger
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
```

### 簡易範例

1.  Root file，執行的時候是 `python xxx.py` 的那個 `xxx.py` 的檔案中應該這樣調用 logger : 

    ```python
    logger = get_logger(rootName=__name__)
    ```

2.  Child file，被 `xxx.py` 所調用的模組

    ```python
    logger = get_logger(childName=__name__)  
    ```

不管是哪個檔案，使用 logger 的時候都直接按照訊息層級的嚴重性，正常使用即可: 

```python
logger.debug("just debug desp")
logger.info("some information")
logger.warning("This is warning, your action may cause some unexpected effect.")
logger.error("something wrong!")
logger.critical("Your code is dead!!")
```

**Hint 1.** 如果覺得預設的 logger 格式太過冗長，可以參考下一章改變範例 code 中的 `formatter` 達成。

**Hint 2.** 如果希望錯誤/例外發生時，可以把 trace 一併寫進去，參考後面的 [紀錄例外的traceback訊息](#紀錄例外的traceback訊息)。 

### 層級架構說明

程式中的說明文字，具體範例如下:

#### 狀況1. 都不使用

完全不使用層級的話，大可以所有的檔案都如下: 

```python
logger = get_logger(rootName=__name__)
```

但強烈不建議，如果這樣何必搞 logger，直接用 logging 就好了吧。

#### 狀況2. 根據套件層級自動設定

簡易範例中即示範了此種狀況，這種情況下，**請勿改變 root file 中 logger 的 rootName 屬性**，讓他保留範例中的樣子，也就是 `__name__` (在 main file 中 `__name__ == __main__`) 

#### 狀況3. 手動設定層級名稱

想搞怪? 自己設定層級名稱! 

```python
logger1 = get_logger(rootName="boss")
logger2 = get_logger(rootName="boss", childName="manager")
logger3 = get_logger(rootName="boss", childName="manager.department")
logger4 = get_logger(rootName="boss", childName="manager.department.engineer")
```



## 訊息格式

logging 模組中，使用最原始的表達方式 `%s` 常常是為了向下兼容

```python
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

### 改變訊息的呈現格式

透過`logging.basicConfig` 的 `format` 參數設定 log 的訊息模式，可以動用的變數可以參考[官方網站](https://docs.python.org/3.7/library/logging.html#logrecord-attributes)，羅列了使用者可以動用的各種資訊，像是 function Name, … 各種的。

```python
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')

''' 
DEBUG:This message should appear on the console
INFO:So should this
WARNING:And this, too
'''
# %(levelname)s = DEBUG, INFO, WARNING... 
# %(messages)s = ()裡面的訊息
 
```

## 紀錄例外的traceback訊息

- `logger.exception('any msg')` ：**直接使用 exception層級，會將堆疊訊息寫進去 log 中**。層級為 error 層級
- `exc_info=True` 若想把例外訊息以**其他層級寫入**，可以把此參數調成True。預設為False，不會把堆疊訊息寫入。

```python
import traceback

def main_loop():
    for i in range(10):
        logger.info(f'print {i}')
        if i== 5:
            raise Exception("Break")
try:
    main_loop()
except Exception:
    # 將引發例外的堆疊訊息寫入logger, 甚麼動作都不用下
    logger.exception('') 
    # 堆疊訊息以info的層級寫入
    logger.info('info has exc_info',exc_info=True)
    # 當例外發生時，只會當純的寫入此行，因為 exc_info=False
    logger.warning('warning without exc_info',exc_info=False)
    
    # [Optional] 只將traceback的紀錄寫進指定txt
    traceback.print_exc(file=open('traceback_INFO.txt','w+'))
```

