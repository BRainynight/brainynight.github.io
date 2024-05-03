---
title: Python 日誌模組 Logging (2) 細探官方文件
date: 2022-01-22 16:41:38
categories: Python
description: logging 模組第二篇，有關過濾特定內容、將日誌內容輸出到特定的目的地、日誌格式可調用哪些系統參數等，模組中四個常見物件的使用方式。
aliases:
- /posts/2022-01-22-python-logging-advance
---

Logging 模組中主要就是這四種物件：

- Loggers : 提供直接讓其他應用程式使用的接口 (expose the interface that application code directly uses)
- Handlers : 發送日誌紀錄到適合的目標地點，像是檔案、stdout、甚至 Qt GUI 等等。
- Formatters : 輸出的格式。
- Filters : 過濾器，決定哪些日誌訊息可以傳到輸出。

## [Loggers](https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial)

logger 負責三個工作

1. 暴露一些方法讓應用程式去調用，在執行期間(runtime) 中紀錄訊息。
2. 根據嚴重性或 filter 物件，決定讓那些訊息要傳遞出去。
   - 預設的過濾條件就是根據嚴重性(severity)
3. 將相關的日誌訊息傳遞到相關的 log handlers 手上。

### 常用的方法

* `Logger.setLevel()` : 設定嚴重性的 threshold 。
* `Logger.addHandler()` , `Logger.removeHandler()` : 新增或移除 handler.
* `Logger.addFilter()` ,`Logger.removeFilter()` : 新增或移除 Filter，

每當 logger 物件被創建時，下面的函數會自動配置產生：

* `Logger.debug()`, `Logger.info()`, `Logger.warning()`, `Logger.error()`, `Logger.critical() `：括號裡面填寫要傳入的日誌訊息， **必須是 string 形式**，剩下的一些參數可以透過 `**kwargs` 傳入 (ex. `exc_info`... )

  - 當紀錄的訊息是從 print 轉過來的時候要注意，所有的訊息要寫在同一條 string 裡面：

    ```python
    print(f"var1={var1}", f"var2={var2}")
    logger.info(f"var1={var1}; var2={var2}")
    ```

    如果像 print 一樣兩個 string 放不同位置，第二個位置的字串會被當作其他參數，必須要改成只有一條 string。

* `Logger.exception() ` : 一個很像 `Logger.error()` 模式的 logger 方法，不同的是它會**追蹤例外發生的紀錄(traceback)** (dumps a stack trace along with it)，這只應該在例外處理中 (exception handler) 使用。

* `Logger.log(level:int, msg: str)` : 除非是用到 **自訂的訊息等級** ，它的效果跟第一點的一樣，但是更加的冗長，沒事可以不要用。

### 注意事項

1. `getLogger()` 回傳的是「和輸入名稱相同的 logger 實例的 reference」，如果沒有指定，則回傳 logger實例名字為 `root` reference。

2. 名稱如之前所提，有上下的層級架構關係

3. 用相同的名稱 呼叫 [`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger) 得到的是 reference :arrow_right: 都參考至相同物件名稱的 logger 物件。

   ```python
   logger1 = logging.get_logger("aaa")
   logger2 = logging.get_logger("aaa") 
   id(logger1)==id(logger2) # True
   
   # 兩條呼叫到的會是同一個 logger 物件：名為 'aaa' 的 logger object. 
   ```

4. 嚴重性等級的定義：Logger 能接受的訊息等級受到其父代所影響

   1. 如果自己的等級沒有另外定義，會使用父代所定義的訊息嚴重性等級。
   2. 如果父代沒有定義，會再往上使用「父代的父代」，往上追朔祖先直到有找到清楚的等級定義 (explicitly set level )
   3. root logger 必然會有一個很清楚的等級定義 (預設是 `warning`) 

5. Logger 所定義能通過的訊息等級，會影響到是否能傳遞到旗下的 handler：

   - 如果在 logger 上定義通過 warning (30)，卻在 handler 定義等級 info (20) 就能紀錄，那這樣實際紀錄下來的也只會有 warning 以上的訊息，因為低於 warning 的根本進不來這個 logger 的手上。

6. 不需要為每個logger 都定義 handler，只要對 root logger 做。

   - 由於 child logger 的訊息會往上傳遞，所以只需要在上層的 logger 設置即可。
   - 但是也可以把往上傳遞的功能關掉：參數 `propagate=False` 

## [Handlers](https://docs.python.org/3/howto/logging.html#handlers)

Handler 物件基於所設定的訊息嚴重等級，將日誌訊息派到**對應的目的地**，像是 stdout。Logger 物件對於 handler 的數量沒什麼限制，可以不加、也可以加很多個。光是官方提供的 handler 就多達 10 個以上，常見的輸出到 std out、輸出到檔案、連接到 Socket、傳遞到 http (`Get`, `POST`)、送到 `Queue`...等等。我也實做過把 logger 直接連動到 Qt GUI 的文字板上面過，不用另外從核心程式拉一條線到前端的 GUI，直接利用現有的 logger 即可非常方便！


Handler 幾乎沒什麼方法可以調用，與其相關的主要是這幾個方法：

- `Logger.addHandler(hdlr)`
  - 舉例說明：目標是 (1) 將所有 log 寫進 log file  (2) 所有高於 error 的 msg 丟到 `stdout` (3)所有 critical 等級的寄信寄出去。一共 3個獨立的 handler 負責做各自的事情。所以需要添加三個不同的 handlers，呼應各自要寄送訊息的目的，還有寄送出去的信息等級。
  - 標準的library 有提供 [很多 handlers](https://docs.python.org/3/howto/logging.html#useful-handlers)，最常用的是 [`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler) 和[`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler)。
- `setLevel `：handler 也有 `setLevel()` 方法，和前面的 `setLevel` 不同

  - `logger.setLevel()` 設定的是哪些嚴重性的訊息可以**被傳送到** handlers，而 `handler.setLevel()`則是決定哪些程度的訊息**可以被派遣到要目的地 (ex. write to file )**
- `setFormatter()`：設定 handler 把訊息傳到目的地時候的訊息格式。
- `addFilter()` and `removeFilter()`：配置和移除 filter 於handler 物件。

## [Formatters](https://docs.python.org/3/howto/logging.html#formatters)

決定訊息的格式，有三個可選擇擇的參數：

1. 訊息字串格式字串 `fmt`：可調用的一些屬性變數參見 [LogRecord attributes](https://docs.python.org/3.7/library/logging.html#logrecord-attributes)
2. 日期格式字串 `datefmt`: 預設使用  [`time.localtime()`](https://docs.python.org/3/library/time.html#time.localtime) 打下時間戳，預設的格式為 `%Y-%m-%d %H:%M:%S`
3. style indicator：撰寫模式的提取符號，預設是 `%`，可修改成 `{` 或 `$`。參考不同的 style-indicator 所對應的 formatter 撰寫模式：
	```python
	logging.Formatter('%(asctime)s - %(message)s', style='%')
	logging.Formatter('$(asctime)s - $(message)s', style='$')
	logging.Formatter('{asctime} - {message}', style='{')
	```

最後舉個例子：

```python
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
```

- `message`：應用程式傳入的日誌訊息
- `asctime`, `name`, `levelname`： [LogRecord attributes](https://docs.python.org/3.7/library/logging.html#logrecord-attributes) 中所提供可以調用的屬性，分別表示時間、哪個 logger (名稱) 傳入的、訊息等級名稱。

## [Filters](https://docs.python.org/3/library/logging.html#filter-objects)

- 用在 handler 和 logger 上，提供比「訊息緊急程度層級」更細節的過濾規則

- 最基本，不用實做改寫的 filter，提供以「logger 階層等級」過濾的方法：只能通過**低於自己的層級**。例如 : 設定`A.B` ，則只會通過 logger `A.B`, `A.B.C`, `A.B.D`…

  ```python
  f = logging.Filter(name="A.B")
  ```

  代表 "A.B" 以下(包含)層級的 logger 事件訊息可以通過這個過濾器。

- 如果以空白字串初始化，則所有的事件都可以通過。

- Filter 必須在 log 事件已經被傳送到 handler 前先附加在 handler 上面，才能起過濾的作用。(反正就是一開始先設定好就對了 = = )

預設功能只是基本的，也可以自己設計規則來決定哪些訊息可以通過。想自訂過濾器要做的事情是：

1. 實作一個 `logging.Filter` 類別，並實作其 `filter` 方法
2. 把這個客製化 filter 實例化後，用 `.addFilter()` 加到 logger 或 handler 

```python
# 稍微用code表示上面的條列項目
import logging

class CustomFilter(logging.Filter):
    def filter(self, record):
        # 實作過濾規則 
        return True # 要 return True 才代表信息被保留

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
f = CustomFilter()logger.addFilter(f)
```

舉例而言，一個過濾敏感資料的自定義 Filter 範例 https://gist.github.com/acdha/9238791