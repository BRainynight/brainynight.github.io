---
title: Build GDB with Python 3
description: 嘗試編譯內建擁有 Python3 GDB 的試誤經驗！以及讓 C++ STL Container 在 GDB 中有漂亮的排版 (pretty-print)。
date: 2022-12-16 21:05:33
categories: Linux
aliases:
- /posts/2022-12-16-build-gdb
---

GDB 自 7.0 之後支援 Python 3，但需要在 compile 的時候就下指令以 python 3 compile。這篇文章是嘗試編譯內建擁有 Python3 GDB 的試誤經驗，以及讓 C++ STL Container 在 GDB 中有漂亮的排版 (pretty-print) 的設定。

## Build GDB

試圖以 GDB 12.1 + Python3.8 的組合，使用 GCC/G++ 11 編譯。

發生了不少的問題，解決的迷迷糊糊… 以下有一些經驗，僅僅是經驗，我尚不太清楚是否確實有直接的影響。

1. 把 GCC 的 Share library 放到環境變數 `$LD_LIBRARY_PATH` 裡面
2. 如果 Python 是用 apt-get 之類的方式下載，不是自己編譯、或不是從 Python.org 載下來的，有可能會沒有 share library。
   可用 `apt-get` / `yum` 的話分別是下載 `python3-dev`, `python3-devel`，沒有權限使用則自己編譯 Python 吧。
3. 使用 python3.8 以上的版本，要修改 `gdb/configure` (見後文)。
4. 出現找不到 Python shared library 之類的，也可以嘗試把 Python shared library 的路徑放到 `$LD_LIBRARY_PATH`。
5. 有改環境變數或改 bashrc 之類的，建議把整個 terminal 關掉重開，避免有一些設定殘留。
6. 只要有改環境變數或 bashrc 等，務必要重新下 `./configure....` 的指令。如果是改 gdb 安裝包裡面的腳本則不影響，可以直接跑 `make`。
7. 如果 `make` 到一半報錯，但錯誤看起來很莫名其妙，可以直接再下一次 `make`，有機會前後兩次錯誤的輸出不同。但解決第二次的錯誤就順著跑下去了。
8. 如果有很莫名其妙的 `ld` error，可嘗試 `make clean`，把所有的東西殺掉重新跑！



### 修改 `gdb/configure`

在 Python binary 的同個資料夾中 (`which python` 得到 binary 位置)，在編譯 GDB 的時候會用到 python-config 的輸出，只是預設是執行 gdb 裡面的 python-config.py 腳本。然而 Python 3.8 之後，`python-config` 之後對於 share library `-lpython3.8` 的配置 (?) 有些更動，詳情我說不大清楚原理，詳請可看[官方在 Python3.8 發布時的說明](https://docs.python.org/zh-tw/3/whatsnew/3.8.html?highlight=python%20config#debug-build-uses-the-same-abi-as-release-build)。

總之，不做以下改動，很容易發生找不到 share library 的狀況。首先創建一個變數 `custom_python_configure` 指向與 python3 binary 相同資料夾的 python-config，接著修改 `python_includes`, `python_libs`, `python_prefix` 三個變數的取得方式，都使用 `custom_python_configure` 來取得。

```shell
  if test "${python_prog}" != missing; then
    have_python_config=yes
    # fix: 
    custom_python_configure="<path-to-python-location>/bin/python-config --embed"
    python_includes=`${custom_python_configure} --includes`
    # origin: python_includes=`${python_prog} ${srcdir}/python/python-config.py --includes`
    if test $? != 0; then
      have_python_config=failed
      if test "${with_python}" != auto; then
	as_fn_error $? "failure running python-config --includes" "$LINENO" 5
      fi
    fi
    # fix:
    python_libs=`${custom_python_configure} --ldflags`
    # origin: python_libs=`${python_prog} ${srcdir}/python/python-config.py --ldflags`
    if test $? != 0; then
      have_python_config=failed
      if test "${with_python}" != auto; then
	as_fn_error $? "failure running python-config --ldflags" "$LINENO" 5
      fi
    fi
    # fix
    python_prefix=`${custom_python_configure} --exec-prefix`
    # origin: python_prefix=`${python_prog} ${srcdir}/python/python-config.py --exec-prefix`
    if test $? != 0; then
      have_python_config=failed
      if test "${with_python}" != auto; then
	as_fn_error $? "failure running python-config --exec-prefix" "$LINENO" 5
      fi
    fi
  else
```



## Build Python

直接從 python.org 下載（我載 gzip file），Python 3.11 的話我以 GCC 11 編譯，GCC 9.2 會報錯。

```bash
./configure --enable-optimizations \
            --with-ensurepip=install \
            --enable-shared --prefix=<python-location>
```

`--enable-shared` 這個參數會有 Share library 產生，在 `<python-location>/lib/` 底下，`libpython3.8.so` 之類的檔案。

## Pretty Print STL Container

我在 windows 上以 msys 安裝的 gdb 是自帶 python 3 的，並且 `info pretty-printer` 的列表中也都有所有 STL container。但在一些 Linux 電腦上，若無法重新編譯 GDB (沒有權限解決之類的)，透過以下方法可以把 pretty printer 註冊給 GDB。

官網說明在此：[STL Support Tools](https://sourceware.org/gdb/wiki/STLSupport)，它需要透過 `svn` 取得 `libstdc++` 再於 `~/.gdbinit` 設定。如果無法拜訪 `svn`，以下將提供一個解決辦法。

1. 在 Github 上的鏡像倉庫中找到 `libstdc++` 
   - GDB 內建 Python3: https://github.com/gcc-mirror/gcc/tree/master/libstdc%2B%2B-v3/python
   - GDB 內建 Python2: [gdb-pretty-printers](https://github.com/faskiri/gdb-pretty-printers/tree/master/gcc.gnu.org/svn/gcc/trunk/libstdc%2B%2B-v3/python/libstdcxx)
2. 把 `gcc/libstdc++-v3/python/libstdcxx/` 之下的所有檔案下載下來，路徑為 `<yourPath>/libstdcxx`
3. 到 `~/.gdbinit` (Github 路徑中有 Makefile，但我懶得理解，自己手動改)

   ```python
   python
   import sys
   sys.path.append("<yourPath>/libstdcxx")
   from libstdcxx.v6.printers import register_libstdcxx_printers
   # register_libstdcxx_printers(None) # 此行視情況添加
   end
   ```

   `register_libstdcxx_printers(None)` 這行在官網的教學是需要添加，但我添加後打開 gdb 卻出現已經註冊的訊息，若屬於此情況，把這行拿掉即可。
4. 打開 gdb，輸入指令看各 std container 是否已經列在之中

   ```
   info pretty-printer
   ```

## 尋找 Home 路徑

在 Linux 底下通常就是在 `~/.gdbinit`，但在 windows 下因為是透過 msys 裝的..... 可以透過下列指令尋找 Home

```bash
# in GDB
show environment HOME	# show home
shell echo $HOME	    # show home
shell pwd			   # current directory
```



