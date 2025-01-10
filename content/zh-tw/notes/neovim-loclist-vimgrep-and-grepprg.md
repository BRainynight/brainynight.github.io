---
title: Neovim - Location list, vimgrep 與 grepprg
date: 2024-12-25 13:05:00
description: 說明如何於 vim 當中調用 external search tool
robotsdisallow: true
---

## Quick Fix 與 Location List 

這兩者有非常相似的功能，都支援對列表內容進行跳轉，甚至 command set 也幾乎一樣。最大的不同是
- 每一個 quickfix 擁有獨立且唯一的 ID，在整個 vim session 當中不會改變。
- location list 與特定 window 關聯，一個 location list 只能被關連到一個 window。
也就是說，每個 window 可以各自擁有自己的 location list。

quickfix 常見的應用就是讀 compile error message，透過 `cn`, `cp` 可以輕鬆的在各個 error 之間跳轉，不需要手動打開檔案、找到 error 的那行。另外，`vimgrep` command 也經常是第一次接觸到 quickfix 的起點。

本篇文章將著重於 location list 與搜尋 Pattern 的應用，說明
- 如何使用 `vimgrep` 
- 當搜尋的 Pattern 眾多時，應該使用 external tool 再把結果導向 location list 
- 關於 Neovim Location List 的 Python API. 

在 vim 體系中，quickfix 和 location list 的 command 幾乎都是相對的，location list 的指令就是在 quickfix 指令前加上 `l`。例如: `grep` 與 `lgrep`，`vimgrep` 與 `lvimgrep`。

本篇在提及指令時會以 quickfix 指令名稱為主，因為官方文件也是主要說明 quickfix command，在 location list command 說與哪個 quickfix command 相似。但要記得，應用於 location list 的 command 得進行轉換，否則內容就會跑到 quickfix 了。


## `vimgrep` 與 `lvimgrep`
這兩個 command 分別對應與 quickfix 和 location list，都是搜尋 Pattern，只差在把結果導向 quickfix 或 location list。語法是
```vim
:lvimgrep <PATTERN> <FILE>
```

例如: 使用 `:help location-list` 打開說明頁面，再於當前的 buffer 搜尋 `external`，就會看到有一個 location list window 在頁面底端顯示。

```vim
:lvimgrep neovim % 
```

## Vimgrep 與 grep 
Vim 當中有兩種搜尋 Pattern 的方式: 
- Internal (`vimgrep`)
- External (`grep`)

### Internal Search (`vimgrep`)

- 優點
  - 只要有裝 vim 就能用，不用管相關套件是否有安裝。
  - 搜尋 Pattern 的語法跟用  Vim 搜索模式一樣 (`/` 進行搜尋) ，不需要特別記得其他語法，易於使用。
  - 官網中敘述了這三個優勢，由於我沒有在用多行 Pattern 等功能，對這幾個特點沒有特別有感觸，就不多做說明。
    ```
    - Line separators and encoding are automatically recognized, as if a file is being edited.
    - Uses Vim search patterns. Multi-line patterns can be used.
    - When plugins are enabled: compressed and remote files can be searched. gzip netrw
    ```

- 缺點

  - 當文件大、或搜尋的 Pattern 眾多時，不但不方便，速度也會變慢。

    (當要搜尋多個 Pattern 時要用 `\|` 把多個 Pattern OR 起來 `/PAT1\|PAT2\|....\|PATN/`。如果想試試看，可以拿下面這個指令，一樣在前面的說明頁面上執行。)

    ```vim
    :lvimgrep /internal\|external/ %
    ```


內部搜索的缺點就是優點的代價，要做到上面提到的那些點，Vim 需要把每個文件加載。進而導致當搜索結果很大時，會讓 vim 的速度變慢。我的使用經驗是

- 搜索 Pattern (被 OR 起來的 Pattern) 在 50~100 以下時速度還可以，或許也跟檔案大小有關，自行評估速度可否接受。
- Pattern 超過 100 個以上，則考慮使用外部搜索的功能。

### External Search (`grep`)

如果使用外部搜索，延續前面的例子在當前 buffer (help 頁面)搜尋關鍵字 `external` 

```
:grep external %
```

上面指令執行後，會看到底下有一行文字: 
```
[Quickfix List] :grep -n external quickfix.txt /dev/null                              
```
這就是背後實際執行的 command

<img src="../img/neovim-loclist-vimgrep-and-grepprg/grep_to_search.png" alt="grep-to-search" style="zoom:80%;" />

## 指定 External Search 使用的工具

如果不想使用 `grep`，想要換成 `rg` (ripgrep) ，如此設定即可: 

```
:set grepprg=rg\ --vimgrep\ -uu
```

而若想結合其他 external flow，再把內容寫入 location list，則可以設置 `grepformat` 和 `grepprg` 兩個變數達成: 

```vim
:echo &grepprg
:echo &grepformat
```

- `grepformat` 預設是 `%f:%l:%m, %f:%l%m,%f :%l%m`
- `grepprg` 預設是 `grep -n $* /dev/null`

在 [Vim 中文幫助: quickfix](https://yianwillis.github.io/vimcdoc/doc/quickfix.html#quickfix:~:text=5.4%20%E9%85%8D%E5%90%88%20id%2Dutils%20%E4%BD%BF%E7%94%A8%20%3Agrep%0A%0A%E4%BD%A0%E5%8F%AF%E4%BB%A5%E8%AE%BE%E5%AE%9A%20%3Agrep%20%E6%9D%A5%E4%BD%BF%E7%94%A8%20GNU%20id%2Dutils%3A%20%0A%0A%20%20%20%20%20%20%20%20%3Aset%20grepprg%3Dlid%5C%20%2DRgrep%5C%20%2Ds%0A%20%20%20%20%20%20%20%20%3Aset%20grepformat%3D%25f%3A%25l%3A%25m) 的 5.4 章節，有提及 「 配合 id-utils 使用 :grep」就是一種指定 external search 的用法。由於我自己不需要用到這個工具，接下來會以別的範例說明。


### grepprg 與 grepformat 
這兩個變數在 quickfix 與 location list 之間是共用的

- grepformat 決定 quickfix / location list 怎麼識別需要被讀取的內容，被讀取時怎麼解析檔名、行數、訊息 (message)。
- grepprg 決定執行什麼 command。

現在，我寫一份 Python 程式，搜尋 Vim 說明文件 "quickfix.txt" 當中所有粗體字 ( `*` 之間的文字)，英文字母與數字以外的 char 會被移除。腳本名稱為 `py_script_to_search.py`，完整程式會放在最後面。

這裡要注意，在下 `rg` 指令的時候，要加上 `--vimgrep` 的參數，這樣檔名跟搜尋結果會在同一行，得以直接被 location list 讀取。

寫好腳本之後，到 vim 改變數，這邊 command 跟 腳本都盡量給絕對路徑會比較安全

```vim
:set grepformat^=%f:%l:%c:%m
:set grepprg=/usr/bin/python3\ /<ABS-PATH-TO-SCRIPT>/py_script_to_search.py 
```

接著執行: (對當前的檔案執行該 Python 腳本並加載到 location list )

```
:lgrep %
```

就可以看到 `rg` 的搜尋結果:

<img src="../img/neovim-loclist-vimgrep-and-grepprg/lgrep_with_customized_script.png" alt="lgrep_with_customized_script.png" style="zoom:60%;" />

再按一次 Enter，就能看到 location list 視窗有搜尋結果了。如果不想要每次都要按一次 enter 之後才能進到 location list，可以加 `silent` 

```
:silent lgrep %
```

<img src="../img/neovim-loclist-vimgrep-and-grepprg/silent_lgrep_with_customized_script.png" alt="silent_lgrep_with_customized_script" style="zoom:60%;" />

## Source Code: `py_script_to_search.py`

```python
import re
import argparse
import os 

def find_patterns(text):
    patterns = re.findall(r'\*(\S+)\*', text)
    return patterns

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    found_patterns = find_patterns(content)
    return found_patterns

def add_quote(ss): # to avoid there are space or special symbol recognized by terminal.
    return "'" + ss + "'"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search for patterns between asterisks in a file.')
    parser.add_argument('file', type=str, help='The path to the file to search.')
    args = parser.parse_args()
    pats = main(args.file)


    rg_cmd = "rg" # the command path (which rg)
    rg_opt = "--vimgrep"
    pat_str = ""
    lt = []
    for pat in pats:
        pat = re.sub(r'[^a-zA-Z0-9]', '', pat) 
        if pat == "":
            continue
        lt.append(pat)
    pat_str = "|".join(lt)

    cmd = " ".join([add_quote(rg_cmd), rg_opt, add_quote(pat_str), args.file])
    # print(cmd)
    os.system(cmd)
```



## 資料來源

- [Quickfix](https://neovim.io/doc/user/quickfix.html)
- [Vimgrep Tips and Tricks](https://dev.to/iggredible/vimgrep-tips-and-tricks-54pl)
- [When to use :grep and :vimgrep in vim?](https://vi.stackexchange.com/questions/9212/when-to-use-grep-and-vimgrep-in-vim#:~:text=There%20are%203%20primary%20advantages%20I%20see) 
- [Vim 中文幫助](https://yianwillis.github.io/vimcdoc/doc/quickfix.html#quickfix)

