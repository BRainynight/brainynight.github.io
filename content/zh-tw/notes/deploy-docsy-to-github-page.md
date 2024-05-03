---
title: 部屬 Docsy 到 Github Page
date: 2024-05-03 13:09:00
description: "實際部屬到 github Page 時遇到的困難"
categories:
  - Default
---

首先，參考 [Hugo: Hosting on github](https://gohugo.io/hosting-and-deployment/hosting-on-github/)建立 workflow 檔案 `.github/workflows/hugo.yaml`，注意 Branch Name 與 Hugo Version 要手動改。

在實際部屬時遇到問題: 
```
Error: error building site: POSTCSS: failed to transform "scss/main.css" (text/css). Check your PostCSS installation; install with "npm install postcss-cli". See [https://gohugo.io/hugo-pipes/postcss/:](https://gohugo.io/hugo-pipes/postcss/:) binary with name "npx" not found
```

我的解法參考自 [Hugo: postcss](https://gohugo.io/hugo-pipes/postcss/)，在自己 Local 的專案資料夾執行指令: 
```bash 
npm i -D postcss postcss-cli autoprefixer
```

下指令後會下載一堆模組，把他們都加到 git 裡面，一起推上 github，問題就解決了。