---
title: Hugo-重新導向網址
description: "學習使用 Config，用最小的設定了解 docsy"
date: 2024-05-03 14:07:00
aliases:
- /2023-01-01-posts
- /2023-01-01-posts.html
---

## redirect URL 

由於舊的部落格網址設計不佳，我希望做 URL redirection。

Hugo 提供了 `aliases` 可以重新導向網址。以這篇文章來說，`domainName/2023-01-01-posts` 或是`domainName/notes/hugo-redirect` 都會導向這份內容 。

```yaml
aliases:
- /2023-01-01-posts
```

