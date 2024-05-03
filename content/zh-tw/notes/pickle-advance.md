---
title: Python 資料永久化套件：Pickle (2) 裝飾器可以被 Pickle?
date: 2022-01-17 20:56:22
categories: Python
description: 繼前一篇文章進一步探討 Pickle 模組：理解 PEP3155談論到的 Qualified name、與帶有裝飾器(decorator) 的函式遇到 Can't pickle local object 應如何解決。
aliases:
- /posts/2022-01-17-pickle-advance
---

## PEP 3155 Qualified name

有關 Fully Qualified Name 的部份我是第一次看到...，嘗試閱讀 PEP 內容，不是很確定閱讀理解是否正確，若有錯誤歡迎指教！

這個 PEP 議題是添加一個 `__qualname__` 屬性在函式跟類別中。對於 Top-Level 的函式與類別，這個屬性等同於 `__name__`，而對於巢狀的類別跟巢狀函式，`__qualname__` 屬性 dotted name 呈現，代表從 Top-Level 算起，該物件的層級位置。`repr()` 跟 `str()` 作用於類別與函式上時，也被修改成使用 `__qualname__`  而非 `__name__`。

dotted name 表示從一個模組的 global 區域到該類別、函式或方法的路徑。

```python
class C:
    class D:
        def meth(self):
            pass

In [2]: C.__qualname__
Out[2]: 'C'

In [3]: C.D.__qualname__
Out[3]: 'C.D'

In [4]: C.D.__name__
Out[4]: 'D'
    
In [5]: C.D.meth.__qualname__
Out[5]: 'C.D.meth'
```

而且對於被 `import` 的模組是不存在 `__qualname__` 屬性的，他們只有 `__name__`屬性，表達的是他的 Fully Qualified Name：該模組到其頂層父模組之間的層級關係：

```python
import email.mime.text
email.mime.text.__name__
```



## 情境探討: 有裝飾器的函式無法被 Pickle

問題來源[自此網站](https://blog.csdn.net/qq_39314099/article/details/83822593)，我們可以嘗試用閱讀完官方文件後的邏輯來解釋這個問題。因為覺得程式繁瑣，所以大概照著意思稍微改寫了一下，博主寫了一個名為 `haha` 的函式，會印出 `hello XXX`，並為它添加了計時裝飾器。雖然沒有明確的說怎麼存檔出了錯，但根據引發的 Error 我大致假設是嘗試存 `haha` 這個函式。

```python
import time, pickle
from functools import wraps

def timer(mth, *args,**kwargs):    
    # @wraps(mth)
    def wrapper(*args,**kwargs):
        st = time.time()
        res = mth(*args,**kwargs)
        et = time.time()
        print(f"Spend {float(et-st)} sec.")
        return res
    return wrapper

@timer
def haha(name=None):
    print(f"Hello {name}")

with open("function.pkl", 'wb') as f:
    print("name of haha function is:", haha)
    pickle.dump(haha, f)
```

在試圖存下這個函式時發生了問題：`AttributeError: Can't pickle local object 'timer.<locals>.wrapper'`。而樓主表示只要給裝飾器裡面裝上 `warp`，問題就解決了。`warp`應該擺放的位置已經寫在程式裡面了，可以試著註解與取消註解看看函式的名稱的不同。

- 沒有 `warp` 的情況：`<function timer.<locals>.wrapper at 0x000001EBECA588B8>`
- 有 `warp` 的情況：`<function haha at 0x000001BF76B188B8>`

所以追根究底，這個問題的癥結點在於包上裝飾器後，若沒有使用 `functools.wraps` 讓裝飾後的函式名稱仍保持原樣，該函式的名稱會變成裝飾器內部函式 `wrapper` 的名稱。而由於 `wrapper` 不是一個 top-level 的函式，而是隸屬 `timer` 函式下的 `<locals>`，因此 Pickle 在試圖存取時直接因為名稱不符合 Pickable 原則而引發了錯誤。

而且決方法僅僅是讓裝飾後的函式保留原本的名稱，一樣叫做 `haha`，Pickle 發現這個名稱存在於 Top-Level 就把他記下來。但實際上他記得的也只有名稱，Unpickle 的時候如果沒有保留定義 `haha` 的函式、或是 `haha` 的內容和 Pickle 時不一樣，執行起來仍會是不同的內容！

## 個人見解

Pickle 是刻意設計不儲存程式碼，對函式與類別都以 name reference 的方式保存的。因此想要透過 pickle 來「永久的」存下函式與類別是不可能的，乍聽起來很不方便。但換個角度或許該想的是：

- 什麼東西是應該被永久保存的呢？應該是資料。

- 資料應該以何種形式存在呢？應該是實例。

- 所以函式、類別是什麼？我想是一個流程、或是一個抽象的敘述。

  理論上，如果有一些變動性的、Runtime 才決定的資料也應該是外部傳入，如果是內部所需要的資料也跟外界無關，作為 local 變數定義在程式碼中就好。

這樣思考起來，好像也能夠明白為何函式與類別不會把程式碼存下來。

但如果，需要函式有一點「記憶力」呢？例如，在執行 Min-max 正規化時，希望函式能夠記住第一次正規化的上下界屬性，後面都直接帶入就好，不用每次都傳入上下界；或是希望把這組正規化參數記下來，但不希望是把 min ＆ max 倆組分別記下來、怕資訊太零散。

這種時候，或許可以考慮使用 Callable Object。定義一個 Class 並實踐 `__call__` 方法，把正規化行為定義在裡面，而需要記憶的屬性紀錄在實例裡面，像是 `self.mins`, `self.maxs`… ，在儲存的時候直接把這個 normalizer 存下來即可。

```python
def norm(arr, mins, maxs):
    return (arr-mins)/(maxs-mins)

class Normalizer:
    def __init__(self, mins, maxs):
        self.mins = mins 
        self.maxs = maxs 
        
    def __call__(self, arr):
        return (arr-self.mins)/(self.maxs-self.mins)
        
# in some main process.... 
if __name__=="__main__":
    for data in datalist:
        mins, maxs = data.min(), data.max()
        data = norm(data, mins, maxs)
        
        # 1. 透過 function 達成
        normalizer = lambda arr: norm(arr, mins, maxs)
        def normalizer(arr): # OR do this... 
            return norm(arr, mins, maxs)
        validation_data = normalizer(validation_data)
        
        joblib.dump(normalizer, "normalizer.pkl") # 決對會出錯.. 
        
        # 2. 透過 callable object 達成 
        normalizer = Normalizer(mins, maxs)
        data = normalizer(data)
        validation_data = normalizer(validation_data)
        joblib.dump(normalizer, "normalizer.pkl")     
```

