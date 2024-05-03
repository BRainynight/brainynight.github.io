---
title: Hexo Blog 客製化 - Next 主題加速
date: 2022-01-26 13:43:09
tags: [hexo]
description: 減少 Next 主題的載入時間!! 修改 Next 主題載入動畫時間長度，改變主題字體並加速載入。
aliases: 
- /posts/2022-01-26-blog-3-speedup
- /posts/2022-01-26-blog-3-speedup.html
---

**2022/01/30**：最近在優化 SEO，想讓 google 可以索引到網站。遲遲不知道問題出在哪裡，google 表示有安排了但還沒索引到。反正就各種搞行動裝置優化，好笑的是把字體設定回預設、把 icon 關掉，一下子行動版跟網頁板效能都變 99~100 了，真是有點嘲諷...。

**2022/01/26** ：說實話，在改字體後還想要網站加速，突然覺得自己有點癡人說夢。改字體本來就會造成額外的負擔! 但還是基於個人的喜好依然想改，照樣記錄一下心路歷程! 

## 改變字體

有關  `_config.next.yml` 與  `source\_data\styles.styl`  的配置參見前面的兩個章節！

1. 在 `_config.next.yml` 中配置字體段落

   ```yaml
   font:
     enable: true 
     host:
     global:
       external: false # 如果寫 true, 就可以不用考慮後面的第三步了。
       family: 'Noto Serif SC'
   ```

2. 在`source\_data\variables.styl` 中設置環境變數，覆蓋原本的設定檔。

   記得要整段 font 的段落都複製！舉例而言，如果只覆蓋了 `font-family-chinese` 與 `font-family-base` 兩個變數，疑似因為在 Next 原本檔案中有其它變數使用到 `font-family-base`，而他們只會記住舊的變數。這會導致畫面有部份（像是 side bar）更改字體，而有部份依然使用微軟正黑體。

   ```stylus
   $font-family-chinese      = 'Noto Serif TC', 'Microsoft YaHei'; 
   
   $font-family-base         = $font-family-chinese, sans-serif;
   $font-family-base         = get_font_family('global'), $font-family-chinese, sans-serif if get_font_family('global');
   
   $font-family-logo         = $font-family-base;
   $font-family-logo         = get_font_family('title'), $font-family-base if get_font_family('title');
   
   $font-family-headings     = $font-family-base;
   $font-family-headings     = get_font_family('headings'), $font-family-base if get_font_family('headings');
   
   $font-family-posts        = $font-family-base;
   $font-family-posts        = get_font_family('posts'), $font-family-base if get_font_family('posts');
   
   $font-family-monospace    = consolas, Menlo, monospace, $font-family-chinese;
   $font-family-monospace    = get_font_family('codes'), consolas, Menlo, monospace, $font-family-chinese if get_font_family('codes');
   
   ```

接下來是第三步驟，主要是我發現改字體後的載入速度比使用原生的微軟正黑體慢了至少 0.5~1秒以上吧。我嘗試想加速字體載入的部份，會先寫建議使用的方法，再紀錄一下我嘗試的方法。

```yaml
font:
  global:
    external: false
    family: 'Noto Serif SC'
```



### 方法一：字體預載入

來到 [google font api](https://fonts.google.com/noto/specimen/Noto+Serif+TC) ，我們選擇要的粗細(Regular) 之後，左邊會有個彈出視窗，教導我們怎麼在 Html 跟 CSS 中嵌入。

> To embed a font, copy the code into the `<head>` of your html

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC&display=fallback" rel="stylesheet">
```

可以用 Vscode 之類的在部落格資料夾中找到寫有 `<head>` 的模板，在我的版本 (V8.9) 中，這位於 `themes\next\layout\_layout.njk`，直接在 `<head>` 中把上面那段落貼上，就完成了！

由於我對網頁前端並不熟悉，不是很確定這是否為關鍵因素。但在我使用預設的 config `external:true` 並把 preload 註解掉之後，透過 [pagespeed](https://pagespeed.web.dev/) 測試，載入時間落差約有一秒左右。

### 方法二：掛載在當前網域下 (不建議)

在 `source\_data\styles.styl` 中添加字體的匯入：

```stylus
@font-face {
  font-family: 'Noto Serif TC';
  font-weight: 400;
  font-style: normal;
  font-display: fallback;
  src: local('Noto Serif TC'), local('Noto-Serif-TC'),
       url('/fonts/NotoSerifTC-Regular.otf');
}
```

`font-display: fallback` 可以使網頁先使用預設字體（微軟正黑體）這種本身就存在於電腦中的字體，使內容可以先顯示。而背景會默默把設定的 Noto Serif TC 下載，事後置換。

選擇掛在於子網域未必會比較好，因為完整的 otf 檔案高達 MB 級，儘管設置了字體置換，等到完整的載入字體也需要長達 10 秒的時間 (視網路速度吧)。而 google font api 本身有把字體切割成很多部份，讓網頁可以選擇載入有用到的部份字形即可，節省下載量。

## 找出網頁的 Bug

可以打開 chrome [開發人員工具](https://support.google.com/campaignmanager/answer/2828688?hl=zh-Hant) 中 "Network" 項目，並 ctrl+R  重新整理網頁。檢查一下都是哪些檔案拖垮了網站速度。我當時發現有一些找不到路徑的字體檔案、Hexo 在產生靜態頁面時有寫的 warning 都有影響，所以修到沒 bug 在推上網路很重要。務必確保網頁在載入的期間只有載入**需要的元件**，不需要花時間試誤。

```
Warning: Accessing non-existent property 'filename' of module exports inside circular dependency
```

Google 一番之後，參考[此篇文章](https://www.haoyizebo.com/posts/710984d0/) 發現是 `nib` 套件出了問題。我的解決方法沒有順著他的教學，先嘗試重新安裝 `hexo-renderer-stylus` 但並沒有用。添加 `"resolutions"` 的部分忘記有沒有嘗試過，或許還是失敗了吧。

最終，我是在 `package-lock.json` 的 `nib` 套件下找到: 

```yaml
"stylus":0.54.5
```

修改成

```yaml
"stylus": 0.54.8
```

`npm install` 之後參照輸出的資訊內容，先後下指令 `npm audit fix` 與 `npm audit fix --force` 解決了這個問題。

## 修改 Next 主題的動畫時間 [不建議]

由於不同版本的 Next 程式碼內容也可能有所不同，參考自: [Hexo NexT 主題修改動畫效果速度](https://blog.csdn.net/Domino_b/article/details/81704118)。

1. 使用 Vscode 之類的編輯器在 Next 主題中尋找關鍵字 `duration`，它可能出現在很多 js 檔案中，有些預設是 200、有些是 500。
2. 直接改數字，我先改成 100 之後大概看一下效果，網頁載入的速度明顯有提升! 可以先在 localhost 上測試。不敢貿然換成 0 的原因是不確定會不會因為某些元素來不及載入造成錯誤，反而拖到整體的時間。
3. 稍微判讀一下程式變數，有些頗容易看出函式意義的可以改短一點，不怕會不會影響載入，例如: `registerSidebarTOC`函式應該是跟側邊欄位「文章目錄」、「本站摘要」之間切換的動畫吧，我會再把數字改小一點。

反覆在 local 端測試會不會造成 Bug 或使用者體驗不佳，之後就可以部屬到 github page 上了。部屬之後可以到 [pagespeed](https://pagespeed.web.dev/) 測試一下表現如何，該網頁會給一些診斷建議，但我自己沒有前端經驗不太知道怎麼改，只是拿來測速度。目前的網頁測試在電腦版中大約有 85-89 分的成績。

## 在 Next Config 中設置動畫選項

在手動更改 duration 數值後依然不滿意的我繼續爬，發現其實 Next 主題在 config 中就已有一段設定了，可以**直接把動畫關掉**。即使想要保留動畫，`async` 也可考慮開起來，讓元素們非同步加載有機會讓 Loading 更快吧。之所以前一段去改 duration 列為不建議是因為，我不太確定修改間隔會不會對元素的加載產生一些問題，但還是記錄起來。

值得一提的是，包括進場動畫其實都是可以改的! 在 Next 主題的 demo 頁面中有展示各個特效名稱對應的效果: https://theme-next.js.org/animate/ 。

這邊是我已經改過的 yaml 部分: 

```yaml
motion:
  enable: true
  async: true
  transition:
    # All available transition variants: https://theme-next.js.org/animate/
    post_block: fadeIn
    post_header: fadeInUp 
    post_body: fadeIn
    coll_header: fadeInLeft
    # Only for Pisces | Gemini.
    sidebar: fadeInUp
```

## Plugin : `hexo-filter-optimize`

下載之後

```sh
npm install hexo-filter-optimize
```

在 site config (hexo config) 中添加設定: 我會把 css 的 bundle 關掉，因為開啟來的時候有一點造成畫面跑版，看得不太舒服。

```yaml
filter_optimize:
  enable: true
  # remove the surrounding comments in each of the bundled files
  remove_comments: false
  css:
    # minify all css files
    minify: true
    # bundle loaded css files into one
    bundle: false
    # use a script block to load css elements dynamically
    delivery: true
    # make specific css content inline into the html page
    #   - only support the full path
    #   - default is ['css/main.css']
    inlines:
    excludes:
  js:
    # minify all js files
    minify: true
    # bundle loaded js files into one
    bundle: true
    excludes:
  # set the priority of this plugin,
  # lower means it will be executed first, default of Hexo is 10
  priority: 12
```

使用 `hexo-filter-optimize` 之後，有機會讓分數提升，我在手機版面上的分數就從 55 提升到了 78 (雖然有點迷惑那個分數的意義)
