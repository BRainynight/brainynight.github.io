---
title: VSCode 的環境設置
description: 到一個新環境必做的基本設置，如何連線到遠端機器等。
date: 2022-06-23 11:52:45
categories: Tool
aliases:
- /posts/2022-06-23-vscode-setting
- /posts/2022-06-23-vscode-setting.html
---
有如 Spyder 的 IPython 互動介面、直接用 VSCode 以 SSH 遠端連線、VSCode 的 anaconda 切換問題等等，有些可能按照 Reference 的做法就成功了，有些會加一些自己的嘗試，所有個人經歷過的問題都記錄在本文中! 
<!--more-->

## Vscode 中的 Anaconda 虛擬環境切換問題

[VScode中Anaconda虚拟环境切换的问题（Python+Jupyter）](https://blog.csdn.net/Ocean_waver/article/details/108306791)

### 情況

即便執行時已經改使用虛擬環境的 python.exe ，但是執行命令時仍常常失敗: 「找不到指定的模組」

### 解決

原因是 Vscode使用的是 powershell 模式，而不是 cmd模式。

透過在預設的 setting.json (`C://User//XXX/AppData/Roaming/Code/User/setting.json`)中，添加指定的終端機執行模式：改指向 cmd.exe

```bash
"terminal.integrated.shell.windows": "C:\\Windows\\System32\\cmd.exe",
```

## 在 terminal 中使用 iPython kernel

請先看看 [Interactive Mode](#使用-Vscode-預設的-Interactive-mode) 是不是更貼近需求！這兩者的設定上可能會有衝突

這邊指的是像 spyder 那樣，可以在側邊欄位 key 東西，而不是像 Jupyter 那樣一個個 block。

### 需求

1. 基本的需要有 python 程式，IPython (pip install)
2. vscode 除了Python 插件，還要額外安裝 multi-command 插件 (支援多步驟的命令)

### 設定檔

1. `setting.json`

   ```json
   "python.terminal.launchArgs": ["-m", "IPython", "--no-autoindent"],     
   "multiCommand.commands": [
       {
           "command": "multiCommand.executeIPython",
           "sequence": [
               "python.execSelectionInTerminal",
               "workbench.action.terminal.focus",
               "workbench.action.terminal.scrollToBottom",
               {"command": "workbench.action.terminal.sendSequence",
                "args": { "text": "\u000D" }},
               "workbench.action.focusActiveEditorGroup"
           ]
       },
   ]
   ```

2. `keybindings.json`

   ```json
   {
   "key": "shift+enter", 
   "command": "multiCommand.executeIPython",
   "when": "editorTextFocus && python.datascience.featureenabled && python.datascience.ownsSelection && !findInputFocussed && !notebookEditorFocused && !replaceInputFocussed && editorLangId == 'python'" 
   },
   ```

### 參考

- [Use IPython REPL in VS Code](https://stackoverflow.com/questions/52310689/use-ipython-repl-in-vs-code/52324509#answer-59485636)
- [Python の 在 VSCode 中使用 IPython Kernel 的方法](https://codingnote.cc/zh-tw/p/191622/)

## SSH Remote setting

- [使用 Visual Studio Code 透過 SSH 進行遠端程式開發](https://xenby.com/b/221-%E6%95%99%E5%AD%B8-%E4%BD%BF%E7%94%A8-visual-studio-code-%E9%80%8F%E9%81%8E-ssh-%E9%80%B2%E8%A1%8C%E9%81%A0%E7%AB%AF%E7%A8%8B%E5%BC%8F%E9%96%8B%E7%99%BC)：現在一般的公開版就可以找到這個模組了！

1. 在 vscode 中下載模組：Remote Development （現在在一般版也可以下載了）
2. 輸入要連線的伺服器：`account@IP -p port`，確認後 enter
3. 會出現一個下拉式選單，列出一些 config 的位置，意思是要把這個 ssh 連線的設定存到哪個 config 裡面。反之，要調整已經紀錄的連線內容，也是在這個 config 裡面。選取要儲存的檔案 (我存在 `C:\User\user\.ssh\config`)
4. 再一次連線
5. 輸入密碼
6. 等待遠端完成一些同步的下載，當左下角顯示的是你的遠端IP，就代表連線成功了

### Find IP 

嘗試 `ifconfig`, `ipconfig` 或 `cat /etc/hosts` 查看! 

###  意外

通常應該是按照[官方教學](https://code.visualstudio.com/docs/remote/ssh) 就可以了，但是我剛才出現了

```
[11:32:55.138] Resolver error: Error: XHR failed at XMLHttpRequest.s.onerror (file:///C:/Program Files/Microsoft VS Code/resources/app/out/vs/workbench/workbench.desktop.main.js:462:158)
```

參考了[How can I install vscode-server in linux offline](https://stackoverflow.com/questions/56671520/how-can-i-install-vscode-server-in-linux-offline)

在 code-server 資料夾下多放一個檔案

```
touch ~/.vscode-server/bin/${commit_id}/0
```

再重新從 vscode 連一次 ssh 進去，就成功拉!

**參考** : 過程中調查到這個網站，或許會有幫助，但沒有實驗 https://github.com/cdr/code-server

## SSH Remote key

- [使用VSCode Remote透過 SSH 進行遠端開發](https://hackmd.io/@brick9450/vscode-remote) ：用其他模組記住密碼
- [如何使用 SSH 遠端連線？](https://www.maxlist.xyz/2020/03/14/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-ssh-%E9%81%A0%E7%AB%AF%E9%80%A3%E7%B7%9A%EF%BC%9F/)：使用 ssh 連線，不用輸入密碼就能登入遠端裝置

但每次登入的時候都要輸入密碼，改用 SSH 可以免除每次都要 key 密碼！

1. 在自己（local）電腦：`ssh-keygen`，直接按 enter 就是產生在預設的資料夾，不使用密碼。
2. 資料夾中，`id_rsa.pub` 是公鑰、`id_rsa` 是私鑰。
3. 用 wordpad 之類的編輯器開啟公鑰，複製。
4. 把公鑰放到遠端電腦的 `~/.ssh/authorized_keys` 檔案裡面：
   A. 使用 Vim 修改
   - 在遠端電腦上輸入 `vim ~/.ssh/authorized_keys`
   - 貼上公鑰
   - 按 `:wq` 儲存並離開
   B. 或者，vim 太難用了，不如改用 vscode 吧! 
   - 在遠端電腦上輸入 `code ~/.ssh/authorized_keys`
   - 貼上公鑰、儲存、離開! 
5. 再一次用 vscode 登入遠端連線，應該可以不用 key 密碼了！

## Port forwarding

如果使用遠端作為 Server，其local host 在遠端機器上，沒辦法從本地取得。這時候需要使用到 port 的映射。以 Docker 的官方新手教學為例: 我嘗試在遠端機器 tx2 上建立了一個網頁伺服器: `localhost:3000`，但在我的電腦上無法取得這個網頁。

於是，在左邊欄位的「連接阜」直接打`3000`，然後在本地的 web 打開 `localhost:3000`，就能連線上去了! 或是如果滑鼠放在在 vscode 「連接阜」下面的內容的某行上，右邊會出現一個地球，也可以直接點擊連上!

## GUI 也能透過SSH傳送過來

[VSCODE 实现远程GUI，显示plt.plot， 设置x11端口转发](https://blog.csdn.net/zb12138/article/details/107160825)
[vscode + remote x11插件 +xserver 终端实现远程GUI显示](https://www.jianshu.com/p/66875a1f294b)

在 mobaxterm 的時候 `plt.show()`，或是 qt GUI 都能透過 ssh 傳送過來，這是因為 Moba 裡面自帶 Xterm 的關係。

1. 在 Vscode, xterminal 是需要額外使用插件的：
   (1) Remote X11 裝在遠端
   (2) Remote X11 (SSH) 裝在本地
2. 需要把 public key 放到遠端的 `~/.ssh/authorized_keys` 裡面。
3. 本地需要載 Xserver，也可以只是打開 mobaXterm 放在那也行。
4. Vscode 裡面 F1後, 打  Remote X11 : Reconnect Display，有彈出通知表示 OK 就可以了 （我的經驗，不OK是因為沒有把公鑰授權過去）
5. 輸入一些 GUI 的測試指令，看有沒有成功，成功的話會看到一雙眼睛或是一顆時鐘跳出來～！

```
xeyes
xclock
```

## 不讓遠端機器記住歷史指令

- [Linux command history: Choosing what to remember and how](https://www.networkworld.com/article/3256279/linux-command-history-choosing-what-to-remember-and-how.html)
- [iT 邦幫忙鐵人賽 DAY 23~30 整合式終端機](https://taichunmin.idv.tw/blog/2019-10-16-ithelp-ironman-09.html)

在 User 的 `settings.json` 中設定 (`c:User/user/AppData/Roaming/Code/User/settings.json`)

```json
{
    "terminal.integrated.defaultProfile.linux": "",
    "terminal.integrated.shell.linux": [ "export HISTCONTROL=ignorespace" ], // 這行
    "terminal.integrated.inheritEnv": false // 這是 vscode 建議如果有啟用 conda 的話設定 false.
}
```

## Terminal 突然字母都變成全形

https://github.com/microsoft/vscode/issues/120004

這是 windows 大小突然改變的問題，重新縮放可以解決。

## 使用 Vscode 預設的 Interactive mode

看看這個影片 [VSCode's Python Interactive mode is AMAZING!](https://www.youtube.com/watch?v=lwN4-W1WR84) 。只要在 .py 中，某個段落的 code 前面加上 `# %%` ，它就會自動跳出一個 block 

- Run cell : 只執行這個 block 
- Run below : 應該是一路往下所有的 cell 都執行
- Debug cell : 對這個 blog 使用 vscode 的偵錯模組。

沒有安裝 jupyter 套件沒關係，在嘗試執行 block 時它發現沒有 ipykernel 編譯器就會建議你安裝 Jupyter 了，按照建議的安裝即可。但個人覺得比起第二點在 terminal 裡面開 ipython ，jupyter 的連線比較慢，一段時間不碰還會自動斷線，有點麻煩。

## [改主題](https://code.visualstudio.com/docs/getstarted/themes)

這邊要說的是基於某主題，進而更改某些不喜歡的設定。

- `workbench.colorCustomizations` 能改變的是 vscode 框架。導覽 bar、整體背景等等。
  - `"sideBar.background"`: 指的是[左邊檔案總管](https://code.visualstudio.com/api/references/theme-color#editor-groups-tabs)那邊
  - `"editor.findMatchHighlightBackground"` : 所有被搜尋到匹配的文字的底色。
- `"editor.tokenColorCustomizations"` : 管理的是語法的顏色。
  - `"comments"` : 所有註解的顏色。我覺得許多預設主題為註解選擇墨綠色很不清楚，改成紫羅蘭色。


```json
    "workbench.colorTheme": "Default High Contrast", // 當前所選用的主題
    "workbench.colorCustomizations" : {
        "[Default High Contrast]":{            
            "sideBar.background": "#347890", // 其實不建議改成這個顏色, 只是改變顯眼列在這裡
            "editor.findMatchHighlightBackground": "#ffff3f70",
        }
    }, 
    "editor.tokenColorCustomizations":{
        "comments": "#85b4ff",

    }
```

