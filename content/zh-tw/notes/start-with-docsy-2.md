---
title: 從零開始 Docsy (2)
date: 2024-05-03 13:07:00
description: "學習使用 Config，用最小的設定了解 docsy"
---

## 學習使用 Config

Config 內容繁雜，參考既有的會比較容易。個人認為 [docsy-example](https://github.com/google/docsy-example) 的 config 不容易參考，下面將提及另一個資源更容易讀。官方列出了[一些範例網站](https://www.docsy.dev/docs/examples/)，可以前往他們的 Github 找 config 參考。這裡提供兩個連結: 
- [Docsy official: Basic Config](https://www.docsy.dev/docs/get-started/basic-configuration/): 官方的文章
- [kubeflow Config](https://github.com/kubeflow/website/blob/master/config.toml): 較簡單，且 config 有分區寫 comment，比官方範例網站更容易讀。

## 簡易 Config
參考自 kubeflow，我設置了較簡易的 config，讓啟動的網站有 Top-level navigation，不再是一片空白。

```yaml
baseURL : "/"
title : "My Site"
description : "This is a site with min settings."

###############################################################################
# Docsy
###############################################################################
enableGitInfo : false
# language settings
contentDir : "content/zh-tw"
defaultContentLanguage : "zh-tw"
# tell Hugo not to include the /en/ element in the URL path for English docs
defaultContentLanguageInSubdir : false
# useful when translating
enableMissingTranslationPlaceholders : true
# disable taxonomies
disableKinds : ["taxonomy"]
# deprecated directories
ignoreFiles : []

###############################################################################
# Hugo - Top-level navigation (horizontal)
###############################################################################

menu:
  main:
    - name: "Notes"
      weight: -102
      pre: "<i class='fas fa-book pr-2'></i>"
      url: "/notes/"
    - name: "Docs"
      weight: -101
      pre: "<i class='fas fa-book pr-2'></i>"
      url: "/docs/"
    - name: "Blogs"
      weight: -100
      pre: "<i class='fas fa-rss pr-2'></i>"
      url: "/blogs/"
    - name: "GitHub"
      weight: -99
      pre: "<i class='fab fa-github pr-2'></i>"
      url: "https://github.com/"
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

`module` 的部分來自前一篇文章。

## 為類別建立類別首頁

現在，local 網站上有 "Event, Docs, Blogs" 幾個 navigation option，但點進去內容卻是 404 。接下來將為各 option 建立該類別的首頁。

首先創建 `contentDir `:

```bash 
mkdir -p content/zh-tw
cd content/zh-tw
```

接著建立 blog 資料夾、創建 `_index.md` 檔案

```bash
mkdir blog 
cd blog
touch _index.md
```


並編輯 `_index.md` 的內容: 

```markdown
---
title: Blog
---
Content here won't show in HTML.
```

再起一次 `hugo server`，blog 的頁面不再是 Not found，而是一片空白。反觀 `docs` 頁面還是404，說明這個 index page 是有效的。

## Layouts
Docsy 會偵測資料夾的名稱，決定套用的 layout。至於支援哪些類別，參考的 [layouts](https://github.com/google/docsy/tree/main/layouts) 。沒有特別列出來的類應該是套用 `_default`。

### blogs
不同的 layout 有不同的特點，在 docsy-example 中，`blog` 下又有兩個資料夾 : "News", "Releases"，文章會列在左邊欄位 (電腦版面)，並且會有 RSS 訂閱按鈕。
注意`blog` layout 的 `_index.md` 內文的部分是不會顯示出來的! 
### docs
Docs layout 沒有 RSS 訂閱按鈕，且 `_index.md` 的內容會顯示在 HTML 上。

### 手動設定套用的 layout
我們也可以在單一 markdown file 中，設置 meta data 指定 type 套用模板。
```
type: blog
```

### 設定整個資料夾套用的類別
每篇文章逐一設置不夠方便，我有一個類別為 "Notes" (content/zh-tw/notes)，但想套用 "docs" layout: 

1. 在 notes 資料夾底下創建 `_index.md`
2. 設置 `_index.md` 內容如下

    ```markdown
    ---
    title: Notes
    description: "Add description here"
    cascade:
    - type: "docs"
    ---
    Some content
    ```

可以嘗試在 content/zh-tw/notes 底下創建其他文章，這些文章將套用 `docs` 的格式!
