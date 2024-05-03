---
title: Linux 上的 SSH 常用模組與設定
description: 先前在 VS Code 的設定文章中有提及過 SSH 登入的設定，本篇以 Linux 的 SSH 登入開始介紹，並且提及 scp 與 sshfs 方便於多台 Linux 機器之前交換資料的模組。
date: 2022-10-24 21:47:12
categories: Linux
aliases:
- /posts/2022-10-24-linux-ssh
- /posts/2022-10-24-linux-ssh.html
---

先前在 VS Code 的設定文章中有提及過 SSH 登入的設定，本篇以 Linux 的 SSH 登入開始介紹，並且提及 `scp`, `sshfs` 兩個基於 SSH 連線，方便於多台 Linux 機器之前交換資料的模組。

## 使用 SSH 登入

1. 首先，本地 (local) 的電腦需要有 SSH key，

   ```
   ssh-keygen
   ```

   首先它會問 ssh 存放的位置，預設是 `~/.ssh` 下面。密碼如果直接按 Enter 相當取用不需要用密碼，可自行斟酌。

   資料夾中 `id_rsa.pub` 是公鑰、`id_rsa` 是私鑰。

2. 取得遠端 (remote) 電腦的 IP。登入遠端機器之後，使用 `ipconfig` 或 `ifconfig` 通常可以找到，如果兩者都無法，可以用指令 `cat /etc/hosts` 查找。

### 把公鑰放到遠端機器上

先說簡單的方法，使用 `ssh-copy-id`

```
ssh-copy-id <remote id> 
```

會需要輸入一次密碼，指令會把 public key 放到遠端機器上設定好。參考：[ssh-copy-id](https://dywang.csie.cyut.edu.tw/dywang/security/node85.html)。

另一種是手動方法，編號接續前面的 Step

3. 在 Linux 上可用 `nano`, `vim` 之類的文字編輯器，在本地打開 `~/.ssh/id_rsa.pub`，複製內容。

4. 把公鑰 (public key) 放到遠端電腦的  `~/.ssh/authorized_keys` 裡面。

5. 從本地端使用 ssh 連線過去，嘗試是否成功！

   ```bash
   ssh username@IP -p port
   ```

使用 SSH 可以免去每次都要輸入密碼的環節，像是 mobaxterm 這種工具雖然有記住密碼的功能，有鑑於之前曾發生忘記 mobaxterm 密碼的慘劇，讓我後來都改用 SSH 的方式 。當然 `.ssh` 如果有設密碼一樣可能面臨相同的困擾，但 `ssh` 在 linux 上可用的範圍更為廣泛，算是個好處吧。

## 給予遠端 IP 別名

像是在用 docker, kubernetes 一次使用多台機器的時候，如果每一台的 IP 都不同，也不怎麼連續。有時候又會需要登入每一台做些設定，這時如果能給每一台機器的 IP 都設其他代稱，可以方便許多。以下會先說名 ssh 部份的作法，後面提及使用 docker 的經驗！

### 設置 .ssh/config

位置在 `~/.ssh/config` 下，

```bash
Host            remoete_machine 	# 代稱
Hostname        192.168.0.1        	# ip address
Port            22                	
User            jonny                # user name
identityfile    ~/.ssh/id_rsa   	 # private key 位置 
```

這樣下次就可以直接用這邊設定的內容連線！但如果前面在產生 ssh key 的時候有設密碼，則每次連線會需要打那個密碼！

```bash
ssh remoete_machine
```

### 在網域上尋找機器

我曾遇到過需要自己找 IP 的情況....，要在網域上尋找機器，可使用使用 nmap，用法可參考文章最後的參考資料。

```bash
sudo apt install nmap
sudo nmap -sn 192.168.1.1-100
```

### 改變 IP address 的 hostname

這是另外一種作法，在使用 docker 管理多台 Raspberry Pi 時曾用此方法：修改檔案 `/etc/hosts` 。把 IP 位置改成自訂的 hostname，例如：

```
192.168.1.181         docker1
192.168.1.182         docker2
192.168.1.183         docker3
192.168.1.184         docker4
```

其實前面提到的 `ssh-copy-id`，如果在這一部先設好每一個 IP，用腳本跑 `ssh-copy-id` 有機會輕鬆的多。

## scp

透過 SSH 執行 Copy ，`scp` 之後第一個位置是 source、第二個位置是 destination

```bash
# local to remote 
scp <local path> user@192.168.0.1:<remote path>
# remote to local
scp user@192.168.0.1:<remote path> <local path>
```

複製目錄也跟原始的 `cp` 相似，加上 `-r` 參數：

```bash
scp -r user@192.168.0.1:<remote path> <local path>
```

要從同台機器上，複製多個資料夾的內容，則在冒號後面把路徑寫在一起：

```bash
# 正確作法
scp -r user@192.168.0.1:"dir1 dir2 dir3" <local path>

# 會複製兩次! （如果有設密碼就要打兩次）
scp -r user@192.168.0.1:dir1 user@192.168.0.1:dir2 <local path>
```

## sshfs

需要注意，如果不是 root 用戶，本地位置**目錄**的**擁有者**必須為使用者自己（不能把檔案從遠端 copy 到這台電腦中，別的 user 所屬的資料夾的概念）。如果遠端機器的 ssh port 不是預設的 22 （是透過 router 設定 port forwarding 之類的），要透過 `-p <port>` 標明連哪個 port，否則會連線不進去。

```bash
sshfs <remote location> <local location>
sshfs username@hostname:/path/to/folder /path/to/local/folder
sshfs -p <remote port> username@hostname:/path/to/folder /path/to/local/folder
# example
sshfs -p 1000 pi@0.0.0.100:/share_files /accept_file
```

這個舉動的意思是：把遠端機器(`0.0.0.100`) 上的 `share_files` 資料夾『掛載 (mount)』到我的機器上的 `accept_file` 資料夾！因為是用 mount 的，所以當遠端機器的 `share_files` 內容有更新，我這邊的 `accept_file` 也會同步更新！

而如果希望解除綁定資料夾的狀態，可以參考下面連結的論壇，用 `fusermount -u /path/to/local/folder` 解除本地資料夾與遠端的連結。

## 參考資料

- [Configuring an SSH login without password](https://www.ibm.com/support/pages/configuring-ssh-login-without-password)

- [Nmap 網路診斷工具基本使用技巧與教學](https://blog.gtwang.org/linux/nmap-command-examples-tutorials/)

- [介紹好用工具： SSH Filesystem (簡單好用的 SSH 檔案系統)](https://blog.miniasp.com/post/2013/11/30/Useful-tool-SSHFS-SSH-Filesystem)

- [How to Run a Raspberry Pi Cluster with Docker Swarm](https://howchoo.com/g/njy4zdm3mwy/how-to-run-a-raspberry-pi-cluster-with-docker-swarm)

- [Linux 的 scp 指令用法教學與範例：遠端加密複製檔案與目錄](https://blog.gtwang.org/linux/linux-scp-command-tutorial-examples/)

- [介紹好用工具： SSH Filesystem (簡單好用的 SSH 檔案系統)](https://blog.miniasp.com/post/2013/11/30/Useful-tool-SSHFS-SSH-Filesystem)
- [How to copy files from one machine to another using ssh](https://unix.stackexchange.com/questions/106480/how-to-copy-files-from-one-machine-to-another-using-ssh#answer-106485)
- [[Linux] 在 CentOS 上使用 sshfs 來掛載 SSH server 上的檔案系統](https://ephrain.net/linux-%E5%9C%A8-centos-%E4%B8%8A%E4%BD%BF%E7%94%A8-sshfs-%E4%BE%86%E6%8E%9B%E8%BC%89-ssh-server-%E4%B8%8A%E7%9A%84%E6%AA%94%E6%A1%88%E7%B3%BB%E7%B5%B1/)



