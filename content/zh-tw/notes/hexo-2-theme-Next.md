---
title: Hexo Blog 客製化 - Next 主題更新與 PrismJs 啟用
date: 2022-01-26 13:33:05
tags: [hexo]
description: 更新 Next 主題與啟用 prismjs，並修改行中程式碼(inline code) 的 CSS 格式。
aliases: 
- /posts/2022-01-26-blog-2-theme-Next-update
- /posts/2022-01-26-blog-2-theme-Next-update.html
---

## 主題版本更新

Next 主題有在定期更新，每次更新後可能 config 的內容位置都可能有更動。

[Next 在 v8.x 的版本中有給予建議](https://theme-next.js.org/docs/getting-started/configuration)，不要將個人的變更寫在 `theme/Next/_config.yml` 下面，這樣每次 config 有改版都要一個個更新，不一定能完美的 merge。

我們可以在與 site config (配置 hexo 的設定檔) 同層級的地方，創建一個 `_config.[theme].yml` 的檔案，`theme` 帶入主題的名稱。這個檔案中的內容會覆蓋 `theme/[next]/_config.yml` 的內容。

如果以 NexT 主題為例：我的 `theme` 底下主題名稱為 `next`，配置的客製化檔案名稱為 `_config.next.yml`。並且我只在裡面放有修改區塊的 config ，避免未來如果要升級，我還花功夫去找哪裡有變更。

## PrismJs 的啟用

這部分跟主題的版本有關，雖然我是在 2021 年底創建部落格的，但不曉得為何用到了很舊版的 Next，其 `_config` 沒有有關 Prismjs 在 codeblock 欄位底下的配置。

後來發現這個問題之後進行版本更新，並遇到在兩個配置落差頗大的 `_config` 之間玩比對遊戲，因此體悟出了上述辦法的優勢。

更新後，codeblock 裡面有如下配置:

```yaml
codeblock:
  theme:
    light: default
    dark: tomorrow-night
  prism:
    light: prism-tomorrow
    dark: prism-tomorrow
```

並且 hexo 的 `_config` 要將 prismjs 開啟、highlight 關閉: 

```yaml
highlight:
  enable: false
  line_number: false
  auto_detect: false
  tab_replace: ''
  wrap: true
  hljs: false
prismjs:
  enable: true
  preprocess: true
  line_number: false
  tab_replace: ''
```

## 修改行中程式碼的格式 (change inline code style)

我不喜歡預設的 inline code 格式，覺得太灰、padding 太大。而且這些 code 不隸屬 prismjs 的主題規範，要從 CSS 下手! 

首先，我們可以透過右鍵檢查元素發現 inline code 也是隸屬於 `code` tag，就瞄準這部份研究，我尋找到的方法是直接去改 css 設定。

在 `source\_data\styles.styl` 當中(沒有則創建!)，寫入設定：

```stylus
code {
  padding: 0.1em 0.25em;
  overflow-wrap: break-word;
  word-break: break-all;
  color: #cf222e;
  background: #fbf7f8;
  border-radius: 0.2em;
  font-size: 1em;
  font-weight: lighter; // bolder
}
```

字體顏色選擇跟 github keyword 相似的顏色 `#cf222e`，雖然這使得 inline code 變得紅字很惹眼，但等到看到受不了再來想其他改法吧。

光寫入沒有用，還要把這個檔案引入 Next 的渲染過程中。在上述的 `_config.next.yml` 中添加一段：

```yaml
custom_file_path:
  style: source/_data/styles.styl
```

再嘗試 `hexo server` 之類的在本地 demo 一下，應該可以看到改動的內容了！

---

參考自：

- [Hexo之Next主題代碼優化](https://www.cnblogs.com/LyShark/p/11834144.html)
- [【Hexo】以 Next 主題為基礎，打造自己的樣式吧！](https://myiaj.github.io/2020/03/14/hexo-custom-style/)

