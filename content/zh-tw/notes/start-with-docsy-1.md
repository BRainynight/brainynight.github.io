---
title: 從零開始 Docsy (1)
date: 2024-05-03 12:05:00
description: "啟動一個 docsy 主題的 hugo 網站"
---
## 開始之前

使用主題有[多種方式](https://www.docsy.dev/docs/get-started/#installation-options)，官方最建議使用 Hugo Module 加載主題。

本文將參考 [docsy-example](https://github.com/google/docsy-example)，嘗試用最少的設定從頭創建一個 docsy theme 的網站。

### 版本資訊
使用 docsy\@v1.0，hugo version 和 go version 分別為
```
go version go1.20.2 windows/amd64
hugo v0.119.0+extended windows/amd64 BuildDate=unknown
```
注意 hugo 對 go 的版本有要求，錯誤的版本將無法執行 hugo command。


## 初始化 Hugo Module 
嘗試從空白開始
```bash
mkdir customize-docsy
cd customize-docsy
hugo mod customize-docsy
# go.mod is generated 
```

這時資料夾中會有一個 `go.mod` 的檔案，內容如下: 
```go
module customize-docsy

go 1.21.9
```

## 設置 hugo.yaml
import 的部分參考 docsy-example 創建一個檔案 `hugo.yaml`，內容如下: 
```yaml
module:
  # uncomment line below for temporary local development of module
  # replacements: "github.com/google/docsy -> ../../docsy"
  proxy: "direct"
  hugoVersion:
    extended: true
    min: "v0.119.0+extended"
  imports:
    - path: "github.com/google/docsy"
      disable: false
    - path: "github.com/google/docsy/dependencies"
      disable: false

```

### Replacement 
如果想把 module 導向 local 的位置，可以使用 replacements。有兩種方式，一種是寫在 go.mod，一種是寫在 hugo.yaml 
#### [go.mod](https://gohugo.io/hugo-modules/use-modules/#make-and-test-changes-in-a-module)

```go
replace github.com/bep/hugotestmods/mypartials => /Users/bep/hugotestmods/mypartials
```

#### [hugo.yaml ](https://gohugo.io/hugo-modules/configuration/#module-configuration-top-level)
如同範例中的註解寫到，如果想把 "github.com/google/docsy" 導向 local 的 docsy，就把該行 unconmment: 

```yaml
replacements: "github.com/google/docsy -> ../../docsy"
```

## 下載相關模組並執行
```go
hugo mod graph
hugo server 
```
前往 "localhost:1313"，因為是從頭創建，目前是一片空白。至此，已經成功套用主題，並且啟動 server。
