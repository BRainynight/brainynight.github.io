---
title: Python 資料永久化套件：Pickle (1) 常見的 lambda PicklingError
date: 2022-01-17 19:46:50
categories: Python
description: 研究 Python 官方文件中的 Pickle 模組，探討常發生的 lambda PicklingError 問題。
aliases:
- /posts/2022-01-17-pickle-basic
- /posts/2022-01-17-pickle-basic.html
---

Pickle 是 Python 裡面物件儲存的原生套件，延伸的套件有不少，我個人就慣用 `joblib`。

Pickle 直接翻譯是醃漬的意思，這樣說起來很怪，所以以下我可能會用「打包、存檔」之類的作為他的中文敘述，unpicke 直翻有拆開的意思，大陸那邊會有人稱為酸洗，同樣覺得很怪異，以下可能會用「復原、讀取、解包」之類的詞來敘述。若撰寫的當下覺得替代的中文會使意義變得模糊，則會直接採用原本的 pickle 與 unpickle 作為敘述。

## [什麼物件可以被 Pickle / Unpickle][what can be pickled and unpickled]

- 基本型態的數值：None、布林值、整數、浮點數、複數
- 基本型態的文字類：字串、位元、位元陣列
- 基本的可迭代類型：tuple、list、set、字典(dictionaries)，若其內含物件都是 picklable 物件的化就可以。
- 在 Top Level 被定義的
  - 函式 (function) ，只接受用 `def` 定義的，用 `lambda` 定義的一樣是 Unpicklable。 **[以 name reference 形式儲存]**
  - 類別 **[以 name reference 形式儲存]**
  - 類別的實例：其 `__dict__` 或 `__getstat__()`的回傳必須是 pickable 的。

企圖將 unpickle 物件存下來會引發[`PicklingError`](https://docs.python.org/3/library/pickle.html#pickle.PicklingError) 例外，嘗試 pickle 一個高度遞迴的資料結構可能會超過最高遞迴深度而引發 [`RecursionError`](https://docs.python.org/3/library/exceptions.html#RecursionError)（對於這個問題可以透過設置  [`sys.setrecursionlimit()`](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit) 解決）

## Pickle Function/Class

不管是 Built-in function 或使用者自訂的函式，都是透過 function 自身的完整名稱 (“fully qualified” name reference) 將 function pickle 下來，而不是透過值 pickle。這是為何 lambda 函數沒辦法被 pickle ，因為所有的 lambda 函數的名稱都一樣叫做 `<lambda>`。Python 官方文件的內容如下：

> Note that functions (built-in and user-defined) are pickled by “fully qualified” name reference, not by value. [2](https://docs.python.org/3/library/pickle.html#id8) This means that only the function name is pickled, along with the name of the module the function is defined in. Neither the function’s code, nor any of its function attributes are pickled. Thus the defining module must be importable in the unpickling environment, and the module must contain the named object, otherwise an exception will be raised. [3](https://docs.python.org/3/library/pickle.html#id9)

有關 [PEP 3155][PEP 3155] 的 "fully qualified" name reference 在之後會稍微提到。

```python
def function_example():
    print("Hi")

lambda_example = lambda : print("this is lambda")

In [5]: lambda_example.__name__ # 所有的 lambda 函式名稱都是 lambda 
Out[5]: '<lambda>'

In [6]: function_example.__name__ # function 的名稱是自己的
Out[6]: 'function_example'
```

此外，被 Pickle 的內容實際只有名稱，而沒有程式碼。因此在 Unpickle 的環境如果沒有在對應的位置定義對應的函式，是沒有辦法被 Unpickle 的! 我們可以先嘗試在一個檔案中定義函式並把他存下來：

```python
import pickle 
def bar():
    print("lalalala~~~~")

with open("function.pkl", 'wb') as f:
    pickle.dump(bar, f)
```

然後在一個全新、沒有定義過 `bar` 函式的環境中，試圖將其復原。會發現引發了 `AttributeError`

```python
import pickle 
with open("function.pkl", "rb") as f:
    bar = pickle.load(f)
# AttributeError: Can't get attribute 'bar' on <module '__main__'>
```

類別也一樣，被儲存的實際上只有名稱而沒有程式碼，若在 Unpickle 的環境中沒有定義該類別，一樣會引發 `AttributeError`。

## [Pickle Class Instance](https://docs.python.org/3/library/pickle.html#pickling-class-instances)

與 Function 相同，儲存類別的方式也是透過 named reference 儲存(classes are pickled by named reference)。

雖然 Pickle 可以儲存類別的實例，但實際上他**不會儲存任何的類別程式碼、類別屬性**。準確的來說，他存的是實例的「屬性」，用 Python 來敘述 pickle 的 `dump` 與 `load` 動作如下：

```python
def save(obj):
    return (obj.__class__, obj.__dict__)

def load(cls, attributes):
    obj = cls.__new__(cls)
    obj.__dict__.update(attributes)
    return obj
```

用實際的例子演示一下儲存跟復原的邏輯：

```python
class Foo:
    attr = 'A class attribute'
    def __init__(self, ):
        self.inst_arr = "Instance attribute!"
        self.fake_attr = "This is fake"
        
foo = Foo()
pickled_info = save(foo) # (__main__.Foo, {'inst_arr': 'Instance attribute!'})
recover_foo = load(*pickled_info)
```

如果我們想要復原存下來的實例，程式碼中必須保留該類別的定義，否則會引發錯誤。上面僅僅是用程式說明邏輯，現在實際套用 pickle 套件

```python
import pickle
        
foo = Foo()
with open("test.pkl", "wb") as f:
    pickle.dump(foo, f)

with open("test.pkl", "rb") as f:
    my_foo = pickle.load(f)
print(my_foo.inst_arr)
print(my_foo.attr)
```

但如果用別份程式碼定義把實例從 pkl 中復原，而該份程式碼中沒有類別 `Foo`，就會引發錯誤：

```python
import pickle
with open("test.pkl", "rb") as f:
    my_foo = pickle.load(f)
# AttributeError: Can't get attribute 'Foo' on <module '__main__'>
```

- `pickle.dump` ：記住該實例所使用類別的名字 (named reference)、與其實例屬性
- `pickle.load`：試圖在程式中尋找記住的類別名字，在不初始化的情況(不調用 `__init__`)下，默默的創建一個實例，並對所有的實例屬性套用 `pkl` 中所記憶的數值。

如果 pickle 沒辦法在程式中尋找到該 named reference 就會引發例外，不是定義在 Top Level 的函式、類別會沒有辦法透過 named reference 取得；而所有的 lambda function 都共享同一個 name reference , `<lambda>`，代表在復原的時候根本沒辦法找到存到的是哪個 lambda 函式，所以在試圖 dump 的時候就先被排除了。

```
PicklingError: Can't pickle <function <lambda> at 0x00000213F8790948>: attribute lookup <lambda> on __main__ failed
```

### 刻意的設計

不儲存有關類別的屬性、類別的程式碼是故意的設計，這樣做的好處是：如果在 v1 版本中我們儲存了某個實例，後來發現該實例對應的類別有錯、或是對類別擴增了方法而修改程式變成 v2 版本。我們依然可以在 v2 版本中讀取曾經存下來的實例，即使他是在前面版本 (v1) 中存下來的。

```python
# V1
import pickle 
class Dog:
    def __init__(self, legs):
        self.legs = 4

dog = Dog(6)
with open("test.pkl", 'wb') as f:
    pickle.dump(dog, f)
```

```python
# V2
import pickle 
class Dog:
    def __init__(self, legs):
        self.legs = 4
        
    def voice(self, ):
        print("woof! woof! woof!")

with open('test.pkl', 'rb') as f:
    dog = pickle.load(f)

dog.voice() # can run! 
```

### 永久保存物件的版本

如果們希望這是一個  long-lived 的物件，可以看到不同版本的類別，或許可以考慮在裡面放置版本號碼，以便透過類別的 `__setstate()__` 方法做適當的轉換。(官方文件裡面這樣寫，但我不是很懂要怎麼實踐)

## 改變 Pickle 時的預設行為

Pickle 實例的時候，如果該實例的類別有設定下列方法，會改變 Pickle 時的預設舉動

### 模組方法

#### `object.__getnewargs_ex__()`

在協定2與3中，實踐了此方法的類別可以在 unpickling 的時候將寫在 `__getnewargs_ex__` 的參數傳遞到 `__new__()` 裡面以建構物件。此方法必須回傳一對 tuple：`(args, kwargs)`，其中 `args` 是一個 tuple 包含著位置參數 (positional arguments)、`kwargs` 是一個字典包含關鍵字參數。

#### `object.__getstate__()`

類別可以可以決定屬於它們的實例要如何被打包，如果類別定義了此方法，pickle 時會直接呼叫此方法，用它的回傳作為實例所存下來的內容。而不是一般使用實例 pickle 的預設方式：使用 `__dict__` 作為存下的內容。

#### `object.__setstate__(state)`

若類別有定義此方法，Unpickle 的時候就會將得到的 state 傳入此方法。如果類別有定義此方法，則 state 物件不限定要是字典，因為在復原物件的時候 `__setstate__` 自己有一套規則了！

但如果沒有實踐此方法，被存下來的 state (pickled state) 必須是字典的形式，這樣才能把它指派給新的(復原的) 實例的字典。大概有點像下面這種感覺吧：

```python
saved_pkl = { arg1:val1, arg2:val2... }
new_obj.__dict__ = saved_pkl
```

關於 `__getstate__` 與 `__setstate__` 方法，可以參考  [Handling Stateful Objects](https://docs.python.org/3/library/pickle.html#pickle-state) 有更多資訊。

### 處理擁有狀態的物件 (Handling Stateful Objects)

這個例子將展示如何 modify 類別的 pickle 行為：`TextReader` 類別打開一個文字檔，當 `readline` 被呼叫的時候會回傳行數以及該行內容。如果 `TextReader` 實例被打包，除了文件物件(file object) 之外的屬性都可以被儲存。當實例復原時(unpickle)，檔案會被重新開啟，並且從上次最後讀取的位置繼續。這樣的功能就是透過 `__setstate__()` 和 `__getstate__()` 方法達成的，如果不實做這兩個方法，在嘗試 `dump` 的時候就會引發例外

```
TypeError: cannot serialize '_io.TextIOWrapper' object
```

這個類別在實做的時候做了幾件事：

- `__getstate__()`：先將物件的 `__dict__` 屬性複製，並將沒辦法 pickle 的 IO 物件移除，回傳剩下的屬性字典(state)。
- `__setstate__()`：
  1. 將獲得的 state 更新進入新實例的 `__dict__` 屬性裡面
  2. 根據已經復原的 `self.fileName`屬性，打開文字檔案。
  3. 根據已經復原 `self.lineno` 屬性，將 `file` 的狀態讀到上次結束時的行數（把 file 復原到上次結束的狀態，因為他不能直接被 pickle）
  4. 把已復原的 `file` 指派給實例的 `self.file` 屬性。

如此一來，`TextReader` 的實例雖然實際上並沒有每個屬性都真正被 pickle 下來，但復原的時候卻彷彿回到上次剛結束的狀態繼續，達到儲存實例狀態的目的。

```python
class TextReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.lineno = 0

    def readline(self):
        self.lineno += 1
        line = self.file.readline()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return "%i: %s" % (self.lineno, line)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['file']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        file = open(self.filename)
        for _ in range(self.lineno):
            file.readline()
        self.file = file
```

```python
reader = TextReader("hello.txt")
reader.readline()
reader.readline()

new_reader = pickle.loads(pickle.dumps(reader))
new_reader.readline()
```





[what can be pickled and unpickled]:<https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled>
[PEP 3155]:<https://www.python.org/dev/peps/pep-3155/> "Qualified name for classes and functions"