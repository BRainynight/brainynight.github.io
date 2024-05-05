---
title: Template Specilization 遇到的 Multiple Definition
date: 2024-05-05 09:15:00
description: "透過關鍵字 inline 解決 Template Specilization 遇到的 Multiple Definition"
categories:
  - cpp
---
雖然 Template 多習慣把實作寫在 hpp，若將 Template Specialiaztion 的**實作**寫在 hpp 卻可能發生問題。

假設有三個檔案，`temp.hpp` 寫著 template 與 Template Specialiaztion 的實作，兩個 cpp: `main.cpp` 與 `func.cpp` 分別都有 include  `temp.hpp`。這會引發 multiple definition  [\*](https://stackoverflow.com/questions/4445654/multiple-definition-of-template-specialization-when-using-different-objects)。

```
/usr/bin/ld: /tmp/ccDDhAUZ.o: in function `Negative get_max<Negative>(Negative, Negative)':
main.cpp:(.text+0x0): multiple definition of `Negative get_max<Negative>(Negative, Negative)'; /tmp/cctmE6oD.o:funcs.cpp:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status
```
![template_spec_and_redefine](/image/template_spec_and_redefine.png)
解決方法有兩種

1. 宣告 Template Specialiaztion 於 hpp，實作放在 cpp
2. 一樣把實作放在 hpp，但是多**宣告 inline** 於 Template Specialiaztion 的實作上。

第一種方法還算好理解，但是為何宣告 inline 就可以解決 template specialiaztion 遇到的 multiple definition? 這關係 C++ 的一個原則: One Definition Rule.

## One Definition Rule

這其實相當有趣，因為 function 是否 inline 取決於 compiler，即使宣告 inline 也不一定代表 compiler 會真的對 function inline。

那麼為何在 hpp 內對  Template Specialiaztion definition 宣告 inline 能解決問題?  [Stackoverflow 的回答](https://stackoverflow.com/a/48403514) 給出了解答。

根據  C++ standard 條目 3.2:4 ([file](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3690.pdf) P49 One definition rule)，可以拆成兩段來看: 
> (1) Every program shall contain exactly one definition of every non-inline function or variable that is odr-used in that program; no diagnostic required. The definition can appear explicitly in the program, it can be found in the standard or a user-defined library, or (when appropriate) it is implicitly defined (see 12.1, 12.4 and 12.8). 
> 
> (2) An inline function shall be defined in every translation unit in which it is ODR use.

當 Specialiaztion 不是 inline 時被當作 non-inline function 對待，而對於 non inline function/variable，在 program 中只應該擁有一份 definition。因此兩次 include 同一份 template header 造成了問題: 多個 definition (include 的本質就是把 hpp 貼到 cpp 裡面)。

當 Specialiaztion 是 inline 的時候，Specialiaztion 滿足了條目的第二部分: inline function 必須被定義於每一個使用到的 translation unit，也就是該則回答裡面提到的 : 

> an inline function must be defined in each module using the function.

## Inline Object 的特性
> 以下內容翻譯、解讀自 [CPP reference - inline specifier](https://en.cppreference.com/w/cpp/language/inline#:~:text=An%20inline%20function%20or%20inline,address%20in%20every%20translation%20unit.)

當 function 或 variable (C++17) 被宣告為 inline，代表它擁有以下特性 (以下簡稱 inline object)

1. 在每一個 TU (translation unit) 當中，inline object 的定義必須是可存取的。
2. 如果一個 inline object 被宣告於 hpp，並且此 hpp 被多個 cpp inlcude，表示
	- 此 inline obejct 擁有 External Linkage (它的名稱在其他 TU 被引用且沒有被宣告 `static`)
	- 它在多個 TU 之間可能擁有**多個定義**，但在每一個 TU 的定義都是相同的。儘管具有這些特性，最終是否予以 inline subsititution 卻仍由 compiler 決定。
## Inline 的歷史淵源
Source: [Cpp Reference](https://en.cppreference.com/w/cpp/language/inline#:~:text=The%20original%20intent,statics%20listed%20above.)

Inline 這個關鍵字最初、最廣為人知的用意是把 function call 替換成 function body 本身，也就是 [inline substitution](https://en.wikipedia.org/wiki/inline_expansion "enwiki:inline expansion")。其代價是 object file 變大，因為每個 call 到 inline 的地方都會被「貼上」一次，但有優化的作用。

然而，因為是否替換 function call 由 compiler 自由決定，被宣告 inline 的 function 不必然被替換，沒被宣告 inline 也不一定不被替換。這代表 inline function optimization 不在綁定於 keyword `inline`。

需要注意的是，Compiler 選擇 inline optimization 與否，並不會改變有關 multiple definition 的規定。

> Function 最終被 compiler inline 與否，都不應該擁有 multiple definition。

在前面 「Inline Object 的特性」 提到，inline function 在多個 TU 當中是擁有多個定義 (multiple definitions) 的，且關鍵字 inline 並不與 inline subsititution 綁定。
這個關鍵字的意義逐漸從「偏好 inline optimization」轉變成 「允許多重定義」，且這重含意在 C++17 中被延伸到 variable 上面。

因此，當 Template Specialiaztion 透過 `inline` 可以解決 Multiple Definition 的原因，就來自於此。
