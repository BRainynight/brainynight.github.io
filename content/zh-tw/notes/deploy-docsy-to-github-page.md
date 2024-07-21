---
title: 部屬 Docsy 到 Github Page
date: 2024-05-03 23:09:00
description: "實際部屬到 github Page 時遇到的困難"
categories:
  - Default
---

## 前情概要
- [從零開始 Docsy (1)](../start-with-docsy-1)
- [從零開始 Docsy (2)](../start-with-docsy-2)

## 正式上線

[Docsy 官方](https://www.docsy.dev/docs/get-started/docsy-as-module/start-from-scratch/)有提供「白手起家」的 command 該怎麼寫: 

```bash
# initialize site 
hugo new site my-new-site
cd  my-new-site
# init mod and add require 
hugo mod init github.com/me/my-new-site
hugo mod get github.com/google/docsy@v0.10.0
# add config
cat >> hugo.toml <<EOL
[module]
proxy = "direct"
[[module.imports]]
path = "github.com/google/docsy"
EOL
hugo server

```

透過 `hugo new site`，`hugo` 會創建一些預設的資料夾，如 `content`, `assets` 等，不像前面得自己創建。
在[先前的簡易範例](../start-with-docsy-2)中只改 config，無須更改網頁主體的內容，因此有無這些其他資料夾無直接影響。在實際上線時，要覆蓋 docsy 預設的 CSS 都得在 `assets/scss` 下加檔案，因此還是用 `hugo new site` 生成完整的架構。

## 使用 Github Page 架站
上網搜尋「架站」，已經可以找到許多資源，這裡不多贅述。如果從未有架站經驗，強烈建議閱讀這篇文章: [技術網站架設經驗雜談](https://www.ithome.com.tw/voice/148476)。先決定: 是否要付費買網域? 

對我來說，部落格像是一個 Side Project。不曉得更新頻率，也不曉得持續到甚麼時候，用且對 Github Page 已有經驗，因此決定繼續使用。Github Page 有一些[限制](https://docs.github.com/zh/pages/getting-started-with-github-pages/about-github-pages#usage-limits)，如果都可接受，那就繼續吧! 
### 關於 Github Page
每個人的帳戶對應的網域名稱是: `<username>.github.io`，以我來說就是`brainynight.github.io`。

你可以擁有多個 github page，但 `<username>.github.io` 只能對應一個專案，這個專案的名稱就必須跟網域有一樣的名稱。像這個網站對應的專案就是: [brainynight.github.io](https://github.com/BRainynight/brainynight.github.io) 。如果有多個 Github Page 需求，其他 Page 會變成 `<username>.github.io/<repository-name>`，被設成 Github Page 的專案必須是 Public 的。

### 步驟
具體步驟參考[官方說明](https://docs.github.com/zh/pages/quickstart)，使用 Hugo 還牽涉到 github action，這裡簡單修改步驟。
1. 創建一個新的 repository，輸入 `<username>.github.io` 作為名稱
  1. 如果是第二個 Github Page (已經有另一個 repository 名為`<username>.github.io`)，這裡就輸想要的名稱就好 (ex. second-blog)。
2. 把剛才 `new site` 生成出的內容上傳到 Github repository
3. 進到 repository，點設定
4. 找到 "Pages" 的設定頁面
5. **不同於 Github 教學文章!** 在 "Build and deployment" 選擇 "Github Actions"，參考 [Hugo-Host on GitHub Pages](https://gohugo.io/hosting-and-deployment/hosting-on-github/)的 Step4
6. 在 Local repository，創建檔案 `.github/workflows/hugo.yaml`，內容複製 Hugo 說明的 Step6。記得 **Branch Name 跟 Hugo Version 要手動改成自己使用的版本!**。這個 Github Action 的觸發條件是當有內容 "push" 的時候。
7. 在 Local repository commit 並且上傳到 Github
8. 回到 Github repository，點選分頁 "Actions"，會看到有 workflow 清單，由於剛才設的動作是「當 Push 的時候執行」，因此現在正在跑。如果失敗了可以一步步點進去看 error message。
9. 成功的話如下圖，可以到自己的網站看 Hugo Build 出來的內容了!
    ![success](https://gohugo.io/hosting-and-deployment/hosting-on-github/gh-pages-4.png)


## 失敗經驗

在實際部屬時遇到問題: 
```
Error: error building site: POSTCSS: failed to transform "scss/main.css" (text/css). Check your PostCSS installation; install with "npm install postcss-cli". See [https://gohugo.io/hugo-pipes/postcss/:](https://gohugo.io/hugo-pipes/postcss/:) binary with name "npx" not found
```

我的解法參考自 [Hugo: postcss](https://gohugo.io/hugo-pipes/postcss/)，在自己 Local 的專案資料夾執行指令: 
```bash 
npm i -D postcss postcss-cli autoprefixer
```

下指令後會下載一堆模組，把他們都加到 git 裡面，一起推上 github，我不確定是否為最佳解，不過問題解決了。