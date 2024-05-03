---
title: 網頁搜尋優化
description: 邁向讓Google收錄文章的心路歷程
date: 2022-06-05 19:31:25
tags: [hexo]
aliases:
- /posts/2022-06-05-blog-4-seo
---

這是一篇在部落格架設之初，嘗試使用 Google Search Console 時的苦痛新路歷程，多數內容是當時所寫。幾乎是每日每日更新當天的發現、新的疑難雜症，因此可能每個段落的「今天」都不一樣(尷尬)，但文章中都有把實際的日期標上去，請以相對時間的角度來閱讀本文!

我並不是專業於網頁前端、SEO 的人，或許文中的推斷與說明會有偏差，但仍嘗試將過程中的試誤以及解決辦法給紀錄下來，對錯與否還請自行斟酌!

------

首先，網頁架設之後如果搜尋引擎沒有收錄，就沒辦法讓網頁在使用者搜尋時被搜索到。Google 的爬蟲「有可能」可以主動探勘到部落格，但或許更大的機率是不會，畢竟現在網路這麼發達，爬蟲很忙的。

要知道自己的網頁是否有被爬蟲收錄，可以直接在搜尋引擎上打 `site:<你的網址>`，像是要看本部落格在搜尋引擎的收錄狀況如下:

```
site:brainynight.github.io
```

我們要做的事情是，讓自己的網頁在搜尋引擎登記在案! 使用的是 Google Search Console 的服務。有關如何登記，可以參考此篇文章: [【完整指南】2022 Google Search Console教學(附索引問題處理) - SEO分解茶](https://www.seo-tea.com/google-search-console-tutorial/)。

本文接下來所分享的內容，是有關我在 Google Search Console 建立網域、登記 Sitemap 之後所遇到的問題。

PS. 在 2022/09 前後，Google 有修改一次搜尋引擎的策略，用 `site:XXX` 看收錄了哪些網站似乎不再管用，與在 Google Search Console 當中看到編入索引數量並不一致，顯示的只有熱門的幾篇文章。

## 提交 Sitemap 後等很久

![image20220126135547909](/uploads/sitemapfail.png)

圖中的三個網址，有兩個是拿來嘗試此情況下 Google 會顯示何狀態，只有 `sitemap.xml` 是我真正希望爬蟲看到的。

- `sitemap_index.xml`: 在我的網頁中不存在，404 not found。Google 的狀態顯示「無法擷取」但點進去之後有寫到錯誤原因: `無法讀取 Sitemap: 一般的 HTTP 錯誤`。

  > 我們嘗試存取您的 Sitemap 時發生錯誤。請確定您的 Sitemap 符合我們的指南，而且可由您提供的位置存取，確認都沒有問題後再重新提交。 示例 HTTP 錯誤：404

- `robots.txt`: 他本身不是 xml 檔案，我在提交 robots.txt 的頁面有提交過，可以成功爬取。可讀取 Sitemap，但其中含有錯誤。

  > 不受支持的檔案格式。您的 Sitemap 格式似乎不受支援。請確認它符合我們的《Sitemap 指南》，然後重新提交。

- `sitemap.xml`: 真正的 sitemap，我確定 google 是可以存取他的，但不知道為何就是顯示無法擷取，點進去的內容也只有「無法讀取 Sitemap」。

網路上關於 sitemap 沒辦法被截取有很多解釋，主要歸類如下:

1. 真的有問題: 如格式不對 (含有 noindex, 不符合 sitemap 規範的幾種格式)、網址不存在 (404)
2. 沒問題，只是 Google 機器人還沒時間爬。

主要就是如果可以確認自己的 sitemap 屬於後者，就只能等。幾天到幾個禮拜不一定... ，這兩篇文章可以參考:

- [Google search console fails to fetch sitemaps | "Sitemap could not be read"](https://stackoverflow.com/questions/53921636/google-search-console-fails-to-fetch-sitemaps-sitemap-could-not-be-read)

- [Sitemap could not be read (Couldn’t fetch) in Google Search Console](https://www.jcchouinard.com/sitemap-could-not-be-read-couldnt-fetch-in-google-search-console/)

  如果狀況如下圖，可能如作者所言，就只是 google 引擎還沒抓到。

  ![img](https://www.jcchouinard.com/wp-content/uploads/2021/07/image-4.png.webp)

## Sitemap 被讀取成功

大約是 1/25 晚上第一次提交 sitemap，1/27 早上看到頁面轉為通過 (快樂)。

在一直不通過的期間我到處爬文，除了上面說的 googlebot delay 的關係，還有一個是 google 難以在茫茫大海中找到這個網站。由於之前有在 Medium 上寫作，知道它的 SEO 做的很好，所以在 Medium 上面發了一篇轉站的文章。

今天早上 (1/27) 不但看到 sitemap 通過了，還發現我的 Blog 首頁在 **網址審查** 那邊，來源是從 Medium 來的!

```
發現方式
Sitemap: https://brainynight.github.io/sitemap.xml
參照網頁: <我的 medium blog 網址>
```

恩，雖然它依然顯示 **網址不在 Google 服務中 (已找到 - 目前尚未建立索引)** 。但這個階段，在 google 找自己的網域(文章一開始說的搜索方式)還是找不到東西的。

網路上說「找到」直到「建立索引」的階段，可能要長達一周以上，反正就慢慢等囉。

## 所申請的主頁被索引成功

1/30 中午 11 點! 我的部落格首頁被索引成功!

一早 10 點起來還沒被索引，我查了一下有利 SEO 的條件基本上要利於手機檢索，於是開始調整東調整西。這之間我曾經嘗試調整字體，然而字體是外部資源，因此會耗費載入時間。對於 Hexo Next 這個主題我所做的優化，都記錄在文章[Hexo Blog 客製化 (3) Next 主題加速](/posts/2022-01-26-blog-3-speedup)當中。諷刺的是，最影響效能的其實就是字體跟外載入的資源! 我把 `min.js` (來自 fontawsome 提供 icon 的) 跟字體客製化都關掉用最原始的預設字體。結果效率分數直接拉到 99~100。

也就是說，甚麼美化都不搞其實更有利於檢索....。由於之前我的 sitemap 有被接收過，其中網址的狀態都被標示沒安排索引，原因是怕伺服器撐不住，我猜測是因為載入過慢的問題，因此做了這樣的調整。也不知道有沒有因果關係，總之做了這一些調整後，首頁被 googel 爬蟲臨幸拉! (快樂)

可以使用 google 引擎看一下自己的收錄狀況，要注意 `site` 跟 `url` 之間不能有空格!

```
site:<your url> [keyword]
# Example: 
site:https://brainynight.github.io
site:https://brainynight.github.io pickle
```

## 我的網頁有變更，Google 沒看到

Google 搜尋引擎的演算法策略不斷改變，數位世代的網頁增長數量也非常快。Google 難以將全世界所有的網頁都收錄一遍、且隨時即時更新。使用 wordpress 或用 github page 自己架設部落格時，SEO 問題就需要自己一盤抓。

而像這種個人的小部落格，Google 的更新頻率不快，即使它已經收錄了 sitemap，也不會有更新就看到。像是現在 2/2 而我的 sitemap 上次被看的時間是 1/27 !

Google 的官方說明文件[要求 Google 重新檢索網址](https://developers.google.com/search/docs/advanced/crawling/ask-google-to-recrawl?visit_id=637793786640453064-2510441601&rd=1)中提及:

- 我們可以用「網址檢查工具」看單一網頁上次被檢索的時間得知狀態，網站數量不多時，我們可以在單一頁面的檢索狀態上按「要求建立索引」來提交，但 Google 對這個通路有數量限制。

- 或是用「索引狀態報表」查看 Sitemap 中有收錄的網址的狀態。提交大量網址時，一般建議使用 Sitemap。如果尚未在 Google Console 中提交 Sitemap 、或是提交後 Google 還沒接受（狀態還不是成功），這個報表是用不到的。

現在面臨的狀況是：我曾經提交 Sitemap 但後來有網址的發布方式，然而 Google 所存檔的是我舊的網址連結。想要讓 Google 知道我的網址都變更了。

### 通知 google 網站已經變更

官方文件[將 Sitemap 提交給 Google](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap#addsitemap) 裡面有這樣一段話

> Google 不會在每次檢索網站時檢查 Sitemap。除非您透過連線偵測 (ping) 告知我們 Sitemap 有異動，否則我們只會在首次偵測到 Sitemap 時進行檢查。如果您並未新增或更新 Sitemap，請勿要求 Google 檢查 Sitemap；也不要重複提交相同的 Sitemap 或為其執行連線偵測 (ping)。

簡單來說：

1. Google第一次偵測到 Sitemap 的時候會對裡面進行檢查，之後不會每次檢索的時候都去看 Sitemap。
2. 所以如果 Sitemap 有變更，Google 沒看到要 Ping 一下它。
3. 如果有已經存在的網頁有更新，要使用 `<lastmod>`標記這些網頁。

有兩種方式讓 Google 存取 Sitemap

1. 尚未讓 Google 收藏過 Sitemap：建議在 Google Console 中提交 [Sitemap 報告](https://support.google.com/webmasters/answer/7451001)
2. 使用連線偵測 (ping) 工具：在網址中傳送 GET 要求：

   ```
   https://www.google.com/ping?sitemap=<你的sitemap完整網址(包括https)>
   ```

## 小技巧: 將 Search Console 的版面切成英文

在參數列添加 `&hl=en` 可以直接將 google console 的報表直接轉換成英文，用英文的 Keyword 在搜尋引擎上查，可以得到比較多相關資料! 中文的討論串實在有點少。

## 分享一下 Sitemap 被光顧的時間頻率

需要注意的是，Google Console 的各表格更新時間**並不一致**！因此有些問題可能會沒辦法即時反應。例如，明明 Sitemap 在 2/5 被讀取了，然而涵蓋範圍頁面的更新日期卻停留在 2/2，因此我沒辦法知道這一次 Google 更新的網址有哪些，也沒辦法知道 Google 有沒有試圖對它們爬蟲、是不是我的頁面有問題等等，只能等。等它的統計表單更新... 。

而包含成效(有多少點擊量)、涵蓋範圍、行動裝置可用性、檢索統計資料，每張表格的更新日期都是不一致的！以我寫這段文字的時間，他們的更新時間分別是 5小時前、2/1、 2/4、 2/2。因此「行動裝置頁面」的有效網頁數量反而比「涵蓋範圍」多，顯得有點弔詭。

- 1/25 第一次提交 sitemap
- 1/27 Sitemap 第一次被讀取，但沒有任何網頁被收錄。顯示「已找到、目前尚未建立索引」
- 1/30 11:00 首頁被索引收錄成功，期間進行手機與電腦板的網頁載入速度優化。

2月：修改 **文章 (post)** 網址的格式，也就是說 Google 收錄的 sitemap 內容，與我當前的網址不一致，只能等待 Google 再爬到我的 sitemap 發現有更新，才能同步兩邊的網址內容。而 tag 頁面的網址沒有被改，跟 sitemap 是一致的。期間，當我手動為 tag 進行索引提交，這些網頁幾乎都當天就被收錄了，而文章頁面則都被不理會。

- 2/5 10:00 發現 Sitemap 被更新，距離上次被讀取相隔將近 9 天，一共處理 25 個網址。
- 2/6 11:00 發現 Sitemap 連續兩天被臨幸，顯示「Sitemap已處理完畢」一共有 25 個網址。
  - 然而涵蓋範圍內標示的網址都是舊網址，且總數只有 22 個。
  - 從網址檢查工具那邊查看，舊網址沒有被 sitemap 收錄，新網址（現在正常的）則都有被收錄。
  - 另外出現一個轉址錯誤，可是我透過其他工具看轉址都是正常的。
  - 發現有一個網址顯示「已檢索 - 目前尚未建立索引」，很難過以為被嫌棄了。
- 2/6 22:00 發現那個原本「已檢索 - 目前尚未建立索引」的網頁被收錄了，是我第一篇真正被收錄的文章（目前為止都是 tag 類的頁面被收錄）！雖然當前在 Google 引擎上我還是看不到。
- 2/9 涵蓋範圍終於更新成我修改後的網址、並且網址數量和與我當前的 sitemap 一致。也就是說從我提交新的網址到涵蓋範圍變動之間大約 7~10 天才在報表上生效，若單論修改到爬蟲來光顧 Sitemap 間隔大約 5天。但目前也只有一篇手動提交的網址被檢索並建立索引，其他都還是「已找到、目前尚未建立索引」
- 2/5~2/10 連續 6 天被 Google 爬蟲臨幸，文章介面實際被爬取的有 3 篇，其他時候都是一些 tag 頁面被爬 (可以去設定那邊的「檢索統計資料、依發現方式」看有多少文章被爬到）
- 5月初爬蟲有再來連續光顧 7天，但其間個人忙碌，沒有更新文章。
- 6/3 爬蟲又來了一天，結果我是隔天才更新文章 (掩面)。

其實網路上許多人也都說了，爬蟲何時來只能耐心等候，我還是稍微紀錄了一下對於這個新開的站，爬蟲光顧的頻率以及我個人所遇到的狀況，如何應對。希望能夠提供給有類似問題的人一個經驗分享!!