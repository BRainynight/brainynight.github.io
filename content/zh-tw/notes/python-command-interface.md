---
title: 用 Python 模組寫互動式選單與 CLI
description: 蒐集與互動式選單、command interface 相關的模組，可以根據用途找到適合的套件。
date: 2022-10-23 15:25:39
categories: Python
aliases:
- /posts/2022-10-23-python-command-interface
- /posts/2022-10-23-python-command-interface.html
---

本篇文章是一個蒐集可使用模組的總集，可以根據用途找到適合的套件。


## Argparse

[官方套件](https://docs.python.org/zh-tw/3/howto/argparse.html) `argparse`讓寫 CLI 介面變得非常輕鬆，特別提一下 [`nargs` 選項](https://docs.python.org/3/library/argparse.html#nargs)。

`nargs`: 只要為數字 (int) ，回傳的型態會是一個 list 擁有 `nargs` 個元素，因此 `nargs=1` 會是一個 list 內容只有一個元素。而沒有添加 `nargs` 的話，就不會以 list 的形式回傳。除了整數，還有 `+`, `?`, `*` 三種特殊符號可以選，`*` 表示可接受任意數量的輸入參數，`+` 是至少要輸入一個、可接受輸入更多數量的參數，否則會報警告。`?` 表示可接受 1 個或 0 個參數，其結果不會以清單的形式存下，而是 single item。

`nargs='?'` 很適合用於有時候需要求 user 附加檔案路徑的需求。

```python
import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--boo', nargs='?') # nargs = 1 or 0, 值不會是清單
    parser.add_argument('--aoo', nargs='*') # nargs = 0 ~ N
    parser.add_argument('--coo', nargs='+') # nargs >= 1
    parser.add_argument('--number', nargs=1)
    parser.add_argument('--single')   
	# Positional Argument
    parser.add_argument("flag1", nargs='?') # the first positional argument is `flag1`
    parser.add_argument("flags", nargs='*') # the second ~ N-th positional argument will be collected to `flags`

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    print(args.aoo)     # 2 
    print(args.boo)     # ['1', '2', '3', '4']
    print(args.coo)     # ['5']
    print(args.number)  # ['2']
    print(args.single)  # 1

# python .\example_argprase.py --aoo 1 2 3 4 --boo 2   --number 2 --coo 5 --single 1 aaa bbb ccc
```

`parser` 的回傳值是一個 namespace，可以直接用名字取用值，像是上面數字的例子那樣直接用 `args.number` 對 `args` 這個回傳的 namespace 取值。另外還有[互斥選項](https://docs.python.org/3/library/argparse.html#mutual-exclusion)、[Argument groups](https://docs.python.org/3/library/argparse.html#argument-groups) 等進階的用法。

```python
import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", help="Clean dir", default=False, action="store_true")
    # 互斥組
    group = parser.add_mutually_exclusive_group(help="you can only choose 1")
    group.add_argument("--dessert", help="Get dessert", default=False, action="store_true")
    group.add_argument("--drink", help="Get drink", default=False, action="store_true")
    return parser.parse_args()
```

## [Curses](https://docs.python.org/3/howto/curses.html)

`curses ` 也是一個 Python 官方的套件，可以使用它開發 console base 的 UI。[Real Python: Your Guide to the Python print() Function](https://realpython.com/python-print/#building-console-user-interfaces) 當中有些示例，像是做個貪吃蛇：

![貪吃蛇](https://files.realpython.com/media/snake.a9589582b58a.gif)

最終沒有涉略這個模組，它似乎都是全螢幕式的，沒有辦法只顯示在打完指令下面的位置，與我的目的不合。

## Inquirer

套件 **[inquirer](https://github.com/magmax/python-inquirer)** 不是 Python 原生的模組，是一個基於 inquire.js 想法產生的 Python 專案，主要支援 Unix 平台，在 [inquirer.js](https://github.com/SBoudrias/Inquirer.js) 裡面有比較多圖片說明。開發上，`pip install inquirer`  即可裝好模組。支援

- 問答，要求使用者輸入內容並包含驗證格式。
- 清單，提供選項，User 用鍵盤上下鍵選擇答案
- Check box 

簡單舉個例子! 

```python
import inquirer
import os 

questions = [
  inquirer.List('subdir',
      message="cd to which dir",
      choices= os.listdir(os.getcwd()),
  ),
]
answers = inquirer.prompt(questions)
questions["subdir"] # user 選到的選項值
```

不過在 colab 的環境中，它沒辦法提供方向鍵在 console 上的互動，因此在印完內容後會報 error，但若在一般的 Linux terminal 用起來體驗是很不錯的！
