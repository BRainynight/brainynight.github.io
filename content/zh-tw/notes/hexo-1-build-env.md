---
title: 建置 Hexo 部落格
date: 2021-12-30 18:30:29
tags: [ hexo]
description: 使用 Hexo 建立部落格並連動發布到 github page (github.io)上、文章發布、Hexo基本設定檔、NexT 主題設定檔...等初次使用的操作。
aliases: 
- /posts/2021-12-30-blog-0-hexo-build-env
- /posts/2021-12-30-blog-0-hexo-build-env.html
---

## 前置作業

1. 安裝 [Node.js](https://nodejs.org/en/) ，下載安裝檔後一路按到底，安裝完成。 

2. 查看是否安裝成功：打開 CMD，輸入

   ```sh
   node -v
   npm -v
   ```

   應該會顯示已經安裝的版本。

3. 安裝 Hexo：打開 CMD 輸入

   ```sh
    npm install hexo-cli -g
   ```

   ```
   added 57 packages, and audited 58 packages in 8s
   
   11 packages are looking for funding
     run `npm fund` for details
   
   found 0 vulnerabilities
   npm notice
   npm notice New minor version of npm available! 8.1.2 -> 8.3.0
   npm notice Changelog: https://github.com/npm/cli/releases/tag/v8.3.0
   npm notice Run npm install -g npm@8.3.0 to update!
   npm notice
   ```

   

4. 查看 Hexo 是否安裝成功：看下面的指令有沒有成功顯示一些相關資訊

   ```sh
   hexo version 
   ```

全部前置作業完成！

## 初始化

1. 建立一個資料夾，這裡創立 `blog-hexo`

2. 進入資料夾，下指令：

   ```sh
   hexo init . 
   ```

3. （仍在資料夾中）下指令安裝需要的 npm 套件

   ```sh
   npm install
   ```

   不需要安裝會出現象這樣的訊息：

   ```sh
   up to date, audited 249 packages in 976ms
   
   15 packages are looking for funding
     run `npm fund` for details
   
   1 moderate severity vulnerability
   
   To address all issues (including breaking changes), run:
     npm audit fix --force
   
   Run `npm audit` for details.
   ```

4. 可以嘗試 Demo 預設的網頁：

   ```sh
   hexo server
   ```

   

## Hexo 設定檔

現在我們回到 `blog-hexo` 資料夾中，注意到 `_config.yml` 設定檔。

1. 其中 `theme` 參數是有關主題的參數，將它設置為想要的主題，這裡我想採用 `next`

   ```yaml
   # Extensions
   ## Plugins: https://hexo.io/plugins/
   ## Themes: https://hexo.io/themes/
   theme: next 
   ```

2. 到`theme`資料夾，將主題的 github 專案 clone 下來

   ```sh
   git clone https://github.com/theme-next/hexo-theme-next.git next
   ```

### 改地區

```yaml
# Site
title: Blog Title
subtitle: ''
description: ''
keywords: # 可以下一些對部落格的關鍵字，方便搜尋引擎找到
author: Who
language: zh-TW # 改成 zh-TW, 大寫！不然在 hexo generate 時會變成阿拉伯文...
timezone: ''
```

### Github 部屬相關

執行這個步驟前需要先在 Github 上創建倉庫，參見：[上傳到 Github 倉庫](#上傳到 Github 倉庫)。預設的情況通常倉庫名稱會建置為 `username.github.io`，以下就以預設的情況舉例說明。

1. 部落格網址：

   ```yaml
   ## Set your site url here. For example, if you use GitHub Page, set url as 'https://username.github.io/project'
   url: https://<使用者名稱>.github.io/
   ```

2. 使用 `hexo deploy` 到 Github 上面的參數選項：

   ```yaml
   deploy:
     type: git
     repo: https://github.com/username/username.github.io.git # http git clone 所給的網址
     branch: master # 或 main, 看主要的 branch 名稱是什麼 
   ```

   `branch` 如果是由本地端使用 `git init .` 創建，預設的分支名稱會是 `master` 。但如果是在 github 倉庫上面創建先的話，預設會是 `main`。Hexo 可以部屬到很多地方，如果在這邊用了多個 `type`，可以在使用 deploy 時一口氣部屬到多個網站：[Deployment | Hexo](https://hexo.io/zh-tw/docs/one-command-deployment.html)

   ```yaml
   deploy:
   - type: git
     repo:
   - type: heroku
     repo:
   ```

## 主題設定檔

### Scheme

`Next` 主題中還有不同的排版模式，設定要進入 `theme/next/_config.yml` 修改：

```yaml
scheme: Gemini
```

### Menu 要顯示的內容

```yaml
menu:
  home: / || fa fa-home
  about: /about/ || fa fa-user
  tags: /tags/ || fa fa-tags
  #categories: /categories/ || fa fa-th
  archives: /archives/ || fa fa-archive
  #schedule: /schedule/ || fa fa-calendar
  #sitemap: /sitemap.xml || fa fa-sitemap
  #commonweal: /404/ || fa fa-heartbeat
```

影響的是左邊 Menu 中顯示的分頁內容，預設只有 home 跟 archives，其他項目如果開起來的話預設的頁面(page) 還沒建立，會連不到內容。

### [添加客製化(Custom) 的設定檔](https://oscarcx.com/tech/hexo-customize.html#%E5%85%B6%E5%AE%83%E6%94%B9%E5%8A%A8)

將想添加的項目取消註解，這裡最簡單粗暴的只使用 `style`。寫在 `styles.styl` 中的 css 會被添加到最尾端，因此可以直接覆蓋默認的格式。

```yaml
custom_file_path:
  #head: source/_data/head.swig
  #header: source/_data/header.swig
  #sidebar: source/_data/sidebar.swig
  #postMeta: source/_data/post-meta.swig
  #postBodyEnd: source/_data/post-body-end.swig
  #footer: source/_data/footer.swig
  #bodyEnd: source/_data/body-end.swig
  #variable: source/_data/variables.styl
  #mixin: source/_data/mixins.styl
  style: source/_data/styles.styl
```



## [第一篇文章](https://hexo.io/zh-tw/docs/writing)

1. 執行下述指令，Hexo 會根據 Layout 的種類建立一個 markdown 檔案在對應的位置，Layout 預設為 Post。下面的指令就會在 `source/_posts` 下建立 `NewPost`

   ```sh
   hexo new [Layout] <PageName>
   hexo new "NewPost"
   ```

   `source` 中是存放各種頁面 markdown 位置，`public` 中則是存已經渲染成 html 格式的檔案。

   [Layout 的種類有三種](https://hexo.io/zh-tw/docs/writing#%E4%BD%88%E5%B1%80%EF%BC%88Layout%EF%BC%89)：

   - `post `：預設種類，儲存的位置是 `source/_posts`

   - `page`：路徑是 `source`，用途應該像是上面 Menu 環節中的 `Tags`, `About` 頁面需要創建時，就該輸入 `hexo new page Tags` 之類的吧。

   - `draft`: 儲存路徑是 `source/_drafts` ，存在這裡的檔案不會顯示在頁面上。當要發布時，可以透過 

     ```sh
     hexo publish [layout] <draft_title>
     ```

     將草稿從 `_drafts` 挪到 `_posts` 或變成 `page` 之類的。

     

2. 來到 `source/_posts/NewPost.md` (應該還可以看到同層級還有一個 Hello world) ，預設的內容如下，紀錄了一些文章的 Metadata。

   ```markdown
   ---
   title: NewPost
   date: 2021-12-26 22:40:55
   tags: tag1 tag2
   ---
   # 標題一
   寫一些東西吧！
   ```

3. 到根目錄 `source` 上：

   ```sh
   hexo generate # 產生靜態 page 
   hexo server # Demo 在 localhost:4000 上
   ```

### scaffolds

在創建文章的時候，根據 `layout` 種類，Hexo 會生成一個對應名稱的 .md 檔案在指定的路徑內。而這個檔案通常會有一些預設的內容，例如：`post` 格式就會有上一個章節中所展示的，有著預設的 metadata：`title`, `date`, `tags` 三個項目。

如果想添加更多的屬性在預設產生的模板中，可以在 `scaffolds/post.md` 中添加。預設中的形式如下：

```markdown
---
title: {{ title }}
date: {{ date }}
tags:
---
```

### 創造頁面(page)

我們在[前面](#Menu 要顯示的內容)選擇了 Menu 裡面要顯示什麼，但如果取消註解了而沒有創建對應的頁面，在主頁上會顯示、但連進去之後會是 404。我們需要依照有列出的 page 創建對應的頁面：

```sh
hexo new page categories
hexo new page tags
```

之類的。參見： [[筆記] 打造自己的 blog，Hexo + Github 之二](https://kemushi54.github.io/2019/04/01/%E7%AD%86%E8%A8%98-%E6%89%93%E9%80%A0%E8%87%AA%E5%B7%B1%E7%9A%84-blog%EF%BC%8CHexo-Github-%E4%B9%8B%E4%BA%8C/)

## 上傳 Github 與部屬網站

### 上傳到 Github 倉庫

1. 在 Github 創建一個名為  `<UserName>.github.io` 的倉庫，如果已經有過這個名稱，需要使用別的名稱創建倉庫名，可以參考這篇文章：[[教學]使用 GitHub Pages + Hexo 來架設個人部落格](https://ed521.github.io/2019/07/hexo-install/#gt-%E8%A8%AD%E5%AE%9A%E9%83%A8%E7%BD%B2%E8%87%B3-GitHub-%E7%9A%84%E8%B3%87%E8%A8%8A)

2. 安裝插件

   ```sh
   npm install hexo-deployer-git --save
   ```

   沒安裝的話會出現 `ERROR Deployer not found: git`

3. 在部落格資料夾中開啟 cmd，確認位置是在根目錄下（這篇的例子就是 `blog-hexo`）

   ```sh
   hexo cl # hexo clean 會把 public 內容刪掉
   hexo g # hexo generate 建立靜態檔案
   hexo d # hexo deploy 部屬到 _config 中有設置的地方
   ```

我的電腦因為本來就有跟自己的 github 倉庫做 ssh 連結，所以沒有跳出帳密驗證（還是過去已經有驗證過了但我忘記了？）。但看起來有些人在第一次部屬的時候會需要在跳出視窗登帳號。

### [Hexo Deployer 的運作原理](https://github.com/hexojs/hexo-deployer-git#how-it-works)

事實上，`hexo-deployer-git` 是將網站的靜態檔案產生在 `.deploy_git` 裡面，並使用強制推送(force pushing) 把東西推上  `<UserName>.github.io`。也因此，如果我們在根目錄或 `public` 資料夾再怎麼使用指令

```sh
git remote -v 	  # 列出所有遠端伺服器
git log --oneline # git commit 紀錄
```

都不會看到什麼內容，但如果進去 `.deploy_git` 資料夾，一切都不同了。

```sh
$ git log --oneline
0c468df (HEAD -> master) update blog
7c6b6b6 First commit
```

但它的 git remote 清單裡面還是空的，我也還沒搞懂運作原理（汗顏



### 保存當前的內容

成功部屬後，進入  `<UserName>.github.io` 的倉庫，可以發現這個倉庫的內容基本上就是 `public` 資料夾的內容。並且我們可以在本地部落格中，透過 `git remote -v` 查看是否有遠端倉庫。（此用法參見：[Git-基礎-與遠端協同工作](https://git-scm.com/book/zh-tw/v2/Git-%E5%9F%BA%E7%A4%8E-%E8%88%87%E9%81%A0%E7%AB%AF%E5%8D%94%E5%90%8C%E5%B7%A5%E4%BD%9C) ）我這邊看起來是空蕩蕩，什麼都沒有。我希望在不同的平台上都可以撰寫部落格，想把當前的內容備份該如何？

Hexo 在幫我們初始化資料夾時已經有了一個 `.gititnore` 檔案，裡面已經將他們為了部屬而產生的資料夾給排除，也把 localhsot 在跑得時候所需要的 `public` 資料夾排除

```gitignore
.DS_Store
Thumbs.db
db.json
*.log
node_modules/
public/
.deploy*/
```

所以我們可以不用額外做設定，直接 `git add .` 把東西加進去 git 倉庫，然後在 github 上面創一個私人的倉庫、按照教學把 github 倉庫跟本地倉庫連結，內容推上去就可以了。

 

## Reference

- [【學習筆記】如何使用 Hexo + GitHub Pages 架設個人網誌](https://hackmd.io/@Heidi-Liu/note-hexo-github#Hexo-%E7%92%B0%E5%A2%83%E5%BB%BA%E7%BD%AE)：介紹如何建制、Hexo 常用的指令、如何發布到 Github 上面。
- [建立自己Blog系列(三) Hexo next theme 介紹](https://isdaniel.github.io/hexo-blog-theme/)：有更詳細的介紹 Configure 區域對應的用途
- [3分鐘完成HexoBlog主題Next設定](https://tiida54.github.io/2018/01/05/3%E5%88%86%E9%90%98%E5%AE%8C%E6%88%90HexoBlog%E4%B8%BB%E9%A1%8CNext%E8%A8%AD%E5%AE%9A/)：講解到 `scheme` 的部份，但似乎版本有點舊，有些屬性沒找到。
- [[教學]使用 GitHub Pages + Hexo 來架設個人部落格](https://ed521.github.io/2019/07/hexo-install/#gt-%E8%A8%AD%E5%AE%9A%E9%83%A8%E7%BD%B2%E8%87%B3-GitHub-%E7%9A%84%E8%B3%87%E8%A8%8A)：也是屬於從頭部屬 Hexo 並上傳 Github，但在 Github Page 的部份有更仔細的解釋。
- [雲沐居: 最新 Hexo NexT v7.4.1 主題優化](https://zenreal.github.io/posts/44730/)：比較多是對文章內容格式有影響的介紹，像是用一些特殊的 block，螢光筆色這種。
- [Hexo博客个性化配置](https://oscarcx.com/tech/hexo-customize.html#%E9%AD%94%E6%94%B9footer)：`Next` 主題的進階修改，偏向一些部落格整體的小工具，如閱讀進度條、音樂播放器...。
- [hexo(Next主题)修改文字大小](https://blog.csdn.net/dpdpdppp/article/details/102387532)
- 主題: [Next](https://theme-next.js.org/next-8-8-2-released/#%F0%9F%9B%A0-Improvements)
- 主題: [Stun](https://github.com/liuyib/hexo-theme-stun/)