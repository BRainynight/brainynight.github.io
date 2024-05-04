---
title: Python 非同步處理-Asyncio
description: asyncio, thread 與 multiprocess 適用的情境，與一份 Asyncio 的入門程式範例。
date: 2022-10-23 23:11:36
categories: Python
aliases:
- /posts/2022-10-23-python-asyncio
- /posts/2022-10-23-python-asyncio.html
---

Python 自 3.4 開始支援asyncio，但在談及這個模組包之前，首先要了解

- `multiprocess` 是真正的平行處理，可以同時間執行不同的程序 (on different processor)。
- `thread`, `asyncio` 都只在單一 processor 上，因此多個項目之間實際上同時間只有一個項目能夠運行。對於計算密集的任務，這兩種都無法加速。

以下文章閱讀、摘要自 Real Python 的文章：[Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/#what-is-concurrency)

## Concurrency

> The dictionary definition of concurrency is simultaneous occurrence.

在 Python 中，有這種意義的字眼有很多，thread, process, task... ，細究起來應用的層面又有些微不同。但就比較廣義的敘述上，他們都是「按照順序運行的指令序列」，並不是所謂的「平行處理」。他們的每一個項目，都是由 CPU、或是某一個決策者，決定是否切換到另一個項目。而這個切換的過程，如同把原本正在執行的項目在某個點暫停，切換到另一個項目上，決策者隨時可以再把執行中的項目暫停，切換回原先項目暫停的點，繼續執行（理想上）。

`threading` 採取的是 [pre-emptive multitasking](https://en.wikipedia.org/wiki/Preemption_(computing)#Preemptive_multitasking)，作業系統 (OS) 知道每一條 thread 的存在，並且可以任意的中斷，任意的切換。

`asyncio` 使用的是 [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking)，每一個 task 必須主動告知 OS 自己的任務完成了，釋放自己的執行權力。

### Thread 與 Asyncio 各自的問題

使用 Thread 並不好 debug，且可能面臨 race condition 的問題，為了避免需要花費額外的功夫處理（像是互斥鎖 Mutex），參考： [thread-safe](https://zh.wikipedia.org/zh-tw/%E7%BA%BF%E7%A8%8B%E5%AE%89%E5%85%A8)。

而 Asyncio 採用 cooperative multitasking 這種「互信」原則的協作方法，如果其中有任務不配合，不肯釋出執行權則滿盤皆輸。如果程式中有 bug 導致該任務長時間的佔據 processor，則會把其他任務卡死。

## Parallelism

採用此種方式的模組是 `multiprocessing` ，Python 會創建完全不同的 process，每一條  process 都有著自己的 python interpreter。由於彼此之間是不同的 process，因此 multiprocess program 可以跑在不同的 CPU core 上。

## I/O-bound vs. CPU-bound

想要透過非同步/平行運算加速程式，首先需要了解程式被卡住的瓶頸為何？這就要談及 I/O-bound 與 CPU-bound。

I/O-bound ：程式在「等待外部資源的 input/output」花費了大量的時間，像是等待網路封包與檔案系統。下圖的 Request (紅色區塊) 可以視為「等待外部資源發送 Request」的期間、而藍色方塊才是街收到 Request 後給予對應處理（計算）所花費的時間。大部分的時間都花費在等待上。

如果程式的瓶頸點在於 I/O-bound，Concurrency 的方法可以帶來速度提昇。不管是 `threading `或 `asyncio`，他們只是透過重新分配任務執行的順序，而非採取序列式執行（下圖）的方式，活用等待時 CPU 沒事做的時間。

![IO-Bound](https://files.realpython.com/media/IOBound.4810a888b457.png)



CPU-bound：程式並不需要跟網路有什麼交互，沒有等待外部資源的時間，只有長時間的計算。面對此問題，使用  `threading `或 `asyncio` 都沒有好處，因為他們終究只會使用一個 CPU core，計算任務不能在同一顆 CPU 上面重疊。

![CPU-bound](https://files.realpython.com/media/CPUBound.d2d32cb2626c.png)

如果有多核心，使用 `multiprocessing` 可以讓計算任務「平行執行」以達到加速的目的。

![multiprocessing](https://files.realpython.com/media/CPUMP.69c1a7fad9c4.png)



## 第一份 Asyncio 的程式

### 概念

下面這段程式參考自官方文件的 [Subprocesses](https://docs.python.org/zh-tw/3/library/asyncio-subprocess.html?highlight=create_subprocess_shell#asyncio.create_subprocess_shell) 與 [wait_for](https://docs.python.org/zh-tw/3/library/asyncio-task.html?highlight=wait_for#timeouts)。將會使用 `asyncio` 執行一系列的指令 `cmds`，並設置 timeout，時間到自動把 process 砍掉。

使用 asyncio 最基礎的用法，不外乎繞著 `await`, `async`, `asyncio.run` 幾個關鍵字轉：

- 要花很多時間等待的那行程式，前面加 `await`。
- function 當中如果有使用 `await`，則 function 前面要加 `async`。
- 執行 async function 要透過 `asyncio.run` 執行。

另外，subprocess 中可使用的 timeout，在 asyncio 當中要透過 `wait_for` 執行。



需要注意，這裡 async 的作用是對「等待 subprocess 的 response 」做異步。傳統的 subprocess 要等到 subprocess  結束才能執行下一行，而透過這個方式可以一次丟出多個 subprocess。

### 範例

```python
import asyncio

async def single_process(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    try:
        await asyncio.wait_for(proc.communicate(), timeout=2)
        print(cmd, "complete")
    except asyncio.TimeoutError:
        print(cmd, "timeout")
        
async def run_all(cmds):
    lt = []
    for cmd in cmds:
        lt.append(single_process(cmd))
    await asyncio.gather(*lt)

if __name__ == "__main__":
    cmds = [
        "sleep 1 && echo hello",
        "sleep 1.5",
        "echo world",
        "sleep 500",        
    ]
    asyncio.run(run_all(cmds))
```

## 延伸閱讀

- [asyncio由簡入繁](https://www.ithome.com.tw/voice/138875)：是我相當推崇的一位作者所寫的導讀文章！
- [Python非同步設計：使用Asyncio](https://www.books.com.tw/products/0010867281?sloc=main)：同位作者寫的翻譯書。

- [Multiprocessing VS Threading VS AsyncIO in Python](https://leimao.github.io/blog/Python-Concurrency-High-Level/)
- [Speed comparison using multiprocessing.Process versus subprocess.Popen](https://stackoverflow.com/questions/47689297/speed-comparison-using-multiprocessing-process-versus-subprocess-popen)
- [System Slow? How to See If Linux is Memory, CPU, or IO Bound](https://www.howtogeek.com/devops/is-your-linux-system-memory-cpu-or-io-bound/)
- [Async Python: The Different Forms of Concurrency](http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/)
- [Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/)



