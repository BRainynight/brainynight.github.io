---
title: 使用 Markdown 寫論文
description: 以 Markdown 寫論文時的文獻、圖片公式等地引用管理，以及使用 pandoc 將 markdown 轉 doc 的操作。
date: 2022-02-11 13:01:31
categories: Tool
aliases:
- /posts/2022-02-11-thesis-markdown
---

## Markdown vs. Latex

主要是因為 Latex 語法有點過於繁雜，網路編輯器 Overleaf 雖然好用，但沒辦法直接輸入中文（或許要研究其他設定吧）。此外語法複雜，如果不是已經上手的人要寫通篇的長論文感覺有點負擔。

相較之下，語法簡單的 Markdown 就好用很多，先大致在 markdown 把文字編輯的內容都完成，再去 word 套用統一格式，這是我選擇使用 Markdown 的原因。

## PDF 生成

套件 pandoc 可以直接將 markdown 轉成 PDF，但是預設的轉換引擎 pdflatex 、或是手動選定 xelatex 都需要下載完整的 Latex 套件。我在 Windows 安裝時被要求加了一堆東西，按得沒完又不想要它載東載西不告訴我，因此後來就改使用 wsl 端安裝跟執行 Pdf 操作。其中要注意中文文字的轉換，有可能需要指定字體！

透過添加參數 `-V CJKmainfont="<some_font>.ttf"`，並確認該字體檔可以被取得，最好是附在資料夾裡面。相關議題參照：[mactex 2015 報錯](https://github.com/ZJU-Awesome/write_with_LaTeX/issues/1)，字體檔案來源 [dolbydu: font/unicode](https://github.com/dolbydu/font/tree/master/unicode)。

## 引用管理

### 文獻文件：bib 檔案

引用的部分採用 BibTex 管理文獻，使用 bibTex 必須遵守文獻規則撰寫並創建 `.bib` 檔案與。以 PanDoc 官網上的範例 bib 檔為例：

- `@` 開頭作為一條新的引用
- `@` 和大括弧 `{`之間表示此 Reference 所屬的類別，是書、文章、或其他類別。
- 大括弧 `{` 後面的第一串字串，代表這條 reference 的 ID，在 markdown 中要如何引用它。

```latex
@Book{book1,
author="John Doe",
title="First Book",
year="2005",
address="Cambridge",
publisher="Cambridge University Press"
}

@Article{art1,
author="John Doe",
title="Article",
year="2006",
journal="Journal of Generic Studies",
volume="6",
pages="33-34"
}

@InCollection{col1,
author="John Doe and Jenny Roe",
title="Why Water Is Wet",
booktitle="Third Book",
editor="Sam Smith",
publisher="Oxford University Press",
address="Oxford",
year="2007"
}
```

BibTex 格式所能設定的 Reference 類別總共有 14 種，參見：[Complete list of BibTeX entry types [with examples] - BibTeX.com](https://www.bibtex.com/e/entry-types/)。

### 寫作文件：md 檔案

建立一個 `demo.md` 檔案，內容如下。

```markdown
# demo 
根據文獻[@book1]所言，今天天氣真好。而文獻[@art1]提到，太陽會影響天氣。
文獻[@col1]更是提到不但太陽會影響天氣，下雨、風也會。
```

經過指令調用 pandoc 來轉換成微軟 word 檔案：

```shell
pandoc --cite --bibliography=biblio.bib demo.md -o demo-citation.docx
```

Word 產生的圖會在後面看到。

### 文獻超連結

上述方法產生的文件，在數字引用的部份只有單純的文字，沒辦法超連結到下面的參考文件區。根據 [PanDoc 官方文件](https://pandoc.org/MANUAL.html#other-relevant-metadata-fields)，這需要在 markdown 中添加 meta-data 把參數開起來：

```markdown
---
link-bibliography: true
link-citations: true
---
```

### 調整文獻插入的格式

我的領域並不慣用上面那種引用方式，要調整引用格式需要透過附加 `.csl` 檔案，上網查了 [IEEE 格式的 csl 檔案](https://github.com/citation-style-language/styles/blob/master/ieee.csl)。並在指令上添加 `--csl=ieee.csl` 參數：

```shell
pandoc --cite --csl=ieee.csl --bibliography=biblio.bib demo.md \
	-o demo-citation.docx
```

## 轉成 docx 時包含預設 MS Word 模板格式

如果希望 docx 轉換成期望的格式，需要添加 `--reference-doc` 參數，我將論文格式儲存成 `render-sample.docx`，放在同一個資料夾。並且在 `.md` 最後加上了參考資料的標題，最後轉換效果如下：

```sh
pandoc --cite --csl=ieee.csl \
        --bibliography=biblio.bib \
        --reference-doc=render-sample.docx demo.md -o cit.docx
```

![不同指令對應的結果](/uploads/4example-footnote.webp)

```sh
pandoc --toc --cite --csl=ieee.csl \
	  --filter pandoc-xnos --bibliography=biblio.bib \
	  --reference-doc=render-sample.docx demo.md -o cit.docx
```

## 交互參照

需下載套件 `pandoc-xnos`，並在下轉換指令的時候添加 `--filter pandoc-xnos`，其中包含四個套件，分別是：圖片 [pandoc-fignos](https://github.com/tomduck/pandoc-fignos)、公式 [pandoc-eqnos](https://github.com/tomduck/pandoc-eqnos)、表格 [pandoc-tablenos](https://github.com/tomduck/pandoc-tablenos)、章節 [pandoc-secnos](https://github.com/tomduck/pandoc-secnos)。

可以直接在 pandoc 的轉換指令中添加  `--filter pandoc-xnos` 一口氣解決，也可以只取自己需要的 `--filter pandoc-fignos` 之類的，如果要同時使用兩個要加兩次參數，例如同時使用表格與圖片的參照 `--filter pandoc-fignos --filter-tablenos`。

以下以表格與圖片的參照用法舉例說明。

### 表格

標註方法: `{#tbl:id}` ，`id` 可以自由換成此表格的專屬 id。

```markdown
|       | Col 1 | Col 2 |
| ----- | ----- | ----- |
| Row 1 | 11    | 12    |
| Row 2 | 21    | 22    |
| Row 3 | 31    | 32    |
Table: 表格介紹 {#tbl:tbl1}
```

而想要參照(reference)某表格，則使用 `{@tbl:id}` 的方式參照。

### 圖片

標註方法: `{#fig:id}` 同樣 id 可以自由替換，參照方式也和表格雷同`{@fig:id}`。

```
![圖片介紹](path\of\fig){#fig:fig1}
```

### 公式參照

使用套件 pandoc-eqnos，然而我按照教學中使用，轉換成 docx 時卻發生錯誤: XML Parsing error。這個問題主因應該是 Word 其實是一個 xml 格式的檔案，eqnos 的套件中哪裡把應對齊 xml 標籤給漏掉了，就好像 html 裡面 `<p>` 後面得要加 `</p>` 這樣成對式的 標籤(tag)。

我依照文章 [[Office] 修復 Xml parsing error 的 Word Docx 檔案](https://ephrain.net/office-%E4%BF%AE%E5%BE%A9-xml-parsing-error-%E7%9A%84-word-docx-%E6%AA%94%E6%A1%88/) ，用網路上的線上 xml 分析網頁，解析了一下是哪裡發生狀況。發現就是在 `w:bookmarkStart` 附近出現 tag 有問題。最後，通過比較 pandoc-fignos 與 pandoc-eqnos ，發現兩份程式在 `bookmarkstart` 變數上處理不一樣! `fignos` 的程式碼沒有加上 `<w:r><w:t>`。

因此，我把 eqnos 中的程式碼(約在 215行附近) 改成如下: 

```python
        bookmarkstart = \
          RawInline('openxml',
                    '<w:bookmarkStart w:id="0" w:name="%s"/>'
                    %attrs.id)
        bookmarkend = \
          RawInline('openxml',
                    '<w:bookmarkEnd w:id="0"/>')
        ret = [bookmarkstart, AttrMath(*value), bookmarkend]
```

然後整個都可以順利引用了! 我不是很確定刪掉 `<w:r><w:t>` pair 之後，會不會對格式造成問題? 但如果圖片引用都這樣處理了，應該是還好? 

至於公式的引用與自動標號

- 段落公式標號 (賦予公式 id )

  ```markdown
  $$
  a+b=c
  $${#eq:eq1} 
  ```

- 引用有 id 的公式

  ```markdown
  如@eq:eq1之計算得到結果
  ```

- 給公式標號，但不賦予 ID 

  ```markdown
  $$
  a=999
  $${#eq:} 
  ```

效果參見範例文件。



### meta-formatter

抬頭的 meta-formatter 需要添加，cleveref 開啟的話參照圖表時前綴才會有「圖」或「表」，plus-name 是設定被參照時在內文中該以何種前綴顯示。

```yaml
fignos-cleveref: true
fignos-plus-name: 圖
fignos-caption-name: 圖
fignos-number-by-section: true
fignos-caption-separator: space # 預設為冒號

tablenos-cleveref: true
tablenos-plus-name: 表
tablenos-caption-name: 表
tablenos-number-by-section: true

eqnos-cleveref: true
eqnos-number-by-section: true
eqnos-plus-name: 公式 # 被引用時前綴詞為何
```



## 圖目錄與表目錄

理論上可以在 meta-data 裡面設置這兩個參數自動生成，但似乎只支援生成 pdf，生成 word 時候這兩個參數不生效。

```
lof: true 
lot: true
```

要注意，雖然文章目錄的縮寫是 TOC (table of content)，但圖目錄與表目錄的縮寫分別是 lof (list of figure), lot (list of table) ，要用這個關鍵字去找! 

生成 PDF 的時候如果有報錯，注意是否為中文字 UTF-8 類字體所造成的轉換問題，相關議題參照前面章節[PDF生成](#PDF 生成)

```sh
pandoc --cite --csl=ieee.csl --filter pandoc-xnos \
		--bibliography=biblio.bib --pdf-engine=xelatex \
		-V CJKmainfont="KaiTi.ttf" --reference-doc=render-sample.docx demo.md \
		-o cit.pdf
		
# 或將 fignos 與 tablenos 分開列
pandoc --cite --csl=ieee.csl \
		--filter pandoc-fignos --filter pandoc-tablenos \
		--bibliography=biblio.bib --pdf-engine=xelatex \
		-V CJKmainfont="KaiTi.ttf" --reference-doc=render-sample.docx demo.md \
		-o cit.pdf
```

## 包含交互參照的 Word 轉換指令

但經過我的實驗，雖然這一連串的操作可以使圖表依照章節標號，卻沒辦法有標號超連結之類的，恐怕也沒辦法在 word 裡面生成圖目錄與表目錄。

```sh
pandoc  --filter pandoc-xnos \
		--cite --csl=ieee.csl --bibliography=biblio.bib \
        --pdf-engine=xelatex \
		-V CJKmainfont="KaiTi.ttf" --reference-doc=render-sample.docx demo.md \
		-o cit.docx
```

## 分頁符號

Markdown 本身是不支援分頁符號的，但我們可以使用 html code 讓它強制分頁：[Markdown 輸出 pdf 強制分頁的方法](https://github.com/hanxi/blog/issues/20) （但轉成 doc 後時靈時不靈，用 Latex 語法 `\newpage` 也一樣，我後來就直接從 doc 模板那邊下手：每個大標題都自動換頁）。

```html
<div style="page-break-after: always;"></div>
```

但是如果轉成 PDF 的話，在 markdown 中直接輸入 `\newpage` 作為分頁是可行的。

轉成 doc 時的強制分頁(分頁符號)，需要直接插入一段 source code ：

```xml
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
```

因為 ms word 本身是一個 xml 格式的檔案，pandoc 在轉換時對 docx 支援這種[部份 raw attribute](https://pandoc.org/MANUAL.html#extension-raw_attribute) 的功能，可以透過此方法達成強制分頁。

## 在 WSL 安裝 Latex

我用的是 Ubuntu 做為 Wsl2 的作業系統。首先安裝 Latex 基本的語法與擴充語法：

```sh
sudo apt-get install texlive
sudo apt-get install texlive-latex-extra
sudo apt-get install texlive-xetex
```

接著依照 [Pandoc 的官方文件](https://github.com/jgm/pandoc/blob/master/INSTALL.md#linux)選擇適合的檔案：

```sh
wget https://github.com/jgm/pandoc/releases/download/2.17.1.1/pandoc-2.17.1.1-1-amd64.deb
sudo dpkg -i pandoc-2.17.1.1-1-amd64.deb
```

並且在 Markdown 中引用的圖片，最好是放在同層級或下層級的資料夾中，比較不容易發生圖片找不到的狀況。

## 範例

範例 markdown 與轉換而成的 MS Word 如下，內文是產生器而得，完全只是要個排版的感覺，請勿深究！轉換指令：

```sh
pandoc --filter pandoc-xnos \
	--cite --csl=ieee.csl --bibliography=biblio.bib \
	--pdf-engine=xelatex -V CJKmainfont="KaiTi.ttf" \
	--reference-doc=render-sample.docx demo.md \
	-o cit.docx
```
- 所使用的 markdown 檔案、bib 引用檔案以及輸出的 word 檔案： [markdown-thesis.zip](/uploads/markdown-thesis.zip)。
- render-sample 為個人的 doc 模板。

## Reference

- [Markdown、.bib、LaTeX + Typora、Pandoc 管理論文文獻](https://blog.csdn.net/qq_39564555/article/details/112496861)
- [using bibtex: a short guide](https://www.economics.utoronto.ca/osborne/latex/BIBTEX.HTM)